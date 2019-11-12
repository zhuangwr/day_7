"""
封装unittest相关实现
"""
# 1.导包
import json
import unittest
import requests
import app
from api.LoginAPI import Login
# 参数化步骤1，导包------------
from parameterized import parameterized


# 参数化步骤2，解析------------
def read_json_file():
    # 1.创建空列表接收数据
    data = []
    # 2.解析文件流
    with open(app.PRO_PATH + "/data/login_data.json", "r", encoding="utf-8") as f:
        for v in json.load(f).values():
            mobile = v.get("mobile")
            password = v.get("password")
            success = v.get("success")
            code = v.get("code")
            message = v.get("message")
            # 组织成元组
            ele = (mobile, password, success, code, message)
            # 追加进列表
            data.append(ele)
    # 3.返回列表
    return data


# 2.创建测试类（继承unittest.TestCase）：
class TestLogin(unittest.TestCase):
    # 3.初始化函数
    def setUp(self) -> None:
        # 初始化session
        self.session = requests.Session()
        # 初始化api对象
        self.login_obj = Login()

    # 4.资源卸载函数
    def tearDown(self) -> None:
        # 销毁session
        self.session.close()

    # 5.核心：测试函数-登录
    # 5-1.参数化
    # 参数化3，调用
    @parameterized.expand(read_json_file())
    def test_login(self, mobile, password, success, code, massage):
        print("-" * 50)
        print("参数化读取数据：", mobile, password, success, code, massage)
        # 5-2.请求业务
        response = self.login_obj.login(self.session, mobile, password)
        print("登录响应结果：", response.json())
        # 5-3.断言业务
        self.assertEqual(success, response.json().get("success"))
        self.assertEqual(code, response.json().get("code"))
        self.assertIn(massage, response.json().get("message"))

    # 手机号有空格,用户名或密码错误
    # 不传参,用户名或密码错误
    # 不传用户名，操作成功

    # 编写登录成功的测试函数
    def test_login_success(self):
        # 1.直接通过提交正向数据发送请求业务
        response = self.login_obj.login(self.session, "13800000002", "123456")
        # 2.断言业务
        # 登录成功的结果： {'success': True, 'code': 10000, 'message': '操作成功！', 'data': '5c4779c4-f0dd-41ee-bc88-8f1c85efcf26'}
        print("登录成功的结果：", response.json())
        self.assertIn("操作成功", response.json().get("message"))
        self.assertEqual(10000, response.json().get("code"))
        self.assertEqual(True, response.json().get("success"))

        # 提取token
        token = response.json().get("data")
        print("登录后响应的token：", token)
        # 预期：允许其他文件调用token，可以扩大token的作用域（将token赋值给app.py的一个全局变量）
        app.TOKEN = token


if __name__ == '__main__':
    unittest.main()
