import sys
from datetime import datetime


class JSONLogger:
    _json_format = 'time="%(asctime)s" level=%(levelname)s env={env} %(message)s'

    def __init__(self, env: str):
        self._env = env

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

        print(f'time="{datetime.now().isoformat()}" level={level} env={self._env} {msg}')

    def info(self, **kwargs):
        self._log("INFO", **kwargs)

    def debug(self, **kwargs):
        self._log("DEBUG", **kwargs)

    def warn(self, **kwargs):
        self._log("WARN", **kwargs)

    def error(self, **kwargs):
        self._log("ERROR", **kwargs)

    def critical(self, **kwargs):
        self._log("CRITICAL", **kwargs)
