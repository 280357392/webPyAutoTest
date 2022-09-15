import os
import pytest
from py.xml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as CH_Options
from selenium.webdriver.firefox.options import Options as FF_Options
from selenium.webdriver.chrome.service import Service
from config import RunConfig
from pytest_html import extras


def pytest_html_report_title(report):
    report.title = "H5 APP测试报告"


def pytest_configure(config):
    # 移除Environment项目
    # 注意：移除不存在的数据项会报错，应先看初始化报告中有什么再移除。
    # config._metadata.pop("JAVA_HOME")
    # config._metadata.pop("Packages")
    # config._metadata.pop("Platform")
    # config._metadata.pop("Plugins")
    # config._metadata.pop("Python")
    config._metadata = {}
    # 添加Environment项
    config._metadata["版本信息"] = "v1.0"
    config._metadata["项目名称"] = "H5 APP"
    config._metadata["运行环境信息"] = "测试环境"


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix):
    prefix.extend([html.p("所属部门: 测试中心")])
    prefix.extend([html.p("测试人员: mengwei")])


# 设置用例描述表头
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    # cells.pop()


# 设置用例描述表格
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    # cells.pop()


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的name和nodeid的中文显示在控制台上
    解决终端日志中文乱码
    """
    for i in items:
        i.name = i.name.encode("utf-8").decode("unicode_escape")
        i._nodeid = i.nodeid.encode("utf-8").decode("unicode_escape")


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    用于向测试用例中添加用例的开始时间、内部注释，和失败截图等.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = description_html(item.function.__doc__)
    extra = getattr(report, 'extra', [])
    # if report.when == 'call' or report.when == "setup":
    # 用例结束后才执行1次
    if report.when == 'call':
        xfail = hasattr(report, 'wasxfail')
        # 失败时截图
        # if (report.skipped and xfail) or (report.failed and not xfail):
        #     case_path = report.nodeid.replace("::", "_") + ".png"
        #     if "[" in case_path:
        #         case_name = case_path.split("-")[0] + "].png"
        #     else:
        #         case_name = case_path
        #     capture_screenshots(case_name)
        #     img_path = "image/" + case_name.split("/")[-1]
        #     if img_path:
        #         html = '<div><img src="%s" ' \
        #                'alt="screenshot" style="border: 1px solid #e6e6e6;width:304px;height:240px;margin-left:5px;" ' \
        #                'onclick="window.open(this.src)" align="right"/></div>' % img_path
        #         extra.append(pytest_html.extras.html(html))
        # 无论是否失败都截图
        case_path = report.nodeid.replace("::", "_") + ".png"
        if "[" in case_path:
            case_name = case_path.split("-")[0] + "].png"
        else:
            case_name = case_path
        capture_screenshots(case_name)
        # img_path = "image/" + case_name.split("/")[-1]
        img_path = "image" + os.sep + case_name.split(os.sep)[-1]
        if img_path:
            html = '<div><img src="%s" ' \
                   'alt="screenshot" style="border: 1px solid #e6e6e6;width:304px;height:240px;margin-left:5px;" ' \
                   'onclick="window.open(this.src)" align="right"/></div>' % img_path
            extra.append(pytest_html.extras.html(html))
        extra.append(extras.url(RunConfig.driver.current_url))  # 添加link
    report.extra = extra
    # 再把编码改回来
    # 解决报告中文乱码问题
    report.nodeid = report.nodeid.encode("unicode_escape").decode("utf-8")


def description_html(desc):
    """
    将用例中的描述转成HTML对象
    :param desc: 描述
    :return:
    """
    if desc is None:
        return "No case description"
    desc_ = ""
    for i in range(len(desc)):
        if i == 0:
            pass
        elif desc[i] == '\n':
            desc_ = desc_ + ";"
        else:
            desc_ = desc_ + desc[i]

    desc_lines = desc_.split(";")
    desc_html = html.html(
        html.head(
            html.meta(name="Content-Type", value="text/html; charset=latin1")),
        html.body(
            [html.p(line) for line in desc_lines]))
    return desc_html


def capture_screenshots(case_name):
    """
    配置用例失败截图路径
    :param case_name: 用例名
    """
    global driver
    file_name = case_name.split(os.sep)[-1]
    if RunConfig.new_report is None:
        raise NameError('没有初始化测试报告目录')
    else:
        image_dir = os.path.join(RunConfig.new_report, "image", file_name)
        RunConfig.driver.save_screenshot(image_dir)


# 启动浏览器
@pytest.fixture(scope='session', autouse=True)
def browser():
    """
    全局定义浏览器驱动
    """
    global driver

    if RunConfig.driver_type == "chrome":
        # 本地chrome浏览器
        s = Service(
            os.path.join(os.path.dirname(os.path.abspath(__file__)) + os.sep + "browser_driver" + os.sep,
                         "mac_chromedriver"))
        driver = webdriver.Chrome(service=s)
        # 最大化窗口
        driver.maximize_window()
        # -----------------------------------------------------------------

    elif RunConfig.driver_type == "firefox":
        # 本地firefox浏览器
        driver = webdriver.Firefox()
        driver.maximize_window()
    elif RunConfig.driver_type == "chrome-headless":
        chrome_options = CH_Options()
        chrome_options.add_argument("--headless")  # 无头模式
        chrome_options.add_argument('--disable-gpu')  # 禁用gpu，谷歌文档提到需要加上这个属性来规避bug。
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')  # 参数是让Chrome在root权限下跑，解决DevToolsActivePort文件不存在的报错。
        # chrome_options.add_argument('blink-settings=imagesEnabled=false') # 禁用图片。
        chrome_options.add_argument('lang=zh_CN.UTF-8')  # Chrome浏览器时的默认编码。
        chrome_options.add_argument('disable-infobars')  # 不弹出自动化提示。

        s = Service(
            os.path.join(os.path.dirname(os.path.abspath(__file__)) + os.sep + "browser_driver" + os.sep,
                         "linux_chromedriver"))
        driver = webdriver.Chrome(service=s, options=chrome_options)
    elif RunConfig.driver_type == "firefox-headless":
        # firefox headless模式
        # firefox_options = FF_Options()
        # firefox_options.headless = True
        # driver = webdriver.Firefox(firefox_options=firefox_options)
        pass
    elif RunConfig.driver_type == "grid":
        # 通过远程节点运行
        # driver = Remote(command_executor='http://localhost:4444/wd/hub',
        #                 desired_capabilities={
        #                     "browserName": "chrome",
        #                 })
        # driver.set_window_size(1920, 1080)
        pass
    else:
        raise NameError("driver驱动类型定义错误！")
    RunConfig.driver = driver
    return driver


# 关闭浏览器
@pytest.fixture(scope="session", autouse=True)
def browser_close():
    yield driver
    driver.quit()
