from processors.params.process_params import TextProcessParams
from utils.text_utils import replace_tokens,split_text,restore_tokens
from utils.srt_utils import process_file
def batch_or_split_text(params: TextProcessParams):
    batchData= {}
    batch_processing = params.batch_processing
    txt_file = params.txt_file
    split_text_flag = params.split_text_flag
    text = params.text
    segment_length = params.segment_length
    # 批量处理
    if batch_processing and txt_file is not None:
        if isinstance(txt_file, list) and len(txt_file) > 1:
            for file in txt_file:
                batchData[file] = process_text(process_file(file),segment_length)
        else:
            file = txt_file if isinstance(txt_file, str) else txt_file[0]
            print(process_file(file))
            batchData[file] = process_text(process_file(file),segment_length)

    if batch_processing:
        text_segments = batchData
    else:
        text_segments = {None: process_text(text, segment_length)}
    return text_segments



def process_text(lines, min_length):
    replaced_tokens = replace_tokens(lines)
    text_segments = split_text(replaced_tokens, min_length=min_length)

    for i, segment in enumerate(text_segments):
        text_segments[i] = restore_tokens(segment)

    return text_segments