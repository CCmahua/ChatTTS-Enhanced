import gradio as gr
from wording import get
from component_manager import register_component,get_component
from typing import Optional
import os
import sys
sys.path.append(os.getcwd())
from utils.files_utils import open_folder
from utils.path_utils import get_path
from processors.audio_processor import audio_pre_processor
from processors.params.process_params import AudioPreProcessParams,TextProcessParams,EnhanceProcessParams
from processors.text_processor import batch_or_split_text
from processors.model_processor import load_chat_tts

TEXT_OUTPUT: Optional[gr.Textbox] = None
ORIGINAL_AUDIO_OUTPUT: Optional[gr.Audio] = None
ENHANCED_AUDIO_OUTPUT: Optional[gr.Audio] = None
CHAT=None

def render():
    global TEXT_OUTPUT, ORIGINAL_AUDIO_OUTPUT, ENHANCED_AUDIO_OUTPUT, GENERATE_BUTTON, OPEN_BUTTON

    TEXT_OUTPUT = gr.Textbox(label="输出信息", interactive=False)
    ORIGINAL_AUDIO_OUTPUT = gr.Audio(label="原输出音频",interactive=False)
    ENHANCED_AUDIO_OUTPUT = gr.Audio(label="增强后的音频", visible=False)

    with gr.Row():
        GENERATE_BUTTON = gr.Button("生成", variant="primary")
    OPEN_BUTTON = gr.Button(get('OutputFolderButton'))
    OPEN_BUTTON.click(open_OutPutfolder)

    register_component("text_output", TEXT_OUTPUT)
    register_component("original_audio_output", ORIGINAL_AUDIO_OUTPUT)
    register_component("enhanced_audio_output", ENHANCED_AUDIO_OUTPUT)






def listen():
    GENERATE_BUTTON.click(
        generate_audio,
        outputs=[get_component('original_audio_output'), get_component('enhanced_audio_output'), get_component('text_output')]
    )




def open_OutPutfolder():
    open_folder(get_path('OUTPUT_DIR'))


def generate_audio():

    CHAT=load_chat_tts()

    text_process_params = TextProcessParams(
    batch_processing = get_component('batch_processing_checkbox').value,
    txt_file = get_component('txt_file_input').value,
    split_text_flag = get_component('split_text_checkbox').value,
    text = get_component('text_input').value,
    segment_length = get_component('segment_length_slider').value
    )

    text_segments = batch_or_split_text(text_process_params)



    audio_pre_Process_Params = AudioPreProcessParams(
    text_segments = text_segments,
    audio_profile_path = get_component('audio_seed_input').value,# 这里先写成固定的，后面改成动态的
    speed_slider = get_component('speed_slider').value,
    temperature = get_component('temperature_slider').value,
    top_P = get_component('top_p_slider').value,
    top_K = get_component('top_k_slider').value,
    refine_oral=get_component('oral_slider').value,
    refine_laugh=get_component('laugh_slider').value,
    refine_break=get_component('break_slider').value,
    refine_text_flag = get_component('refine_text_checkbox').value,
    nums2text_switch = get_component('nums2text_checkbox').value,
    concatenate_audio=get_component('concatenate_audio_checkbox').value,
    emb_upload=get_component('emb_upload_checkbox').value,
    emb_upload_path=get_component('emb_upload_input').value,
    srt_flag=get_component('srt_processing_checkbox').value,
    batch_processing=get_component('batch_processing_checkbox').value
    )
    enhance_parms = EnhanceProcessParams(
        enhance_audio=get_component('enhance_audio_checkbox').value,
        denoise_audio=get_component('denoise_audio_checkbox').value,
        nfe=get_component('nfe_slider').value,
        solver=get_component('solver_dropdown').value,
        tau=get_component('tau_slider').value,
    )
    original_audio_output,enhanced_audio_output, text = audio_pre_processor(audio_pre_Process_Params,enhance_parms,CHAT)
    # text=''
    return original_audio_output,enhanced_audio_output, text
