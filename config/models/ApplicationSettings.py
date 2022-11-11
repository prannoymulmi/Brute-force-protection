from config.config_util import get_config


class ApplicationSettings:
    """ Application Configuration"""
    __DATA = get_config()['APPLICATION_CONFIG']
    LOGIN_MAX_ATTEMPT_COUNT = __DATA["LOGIN_MAX_ATTEMPT_COUNT"]
    LOGIN_USER_BLOCKED_TIME_MINUTES = __DATA["LOGIN_USER_BLOCKED_TIME_MINUTES"]