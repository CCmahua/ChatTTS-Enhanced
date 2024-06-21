from typing import Optional
import gradio as gr
from wording import get
import random
from component_manager import register_component,update_component_value


AUDIO_SEED_INPUT: Optional[gr.Number] = None
TEXT_SEED_INPUT: Optional[gr.Number] = None
EXPERIMENTAL_OPINION_CHECKBOX: Optional[gr.Checkbox] = None
GENERATE_AUDIO_SEED: Optional[gr.Button] = None
GENERATE_TEXT_SEED: Optional[gr.Button] = None
EMB_UPLOAD_INPUT: Optional[gr.File] = None
EMB_UPLOAD_CHECKBOX: Optional[gr.Checkbox] = None
def render():
    global AUDIO_SEED_INPUT, TEXT_SEED_INPUT, EXPERIMENTAL_OPINION_CHECKBOX, GENERATE_AUDIO_SEED, GENERATE_TEXT_SEED,EMB_UPLOAD_INPUT,EMB_UPLOAD_CHECKBOX

    with gr.Row():
        EXPERIMENTAL_OPINION_CHECKBOX = gr.Checkbox(
            label=get('ExperimentalOption'),
            value=False,
            info=get('ExperimentalOptionInfo'),
            visible=False
        )
    with gr.Row():
        # 增加音色上传
        EMB_UPLOAD_CHECKBOX = gr.Checkbox(
            label=get('EmbUpload'),
            value=False,
            info=get('EmbUpload')
        )
    with gr.Row():
        EMB_UPLOAD_INPUT = gr.File(
            label=get('EmbUpload'),
            type="filepath", file_types=['.pt'], interactive=True, visible=False
        )
    with gr.Row():

        AUDIO_SEED_INPUT = gr.Textbox(
            value=2, label=get('AudioSeed'),
            info=get('AudioSeedInfo'),visible=True
        )
        GENERATE_AUDIO_SEED = gr.Button(
            get('GenerateAudioSeed'),visible=True
        )
    with gr.Row():
        TEXT_SEED_INPUT = gr.Number(
            value=42, label=get('TextSeed'),
            info=get('TextSeedInfo'),
            visible=True
        )
        GENERATE_TEXT_SEED = gr.Button(
            get('GenerateTextSeed'),
            visible=True
        )

    GENERATE_AUDIO_SEED.click(generate_audio_seed_FN, inputs=[], outputs=AUDIO_SEED_INPUT)
    GENERATE_TEXT_SEED.click(generate_text_seed_FN, inputs=[], outputs=TEXT_SEED_INPUT)

    register_component("audio_seed_input", AUDIO_SEED_INPUT)
    register_component("text_seed_input", TEXT_SEED_INPUT)
    register_component("experimental_opinion_checkbox", EXPERIMENTAL_OPINION_CHECKBOX)
    register_component("emb_upload_checkbox", EMB_UPLOAD_CHECKBOX)
    register_component("emb_upload_input", EMB_UPLOAD_INPUT)





def listen():
    EXPERIMENTAL_OPINION_CHECKBOX.change(lambda value: update_component_value("experimental_opinion_checkbox", value),
                                         inputs=EXPERIMENTAL_OPINION_CHECKBOX, outputs=[])
    AUDIO_SEED_INPUT.change(lambda value: update_component_value("audio_seed_input", value),
                                         inputs=AUDIO_SEED_INPUT, outputs=[])
    TEXT_SEED_INPUT.change(lambda value: update_component_value("text_seed_input", value),
                                         inputs=TEXT_SEED_INPUT, outputs=[])
    EMB_UPLOAD_CHECKBOX.change(lambda value: EMB_UPLOAD_FN(value),
                           inputs=EMB_UPLOAD_CHECKBOX, outputs=[AUDIO_SEED_INPUT,GENERATE_AUDIO_SEED,EMB_UPLOAD_INPUT])
    EMB_UPLOAD_INPUT.change(lambda value: update_component_value("emb_upload_input", value),
                           inputs=EMB_UPLOAD_INPUT, outputs=[])



def generate_audio_seed_FN():
    new_seed = random.randint(1, 100000000)
    update_component_value("audio_seed_input", new_seed)
    return {
        "__type__": "update",
        "value": str(new_seed)
    }


def generate_text_seed_FN():
    new_seed = random.randint(1, 100000000)
    update_component_value("text_seed_input", new_seed)
    return {
        "__type__": "update",
        "value": new_seed
    }


def EMB_UPLOAD_FN(value):
    update_component_value("emb_upload_checkbox", value)
    return {
        AUDIO_SEED_INPUT:gr.update(visible=not value),
        GENERATE_AUDIO_SEED: gr.update(visible=not value),
        EMB_UPLOAD_INPUT: gr.update(visible=value),
    }


