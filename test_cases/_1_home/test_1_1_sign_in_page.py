import pytest
from config import RunConfig
from page._1_home.home_page import HomePage
from page._1_home.sign_in_page import SigInPage
from time import sleep
from common.parse_data import parse_csv


# sys.path.insert(0, dirname(dirname(abspath(__file__))))
@pytest.mark.skipif('_1_home' in RunConfig.skip_module, reason="跳过的模块")
@pytest.mark.run(order=1)
class TestSignInPage(object):
    """

    """

    @pytest.mark.parametrize(
        "username,password,status",  # 列
        parse_csv('test_login.csv'),
        ids=[  # 行
            "1.有效用户登录。",
            "2.无效用户登录。",
        ]
    )
    # @pytest.mark.skipif(RunConfig.debug, reason="debug模式跳过用例")
    def test_login(self, browser, username, password, status):
        """
        登录功能：
        输入正确的账号和密码，并点击登录按钮。
        预期：
        1.登录成功时，跳转百度页。
        2.登录失败时，弹出账号或密码弹出。
        """
        sign_in_page = SigInPage(browser)
        sign_in_page.login_valid_user(username, password)
        if status == '1':
            # 以有效用户身份登录
            # sign_in_page.get_cookies()
            assert HomePage(browser).is_title('百度一下，你就知道1')
        if status == '0':
            # 以失效用户身份登录
            alert_text = sign_in_page.close_confirm_alert_and_get_text()
            assert '账号或密码错误1' == alert_text

    @pytest.mark.skipif(RunConfig.debug, reason="debug模式跳过用例")
    def test_001(self, browser):
        """
        临时测试
        :param browser:
        :return:
        """
        browser.get('http://sahitest.com/demo/clicks.htm')
        page = HomePage(browser)
        page.set_cookies('home.json')


if __name__ == '__main__':
    # 调试模式
    pytest.main(["-vs", "xxxxxx.py"])
