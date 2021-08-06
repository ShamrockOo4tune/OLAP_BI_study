from pdfminer.high_level import extract_text
import re
import csv
from os import listdir
from datetime import datetime

result = []
exp_list = []
pdf_statements_list = listdir('./pdf_statements')
for pdf_statement in pdf_statements_list:
    data = extract_text(f'./pdf_statements/{pdf_statement}')
    exp_list.extend(re.findall('ОПЛАТА КАРТОЙ\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n|'
                               'СНЯТИЕ НАЛИЧНЫХ В БАНКОМАТЕ\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n', data)) if \
        re.search('Номер счета 40817810930840235807', data) \
        else None  # TODO Добавить такой же функционал для сберовских выписок

fieldnames = ['date', 'raw_stmt', 'value', 'mcc']
with open('result.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()
    while exp_list:
        exp = exp_list.pop()
        statement = {}
        statement['mcc'] = re.search('\s\d\d\d\d\d\d\s\d\d\d\d\s', exp).group(0)[-5:-1]
        statement['value'] = re.search('\S*\sRUB', exp).group(0)[:-4] if re.search('\d*\.\d\d\sRUB', exp) else ''
        statement['raw_stmt'] = exp
        statement['date'] = datetime.strptime(re.search('\n\d\d\d\d\d\d\n', exp).group(0).strip(), '%y%m%d')
        writer.writerow(statement)
