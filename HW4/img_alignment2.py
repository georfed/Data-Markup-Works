import shutil

import cv2
import numpy as np
import os


def align_images(original_path, result_path, output_path):
    original = cv2.imread(original_path, cv2.IMREAD_GRAYSCALE)
    result = cv2.imread(result_path, cv2.IMREAD_GRAYSCALE)
    color_result = cv2.imread(result_path)

    if original is None or result is None:
        print(f"Error loading images: {original_path}, {result_path}")
        return False

    sift = cv2.SIFT_create()
    keypoints1, descriptors1 = sift.detectAndCompute(original, None)
    keypoints2, descriptors2 = sift.detectAndCompute(result, None)

    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(descriptors1, descriptors2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    if len(good_matches) < 10:
        print(f"Not enough good matches for {result_path}, skipping alignment.")
        return False

    src_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    if H is None:
        print(f"Homography not found for {result_path}, skipping.")
        return False

    h, w = original.shape
    aligned_result = cv2.warpPerspective(color_result, H, (w, h))

    gray_aligned = cv2.cvtColor(aligned_result, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_aligned, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print(f"No valid content detected for {result_path}, skipping.")
        return False

    x, y, w_c, h_c = cv2.boundingRect(np.concatenate(contours))

    if w_c < w or h_c < h:
        # print(f"Black borders detected for {result_path}, skipping.")
        return False

    mask_filled = np.zeros_like(gray_aligned, dtype=np.uint8)
    cv2.drawContours(mask_filled, contours, -1, (255), thickness=cv2.FILLED)
    black_pixel_ratio = np.sum(mask_filled == 0) / (h * w)

    if black_pixel_ratio > 0.005:
        # print(f"Rotational black borders detected for {result_path}, skipping.")
        return False

    if abs((aligned_result.shape[1] / aligned_result.shape[0]) - (w / h)) > 0.01:
        print(f"Aspect ratio mismatch for {result_path}, skipping.")
        return False

    cv2.imwrite(output_path, aligned_result)
    # print(f"Successfully aligned and saved: {output_path}")
    return True


def process_folder(folder_path, output_folder):

    image_files = sorted([f for f in os.listdir(folder_path) if f.endswith(('png', 'jpg', 'jpeg'))])
    edits_aligned = 0

    if not image_files or "original" not in image_files[0].lower():
        print("Error: Original image not found or improperly named.")
        return

    original_path = os.path.join(folder_path, image_files[0])
    os.makedirs(output_folder, exist_ok=True)

    for file in image_files[1:]:  # Skip the original
        result_path = os.path.join(folder_path, file)
        output_path = os.path.join(output_folder, file)
        if align_images(original_path, result_path, output_path):
            edits_aligned += 1

    if edits_aligned == 0:
        shutil.rmtree(output_folder)
    else:
        cv2.imwrite(os.path.join(output_folder, image_files[0]), cv2.imread(original_path))


# Example usage
if __name__ == '__main__':
    process_folder("/photoshop_requests/data_subsample/too-stylized_1iggl85",
                   "/photoshop_requests/data_subsample/done_too-stylized_1iggl85")
