import hashlib


def get_md5(file):
    """
    返回文件的md5值
    :param file: 文件路径
    :return: md5
    """
    m = hashlib.md5()
    with open(file, 'rb') as f:
        for line in f:
            m.update(line)
    md5code = m.hexdigest()
    return md5code


if __name__ == '__main__':
    print(get_md5('/Users/mengwei/Downloads/test/storm.txt.zip'))
