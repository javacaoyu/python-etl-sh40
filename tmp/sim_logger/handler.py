

class MyFileHandler:

    def __init__(self, path):
        self.path = path
        self.fmt = None
        self.f = open(self.path, 'a', encoding="UTF-8")

    def setFormatter(self, fmt):
        self.fmt = fmt

    def output(self, msg, level):
        if self.fmt.fmt_type == 1:
            self.f.write(f"打印日志：{msg}, 日志级别：{level}")
            self.f.write("\n")
        elif self.fmt.fmt_type == 2:
            self.f.write(f"---{msg}---, [{level}]")
            self.f.write("\n")
        elif self.fmt.fmt_type == 3:
            self.f.write(f"[{level}:{msg}]")
            self.f.write("\n")
        else:
            self.f.write(f"{msg}")
            self.f.write("\n")
