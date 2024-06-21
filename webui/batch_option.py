import gradio as gr
from wording import get
from component_manager import register_component,get_component,update_component_value
from typing import Optional

BATCH_PROCESSING_CHECKBOX: Optional[gr.Checkbox] = None
SRT_PROCESSING_CHECKBOX: Optional[gr.Checkbox] = None
TEXT_INPUT: Optional[gr.Textbox] = None
TXT_FILE_INPUT: Optional[gr.Files] = None


def render():
    global BATCH_PROCESSING_CHECKBOX, SRT_PROCESSING_CHECKBOX, TEXT_INPUT, TXT_FILE_INPUT

    with gr.Row():
        BATCH_PROCESSING_CHECKBOX = gr.Checkbox(
            label=get('BatchProcessing'), value=False, info=get('BatchProcessingInfo')
        )

        SRT_PROCESSING_CHECKBOX = gr.Checkbox(
            label=get('SrtProcessing'), value=False, visible=False, info=get('SrtProcessingInfo'),interactive=True
        )

    TEXT_INPUT = gr.Textbox(
        label=get('TextInputLabel'), lines=4, placeholder=get('TextInputPlaceholder'), value=get('default_text'),interactive=True
    )
    TXT_FILE_INPUT = gr.Files(
        label=get('TxtFileInputLabel'), type="filepath", file_types=['.txt','.srt'], visible=BATCH_PROCESSING_CHECKBOX.value,interactive=True
    )

    register_component("batch_processing_checkbox", BATCH_PROCESSING_CHECKBOX)
    register_component("srt_processing_checkbox", SRT_PROCESSING_CHECKBOX)
    register_component("text_input", TEXT_INPUT)
    register_component("txt_file_input", TXT_FILE_INPUT)

def listen():
    BATCH_PROCESSING_CHECKBOX.change(lambda value: update_visibility(value), inputs=BATCH_PROCESSING_CHECKBOX, outputs=[
        TEXT_INPUT, TXT_FILE_INPUT, get_component('split_text_checkbox'), get_component('concatenate_audio_checkbox'), SRT_PROCESSING_CHECKBOX
    ])
    SRT_PROCESSING_CHECKBOX.change(lambda value: update_component_value("srt_processing_checkbox", value), inputs=SRT_PROCESSING_CHECKBOX, outputs=[])
    TXT_FILE_INPUT.change(lambda value: update_component_value("txt_file_input", value), inputs=TXT_FILE_INPUT, outputs=[])
    TEXT_INPUT.change(lambda value: update_component_value("text_input", value), inputs=TEXT_INPUT,
                          outputs=[])


def update_visibility(batch_processing):
    text_input=get_component("text_input")
    txt_file_input=get_component("txt_file_input")
    split_text_checkbox=get_component("split_text_checkbox")
    concatenate_audio_checkbox=get_component("concatenate_audio_checkbox")
    srt_processing_checkbox=get_component("srt_processing_checkbox")
    update_component_value('batch_processing_checkbox',batch_processing)
    return {
        text_input: gr.update(visible=not batch_processing),
        txt_file_input: gr.update(visible=batch_processing),
        split_text_checkbox: gr.update(interactive=not batch_processing, value=False),
        concatenate_audio_checkbox: gr.update(interactive=batch_processing),
        srt_processing_checkbox: gr.update(visible=batch_processing)
    }