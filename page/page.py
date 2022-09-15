"""
page.home.page
~~~~~~~~~~~~~~~~~~~

page基类
封装和业务无关的方法
"""
import json
from time import sleep
from pathlib import Path
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import RunConfig


class Page(object):

    def __init__(self, browser):
        self.browser = browser
        self.base_url = RunConfig.base_url
        self.accept_next_alert = True

    def find_element(self, loc, timeout=5):
        """
        获取页面某个元素的对象。\n
        :param loc: 元组，如：(By.ID, u"kw")
        :param timeout: 查找元素显式等待时间秒，如：1
        :return: 元素对象
        """
        # return self.browser.find_element(*loc)
        message = '未查找到该元素，url：{}，by：{}，value：{}'.format(self.browser.current_url, *loc)
        return WebDriverWait(self.browser, timeout=timeout).until(lambda d: d.find_element(*loc), message)

    def find_elements(self, loc, timeout=5):
        """
        获取页面元素
        :param loc: 元组，如(By.ID, u"kw")
        :param timeout: 显示等待时间
        :return: 元素对象列表
        """
        # return self.browser.find_elements(*loc)
        message = '未查找到该元素组，url：{}，by：{}，value：{}'.format(self.browser.current_url, *loc)
        return WebDriverWait(self.browser, timeout=timeout).until(lambda d: d.find_elements(*loc), message)

    def is_title(self, title, timeout=5):
        """
        判断当前页面的title是否等于预期标题。\n
        :param title: 预期的编标题字符串。
        :param timeout: 显示等待时间(秒)整数。
        :return: 相等时返回True否则报错。
        """
        message = '标题与预期不匹配，url：{}，标题：{}，预期标题：{}'.format(self.browser.current_url, self.title(), title)
        return WebDriverWait(self.browser, timeout=timeout).until(EC.title_is(title), message)

    def is_text(self, loc, text, timeout=5):
        """
        判断当前元素的text是否等于预期的字符串。\n
        元素text属性: 如a标签之间的文字和button标签之间的文字。\n
        :param loc: 元组，如：(By.ID, u"kw")
        :param text: 预期的text，如：'1'
        :param timeout: 查找元素显式等待时间秒，如：1
        :return: 相等时返回True否则报错。
        """
        message = '元素text与预期不匹配，url：{}，预期text：{}，by：{}，value：{}'.format(self.browser.current_url, text, *loc)
        return WebDriverWait(self.browser, timeout=timeout).until(EC.text_to_be_present_in_element(loc, text), message)

    def is_attribute(self, loc, name, text, timeout=5):
        """
        判断当前元素的某个属性值是否等于预期的字符串。\n
        :param loc: 元组，如：(By.ID, u"kw")
        :param name: 属性，列如：'id'
        :param text: 预期的属性值。
        :param timeout: 查找元素显式等待时间秒，如：1
        :return: 相等时返回True否则报错。
        """
        message = '元素{}属性值与预期不匹配，url：{}，预期{}属性值：{}，by：{}，value：{}'.format(name, self.browser.current_url, name, text,
                                                                          *loc)
        return WebDriverWait(self.browser, timeout=timeout).until(
            EC.text_to_be_present_in_element_attribute(loc, name, text), message)

    def is_not_element(self, loc, timeout=5):
        """
        用于判断是否还能查找到被删除(隐藏)的元素。\n
        如果查找到元素，会报错。\n
        :param loc: 元组，如：(By.ID, u"kw")
        :param timeout: 查找元素显式等待时间秒，如：1
        :return: 如果未找到元素时返回True，如果找到元素时报错。
        """
        message = '因为该元素被删除或者隐藏了，所以该元素不应存在，url：{}，by：{}，value：{}'.format(self.browser.current_url, *loc)
        return WebDriverWait(self.browser, timeout=timeout).until_not(lambda d: d.find_element(*loc), message)

    def current_url(self):
        """
        :return: 当前页面URL
        """
        return self.browser.current_url

    def title(self, timeout=5):
        """
        :return: 当前页面title
        """
        if self.browser.title == "":
            return self.find_element((By.XPATH, '/html/head/title'), timeout=timeout).get_attribute("textContent")
        else:
            return self.browser.title

    def close_alert_and_get_text(self, timeout=5):
        """
        获取alert对话框的信息，并关闭对话框
        :param timeout: 显示等待时间s
        :return: 对话框中的警告信息
        """
        sleep(2)
        alert = WebDriverWait(self.browser, timeout=timeout).until(EC.alert_is_present(), '未查找到alert弹窗')
        text = alert.text
        alert.accept()
        return text

    def close_confirm_alert_and_get_text(self, timeout=5):
        """
        获取确认对话框的信息，并关闭对话框。\n
        :param timeout: 显示等待时间s
        :return: 对话框中的警告信息
        """
        sleep(2)
        WebDriverWait(self.browser, timeout=timeout).until(EC.alert_is_present(), '未查找到confirm弹窗')
        alert = self.browser.switch_to.alert
        text = alert.text
        # 按取消按钮
        alert.dismiss()
        return text

    def close_prompt_and_send_text(self, text, timeout=5):
        """
        Prompt提示框，提交text信息
        :param timeout: 显示等待时间s
        :param text: 提交的文本内容
        :return: 对话框中的警告信息
        """
        sleep(2)
        WebDriverWait(self.browser, timeout=timeout).until(EC.alert_is_present(), '未查找到prompt弹窗')
        # 将警报存储在变量中以供重用
        alert = Alert(self.browser)
        # Type your message
        alert.send_keys(text)
        # 按确定按钮
        alert.accept()

    def switch_window(self, title="", index=None):
        """
        未传任何参数时，默认切换到最新的窗口。\n
        只传title时，根据title判断切换窗口。\n
        只传index时，根据窗口id切换窗口。\n
        :param title: 根据标题切换窗口
        :param index: 根据角标切换窗口，0开始。
        """
        if title != "":
            for window_handle in self.browser.window_handles:
                self.browser.switch_to.window(window_handle)
                if title == self.browser.title:
                    break
            pass
        elif index is not None:
            self.browser.switch_to.window(self.browser.window_handles[index])
            pass
        else:
            self.browser.switch_to.window(self.browser.window_handles[-1])
            pass
        pass

    def set_cookies(self, file_name):
        """
        读取cookies目录中json文件，并设置cookie。\n
        :param file_name: cookies目录中的某个文件的文件名，例如：home.json。
        """
        file_path = str(Path.cwd() / 'cookies' / file_name)
        with open(file_path, "r") as f:
            # 读取本地的cookie文件
            cookies_dict = json.load(f)  # 字典或者list
        # 清除原有的所有cookies
        self.browser.delete_all_cookies()
        for cookie in cookies_dict:
            for k in cookie.keys():
                if k == "expiry":
                    cookie[k] = int(cookie[k])
            self.browser.add_cookie(cookie)
        # 刷新页面
        self.browser.refresh()

    def get_cookies(self, file_name):
        """
        获取全部cookie,转换成JSON格式的字符串并保存到 cookies 目录中。\n
        建议login业务中获取。\n
        :param file_name: cookies目录中的某个文件的文件名，例如：home.json。
        """
        file_path = str(Path.cwd() / 'cookies' / file_name)
        with open(file_path, 'w') as f:
            json.dump(self.browser.get_cookies(), f)
