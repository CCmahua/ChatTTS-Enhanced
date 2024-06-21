import torchaudio
import torch
from modules.enhance.enhancer.inference import denoise, enhance
from processors.params.process_params import EnhanceProcessParams
import os
from utils.path_utils import get_path

def enhance_processor(Params: EnhanceProcessParams):
    segment_audio_path=Params.segment_audio_path
    denoise_audio=Params.denoise_audio
    nfe = Params.nfe
    solver=Params.solver
    tau=Params.tau
    file_name=Params.file_name
    i=Params.i

    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    dwav, sr = torchaudio.load(segment_audio_path)
    dwav = dwav.mean(dim=0)

    if denoise_audio:
        dwav, sr = denoise(dwav, sr, device)

    # 执行增强
    enhanced_wav, sr = enhance(dwav, sr, device, nfe=nfe, solver=solver.lower(),
                               lambd=0.9 if denoise_audio else 0.1, tau=tau)

    enhanced_audio_data = enhanced_wav.cpu().numpy()
    enhanced_sample_rate = sr

    # 保存增强的音频
    output_path = os.path.join(get_path('OUTPUT_DIR'), file_name, '增强切片')
    enhanced_segment_audio_path = os.path.join(output_path, f"{file_name}_增强_片段_{i}.wav")
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)
    torchaudio.save(enhanced_segment_audio_path, torch.tensor(enhanced_audio_data).unsqueeze(0),
                    enhanced_sample_rate)
    print(f"增强处理的音频保存至: {enhanced_segment_audio_path}")
    print('------音频增强/降噪完成------')

    return enhanced_sample_rate , enhanced_audio_data
