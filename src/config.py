import configparser


def get_config():
    return config


def save_changes():
    with open("config.ini", "w", encoding="utf-8") as configfile:
        config.write(configfile)

def init():
    config["AUTO_LOGIN"] = {}
    config["ORG_SELECTION"] = {}
    save_changes()

config = configparser.ConfigParser()
config.read("config.ini")
if "AUTO_LOGIN" not in config:
    init()
