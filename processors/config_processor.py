import json
import os
from utils.path_utils import get_path
from processors.params.config_params import ConfigParams
from processors.model_processor import get_seed_tensor
import torch

def save_config(name,con_params: ConfigParams):
    con_params.tensor=get_seed_tensor(con_params.audio_seed)
    if con_params.custom_emb and con_params.emb_path is not None:
        con_params.tensor=torch.load(con_params.emb_path)
    save_path=os.path.join(get_path('CONFIG_DIR'), f"{name}.pt")
    torch.save(con_params, save_path)
    return f"配置保存至 {save_path}"



def load_config():
    settings_files = []
    for filename in os.listdir(get_path('CONFIG_DIR')):
        if filename.endswith(".pt"):
            settings_files.append(filename[:-3])
    return settings_files


def apply_config(name):
    filename = os.path.join(get_path('CONFIG_DIR'), f"{name}.pt")
    loaded_conf_params = torch.load(filename)
    return (
        f"{name}.pt",
        loaded_conf_params.text_seed,
        loaded_conf_params.temperature,
        loaded_conf_params.top_P,
        loaded_conf_params.top_K,
        loaded_conf_params.enhance_audio,
        loaded_conf_params.denoise_audio,
        loaded_conf_params.solver,
        loaded_conf_params.nfe,
        loaded_conf_params.tau,
        loaded_conf_params.experimental_opinion,
        loaded_conf_params.speed,
        loaded_conf_params.oral,
        loaded_conf_params.laugh,
        loaded_conf_params.break_s
    )



def upload_speaker_config(name):
    print('111上传音色')