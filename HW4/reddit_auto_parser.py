import praw
import requests
import os
from PIL import Image
from io import BytesIO
import shutil
import pandas as pd
from tqdm import tqdm


# def is_paid(post) -> bool:
#     return 'free' not in post.link_flair_text.lower()


# def is_matching_ar(orig: Image, candidate: Image) -> bool:
#     return ((orig.size[0] == candidate.size[0] and orig.size[1] == candidate.size[1])
#             or (abs(orig.size[0] / orig.size[1] - candidate.size[0] / candidate.size[1]) < 0.001))


def download_image(url, save_path) -> Image:
    """Download an image from a given URL, verify it, save it to the specified path and return it as a PIL Image."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img.verify()
        img_ext = '.' + img.format.lower()
        if img.format not in ['PNG', 'JPEG']:
            raise Exception(f'non-common format: {img.format}')
        with open(save_path+img_ext, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {save_path+img_ext}")
        return img

    except Exception as e:
        print(f"Failed to download image: {url}, Error: {e}")
        return None


def parse_photoshop_request(time_filter):
    subreddit = reddit.subreddit('PhotoshopRequest')
    for i, post in tqdm(enumerate(subreddit.top(time_filter=time_filter, limit=None))):

        the_post = post

        # save csv changes once in 10 posts
        if i % 10 == 0:
            print('SAVING...')
            df.drop(columns=[x for x in df.columns if 'Unnamed:' in x], inplace=True)
            df.to_csv(os.path.join(base_folder, 'data.csv'))


        if post.over_18:
            print(f'NSFW: {post.title}\n Skipping...')
            continue

        if not post.link_flair_text:
            print('no flare,  skipping...')
            continue

        if post.link_flair_text.lower() != 'free :snoo:':
            print('not free post, skipping...')
            continue

        if post.url.endswith(('.jpg', '.jpeg', '.png')):
            print(f"Parsing post: {post.title}")

            text = post.title + '\n' + post.selftext
            if any(list(zoomword in text.lower() for zoomword in ['resize', 'zoom', 'expand', 'generative fill'])):
                print('zoom request, skipping...')
                continue
            # text = post.title + '\n' + post.selftext
            # if any(list(payword in text.lower() for payword in ['$', '﹩', '＄', 'tip', 'pay', '€', '￡', '£', 'price',
            #                                                     'usd', 'eur', 'gbp', 'paid', 'euro', 'dollar'])):
            #     print('paid, skipping...')
            #     continue

            # subfolder = 'paid' if is_paid(post) else 'free'
            post_folder = os.path.join(output_folder, post.id)
            if os.path.isdir(post_folder):
                print('already parsed, skipping...')
                continue

            os.makedirs(post_folder, exist_ok=True)

            # Parsing edit request
            # with open(os.path.join(post_folder, 'edit.txt'), "w") as f:
            #     f.write(text)

            # Download original post image
            original_image_path = os.path.join(post_folder, "original")
            orig = download_image(post.url, original_image_path)
            if orig is None:
                print('no image, skipping...')
                continue

            # Fetch top comments with images
            post.comments.replace_more(limit=None)
            top_comments = sorted(post.comments, key=lambda x: x.score, reverse=True)
            has_edits = False
            img_counter = 0
            # wrong_ar_counter = 0
            # correct_img_max = 3  # load top-3 correct-AR edits for common posts
            # if post.score >= 100:
            #     correct_img_max = 5  # top-5 for popular posts
            # if post.score >= 1000:
            #     correct_img_max = 10  # top-10 for trends
            # wrong_ar_max = 3

            for comment in top_comments:
                if post.author and comment.author:
                    if post.author.name == comment.author.name:
                        continue

                # if img_counter == correct_img_max:
                #     break
                if hasattr(comment, "body"):
                    # Extract URLs in comment
                    for word in comment.body.split():
                        if word.startswith("https://preview.redd.it/"):
                            comment_image_path = os.path.join(post_folder, f"result_{img_counter}")
                            candidate = download_image(word, comment_image_path)
                            if candidate is None:
                                print('no comment image, skipping...')
                                continue
                            # if not is_matching_ar(orig, candidate):
                            #     os.rename(
                            #         comment_image_path + f'.{candidate.format.lower()}',
                            #         os.path.join(
                            #             post_folder, f"wrong_ar_result_{wrong_ar_counter}.{candidate.format.lower()}"
                            #         )
                            #     )
                            #     comment_image_path = os.path.join(post_folder, f"wrong_ar_result_{wrong_ar_counter}")
                            #     wrong_ar_counter += 1
                            #     has_edits = True
                            # else:
                            img_counter += 1
                            has_edits = True

                            df.loc[len(df)] = [
                                original_image_path + '.' + orig.format.lower(),  # img1_path
                                comment_image_path + '.' + candidate.format.lower(),  # img2_path
                                post.title,  # title
                                post.selftext,  # body
                                orig.size[0],  # img1_width
                                orig.size[1],  # img1_height
                                candidate.size[0],  # img2_width
                                candidate.size[1],  # img2_height
                                post.id,  # post_id
                                post.score,  # post_score
                                post.link_flair_text.lower() if post.link_flair_text else '[no flare]',  # post_flare
                                comment.author.name if comment.author else '[no author]'
                            ]

                            break

            if not has_edits:
                print('no edits, removing session folder...')
                shutil.rmtree(post_folder)


reddit = praw.Reddit('bot1')

base_folder = 'photoshop_requests'
output_folder = os.path.join(base_folder, 'data')
os.makedirs(output_folder, exist_ok=True)
df = pd.read_csv(os.path.join(base_folder, 'data.csv'))
df.drop(columns=[x for x in df.columns if 'Unnamed:' in x], inplace=True)


if __name__ == "__main__":
    print(f'Red dataframe of {len(df)} entries.')
    # try:
    parse_photoshop_request(time_filter='week')
    # except Exception:
    #     df.to_csv(os.path.join(base_folder, 'emergency_save.csv'))
    df.drop(columns=[x for x in df.columns if 'Unnamed:' in x], inplace=True)
    df.to_csv(os.path.join(base_folder, 'data.csv'))
