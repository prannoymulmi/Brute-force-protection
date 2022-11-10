from config.config_util import get_config


class DBSettings:
    """ Project Configuration"""
    __DATA = get_config()['DB_CONFIG']
    DB_URL = __DATA["DB_URL"]
