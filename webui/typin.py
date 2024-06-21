from typing import Literal, Any, IO
import gradio

File = IO[Any]
Component = gradio.File or gradio.Image or gradio.Video or gradio.Slider or gradio.Checkbox
ComponentName = Literal\
[
	'batch_processing_checkbox',
	'srt_processing_checkbox',
	'text_input',
	'txt_file_input',
	'source_image',
	'speed_slider',
	'oral_slider',
	'laugh_slider',
	'break_slider',
	'temperature_slider',
	'top_p_slider',
	'top_k_slider',
	'audio_seed_input',
	'text_seed_input',
	'experimental_opinion_checkbox',
	'enhance_audio_checkbox',
	'denoise_audio_checkbox',
	'solver_dropdown',
	'nfe_slider',
	'tau_slider',
	'text_output',
	'original_audio_output',
	'enhanced_audio_output',
	'refine_text_checkbox',
	'split_text_checkbox',
	'segment_length_slider',
	'concatenate_audio_checkbox',
	'nums2text_checkbox',
	'save_name_input',
	'emb_upload_checkbox',
	'emb_upload_input'

]


