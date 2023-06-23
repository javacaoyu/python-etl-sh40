# coding:utf8
"""
后端服务写出log日志的模拟数据生成器
"""
import datetime
import random
import sys
import time

single_log_lines = 1024                             # 一个logs文件生成多少行数据
generate_files = 1                                  # 一次运行生成多少个文件
output_path = "E:/pyetl-data-backend-logs/"         # 数据写出的路径

# 前置检查
print(f"模拟器生成的数据将写入到：{output_path}，"
      f"请确认\n"
      f"\t 正确：输入y并回车\n"
      f"\t 错误：输入n并回车\n")
choose = input("请输入你的选择[y/n]：")
if not choose == 'y':
    print("数据写入路径未确认，程序退出。", file=sys.stderr)
    print("请修改代码中：output_path变量的值", file=sys.stderr)
    sys.exit()

# 准备日志级别数据
log_level_array = ['WARN', 'WARN', 'WARN', 'INFO', 'INFO', 'INFO', 'INFO', 'INFO', 'INFO', 'INFO', 'INFO',
                   'INFO', 'INFO', 'INFO', 'INFO', 'INFO', 'INFO', 'INFO', 'INFO', 'INFO', 'INFO', 'INFO', 'INFO',
                   'ERROR']

# 准备后台代码模块名称
backend_files_name = ['barcode_service.py', 'barcode_service.py', 'barcode_service.py',
                      'orders_service.py', 'orders_service.py', 'orders_service.py', 'orders_service.py',
                      'orders_service.py', 'orders_service.py',
                      'shop_manager.py', 'shop_manager.py',
                      'user_manager.py', 'user_manager.py', 'user_manager.py',
                      'goods_manager.py', 'goods_manager.py', 'goods_manager.py', 'goods_manager.py',
                      'goods_manager.py', 'goods_manager.py',
                      'base_network.py', 'base_network.py',
                      'event.py', 'event.py', 'event.py', 'event.py', 'event.py', 'event.py', 'event.py']

# 行政区域数据准备
visitor_areas = {
    '北京市': ['海淀区', '大兴区', '丰台区', '朝阳区', '昌平区', '海淀区', '怀柔区'],
    '上海市': ['静安区', '黄浦区', '徐汇区', '普陀区', '杨浦区', '宝山区', '浦东新区', '浦东新区'],
    '重庆市': ['万州区', '万州区', '涪陵区', '渝中区', '沙坪坝区', '九龙坡区', '南岸区'],
    '江苏省': ['南京市', '南京市', '南京市', '苏州市', '苏州市', '无锡市', '常州市', '宿迁市', '张家港市'],
    '安徽省': ['阜阳市', '阜阳市', '六安市', '合肥市', '合肥市', '合肥市', '池州市', '铜陵市', '芜湖市'],
    '山东省': ['济南市', '济南市', '青岛市', '青岛市', '青岛市', '菏泽市'],
    '湖北省': ['武汉市', '武汉市', '武汉市', '十堰市', '荆州市', '恩施土家族苗族自治州'],
    '广东省': ['广州市', '广州市', '广州市', '深圳市', '深圳市', '深圳市', '珠海市'],
    '天津市': ['和平区', '河东区', '河西区', '武清区', '宝坻区'],
    '湖南省': ['长沙市', '长沙市', '长沙市', '长沙市', '长沙市', '长沙市', '长沙市', '株洲市', '张家界市', '常德市', '益阳市'],
    '浙江省': ['杭州市', '杭州市', '湖州市', '绍兴市', '舟山市', '金华市', '嘉兴市', '丽水市']
}
# 准备省份
visitor_province = ['北京市', '上海市', '重庆市', '江苏省', '安徽省', '山东省', '湖北省', '广东省', '天津市', '湖南省', '浙江省']

response_flag = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
response_for_error_flag = [1, 1, 1, 1, 1, 0]

# 准备日志信息
messages = [
    "服务器宕机啦，快来恢复。", "数据库崩溃啦，快来恢复。", "明天就发工资了，今天大家好好卷。",
    "学IT来黑马，就来黑马程序员", "键盘敲烂，月薪过万。笔记翻烂，薄纱面试官。",
    "招商银行提示您，您尾号0000的账号，入账工资：150000元【代发】", "哥，保时捷新款SUV要来了解一下不",
    "看啥呢，别看日志了，快写代码，说的就是你。",
    "【骚扰短信】招商银行提示您：您尾号0000的账户，存款超过10000000，可以升级到SVIP级别，详情点击：https://www.itheima.com",
    "看的爽不爽？多写两行代码都能实现。", "【杭州下沙奔驰4S店】您的爱车：迈巴赫S650已经到了保养日期了，欢迎您到店保养。",
    "【腾讯游戏】S99赛季结算完成，您在本赛季的排名是：青铜，请在S100赛季继续努力",
    "【Apache Spark】感谢您对Apache Spark开源项目的支持，截至今日您已贡献超过100000行代码。",
    "【骚扰短信】我们是专业保洁公司的，哥，您在下沙滨江的别墅需要打扫卫生吗，价格合适，详情：400-618-9090",
    "想要高薪就业？除了Hadoop、Hive、Spark、项目以外，没事就要刷刷SQL，SQL经常面试用到哦。"
]
for j in range(0, generate_files):
    write_file_path = f'{output_path}{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.log'
    with open(write_file_path, 'w', encoding="UTF-8") as f:
        for i in range(single_log_lines):
            date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            log_level = log_level_array[random.randint(0, len(log_level_array) - 1)]
            file_name = backend_files_name[random.randint(0, len(backend_files_name) - 1)]
            if not log_level == "ERROR":
                if response_flag[random.randint(0, len(response_flag) - 1)] == 1:
                    response_time = random.randint(0, 1000)
                else:
                    response_time = random.randint(1000, 9999)
            else:
                if response_for_error_flag[random.randint(0, len(response_for_error_flag) - 1)] == 1:
                    response_time = random.randint(0, 1000)
                else:
                    response_time = random.randint(1000, 9999)

            province = visitor_province[random.randint(0, len(visitor_province) - 1)]
            city = visitor_areas[province][random.randint(0, len(visitor_areas[province]) - 1)]

            log_str = f"{date_str}\t[{log_level}]\t{file_name}\t响应时间:{response_time}ms\t{province}\t{city}\t" \
                      f"{random.choice(messages)}"

            f.write(log_str)
            f.write("\n")
    print(f"本次写出第: {j + 1}个文件完成, 文件为: {write_file_path}, 行数:{single_log_lines}")
    time.sleep(1)
