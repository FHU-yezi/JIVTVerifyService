import json
import logging
from datetime import datetime

from flask import Flask, request

from db_config import ActivationCodeData, db

api = Flask(__name__)

logging.basicConfig(filename="verify_log.log", level=logging.DEBUG, 
                    format="[%(asctime)s] %(levelname)s: %(message)s")

def SearchByCode(code):
    try:
        search_result = ActivationCodeData.get(ActivationCodeData.code==code).__dict__["__data__"]
    except Exception:  # 没有对应的激活码
        logging.debug(f"没有找到 {code} 对应的激活码信息")
        return None
    else:
        logging.debug(f"找到了 {code} 对应的激活码信息")
        return search_result

def ExistCode(code):
    search_result = SearchByCode(code)
    if search_result != None:
        logging.debug(f"存在 {code} 对应的激活码")
        return True
    else:
        logging.debug(f"不存在 {code} 对应的激活码")
        return False

def CodeNotUsed(code):
    if ExistCode(code) == False:
        logging.debug(f"因 {code} 对应的激活码不存在，CodeNotUsed 函数返回了 False")
        return False
    code_data = SearchByCode(code)
    if code_data["used"] == False and code_data["use_time"] == None:
        return True
    else:
        return False

def MarkCodeUsed(code):
    use_time = datetime.fromtimestamp(round(datetime.now().timestamp()))  # 获取当前时间，精确到秒
    ActivationCodeData.update(used=True, use_time=use_time).where(ActivationCodeData.code==code).execute()
    logging.info(f"已将 {code} 对应的激活码标记为已使用，使用时间为 {use_time}")

@api.route("/jivt/VerifyCode", methods=["POST"])
def VerifyCode():
    if "code" not in request.form:
        logging.warning("收到了一个缺少 code 参数的请求")
        result = {
            "status_code": 400, 
            "message": "缺少 code 参数"
        }
        return json.dumps(result)
    
    code = request.form["code"]
    logging.info(f"已从请求表单中获取激活码，值为 {code}")
    if ExistCode(code) == False:
        logging.warning(f"因 {code} 对应的激活码不存在，返回状态码 404")
        result = {
            "status_code": 404, 
            "message": "激活码不存在"
        }
        return json.dumps(result)
    if CodeNotUsed(code) == False:
        logging.warning(f"因 {code} 对应的激活码已被使用，返回状态码 403")
        result = {
            "status_code": 403, 
            "message": "激活码已被使用"
        }
        return json.dumps(result)
    
    MarkCodeUsed(code)
    logging.info(f"{code} 已使用，返回状态码 200")
    result = {
        "status_code": 200, 
        "message": "激活成功"
    }
    return json.dumps(result)

if __name__ == "__main__":
    logging.info("程序开始运行")
    api.run(port=8505)