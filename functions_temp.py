import datetime
import ast


def convert_date(date):
    monthdict = {'JAN': 1, 'FEB': 1, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8,
                 'SEP': 9, 'SEPT': 9, 'OCT': 10, "NOV": 11, "DEC": 12}
    date = str(date).split()
    new_date = datetime.datetime(int(date[2]), monthdict[date[1]], int(date[0]))
    return new_date


def convert_matchname(names):
    if "VIP" in names:
        names = names.split(" (")[0]
    names = names.split(" vs ")
    for name in names:
        name = name.strip()
    return names


def convert_price(price):
    return int(price.replace("€", "").replace(",", ""))


def convert_date_from_str(date):
    print(type(date))
    date = date.split("-")
    date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
    print(type(date))
    return date


def eval_code(code):
    parsed = ast.parse(code, mode='eval')
    fixed = ast.fix_missing_locations(parsed)
    compiled = compile(fixed, '<string>', 'eval')
    compiled = eval(compiled)
    return compiled
