# -*- coding: utf-8 -*-
'''
@Time    : 2022/4/28 11:01
@Author  : Terry
@File    : rsa_encrypt.py

'''
import base64

import rsa

from commom.handle_log import mylogger


def rsaEncrypt(msg):
    # 公钥文件
    server_pub_key = """
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAyYz+Q+dh+8ZNqzetthqA
CQW7bzAklGVqQb7DIeu5uAvMdowO0q/dNg+HLaUmTb4auA6tdN2MQa5/SzloE2qx
LFCx9itHuUXbKIVIApr+98R8f11S0GvNX1PVtSbActrWQnjpgXt1Agu9pyX1YNwx
sXi6MBYobKMcyXetSazkXXePZw+Um5/cCycVlBH56NlKXGSlRU4xw20H5iiDJX7K
1eR5K1eBrAdDkvxJX0IW+B3hpimLfNQM9gNhAikDaI/hz+my4M9YWSWq9aelCOro
l3sbOat7IHeSBzWAi8cLxke50c1oCdoDIqPvrOmj/GDZ8ZHBgiFZgBQpS6IPqPPl
qDm86RTxyHz9clhgctjPEXbBGEszq79KpL6oDUjOkpmFOXNl1SnEEOWf71pC7hHv
WR32JoSiZlDGipakgQciNVQl5OjWUXvHPKlyD1N784F8vZcEhCEGTR1P+eDyEWhb
wHVusjZlrZ1Sv3Owro77BUSq4N6yDkvmpolY/2xrZuVZtiH1SO1yEPk6Qlnp8FH4
uaMXBYmaX82ZJaJj8UFyHY0ZYYMJrWH93ExQ2cS4jH2tzo1V0KFncFloN6FeeX3b
s9gN6up721L2EzXLhBWqDc7ZI3cSAz9CD6IEgTikGpQHBbAtIYGXY3ee3ksrQwrS
+GD8Y8XPb3tmO1j8lDv2MRMCAwEAAQ==
-----END PUBLIC KEY-----
"""
    # 生成公钥对象
    pub_key_byte = server_pub_key.encode("utf-8")
    pub_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key_byte)

    # 要加密的数据转换成字节对象
    content = msg.encode("utf-8")

    # 加密数据，返回加密文本
    cryto_msg = rsa.encrypt(content, pub_key_obj)

    # base64编码
    cipher_base64 = base64.b64encode(cryto_msg)
    mylogger.info("数据加密后的结果为：{}".format(cipher_base64.decode()))
    # 转成字符串
    return cipher_base64.decode()

if __name__ == '__main__':
    msg = "ars@12345678"
    res = rsaEncrypt(msg)
    print(res)

