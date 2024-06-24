import base64
import numpy as np
from flask import Flask, request, send_file
import os
import sys
from scipy.io.wavfile import write

sys.path.append(os.getcwd())
from processors.audio_processor import audio_pre_processor
from processors.params.process_params import AudioPreProcessParams, TextProcessParams, EnhanceProcessParams
from processors.text_processor import batch_or_split_text
from processors.model_processor import load_chat_tts

app = Flask(__name__)
CHAT = load_chat_tts()

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    data = request.json
    
    text_process_params = TextProcessParams(
        batch_processing=data.get('batch_processing', False),
        txt_file=data.get('txt_file', ''),
        split_text_flag=data.get('split_text_flag', False),
        text=data.get('text', ''),
        segment_length=data.get('segment_length', 100)
    )

    text_segments = batch_or_split_text(text_process_params)

    audio_pre_process_params = AudioPreProcessParams(
        text_segments=text_segments,
        audio_profile_path=data.get('audio_profile_path', ''),
        speed_slider=data.get('speed_slider', 1.0),
        temperature=data.get('temperature', 0.7),
        top_P=data.get('top_P', 0.9),
        top_K=data.get('top_K', 50),
        refine_oral=data.get('refine_oral', 0.5),
        refine_laugh=data.get('refine_laugh', 0.5),
        refine_break=data.get('refine_break', 0.5),
        refine_text_flag=data.get('refine_text_flag', False),
        nums2text_switch=data.get('nums2text_switch', False),
        concatenate_audio=data.get('concatenate_audio', False),
        emb_upload=data.get('emb_upload', False),
        emb_upload_path=data.get('emb_upload_path', ''),
        srt_flag=data.get('srt_flag', False),
        batch_processing=data.get('batch_processing', False)
    )
    
    enhance_params = EnhanceProcessParams(
        enhance_audio=data.get('enhance_audio', False),
        denoise_audio=data.get('denoise_audio', False),
        nfe=data.get('nfe', 1.0),
        solver=data.get('solver', 'default'),
        tau=data.get('tau', 0.1)
    )
    
    original_audio_output, enhanced_audio_output, text = audio_pre_processor(audio_pre_process_params, enhance_params, CHAT)
    
    # 将ndarray写入到WAV文件中
    write('output_audio.wav', 24000, original_audio_output[1])
    
    if original_audio_output[1] is None:
        return {'error': 'Failed to encode audio.'}, 500
    
    # 直接发送音频文件
    return send_file('output_audio.wav', mimetype='audio/wav')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
