import gradio as gr
import pandas as pd


def classify_text(*selections):
    global current_index, df_sample

    # Flatten and filter selections
    selected_types = [item for sublist in selections if sublist for item in sublist]
    chosen = ', '.join(selected_types) if selected_types else 'vague'

    df_sample.loc[current_index, 'task'] = chosen
    current_index += 1

    if current_index >= len(df_sample):
        df_sample.to_csv('done_markup.csv')
        return gr.update(visible=False), gr.update(visible=False), "Отлично, всё размечено!", *[
            gr.update(visible=False) for _ in types]

    next_text = df_sample.loc[current_index, 'fulltext']
    return next_text, gr.update(value=[]), "", *[gr.update(value=[]) for _ in types]


def get_initial_text():
    return df_sample.at[current_index, 'fulltext']


df_sample = pd.read_csv('to_markup.csv').drop(columns='Unnamed: 0')
df_sample['task'] = ''
current_index = 0
types = {
    'addition': [
        'add',
        'add clothes'
    ],

    'removal': [
        'remove',
        'remove bg',
        'remove text',
        'remove watermarks'
    ],

    'replacing': [
        'replace',
        'replace text'
    ],

    'changing': [
        'change',
        'change color',
        'change size',
        'change clothes',
        'change expression',
        'change hair',
        'change bg',
        'move',
        'face swap'
    ],

    'enhancing': [
        'enhance colors',
        'enhance image',
        'deblur',
        'blur',
        'restore photo',
        'colorize',
        'better',
        'upscale',
        'outline',
        'stylize'
    ],

    'common': [
        'memorial',
        'profile'
    ],

    'person': [
        'makeup',
        'age',
        'thinner'
    ]
}

if __name__ == '__main__':
    with gr.Blocks() as demo:
        gr.Markdown("## Разметка типов операций")

        text_display = gr.Textbox(label="Инструкция", value=get_initial_text(), interactive=False, lines=4)

        checkbox_groups = []
        with gr.Row():
            for col_name, col_options in types.items():
                with gr.Column():
                    gr.Markdown(f"**{col_name}**")
                    cb = gr.CheckboxGroup(choices=col_options, label="", interactive=True)
                    checkbox_groups.append(cb)

        status_display = gr.Markdown("")
        next_button = gr.Button("Далее")

        next_button.click(
            classify_text,
            inputs=checkbox_groups,
            outputs=[text_display, next_button, status_display] + checkbox_groups
        )

    demo.launch()
