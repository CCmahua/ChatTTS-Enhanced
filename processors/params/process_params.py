class AudioPreProcessParams:
    def __init__(self, text_segments=None,audio_profile_path=None, speed_slider=None,temperature=None,top_P=None,top_K=None
                 ,refine_oral=None,refine_laugh=None,refine_break=None,refine_text_flag=None,nums2text_switch=None,concatenate_audio=None,emb_upload=None,emb_upload_path=None,srt_flag=None,batch_processing=None):
        self.text_segments = text_segments
        self.audio_profile_path = audio_profile_path
        self.speed_slider = speed_slider
        self.temperature = temperature
        self.top_P = top_P
        self.top_K = top_K
        self.refine_oral=refine_oral
        self.refine_laugh=refine_laugh
        self.refine_break=refine_break
        self.refine_text_flag=refine_text_flag
        self.nums2text_switch=nums2text_switch
        self.concatenate_audio = concatenate_audio
        self.emb_upload = emb_upload
        self.emb_upload_path = emb_upload_path
        self.srt_flag=srt_flag
        self.batch_processing=batch_processing




class AudioProcessParams:
    def __init__(self, text_segments=None, aduio_profile_path=None, speed_slider=None, temperature=None, top_P=None,
                 top_K=None
                 , refine_oral=None, refine_laugh=None, refine_break=None):
        self.text_segments = text_segments
        self.aduio_profile_path = aduio_profile_path
        self.speed_slider = speed_slider
        self.temperature = temperature
        self.top_P = top_P
        self.top_K = top_K
        self.refine_oral = refine_oral
        self.refine_laugh = refine_laugh
        self.refine_break = refine_break

class EnhanceProcessParams:
    def __init__(self, segment_audio_path=None,enhance_audio=None, denoise_audio=None, nfe=None, solver=None, tau=None,
                 file_name=None,i=None
                ):
        self.segment_audio_path = segment_audio_path
        self.enhance_audio = enhance_audio
        self.denoise_audio = denoise_audio
        self.nfe = nfe
        self.solver = solver
        self.tau = tau
        self.file_name = file_name
        self.i=i




class TextProcessParams:
    def __init__(self, batch_processing=None, txt_file=None, split_text_flag=None, text=None,segment_length=None):
        self.batch_processing = batch_processing
        self.txt_file = txt_file
        self.split_text_flag = split_text_flag
        self.text = text
        self.segment_length = segment_length