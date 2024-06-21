from modules import ChatTTS
import torch
chat = None

def load_chat():
    global chat
    chat = ChatTTS.Chat()
    chat.load_models()



def load_chat_tts():
    if chat is None:
        load_chat()
    if chat is None:
        raise Exception("ChatTTS加载失败")
    return chat


def get_seed_tensor(audio_seed):
    global chat
    if chat is None:
        load_chat()
    torch.manual_seed(audio_seed)
    tensor= chat.sample_random_speaker()
    return tensor


