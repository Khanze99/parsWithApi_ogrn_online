import requests
import csv
import json

DICT_NAME_COMPANY = {}
BASE_URL = 'https://огрн.онлайн/{}'
API_TOKEN = '###'
headers = {'X-ACCESS-KEY': API_TOKEN}
DATA = []  #COMPANY_NAME,REGION,DATA,INSTITUTION_COMPANY'.split(',')
DATA_FINANCE = []  #'COMPANY_NAME,FINANCE'.split(',')


def get_inn_id(search):  # Поиск компаний по инн
    url = BASE_URL.format('интеграция/компании/')
    params = {'инн': search}
    get_id = requests.get(url, timeout=(5, 2), headers=headers, params=params).json()  # заддержка т.к. >10 запросов в 1 сек, блокировка
    global companyName
    companyName = get_id[0]['name']
    return get_id[0]['id']


def get_id_company(id):  # Поиск общей информации по id компании
    url = BASE_URL.format('интеграция/компании/{}/'.format(id))
    params = {'id': id}
    get_about = requests.get(url, timeout=(5, 2), headers=headers, params=params).json()
    get_name_company = get_about['name']  # Имя компании
    get_inn_company = get_about['inn']
    if 'address' in get_about:
        global get_addr_company
        get_addr_company = get_about['address']['fullHouseAddress']  # Адрес компании
    elif 'address' not in get_about:
        if 'fullHouseAddress' in get_about:
            get_addr_company = get_about['fullHouseAddress']
    else:
        get_addr_company = get_about['address']
    get_date_company = get_about['ogrnDate']  # Дата регистрации компании
    values = [get_name_company, get_inn_company, get_addr_company, get_date_company]
    return values


def get_comp_finance(id):  # Бухгалтерия компании
    url = BASE_URL.format('интеграция/компании/{}/финансы/'.format(id))
    params = {'id': id}
    get_finance = requests.get(url, headers=headers, params=params).json()
    names = []
    for item in range(len(get_finance)):
        year = get_finance[item]['year']
        f12003 = get_finance[item]['f12003']
        f16003 = get_finance[item]['f16003']
        f13103 = get_finance[item]['f13103']
        f13703 = get_finance[item]['f13703']
        f13003 = get_finance[item]['f13003']
        f17003 = get_finance[item]['f17003']
        f21103 = get_finance[item]['f21103']
        f24003 = get_finance[item]['f24003']
        f33118 = get_finance[item]['f33118']
        finance = [companyName, year, f12003, f16003, f13103, f13703, f13003, f17003, f21103,
                   f24003, f33118]
        names.append(finance)
    return names


def get_institution(id):  # Поиск учредителей компании
    params = {'id': id}
    url = BASE_URL.format('интеграция/компании/{}/учредители/').format(id)
    get_instit = requests.get(url, timeout=(5, 2), headers=headers, params=params).json()
    names = []
    for item in range(len(get_instit)):
        if 'personOwner' in get_instit[item]:
            first_name = get_instit[item]['personOwner']['firstName']
            middle_name = get_instit[item]['personOwner']['middleName']
            sur_name = get_instit[item]['personOwner']['surName']
            inn_inst = get_instit[item]['personOwner']['inn']
            name_inst = '{} {} {}'.format(first_name, middle_name, sur_name)
            name = [inn_inst, name_inst]
            names.extend(name)
        elif 'company' in get_instit[item]:
            company_name = get_instit[item]['company']['name']
            inn_company = get_instit[item]['company']['inn']
            names.extend([company_name, inn_company])
        else:
            company_name = get_instit[item]['name']
            inn_company = get_instit[item]['inn']
            names.extend([company_name, inn_company])
    return names


def get_postname(id):  # Поиск компаний где работает учредитель
    url = BASE_URL.format('интеграция/компании/{}/сотрудники/').format(id)
    params = {'id': id}
    get_name = requests.get(url, headers=headers, params=params).json()
    first_name = get_name[0]['person']['firstName']
    middle_name = get_name[0]['person']['middleName']
    sur_name = get_name[0]['person']['surName']
    inn = get_name[0]['person']['inn']
    fullname = '{} {} {} '.format(first_name, middle_name, sur_name)
    post_name = get_name[0]['postName']
    names = [fullname, inn, post_name]
    return names


if __name__ == '__main__':  # Начало программы, считывание ИНН, подача контекст в функции для запросов
    with open('100.txt', 'r', encoding='utf-8') as file:
        read = file.read().split('\n')
        for line in read:
            inn = str(line.rstrip('\n'))
            id_company = get_inn_id(inn)
            name_company = get_id_company(id_company)
            name_inst = get_institution(id_company)
            name_post = get_postname(id_company)
            finance_comp = get_comp_finance(id_company)
            name_company.extend(name_post)
            name_company.extend(name_inst)
            DATA.append(name_company)
            DATA_FINANCE.append(finance_comp)



with open('first_100.csv', 'a', encoding='utf-8') as file_write:  # Распределение в файл csv общей информации о компании
        writer = csv.writer(file_write, delimiter=',')
        for line in DATA:
            writer.writerow(line)
with open('finance.csv', 'a', encoding='utf-8') as finance_write:  # Распределение в файл csv финансов компании
        writer = csv.writer(finance_write, delimiter=',')
        for line in DATA_FINANCE:
            for item in line:
                writer.writerow(item)
