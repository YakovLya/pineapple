import json
import re

def find_all_indexes(data_list, value):
    return [i for i, x in enumerate(data_list) if x == value]


def replace_bad_chars(s):
    return s.replace("'", '"').replace('\\xa0', '')


def read_list_from_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.loads(replace_bad_chars(f.read()))

BAD_WORDS_EMAIL = ['pulscen.ru']

def check_email(string):
    if re.match(r'[\w\.-]+@[\w\.-]+', string):
        return True
    return False


def is_valid_phone(phone):
    return re.match(r'(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+', phone)


def check_out_data(data_list):
    for el in data_list:
        if el[-1] == 'email':
            if not check_email(el[1]):
                print('Bad email: ', el)
                break
        elif el[-1] == 'phone':
            if not is_valid_phone(el[1]):
                print('Bad phone: ', el)
                break
        elif el[-1] == 'ОГРН':
            if not el[1].isdigit() or not (len(el[1]) == 13 or len(el[1]) == 15):
                print('Bad ОГРН: ', el)
                break
        elif el[-1] == 'ИНН':
            if not el[1].isdigit() or not (len(el[1]) == 10 or len(el[1]) == 12):
                print('Bad ИНН: ', el)
                break
        else:
            print('Unknown type: ', el)
            break

def clear_data(data_list):
    for el in data_list:
        if el[-1] == 'phone':
            el[1] = re.sub(r'[^0-9]', '', el[1])
        elif el[-1] == 'email':
            el[1] = el[1].lower()
        elif el[-1] == 'ОГРН':
            el[1] = re.sub(r'[^0-9]', '', el[1])
        elif el[-1] == 'ИНН':
            el[1] = re.sub(r'[^0-9]', '', el[1])
        
        if el[1] == '':
            data_list.remove(el)
            continue
    return data_list

def convert_data_to_dict(data_list):
    res = {}
    for el in data_list:
        if el[0] not in res:
            res[el[0]] = {'email': [], 'phone': [], 'ОГРН': [], 'ИНН': []}
        res[el[0]][el[-1]].append(el[1])
    return res

def main():
    data_list = clear_data(read_list_from_file('out/out.txt'))
    check_out_data(data_list)
    with open('out/out.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(convert_data_to_dict(data_list)))

if __name__ == "__main__":
    main()