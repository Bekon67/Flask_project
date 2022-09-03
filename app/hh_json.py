from pprint import pprint
from pickle import load, dump as p_dump
from os.path import exists
import re
from collections import Counter
from json import dump as j_dump
from requests import get
from pycbrf import ExchangeRates
from functions_hh import salary_processing


def parce(vacancy, limit_pages='3', limit_skills='5'):
    """
    :param vacancy: название вакансии
    :param limit_pages: количество страниц вакансий для анализа
    :param limit_skills: количество выводимых основных навыков
    :return:
    """
    url = 'https://api.hh.ru/vacancies'
    rate = ExchangeRates()  # загрузка текущих курсов валют

    # загрузка файла с цифровыми кодами
    if exists('area.pkl'):
        with open('area.pkl', mode='rb') as f:
            area = load(f)
    else:
        area = {}
    param_request = {'text': vacancy}
    answer = get(url=url, params=param_request).json()
    # pprint(answer)
    count_pages = answer['pages']
    result = {'keywords': vacancy,
              'count': 0}
    sal = {'from': [], 'to': []}
    skills_all = []

    # Сначала выявляем сколько будет получено страниц
    # и готовим нужные переменные. А затем проходим по каждой из полученных страниц.
    for page in range(count_pages):
        if page > int(limit_pages) - 1:
            break
        else:
            print(f"Обрабатывается страница {page}")
        p = {'text': vacancy,
             'page': page}
        answer = get(url=url, params=p).json()
        count_on_page = len(answer['items'])
        result['count'] += count_on_page
        for res in answer['items']:
            # print('$'*100)
            # pprint(res)
            # print('#' * 100)
            skills_set = set()
            city_vac = res['area']['name']
            # добавление города из ответа на запрос, если его нет в файле.
            if city_vac not in area:
                area[city_vac] = res['area']['id']
            ar = res['area']
            res_full = get(res['url']).json()
            # pprint(res_full)
            # pprint(rate[res_full['salary']['currency']])
            # pprint(res_full['key_skills'])
            #  Обработка описания вакансии. Вытаскивание английских слов из описания вакансии
            #  предполагается, что это навыки для IT
            pp = res_full['description']
            # print(pp)
            pp_re = re.findall(r'\s[A-Za-z-?]+', pp)
            # print(pp_re)
            its = set(x.strip(' -').lower() for x in pp_re)
            # print(its)

            # формирование общего списка навыков из тегов и вытащенных из описания
            for sk in res_full['key_skills']:
                skills_all.append(sk['name'].lower())
                skills_set.add(sk['name'].lower())
            for it in its:
                if not any(it in x for x in skills_set):
                    skills_all.append(it)
            # окончание формирования списка навыков

            sal = salary_processing(res_full, res, sal, rate)  # обработка заплаты

    sk2 = Counter(skills_all)
    # pprint(sk2)
    skills_out = [{'name': name, 'count': count, 'percent': round((count / result['count']) * 100, 2)}
                  for name, count in sk2.most_common(int(limit_skills))]
    up = sum(sal['from']) / len(sal['from'])
    down = sum(sal['to']) / len(sal['to'])
    result.update({'salary_down': round(up, 2),
                   'salary_up': round(down, 2),
                   'requirements': skills_out})

    pprint(result)
    # сохранение файла с результатами работы
    with open('result.json', mode='w') as f:
        j_dump([result], f)
    with open('area.pkl', mode='wb') as f:
        p_dump(area, f)

    return result


if __name__ == '__main__':
    vacancy_name = input('Введите интересующую вакансию: ')
    answer_limit_pages = input('Введите интересующее число страниц: ')
    answer_limit_skills = input('Введите интересующее число навыков: ')
    parce(vacancy_name, answer_limit_pages, answer_limit_skills)
