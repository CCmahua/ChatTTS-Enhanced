import srt
from datetime import timedelta
import librosa
import os

def generate_srt_from_audio_segments(audio_segments, text_segments, output_srt_file):
    """
    生成 SRT 文件，记录每段音频的时间戳和文本内容。

    参数:
    - audio_segments: 每段音频文件的路径列表。
    - text_segments: 每段音频对应的文本内容列表。
    - output_srt_file: 输出的 SRT 文件路径。
    """
    timestamps = []
    current_time = 0.0

    # 遍历每个音频文件，记录开始和结束时间
    for audio_path in audio_segments:
        # 使用 librosa 获取音频文件的时长
        y, sr = librosa.load(audio_path, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)

        start_time = current_time
        end_time = start_time + duration
        timestamps.append((start_time, end_time))

        current_time = end_time

    # 生成 SRT 内容
    subtitles = []
    for i, (text, (start_time, end_time)) in enumerate(zip(text_segments, timestamps)):
        subtitle = srt.Subtitle(
            index=i + 1,
            start=timedelta(seconds=start_time),
            end=timedelta(seconds=end_time),
            content=text
        )
        subtitles.append(subtitle)

    srt_content = srt.compose(subtitles)
    with open(output_srt_file, 'w', encoding='utf-8') as f:
        f.write(srt_content)

    print(f"SRT file saved to {output_srt_file}")




# def process_srt_file(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         srt_content = file.read()
#     subtitles = list(srt.parse(srt_content))
#     print(subtitles)
#     subtitle_lines = [subtitle.content for subtitle in subtitles]
#     return subtitle_lines
#
# def process_txt_file(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         content = file.readlines()
#     return content


def process_srt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()
    subtitles = list(srt.parse(srt_content))
    subtitle_text = "\n".join([subtitle.content for subtitle in subtitles])
    return subtitle_text

# Function to process TXT files
def process_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def process_file(file_path):
    results =''
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext == '.srt':
        results = process_srt_file(file_path)
    elif file_ext == '.txt':
        results = process_txt_file(file_path)
    else:
        results = "Unsupported file type"

    return results