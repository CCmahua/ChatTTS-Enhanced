

class ConfigParams:
    def __init__(self, audio_seed=None, text_seed=None, tensor=None, temperature=None, top_P=None, top_K=None, enhance_audio=None, denoise_audio=None, solver=None, nfe=None, tau=None, experimental_opinion=None, speed=None, oral=None, laugh=None, break_s=None,custom_emb=None,emb_path=None):
        self.audio_seed = audio_seed
        self.text_seed = text_seed
        self.tensor = tensor
        self.temperature = temperature
        self.top_P = top_P
        self.top_K = top_K
        self.enhance_audio = enhance_audio
        self.denoise_audio = denoise_audio
        self.solver = solver
        self.nfe = nfe
        self.tau = tau
        self.experimental_opinion = experimental_opinion
        self.speed = speed
        self.oral = oral
        self.laugh = laugh
        self.break_s = break_s
        self.custom_emb=custom_emb
        self.emb_path = emb_path
