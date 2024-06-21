import gradio as gr
from wording import get
import batch_option
import text_options
import seed_option
import aduio_option
import enhance_option
import output_option
import config_option
from webuiutils import read_config, get_server_config



def main():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown(get('Title'))
        gr.Markdown(get('VersionDescription'))
        with gr.Row():
            with gr.Column():
                batch_option.render()
                with gr.Row():
                    gr.Markdown(get('TextOptionsTitle'))
                text_options.render()
                with gr.Row():
                    gr.Markdown(get('SeedOptionsTitle'))
                seed_option.render()
                with gr.Row():
                    gr.Markdown(get('AudioOptionsTitle'))
                aduio_option.render()
                with gr.Row():
                    gr.Markdown(get('AudioEnhancementTitle'))
                enhance_option.render()

            with gr.Column():
                output_option.render()
                gr.Markdown(get('configmanager'))
                config_option.render()
                with gr.Accordion(get('HelpTitle'), open=False):
                    gr.Markdown(get('HelpContent'))
                    with gr.Row():
                        gr.Markdown(" ")
                    with gr.Row():
                        gr.Markdown(" ")
                with gr.Row():
                    gr.Markdown('🔧项目地址:https://github.com/CCmahua/ChatTTS-Enhanced')

        batch_option.listen()
        text_options.listen()
        seed_option.listen()
        aduio_option.listen()
        enhance_option.listen()
        output_option.listen()

        config = read_config('config.ini')
        custom_server, ip_address, port = get_server_config(config)
        if custom_server:
            demo.launch(inbrowser=True, server_name=ip_address, server_port=port)
        else:
            demo.launch(inbrowser=True)



if __name__ == '__main__':
    main()