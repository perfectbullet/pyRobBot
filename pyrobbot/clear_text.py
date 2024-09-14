import emoji
import re


def clear_text(text):
    '''
    清理字符串中的表情，空行
    '''
    result = emoji.replace_emoji(text)
    result = re.sub(r'\n+', '\\n', result)  # 去连续空行
    result = re.sub(r'\n$', '', result)  # 去末尾空行
    result = re.sub(r'^\n', '', result)  # 去开头空行
    result = re.sub(r'```.*```', '', result)
    result = re.sub(r' +', r' ', result)  # 去连续空格换单个
    result = re.sub(r'^ ', r'', result)  # 开头去连空格
    result = re.sub(r'$ ', r'', result)  # 结尾去掉空个
    return result


if __name__ == '__main__':
    t = '''🤔

    一加一等于二！```1 + 1 = 2```
    '''

    result = clear_text(t)
    print(result)
    # print('****************')
    # print(emoji.emojize(result))
