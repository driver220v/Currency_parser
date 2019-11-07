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


def take_data(
        con, table,
        time_begin, time_end
):
    cur = con.cursor()
    cur.execute(f"""Select * from {table}
                    where renew_date between '{time_begin}' and 
                                             '{time_end}' """)
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
units = {
    1: 'USD',
    2: 'EUR',
    3: 'DKK',
    4: 'CAD',
    5: 'SEK',
    6: 'CHF',
    7: 'JPY',
    8: 'AUD'
}
print(units)

# input dates between which exchange rate will be displayed


while True:
    p_table = int(input(
        'For exit press 0. '
        'Input number of unit: '
    ))
    if p_table == 0:
        break
    if 1 < p_table or p_table >= 9:
        print("Error")
        break

    table = units[p_table]
    time_begin, time_end = (
        input('Input initial date in "dd.mm.yyyy" format: '),
        input('Input terminal date in "dd.mm.yyyy" format: ')
    )
    # check date

    rows = take_data(con,
                     table,
                     time_begin,
                     time_end)
    graph(rows, table)

