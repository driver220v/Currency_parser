from psycopg2 import connect
import matplotlib.pyplot as plt


def connection_db():
    con = connect(
        database="Currencies",
        user="postgres",
        password='911',
        host="127.0.0.1",
        port="5432"
    )
    return con


def choose_unit(p_table):
    table = ''
    units = {
        1: 'USD',
        2: 'EUR',
        3: 'DKK',
        4: 'CAD',
        5: 'SEK',
        6: 'CHF',
        7: 'JPY',
        8: 'AUD'}
    for key in units:
        if key == p_table:
            table = units[key]
    return table


def take_data(
    con, table,
    time_begin, time_end
):
    
    cur = con.cursor()
    cur.execute(f'''Select * from {table}
                    where renew_date between '{time_begin}' and '{time_end}' ''')
    rows = cur.fetchall()
    return rows


def graph(rows, table):
    purchase_course = []
    sale_course = []
    dates = []
    for i in rows:
        purchase_course.append(i[0])
        sale_course.append(i[1])
        dates.append(f'{i[2].day}.{i[2].month}.{i[2].year} '
                     f'{i[2].hour}:{i[2].minute}')

    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(12, 7))
    sale_course = plt.plot(dates,
                           sale_course,
                           color='r',
                           linewidth=3,
                           marker='o',
                           label='Sale course')

    purchase_course = plt.plot(dates,
                               purchase_course,
                               color='g',
                               linewidth=3,
                               marker='o',
                               label='Purchase course')
    plt.legend()

    plt.xlabel('date')
    plt.ylabel('price')
    plt.title(f'{table} exchange rate')

    purchase_course.clear()
    sale_course.clear()
    dates.clear()
    plt.show()


con = connection_db()

print('1 - USD',
      '2 - EUR',
      '3 - DKK',
      '4 - CAD',
      '5 - SEK',
      '6 - CHF',
      '7 - JPY',
      '8 - AUD',
      sep='\n'
      )
p_table = int(input(
    'For exit press 0. '
    'Input number of unit: '
))
# Enter dates between which exchange rate will be displayed
time_begin, time_end = (
        input('Input intital date in "dd.mm.yyyy" format: '),
        input('Input terminal date in "dd.mm.yyyy" format: ')
        )

while 1 <= p_table < 9:
    table = choose_unit(p_table)
    rows = take_data(con, table,
                     time_begin, time_end)
    graph(rows, table)
    p_table = int(input('For exit press 0. Enter number of unit: '))
    if p_table != 0:
        time_begin, time_end = (
        input('Input initial date in "dd.mm.yyyy" format: '),
        input('Input terminal date in "dd.mm.yyyy" format: '))
    else:
        pass
else:
    pass
