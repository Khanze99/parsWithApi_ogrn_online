import requests
import json
import csv

DICT_NAME_COMPANY = {}
BASE_URL = 'https://огрн.онлайн/{}'
API_TOKEN = '....'
headers = {'X-ACCESS-KEY': API_TOKEN}
DATA = []  #COMPANY_NAME,REGION,DATA,INSTITUTION_COMPANY'.split(',')
DATA_FINANCE = []  #'COMPANY_NAME,FINANCE'.split(',')


def get_inn_id(search):  # Поиск компаний по инн
    url = BASE_URL.format('интеграция/компании/')
    params = {'инн': search}
    get_id = requests.get(url, timeout=(5, 2), headers=headers, params=params,)  # заддержка т.к. >10 запросов в 1 сек, блокировка
    print(get_id.json()[0]['id'])
    return get_id.json()[0]['id']


def get_id_company(id):  # Поиск общей информации по id компании
    url = BASE_URL.format('интеграция/компании/{}/'.format(id))
    params = {'id': id}
    get_about = requests.get(url, timeout=(5, 2), headers=headers, params=params)
    # url_company_man = BASE_URL.format('интеграция/компании/{}/учредители/'.format(id))
    # get_company_man = requests.get(url_company_man, timeout=(5, 2), headers=headers, params=params)
    # get_man = get_company_man.json()
    # print(get_about.json())
    # print(get_company_man.json())
    # first_name = get_man[0]['personOwner']['firstName']
    # middle_name = get_man[0]['personOwner']['middleName']
    # sur_name = get_man()[0]['personOwner']['surName']
    # inn_inst = get_man[0]['inn']
    get_name_company = get_about.json()['name']  # Имя компании
    DATA_FINANCE.append(get_name_company)
    get_inn_company = get_about.json()['inn']
    get_addr_company = get_about.json()['address']['fullHouseAddress']  # Адрес компании
    get_date_company = get_about.json()['ogrnDate']  # Дата регистрации компании
    values = [get_name_company, get_inn_company, get_addr_company, get_date_company]
    # print(values)
    return values


def get_comp_finance(id):  # Бухгалтерия компании
    url = BASE_URL.format('интеграция/компании/{}/финансы/'.format(id))
    params = {'id': id}
    get_finance = requests.get(url, headers=headers, params=params)
    get_finance_json = get_finance.json()
    return get_finance_json


def get_institution(id):  # Поиск учредителя компании
    params = {'id': id}
    url = BASE_URL.format('интеграция/компании/{}/учредители/').format(id)
    get_instit = requests.get(url, timeout=(5, 1), headers=headers, params=params)
    print(get_instit.json())
    print('personOwner' in get_instit.json()[0])
    print('company' in get_instit.json()[0])

    if 'personOwner' in get_instit.json()[0]:
        first_name = get_instit.json()[0]['personOwner']['firstName']
        middle_name = get_instit.json()[0]['personOwner']['middleName']
        sur_name = get_instit.json()[0]['personOwner']['surName']
        inn_inst = get_instit.json()[0]['inn']
        name_inst = '{} {} {}'.format(first_name, middle_name, sur_name)
        name = [name_inst, inn_inst]
        print(name)
        return name
    elif 'company' in get_instit.json()[0]:
        company_name = get_instit.json()[0]['company']['name']
        inn_company = get_instit.json()[0]['company']['inn']
        name = [company_name, inn_company]
        print(name)
        return name


# def get_postname(id):  # Поиск компаний где работает учредитель
#     url = BASE_URL.format('интеграция/компании/{}/сотрудники/').format(id)
#     params = {'id': id}
#     get_name = requests.get(url, headers=headers, params=params)
#     return get_name.json()


if __name__ == '__main__':
    with open('100.txt', 'r', encoding='utf-8') as file:
        read = file.readlines()
        for line in read:
            inn = int(line)
            print(inn)
            name_company = get_id_company(get_inn_id(str(inn)))
            name_inst = get_institution(get_inn_id(str(inn)))
            print(name_company)
            print(name_inst)
            list_company = name_company.extend(name_inst)
            # list_company.extend(get_comp_finance(get_inn_id(str(line.split()))[2:-2]))
            DATA.append(list_company)

            with open('first_100.csv', 'a', encoding='utf-8') as file_write:
                writer = csv.writer(file_write, delimiter=',')
                for line in DATA:
                    print(line)
                    writer.writerow(line)
            # with open('finance.csv', 'a', encoding='utf-8') as finance_write:
            #     writer = csv.writer(finance_write, delimiter='\n')
            #     for line in DATA_FINANCE:
            #         writer.writerow([line])
