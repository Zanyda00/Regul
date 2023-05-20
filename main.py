import csv
import re


def read_csv(path):
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=",")
        header = next(reader)
        contacts_list = list(reader)
    return header, contacts_list


def format_contacts_list(cont_list):
    format_position_list = list()
    format_number_list = list()

    for i in cont_list:
        con_str = ','.join(i)
        pattern = r'^(\w+)[,\s](\w+)?[,\s](\w+)?(,+)(\w+)?(,+)(\w+\D+)?(,+)(.+)?(,+)(.+@.+)?'
        repl = r'\1,\2,\3,\5,\7,\9,\11'
        result = re.sub(pattern, repl, con_str)
        format_position_list.append(result.split(','))

    for i in format_position_list:
        new_str = ','.join(i)
        pattern = r'(\+7|8)?\s*\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})\s*\(?(\w+.)?\s?(\d{4})?\)?'
        repl = r'+7(\2)\3-\4-\5 \6\7'
        result = re.sub(pattern, repl, new_str)
        format_number_list.append(result.split(','))
    return format_number_list


def del_duplication(cont_list):
    for i in cont_list:
        for j in cont_list:
            if i[0] == j[0] and i[1] == j[1]:
                if i[2] == '':
                    i[2] = j[2]
                if i[3] == '':
                    i[3] = j[3]
                if i[4] == '':
                    i[4] = j[4]
                if i[5] == '':
                    i[5] = j[5]
                if i[6] == '':
                    i[6] = j[6]
    without_duplicat = list()
    for i in cont_list:
        if i not in without_duplicat:
            without_duplicat.append(i)
    return without_duplicat


def write_csv(path, cont_list, header):
    with open(path, "w", encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerow(header)
        for row in cont_list:
            datawriter.writerow(row)


if __name__ == '__main__':
    header, contacts_list = read_csv("phonebook_raw.csv")
    format_list = format_contacts_list(contacts_list)
    contacts_list = del_duplication(format_list)
    write_csv('phonebook.csv', contacts_list, header)
