from config.config_util import get_config


class ProjectSettings:
    """ Project Configuration"""
    __DATA = get_config()['PROJECT_CONFIG']
    PROJECT_NAME = __DATA["PROJECT_NAME"]
    PROJECT_DESCRIPTION = __DATA["PROJECT_DESCRIPTION"]
    API_VERSION = __DATA["API_VERSION"]
    API_VERSION_PATH = __DATA["API_VERSION_PATH"]