import requests
import csv

DICT_NAME_COMPANY = {}
BASE_URL = 'https://огрн.онлайн/{}'
API_TOKEN = '###'
headers = {'X-ACCESS-KEY': API_TOKEN}
DATA = []  #COMPANY_NAME,REGION,DATA,INSTITUTION_COMPANY'.split(',')
DATA_FINANCE = []  #'COMPANY_NAME,FINANCE'.split(',')


def get_inn_id(search):  # Поиск компаний по инн
    url = BASE_URL.format('интеграция/компании/')
    params = {'инн': search}
    get_id = requests.get(url, timeout=(5, 2), headers=headers, params=params,)  # заддержка т.к. >10 запросов в 1 сек, блокировка
    global companyName
    companyName = get_id.json()[0]['name']
    return get_id.json()[0]['id']


def get_id_company(id):  # Поиск общей информации по id компании
    url = BASE_URL.format('интеграция/компании/{}/'.format(id))
    params = {'id': id}
    get_about = requests.get(url, timeout=(5, 2), headers=headers, params=params)
    get_name_company = get_about.json()['name']  # Имя компании
    DATA_FINANCE.append(get_name_company)
    get_inn_company = get_about.json()['inn']
    get_addr_company = get_about.json()['address']['fullHouseAddress']  # Адрес компании
    get_date_company = get_about.json()['ogrnDate']  # Дата регистрации компании
    values = [get_name_company, get_inn_company, get_addr_company, get_date_company]
    return values


def get_comp_finance(id):  # Бухгалтерия компании
    url = BASE_URL.format('интеграция/компании/{}/финансы/'.format(id))
    params = {'id': id}
    get_finance = requests.get(url, headers=headers, params=params)
    get_finance_json = get_finance.json()[0]
    names = [companyName]
    for item in get_finance_json:
        names.append(get_finance_json[item])
    return names


def get_institution(id):  # Поиск учредителя компании
    params = {'id': id}
    url = BASE_URL.format('интеграция/компании/{}/учредители/').format(id)
    get_instit = requests.get(url, timeout=(5, 1), headers=headers, params=params)
    if 'personOwner' in get_instit.json()[0]:
        first_name = get_instit.json()[0]['personOwner']['firstName']
        middle_name = get_instit.json()[0]['personOwner']['middleName']
        sur_name = get_instit.json()[0]['personOwner']['surName']
        inn_inst = get_instit.json()[0]['personOwner']['inn']
        name_inst = '{} {} {}'.format(first_name, middle_name, sur_name)
        name = [name_inst, inn_inst]
        return name
    elif 'company' in get_instit.json()[0]:
        company_name = get_instit.json()[0]['company']['name']
        inn_company = get_instit.json()[0]['company']['inn']
        name = [company_name, inn_company]
        return name
    else:
        company_name = get_instit.json()[0]['name']
        inn_company = get_instit.json()[0]['inn']
        name = [company_name, inn_company]
        return name


def get_postname(id):  # Поиск компаний где работает учредитель
    url = BASE_URL.format('интеграция/компании/{}/сотрудники/').format(id)
    params = {'id': id}
    get_name = requests.get(url, headers=headers, params=params).json()
    if 'fullNameWithInn' in get_name[0]['person']:
        full_name = get_name[0]['person']['fullNameWithInn']
        full_name_post = get_name[0]['post']['fullName']
        post_in_company = get_name[0]['postName']
        names = [full_name, full_name_post, post_in_company]
        return names
    elif 'fullName' not in get_name[0]['person']:
        first_name = get_name[0]['person']['firstName']
        middle_name = get_name[0]['person']['middleName']
        sur_name = get_name[0]['pesron']['surName']
        inn = get_name[0]['person']['inn']
        fullnameWithInn = '{} {} {} {}'.format(first_name, middle_name, sur_name, inn)
        fulname_post = get_name[0]['post']['fullName']
        post_name = get_name[0]['postName']
        names = [fullnameWithInn, fulname_post, post_name]
        return names


if __name__ == '__main__':
    with open('100.txt', 'r', encoding='utf-8') as file:
        read = file.read().split('\n')

        for line in read:
            inn = str(line.rstrip('\n'))
            try:
                name_company = get_id_company(get_inn_id(inn))
                name_inst = get_institution(get_inn_id(inn))
                name_post = get_postname(get_inn_id(inn))
                finance_comp = get_comp_finance(get_inn_id(inn))
                name_company.extend(name_inst)
                name_company.extend(name_post)
                DATA.append(name_company)
                print('_-----------------------------------------------------------------------_')
                print(finance_comp)
                DATA_FINANCE.append(finance_comp)
                print(DATA_FINANCE)
            except BaseException:
                continue


with open('first_100.csv', 'a', encoding='utf-8') as file_write:
        writer = csv.writer(file_write, delimiter=',')
        for line in DATA:
            writer.writerow(line)
with open('finance.csv', 'a', encoding='utf-8') as finance_write:
        writer = csv.writer(finance_write, delimiter='\n')
        for line in DATA_FINANCE:
            writer.writerow([line])
