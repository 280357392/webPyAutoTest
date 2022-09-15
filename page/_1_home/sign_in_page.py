from selenium.webdriver.common.by import By
from page.page import Page
from pathlib import Path


class SigInPage(Page):
    """
    首页页面 \n
    页面地址：/
    """

    username_input_by = (By.ID, 'account')
    '''用户名输入框 <input type="text" id="account" placeholder="请输入账号">'''

    password_input_by = (By.ID, 'password')
    '''密码输入框 <input type="text" id="password" placeholder="请输入密码">'''

    login_btn_by = (By.ID, 'login')
    '''登录按钮 <button id="login" onclick="login()">登录</button>'''

    alert_by = (By.TAG_NAME, 'h1')
    '''alert弹窗 <h1>Hello userName</h1>'''

    def __init__(self, browser, url=u'/'):
        super().__init__(browser)
        self.url = ''.join([self.base_url, url])

    def login_valid_user(self, username, password):
        """
        以有效用户身份登录。\n
        :param username: 用户名字符串
        :param password: 密码字符串
        :return: None
        """
        # self.browser.get(self.url)
        self.browser.get('file://' + str(Path.cwd() / 'demo1.html'))
        username_input = self.find_element(self.username_input_by)
        username_input.clear()
        username_input.send_keys(username)
        password_input = self.find_element(self.password_input_by)
        password_input.clear()
        password_input.send_keys(password)
        self.find_element(self.login_btn_by).click()

    def is_xx_text(self, message):
        return self.is_text((By.TAG_NAME, 'h1'), message)

    def get_xx_is_displayed(self):
        return self.find_element((By.ID, 'btn')).is_displayed()
