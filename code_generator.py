from print_with_color import print_green
from db_config import ActivationCodeData, db
from random import choice

all_character = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "A", "B", "C", "D", "E", "F"]

def GenerateFive():
    result = ""
    for _ in range(5):
        result += choice(all_character)
    return result

def GenerateNewCode():
    result = "-".join([GenerateFive() for _ in range(5)])
    return result

print("激活码生成程序")

answer = input("请选择操作：\n1. 生成一般激活码\n2. 生成特殊类型 1 激活码\n3. 生成测试用激活码\n>>>")

if answer not in ["1", "2", "3"]:
    exit()

total_codes_count = int(input("请输入要生成的激活码数量\n>>>"))

if input("确认生成？(y/n)\n>>>") != "y":
    exit()

print("开始生成")

codes_list = []
for _ in range(total_codes_count):
    codes_list.append(GenerateNewCode())

data_list = []
for code in codes_list:
    code_data = {
        "code": code, 
        "code_type": {
            "1": 1, 
            "2": 2, 
            "3": 0
            }[answer], 
        "used": False, 
    }
    data_list.append(code_data)

db.connect()
db.create_tables([ActivationCodeData])  # 如果表已存在则不会创建
ActivationCodeData.insert_many(data_list).execute()

print_green(f"已生成 {total_codes_count} 个激活码")