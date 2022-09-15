from selenium.webdriver.common.by import By
from page.page import Page

"""
PO本身绝不应进行判断或断言。应始终在测试的代码内, 而不是在PO中.
PO不一定需要代表整个页面. PO设计模式可用于表示页面上的组件. 
如果自动化测试中的页面包含多个组件, 则每个组件都有单独的页面对象, 则可以提高可维护性.
"""

class HomePage(Page):

    message_by = (By.TAG_NAME, 'h1')
    '''<h1>Hello userName</h1>'''

    def __init__(self, browser):
        super().__init__(browser)

    def get_message_text(self):
        return self.find_element(self.message_by).text  # 可能会报错

