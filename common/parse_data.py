import csv
from pathlib import Path


def parse_csv(file_name):
    """
    解析csv文件。
    :param file_name: 文件名
    :return: list(tuple) 例如：[('admin', 'error', '0'), ('admin', 'rootroot', '1')]
    """
    file_path = Path.cwd() / 'data' / file_name
    list_data = []
    with open(file_path, 'r', encoding='utf8') as f:
        data = csv.reader(f)
        for i in data:
            list_data.append(tuple(i))
    del list_data[0]  # 删除标题行
    return list_data
