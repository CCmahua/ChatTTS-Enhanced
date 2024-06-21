import configparser



def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def get_server_config(config):
    custom_server = config.getboolean('server', 'custom_server', fallback=False)
    ip_address = config.get('server', 'ip', fallback='127.0.0.1')
    port = config.getint('server', 'port', fallback=7860)
    return custom_server, ip_address, port
