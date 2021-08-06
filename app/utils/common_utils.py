from . import constants as const


def print_line(char='-', cnt=30, desc='分割线'):
    print(f'\n{char * cnt + desc + char * cnt}\n')


def str_to_price(price=None):
    if not price:
        return 0

    ret = 0
    if price.find(const.TRILLION) > 0:
        ret = float(price.replace(const.TRILLION, '')) * 1_0000_0000_0000
    elif price.find(const.HUNDRED_MILLION) > 0:
        ret = float(price.replace(const.HUNDRED_MILLION, '')) * 1_0000_0000
    elif price.find(const.TEN_THOUSAND) > 0:
        ret = float(price.replace(const.TEN_THOUSAND, '')) * 1_0000
    elif price.find(const.THOUSAND) > 0:
        ret = float(price.replace(const.THOUSAND, '')) * 1_000
    elif price.find(const.HUNDRED) > 0:
        ret = float(price.replace(const.HUNDRED, '')) * 1_00

    return ret


def which_trade(code):
    """
    沪市600开头，科创板是688开头的，B股是900开头；
    深市A主板是000开头，中小板是002开头、创业板是300开头、B股是200开头。
    :param code:
    :return:
    """
    if not code:
        raise ValueError('code must not be null')
    if str(code).startswith('600') or str(code).startswith('601') or str(code).startswith('603') or str(
            code).startswith('900') or str(code).startswith('688'):  # 上证
        return f'SH{code}'
    elif str(code).startswith('000') or str(code).startswith('200') or str(code).startswith('300') or str(
            code).startswith('002'):  # 深证
        return f'SZ{code}'


if __name__ == '__main__':
    # print_line()
    str_to_price('36.96亿')
    # print('36.96万'.find(const.HUNDRED_MILLION))
