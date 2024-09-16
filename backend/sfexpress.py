# 导入必要的模块
from fastapi import FastAPI  # 用于创建 API 应用
from pydantic import BaseModel  # 用于数据验证和序列化
import time  # 用于生成时间戳
import uuid  # 用于生成唯一标识符
import requests  # 用于发送 HTTP 请求
import hashlib  # 用于生成 MD5 哈希
import base64  # 用于 Base64 编码
import urllib  # 用于 URL 编码
import json  # 用于 JSON 处理
import os  # 用于操作系统相关功能（此代码中未使用）

# 创建 FastAPI 应用实例
app = FastAPI()

# 定义常量
partnerID = 'Y4E4GTVT'  # 合作伙伴ID
checkword = 'UC5OG1vBK9WoDiHQLh1aEAp0gts3Qkxn'  # 校验码
reqURL = 'https://sfapi.sf-express.com/std/service'  # API 请求URL
serviceCode = "EXP_RECE_QUERY_DELIVERTM"  # 服务代码

# 定义地址模型
class Address(BaseModel):
    province: str  # 省份
    city: str  # 城市
    district: str  # 区/县
    address: str  # 详细地址

# 定义查询数据模型
class QueryData(BaseModel):
    businessType: str  # 业务类型
    consignedTime: str  # 托运时间
    searchPrice: str  # 查询价格
    weight: float  # 重量
    srcAddress: Address  # 始发地址
    destAddress: Address  # 目的地址

# 定义调用顺丰快递服务的函数
def callSfExpressServiceByCSIM(reqURL, partnerID, requestID, serviceCode, timestamp, msgData, checkword):
    # 构建待哈希的字符串
    str_to_hash = urllib.parse.quote_plus(msgData + timestamp + checkword)
    # 创建 MD5 哈希对象
    m = hashlib.md5()
    # 更新哈希对象with编码后的字符串
    m.update(str_to_hash.encode('utf-8'))
    # 获取 MD5 哈希值
    md5Str = m.digest()
    # 将 MD5 哈希值转换为 Base64 编码
    msgDigest = base64.b64encode(md5Str).decode('utf-8')
    # 构建请求数据
    data = {
        "partnerID": partnerID,
        "requestID": requestID,
        "serviceCode": serviceCode,
        "timestamp": timestamp,
        "msgDigest": msgDigest,
        "msgData": msgData
    }
    # 发送 POST 请求到顺丰 API
    res = requests.post(reqURL, data=data)
    # 返回响应文本
    return res.text

# 定义查询接口
@app.post("/query")
async def query(data: QueryData):
    # 将查询数据转换为 JSON 格式
    msgData = data.model_dump_json()
    # 生成唯一请求 ID
    requestID = str(uuid.uuid1())
    # 生成当前时间戳
    timestamp = str(int(time.time()))

    # 调用顺丰快递服务
    respJson = callSfExpressServiceByCSIM(reqURL, partnerID, requestID, serviceCode, timestamp, msgData, checkword)
    # 返回 JSON 格式的响应
    return json.loads(respJson)

# 主程序入口
if __name__ == "__main__":
    import uvicorn
    # 启动 FastAPI 应用
    uvicorn.run(app, host="0.0.0.0", port=8000)