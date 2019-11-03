import requests
from psycopg2 import connect
from psycopg2.extensions import AsIs


def add_items(url):
    r = requests.get(url)
    beacon = r.text.find('<section class="widget" data-test="exchange-office-rates">')
    data = {}

    currencies = ['USD',
                  'EUR',
                  'AUD',
                  'CAD',
                  'DKK',
                  'SEK',
                  'CHF',
                  'JPY']

    for cur in currencies:
        unit_search = r.text.find(cur, beacon)
        if unit_search == -1:
            continue
        td_tag_open = '<td class="font-size-large">'
        td_tag_close = '</td>'

        purchase_cr_open_tag = r.text.find(td_tag_open,
                                           unit_search)
        purchase_cr_close_tag = r.text.find(td_tag_close,
                                            purchase_cr_open_tag)

        sale_cr_open_tg = r.text.find(td_tag_open,
                                      purchase_cr_close_tag)
        sale_cr_close_tg = r.text.find(td_tag_close,
                                       sale_cr_open_tg)

        td_tag_open_time = '<td class="color-border-dark font-size-default">'
        time_open = r.text.find(td_tag_open_time,
                                sale_cr_close_tg)
        time_close = r.text.find(td_tag_close,
                                 time_open)

        assert (purchase_cr_open_tag < sale_cr_open_tg
                and purchase_cr_close_tag < sale_cr_open_tg
                and time_open < time_close)
        i2 = purchase_cr_open_tag + len(td_tag_open)
        i3 = sale_cr_open_tg + len(td_tag_open)
        i4 = time_open + len(td_tag_open_time)

        data[cur] = (float(r.text[i2:purchase_cr_close_tag].strip().replace(',', '.')),
                     float(r.text[i3:sale_cr_close_tg].strip().replace(',', '.')),
                     str(r.text[i4:time_close].strip()))
    return data


def connection_db():
    con = connect(
        database="Currencies",
        user="postgres",
        password='911',
        host="127.0.0.1",
        port="5432")
    return con


def create_tables(con, data):
    query = """Create table %(table)s
      (purchase_course   real,
       sale_course       real,
       renew_date        timestamp )"""
    for key in data:
        cur = con.cursor()
        try:
            cur.execute(query, {'table': AsIs(key)})
        except:  # Prevent program from creating tables twicely
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


url = 'https://www.banki.ru/products/currency/bank/mkb/moskva/'
data = add_items(url)
con = connection_db()
cur = create_tables(con, data)
insert_Tables = insert_into_tables(con, data)

con.close()
