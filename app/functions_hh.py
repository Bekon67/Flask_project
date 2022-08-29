from pycbrf import ExchangeRates


def salary_processing(res_full, res, sal, rate):
    """
    Создает массив зарплатных предложений
    :param res_full:
    :param res:
    :param sal:
    :param rate:
    :return:
    """
    if res_full['salary']:
        code = res_full['salary']['currency']
        if code == 'RUR':
            k = 1
        elif code == 'BYR':
            k = 23.47
        else:
            k = float(rate[code].rate)
        print(k, '*' * 100)
        sal['from'].append(k * res_full['salary']['from']
                           if res['salary']['from'] else
                           k * res_full['salary']['to'])
        sal['to'].append(k * res_full['salary']['to']
                         if res['salary']['to'] else
                         k * res_full['salary']['from'])
    return sal