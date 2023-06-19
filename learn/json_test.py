# coding:utf8
"""
演示Json和字典的关系
"""
import json

stu_dict1 = {"name": "周杰轮", "age": 11, "addr": "上海"}
stu_dict2 = {"name": "周杰轮", "age": 11, "hobby": ["football", "basketball"]}

# 这种字符串，称之为Json数据格式
stu_str1 = '{"name": "林军杰", "age": 11, "addr": "上海"}'
stu_str2 = '{"name": "林军杰", "age": 11, "hobby": ["football", "basketball"]}'

# 字典转字符串
print("-" * 15, "字典转字符串")
dict_to_str1 = json.dumps(stu_dict1, ensure_ascii=False)
dict_to_str2 = json.dumps(stu_dict2, ensure_ascii=False)
print(type(dict_to_str1), type(dict_to_str2))
print(dict_to_str1)
print(dict_to_str2)


# 字符串转字典
print("-" * 15, "字符串转字典")
str_to_dict1 = json.loads(stu_str1)
str_to_dict2 = json.loads(stu_str2)
print(type(str_to_dict1), type(str_to_dict2))
print(str_to_dict1['name'])
print(str_to_dict2['hobby'])

