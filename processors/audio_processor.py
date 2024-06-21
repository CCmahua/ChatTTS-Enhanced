from processors.params.process_params import AudioPreProcessParams,AudioProcessParams,EnhanceProcessParams
from processors.enhance_processors import enhance_processor
from processors.concatente_processor import concatenate_audiofile
import os
import torch
import torchaudio
import numpy as np
from utils.path_utils import get_path
from utils.srt_utils import generate_srt_from_audio_segments
#音频列表
audio_files = []
enhanced_audio_files = []

def audio_pre_processor(params: AudioPreProcessParams,enparams: EnhanceProcessParams,CHAT):

    text_segments = params.text_segments
    audio_profile_path = params.audio_profile_path
    speed_slider = params.speed_slider
    temperature = params.temperature
    top_P = params.top_P
    top_K = params.top_K
    refine_oral=params.refine_oral
    refine_laugh = params.refine_laugh
    refine_break = params.refine_break
    refine_text_flag=params.refine_text_flag
    nums2text_switch = params.nums2text_switch
    concatenate_audio =params.concatenate_audio
    emb_upload=params.emb_upload
    emb_upload_path=params.emb_upload_path
    srt_flag=params.srt_flag
    batch_processing=params.batch_processing


    enhance_audio=enparams.enhance_audio
    denoise_audio=enparams.denoise_audio

    if emb_upload:
        rand_spk = torch.load(emb_upload_path)
    else:
        if isinstance(audio_profile_path, str) and audio_profile_path.endswith('.pt'):
            spk = torch.load(os.path.join(get_path('CONFIG_DIR'), audio_profile_path))
            rand_spk = spk.tensor
        else:
            torch.manual_seed(audio_profile_path)
            rand_spk = CHAT.sample_random_speaker()

    params_infer_code = {
        'prompt': f'[speed_{speed_slider}]',
        'spk_emb': rand_spk,
        'temperature': temperature,
        'top_P': top_P,
        'top_K': top_K,
    }

    params_refine_text = {'prompt': f'[oral_{refine_oral}][laugh_{refine_laugh}][break_{refine_break}]'}
    file_name = None
    for file, content in text_segments.items():
        audio_files = []
        enhanced_audio_files = []
        if file:
            file_name = os.path.splitext(os.path.basename(file))[0]
        else:
            file_name = 'segment'

        for i, segment in enumerate(content):
            print('')
            print('')
            print('')
            print(segment)
            if not isinstance(segment, str):
                segment = str(segment)
            segment_audio_path,sample_rate,audio_data = audio_processor(CHAT, file_name,segment,refine_text_flag,nums2text_switch,params_refine_text,params_infer_code,i)
            audio_files.append(segment_audio_path)

            if enhance_audio or denoise_audio:
                enparams.segment_audio_path=segment_audio_path
                enparams.file_name = file_name
                enparams.i=i
                enhanced_sample_rate, enhanced_audio_data = enhance_processor(enparams)
                enhanced_audio_files.append(segment_audio_path)

        if srt_flag and batch_processing:
            srt_path = os.path.join(get_path('OUTPUT_DIR'), file_name, f'{file_name}.srt')
            generate_srt_from_audio_segments(audio_files, content, srt_path)


        if len(audio_files) > 1:
            concatenated_or, concatenated_en =concatenate_audiofile(file_name,audio_files,enhanced_audio_files)

    original_audio_output = None
    enhanced_audio_output = None
    if len(audio_files) > 1:
        text = '批量合并处理完成'
        original_audio_output = concatenated_or
        if enhance_audio:
            enhanced_audio_output = concatenated_en
            text = '批量合并增强处理完成'
        else:
            enhanced_audio_output = None
        if len(text_segments) > 1:
            original_audio_output =None
            enhanced_audio_output =None
    else:
        original_audio_output = (sample_rate, audio_data)
        text = '音频处理完成'
        if enhance_audio:
            text = '音频增强处理完成'
            enhanced_audio_output = (enhanced_sample_rate,enhanced_audio_data)
        else:
            enhanced_audio_output = None
    # 当关闭增强的时候报错问题
    return original_audio_output,enhanced_audio_output, text

def audio_processor(chat,file_name,segment,refine_text_flag,nums2text_switch,params_refine_text,params_infer_code,i):
    if refine_text_flag:
        segment = chat.infer(segment,
                             skip_refine_text=False,
                             refine_text_only=True,
                             params_refine_text=params_refine_text,
                             params_infer_code=params_infer_code
                             )

    wav = chat.infer(segment,
                     skip_refine_text=True,
                     params_refine_text=params_refine_text,
                     params_infer_code=params_infer_code
                     )
    # 获取音频Data
    audio_data = np.array(wav[0]).flatten()
    # 音频码率
    sample_rate = 24000
    # enhanced_sample_rate = 0
    # 保存tts切片输出

    output_path=os.path.join(get_path('OUTPUT_DIR'), file_name, '切片')
    segment_audio_path = os.path.join(output_path, f"{file_name}_{i}.wav")
    if not os.path.exists(output_path):
       os.makedirs(output_path, exist_ok=True)
    torchaudio.save(segment_audio_path, torch.tensor(audio_data).unsqueeze(0), sample_rate)
    print(f"切片音频保存至: {segment_audio_path}")
    print('------ChatTTS生成完成------')
    return segment_audio_path,sample_rate,audio_data




