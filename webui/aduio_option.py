import gradio as gr
from wording import get
from component_manager import register_component,update_component_value
from typing import Optional

SPEED_SLIDER : Optional[gr.Slider] = None
ORAL_SLIDER: Optional[gr.Slider] = None
LAUGH_SLIDER: Optional[gr.Slider] = None
BREAK_SLIDER: Optional[gr.Slider] = None
TEMPERATURE_SLIDER: Optional[gr.Slider] = None
TOP_P_SLIDER: Optional[gr.Slider] = None
TOP_K_SLIDER: Optional[gr.Slider] = None

def render():
    global SPEED_SLIDER,ORAL_SLIDER,LAUGH_SLIDER,BREAK_SLIDER,TEMPERATURE_SLIDER,TOP_P_SLIDER,TOP_K_SLIDER
    SPEED_SLIDER = gr.Slider(
        minimum=0, maximum=10, step=1, label=get('Speed'),
        value=0,
        info=get('SpeedInfo')
    )
    ORAL_SLIDER = gr.Slider(
        minimum=0, maximum=9, step=1, value=2, label=get('Oral'),
        info=get('OralInfo')
    )
    LAUGH_SLIDER = gr.Slider(
        minimum=0, maximum=9, step=1, value=0, label=get('Laugh'),
        info=get('LaughInfo')
    )
    BREAK_SLIDER = gr.Slider(
        minimum=0, maximum=9, step=1, value=0, label=get('Break'),
        info=get('BreakInfo')
    )

    TEMPERATURE_SLIDER = gr.Slider(
        minimum=0.00001, maximum=1.0, step=0.00001, value=0.3,
        label=get('Temperature'),
        info=get('TemperatureInfo')
    )
    TOP_P_SLIDER = gr.Slider(
        minimum=0.1, maximum=0.9, step=0.05, value=0.7,
        label=get('TopP'),
        info=get('TopPInfo')
    )
    TOP_K_SLIDER = gr.Slider(
        minimum=1, maximum=20, step=1, value=20,
        label=get('TopK'),
        info=get('TopKInfo')
    )

    register_component("speed_slider", SPEED_SLIDER)
    register_component("oral_slider", ORAL_SLIDER)
    register_component("laugh_slider", LAUGH_SLIDER)
    register_component("break_slider", BREAK_SLIDER)
    register_component("temperature_slider", TEMPERATURE_SLIDER)
    register_component("top_p_slider", TOP_P_SLIDER)
    register_component("top_k_slider", TOP_K_SLIDER)


def listen():
    SPEED_SLIDER.change(lambda value: update_component_value("speed_slider", value), inputs=SPEED_SLIDER, outputs=[])
    ORAL_SLIDER.change(lambda value: update_component_value("oral_slider", value), inputs=ORAL_SLIDER, outputs=[])
    LAUGH_SLIDER.change(lambda value: update_component_value("laugh_slider", value), inputs=LAUGH_SLIDER, outputs=[])
    BREAK_SLIDER.change(lambda value: update_component_value("break_slider", value), inputs=BREAK_SLIDER, outputs=[])
    TEMPERATURE_SLIDER.change(lambda value: update_component_value("temperature_slider", value),
                              inputs=TEMPERATURE_SLIDER, outputs=[])
    TOP_P_SLIDER.change(lambda value: update_component_value("top_p_slider", value), inputs=TOP_P_SLIDER, outputs=[])
    TOP_K_SLIDER.change(lambda value: update_component_value("top_k_slider", value), inputs=TOP_K_SLIDER, outputs=[])

