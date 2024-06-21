import gradio as gr
from wording import get
from component_manager import register_component,update_component_value,get_component
from typing import Optional

ENHANCE_AUDIO_CHECKBOX: Optional[gr.Checkbox] = None
DENOISE_AUDIO_CHECKBOX: Optional[gr.Checkbox] = None
SOLVER_DROPDOWN: Optional[gr.Dropdown] = None
NFE_SLIDER: Optional[gr.Slider] = None
TAU_SLIDER: Optional[gr.Slider] = None

def render():
    global ENHANCE_AUDIO_CHECKBOX, DENOISE_AUDIO_CHECKBOX, SOLVER_DROPDOWN, NFE_SLIDER, TAU_SLIDER

    with gr.Row():
        ENHANCE_AUDIO_CHECKBOX = gr.Checkbox(
            value=False, label=get('EnhanceAudio'),
            info=get('EnhanceAudioInfo')
        )
        DENOISE_AUDIO_CHECKBOX = gr.Checkbox(
            value=False, label=get('DenoiseAudio'),
            info=get('DenoiseAudioInfo')
        )
    with gr.Row():
        SOLVER_DROPDOWN = gr.Dropdown(
            choices=["Midpoint", "RK4", "Euler"], value="Midpoint",
            label=get('Solver'),
            info=get('SolverInfo')
        )
    with gr.Row():
        NFE_SLIDER = gr.Slider(
            minimum=1, maximum=128, value=64, step=1,
            label=get('Nfe'),
            info=get('NfeInfo')
        )
    with gr.Row():
        TAU_SLIDER = gr.Slider(
            minimum=0, maximum=1, value=0.5, step=0.01,
            label=get('Tau'),
            info=get('TauInfo')
        )

    register_component("enhance_audio_checkbox", ENHANCE_AUDIO_CHECKBOX)
    register_component("denoise_audio_checkbox", DENOISE_AUDIO_CHECKBOX)
    register_component("solver_dropdown", SOLVER_DROPDOWN)
    register_component("nfe_slider", NFE_SLIDER)
    register_component("tau_slider", TAU_SLIDER)


def listen():
    ENHANCE_AUDIO_CHECKBOX.change(
        handle_enhance_audio_change,
        inputs=ENHANCE_AUDIO_CHECKBOX,
        outputs=[get_component('enhanced_audio_output')]
    )
    DENOISE_AUDIO_CHECKBOX.change(lambda value: update_component_value("denoise_audio_checkbox", value),
                                  inputs=DENOISE_AUDIO_CHECKBOX, outputs=[])
    SOLVER_DROPDOWN.change(lambda value: update_component_value("solver_dropdown", value), inputs=SOLVER_DROPDOWN,
                           outputs=[])
    NFE_SLIDER.change(lambda value: update_component_value("nfe_slider", value), inputs=NFE_SLIDER, outputs=[])
    TAU_SLIDER.change(lambda value: update_component_value("tau_slider", value), inputs=TAU_SLIDER, outputs=[])

def handle_enhance_audio_change(value):
    update_component_value("enhance_audio_checkbox", value)
    return gr.update(visible=value)