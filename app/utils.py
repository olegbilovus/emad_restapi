import logging


class JSONLogger:
    _json_format = 'time="%(asctime)s" level=%(levelname)s env={env} %(message)s'

    def __init__(self, name: str, env: str):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(self._json_format.format(env=env)))
        self._logger.addHandler(stream_handler)

    def _log(self, level, **kwargs):
        msg = ""
        for k, v in kwargs.items():
            msg += f'{k}='
            _v = str(v)

            match v:
                case bool():
                    if v:
                        msg += "true"
                    else:
                        msg += "false"
                case float() | int():
                    msg += _v
                case _:
                    msg += f'"{_v.replace('"', '\\"')}"'

            msg += " "
        msg = msg.strip()

        self._logger.log(level, msg)

    def info(self, **kwargs):
        self._log(logging.INFO, **kwargs)

    def debug(self, **kwargs):
        self._log(logging.DEBUG, **kwargs)

    def warn(self, **kwargs):
        self._log(logging.WARN, **kwargs)

    def error(self, **kwargs):
        self._log(logging.ERROR, **kwargs)

    def critical(self, **kwargs):
        self._log(logging.CRITICAL, **kwargs)
