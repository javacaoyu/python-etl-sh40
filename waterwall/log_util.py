import time


class MyLogUtil:
    def __init__(self, path='e:\\a.log'):
        self.f = open(path, 'a', encoding="UTF-8")

    def write_log(self, msg: str, level='普通'):
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        msg = f"{dt} {level} {msg}"
        self.f.write(msg)
        self.f.write("\n")
        self.f.flush()

    def close(self):
        self.f.close()
