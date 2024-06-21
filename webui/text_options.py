import gradio as gr
from wording import get
from component_manager import register_component,update_component_value
from typing import Optional

REFINE_TEXT_CHECKBOX: Optional[gr.Checkbox] = None
SPLIT_TEXT_CHECKBOX: Optional[gr.Checkbox] = None
SEGMENT_LENGTH_SLIDER: Optional[gr.Slider] = None
CONCATENATE_AUDIO_CHECKBOX: Optional[gr.Checkbox] = None
NUMS2TEXT_CHECKBOX: Optional[gr.Checkbox] = None

def render():
    global REFINE_TEXT_CHECKBOX, SPLIT_TEXT_CHECKBOX, SEGMENT_LENGTH_SLIDER, CONCATENATE_AUDIO_CHECKBOX, NUMS2TEXT_CHECKBOX

    with gr.Row():
        REFINE_TEXT_CHECKBOX = gr.Checkbox(
            label=get('RefineText'),
            info=get('RefineTextInfo'),
            value=False
        )
        SEGMENT_LENGTH_SLIDER = gr.Slider(
            minimum=10, maximum=200, step=10, value=60,
            label=get('SegmentLength'),
            info=get('SegmentLengthInfo')
        )
    with gr.Row():
        SPLIT_TEXT_CHECKBOX = gr.Checkbox(
            label=get('SplitText'),
            value=False,
            info=get('SplitTextInfo'),
            visible=False
        )
        CONCATENATE_AUDIO_CHECKBOX = gr.Checkbox(
            label=get('ConcatenateAudio'),
            value=False, interactive=False,
            info=get('ConcatenateAudioInfo'),
            visible=False
        )
        NUMS2TEXT_CHECKBOX = gr.Checkbox(
            label=get('Nums2Text'),
            value=False,
            info=get('Nums2TextInfo'),
            visible=False
        )

    register_component("refine_text_checkbox", REFINE_TEXT_CHECKBOX)
    register_component("split_text_checkbox", SPLIT_TEXT_CHECKBOX)
    register_component("segment_length_slider", SEGMENT_LENGTH_SLIDER)
    register_component("concatenate_audio_checkbox", CONCATENATE_AUDIO_CHECKBOX)
    register_component("nums2text_checkbox", NUMS2TEXT_CHECKBOX)


def listen():
    REFINE_TEXT_CHECKBOX.change(lambda value: update_component_value("refine_text_checkbox", value),
                                inputs=REFINE_TEXT_CHECKBOX, outputs=[])
    SPLIT_TEXT_CHECKBOX.change(
        handle_split_text_change,
        inputs=SPLIT_TEXT_CHECKBOX,
        outputs=[CONCATENATE_AUDIO_CHECKBOX]
    )
    SEGMENT_LENGTH_SLIDER.change(lambda value: update_component_value("segment_length_slider", value),
                                 inputs=SEGMENT_LENGTH_SLIDER, outputs=[])
    CONCATENATE_AUDIO_CHECKBOX.change(lambda value: update_component_value("concatenate_audio_checkbox", value),
                                      inputs=CONCATENATE_AUDIO_CHECKBOX, outputs=[])
    NUMS2TEXT_CHECKBOX.change(lambda value: update_component_value("nums2text_checkbox", value),
                              inputs=NUMS2TEXT_CHECKBOX, outputs=[])


def handle_split_text_change(value):
    update_component_value("split_text_checkbox", value)
    return gr.update(interactive=value)