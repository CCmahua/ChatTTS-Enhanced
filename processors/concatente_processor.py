import os
from utils.path_utils import get_path
import torchaudio
def concatenate_audio(audio_files, output_path):
    with open("filelist.txt", "w", encoding="utf-8") as f:
        for audio_file in audio_files:
            f.write(f"file '{audio_file}'\n")
    os.system(f"ffmpeg -y -loglevel error -f concat -safe 0 -i filelist.txt -c copy {output_path}")
    os.remove("filelist.txt")




def concatenate_audiofile(file_name,audio_files,enhanced_audio_files):
    original_audio_output = None
    enhanced_audio_output = None
    out_con_audio=os.path.join(get_path('OUTPUT_DIR'), file_name, '合并')
    concatenated_audio_path = os.path.join(out_con_audio, f"{file_name}_合并.wav")

    if not os.path.exists(out_con_audio):
        os.makedirs(out_con_audio, exist_ok=True)
    concatenate_audio(audio_files, concatenated_audio_path)
    print(f"合并音频保存至: {concatenated_audio_path}")

    concatenated_wav, concatenated_sr = torchaudio.load(concatenated_audio_path)
    concatenated_audio_data = concatenated_wav.flatten().numpy()
    original_audio_output = (concatenated_sr, concatenated_audio_data)
    print('------音频合并完成------')
    if len(enhanced_audio_files) > 1:
        concatenated_enhanced_audio_path = os.path.join(out_con_audio, f"{file_name}_合并_增强.wav")
        concatenate_audio(enhanced_audio_files, concatenated_enhanced_audio_path)
        print(f"增强合并音频至: {concatenated_enhanced_audio_path}")

        concatenated_enhanced_wav, concatenated_enhanced_sr = torchaudio.load(concatenated_enhanced_audio_path)
        concatenated_enhanced_audio_data = concatenated_enhanced_wav.flatten().numpy()
        enhanced_audio_output = (concatenated_enhanced_sr, concatenated_enhanced_audio_data)

    return original_audio_output, enhanced_audio_output