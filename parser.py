import requests
from time import time
from psycopg2 import connect
from psycopg2.extensions import AsIs
from requests.exceptions import ConnectionError

start = time()


def logger(original_function):
    def wrapper(*args):
        result = original_function(*args)
        wrapper.called += 1
        return result
    wrapper.called = 0
    return wrapper


def slow_watch(n):
    def timer(original_func):
        import time
        def wrapper(*args):
            start = time.time()
            original_func(*args)
            end = time.time()
            difference = end - start
            if difference >= n:
                print(f'function {original_func.__name__} executed in more then {n} second')
            else:
                print(f'function {original_func.__name__} executed in less then {n} second')
        return wrapper
    return timer

print()
@slow_watch(n=float(input('введите время в секунд для add_items: ')))
def add_items(url, units):
    req = requests.get(url)
    beacon = req.text.find('<section class="widget" data-test="exchange-office-rates">')
    data = {}

    for cur in units:
        unit_search = req.text.find(cur, beacon)
        if unit_search == -1:
            continue
        td_tag_open = '<td class="font-size-large">'
        td_tag_close = '</td>'

        purchase_cr_open_tag = req.text.find(td_tag_open,
                                             unit_search)
        purchase_cr_close_tag = req.text.find(td_tag_close,
                                              purchase_cr_open_tag)

        sale_cr_open_tg = req.text.find(td_tag_open,
                                        purchase_cr_close_tag)
        sale_cr_close_tg = req.text.find(td_tag_close,
                                         sale_cr_open_tg)

        td_tag_open_time = '<td class="color-border-dark font-size-default">'
        time_open = req.text.find(td_tag_open_time,
                                  sale_cr_close_tg)
        time_close = req.text.find(td_tag_close,
                                   time_open)

        assert (purchase_cr_open_tag < sale_cr_open_tg
                and purchase_cr_close_tag < sale_cr_open_tg
                and time_open < time_close)
        i2 = purchase_cr_open_tag + len(td_tag_open)
        i3 = sale_cr_open_tg + len(td_tag_open)
        i4 = time_open + len(td_tag_open_time)

        data[cur] = (
            float(req.text[i2:purchase_cr_close_tag].strip().replace(',', '.')),
            float(req.text[i3:sale_cr_close_tg].strip().replace(',', '.')),
            str(req.text[i4:time_close].strip())
        )
    return data


@logger
@slow_watch(n=float(input('введите время в секундах: ')))
def connection_db():
    con = connect(
        database="Currencies",
        user="postgres",
        password='Ssb68mNk',
        host="127.0.0.1",
        port="5432"
    )
    return con


def create_tables(con, data):

    for key in data:
        query = """Create table %(table)s
            (purchase_course   real,
             sale_course        real,
             renew_date         timestamp )"""
        cur = con.cursor()
        # Prevent program from creating tables twicely
        try:
            cur.execute(query, {'table': AsIs(key)})
        except:
            con.commit()
            cur.close()


def insert_into_tables(con, data):
    for key, value in data.items():
        cur = con.cursor()
        query = f"""Insert into {key}(purchase_course, sale_course, renew_date)
                values({value[0]}, {value[1]}, '{value[2]}')"""
        cur.execute(query)
        con.commit()
        cur.close()


units = [
    'USD',
    'EUR',
    'AUD',
    'CAD',
    'DKK',
    'SEK',
    'CHF',
    'JPY']
try:
    url = 'https://www.banki.ru/products/currency/bank/mkb/moskva/'
    data = add_items(url, units)
    con = connection_db()
    cur = create_tables(con, data)
    insert_Tables = insert_into_tables(con, data)
    con.close()
except ConnectionError:
    print('Connection error. Check your internet connection')

#print('connection_db has been called', connection_db.called, 'time(s)')

end = time()

dif = end - start

