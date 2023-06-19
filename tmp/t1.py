
class Dog:
    def __init__(self, name):
        self.name = name

    def wangwang(self):
        print(f"我是一条小狗，我叫：{self.name}，汪汪汪")

    @staticmethod
    def dance():
        print(f"我是小狗，我会跳舞。。。")

# class：模板
# 对象： 基于模板创建的

# class：规划好的流水线
# 对象：流水线生成的产品

# class：手机流水线.输出流水线信息
# 对象：Iphone6
