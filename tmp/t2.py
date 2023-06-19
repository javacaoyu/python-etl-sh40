import json
stu_str1 = '{"name": "王力鸿", "age": 11, "addr": "航头"}'
stu_str2 = '{"name": "周杰轮", "age": 13, "addr": "周浦"}'
stu_str3 = '{"name": "张学油", "age": 16, "addr": "下沙"}'

stu_dict1 = json.loads(stu_str1)
stu_dict2 = json.loads(stu_str2)
stu_dict3 = json.loads(stu_str3)
print(stu_dict1)

class Stu:

    def __init__(self, name, age, addr):
        self.name = name
        self.age = age
        self.addr = addr

    def __str__(self):
        s = f"哥们叫：{self.name}，来自：{self.addr}，今年：{self.age}大啦。"
        return s

    def to_csv(self):
        return self.name + "," + str(self.age) + "," + self.addr

    def generate_insert_sql(self):
        return f"INSERT INTO itheima666 VALUES('{self.name}', {self.age}, '{self.addr}')"

stu1 = Stu(stu_dict1['name'], stu_dict1['age'], stu_dict1['addr'])
stu2 = Stu(stu_dict2['name'], stu_dict2['age'], stu_dict2['addr'])
stu3 = Stu(stu_dict3['name'], stu_dict3['age'], stu_dict3['addr'])
print(stu1.to_csv())
print(stu2.to_csv())
print(stu3.to_csv())

print(stu1.generate_insert_sql())
print(stu2.generate_insert_sql())
print(stu3.generate_insert_sql())





