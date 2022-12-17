import pandas as pd


data = eval(open('out.txt', 'r', encoding='utf8').readline())


def check_inn(s):
    k = ''
    for i in s:
        if i.isdigit():
            k += i
    return k


def check_ogrn(s):
    if '-' in s:
        return 'Err'
    k = ''
    for i in s:
        if i.isdigit():
            k += i
    return k


def check_phone(s):
    s = s.replace('+7', '8')
    k = ''
    for i in s:
        if i.isdigit():
            k += i
    if len(k) == 11 and k[0] == '7':
        k = '8' + k[1:]
    return k


def check_email(em, s):
    if '.' in s:
        return s
    else:
        return s + '.' + em.split('.')[-1]


def check_url(url):
    return url.replace('.html', '')


for i in range(len(data)):
    data[i][0] = check_url(data[i][0])
    if data[i][2] == 'ИНН':
        data[i][1] = check_inn(data[i][1])
    elif data[i][2] == 'phone':
        data[i][1] = check_phone(data[i][1])
    elif data[i][2] == 'ОГРН':
        data[i][1] = check_ogrn(data[i][1])
    elif data[i][2] == 'email':
        data[i][1] = check_email(data[i][0], data[i][1])

df = pd.DataFrame(data)
df = df.drop_duplicates()

ff = open('out_t.txt', 'w', encoding='utf8')
ff.write(str(df.values.tolist()))
ff.close()