import os
import json
import gradio as gr
from wording import get
from component_manager import register_component,get_component
from utils.files_utils import open_folder
from typing import Optional
from utils.path_utils import get_path
from processors.model_processor import load_chat_tts
from processors.config_processor import save_config,load_config,apply_config
from processors.params.config_params import ConfigParams

SAVE_NAME_INPUT: Optional[gr.Textbox] = None
SAVE_SEED_BUTTON: Optional[gr.Button] = None
SAVE_FEEDBACK: Optional[gr.Textbox] = None
LOAD_SEED_DROPDOWN: Optional[gr.Dropdown] = None
REFRESH_SEEDS_BUTTON: Optional[gr.Button] = None
APPLY_SEED_BUTTON: Optional[gr.Button] = None
OPENCONFIG_BUTTON: Optional[gr.Button] = None

def render():
    global SAVE_NAME_INPUT, SAVE_SEED_BUTTON, SAVE_FEEDBACK, LOAD_SEED_DROPDOWN, REFRESH_SEEDS_BUTTON, APPLY_SEED_BUTTON, OPENCONFIG_BUTTON
    with gr.Row():
        SAVE_NAME_INPUT = gr.Textbox(label=get('SaveNameInput'))
        SAVE_SEED_BUTTON = gr.Button(get('SaveSeedButton'))
    with gr.Row():
        SAVE_FEEDBACK = gr.Textbox(label=get('SaveFeedback'), interactive=False)
    with gr.Row():
        LOAD_SEED_DROPDOWN = gr.Dropdown(label=get('LoadSeedDropdown'), choices=load_settings(), interactive=True)
        REFRESH_SEEDS_BUTTON = gr.Button(get('RefreshSeedsButton'))
    with gr.Row():
        APPLY_SEED_BUTTON = gr.Button(get('ApplySeedButton'))
    OPENCONFIG_BUTTON = gr.Button(get('OpenConfigFolderButton'))

    OPENCONFIG_BUTTON.click(open_configfolder)
    REFRESH_SEEDS_BUTTON.click(refresh_settings, inputs=[], outputs=LOAD_SEED_DROPDOWN)
    SAVE_SEED_BUTTON.click(save_settings, inputs=[SAVE_NAME_INPUT], outputs=SAVE_FEEDBACK)
    APPLY_SEED_BUTTON.click(apply_settings, inputs=[LOAD_SEED_DROPDOWN], outputs=[
        get_component('audio_seed_input'),
        get_component('text_seed_input'),
        get_component('temperature_slider'),
        get_component('top_p_slider'),
        get_component('top_k_slider'),
        get_component('enhance_audio_checkbox'),
        get_component('denoise_audio_checkbox'),
        get_component('solver_dropdown'),
        get_component('nfe_slider'),
        get_component('tau_slider'),
        get_component('experimental_opinion_checkbox'),
        get_component('speed_slider'),
        get_component('oral_slider'),
        get_component('laugh_slider'),
        get_component('break_slider')
    ])



    register_component("save_name_input", SAVE_NAME_INPUT)

def save_settings(name):
    conf_params = ConfigParams(
        audio_seed=get_component('audio_seed_input').value,
        text_seed=get_component('text_seed_input').value,
        tensor=None,
        temperature=get_component('temperature_slider').value,
        top_P=get_component('top_p_slider').value,
        top_K=get_component('top_k_slider').value,
        enhance_audio=get_component('enhance_audio_checkbox').value,
        denoise_audio=get_component('denoise_audio_checkbox').value,
        solver=get_component('solver_dropdown').value,
        nfe=get_component('nfe_slider').value,
        tau=get_component('tau_slider').value,
        experimental_opinion=get_component('experimental_opinion_checkbox').value,
        speed=get_component('speed_slider').value,
        oral=get_component('oral_slider').value,
        laugh=get_component('laugh_slider').value,
        break_s=get_component('break_slider').value,
        custom_emb=get_component('emb_upload_checkbox').value,
        emb_path=get_component('emb_upload_input').value
    )
    text= save_config(name,conf_params)

    return text


def load_settings():
    settings_files =load_config()
    return settings_files

def apply_settings(name):
    se = apply_config(name)
    return se

def open_configfolder():
    open_folder(get_path('CONFIG_DIR'))


def refresh_settings():
    return gr.update(choices=load_settings())