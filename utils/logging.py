import logging
from datetime import datetime
from pythonjsonlogger import jsonlogger
from config.models.ApplicationSettings import ApplicationSettings

"""
A function which gets the configured logger function 
"""
def get_logger(name: str = __name__):
    # init the logger as usual
    log = logging.getLogger(name)
    log.setLevel(ApplicationSettings.LOG_LEVEL)
    log_handler = logging.StreamHandler()

    if ApplicationSettings.LOG_FORMAT == "JSON":
        formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
        log_handler.setFormatter(formatter)
    log.addHandler(log_handler)
    return log


"""
Custom Class which creates a log in JSON Format 
"""
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
