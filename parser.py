import re
import requests
from time import time
from psycopg2 import connect
from bs4 import BeautifulSoup
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
            result = original_func(*args)
            end = time.time()
            difference = end - start
            if difference >= n:
                print(f'function {original_func.__name__} executed in more then {n} second')
            else:
                print(f'function {original_func.__name__} executed in less then {n} second')
                return result

        return wrapper

    return timer



def gen_courses_time(courses, renew_time):
    for time, course in zip(renew_time, range(0, len(courses), 2)):
        yield float(courses[course].group(0).replace(',','.')), float(courses[course + 1].group(0).replace(',', '.')), time.group(0)

@slow_watch(n=float(input('input time in seconds for add_items: ')))
def add_items(url):
    data = {}
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    table = soup.body.tbody

    units = table.find_all('td',
                           class_="text-nowrap")
    courses = table.find_all('td',
                             class_="font-size-large")
    time = table.find_all('td',
                          class_="color-border-dark font-size-default")

    pattern_courses = re.compile(r'\d{2,3},\d+')
    pattern_units = re.compile(r'[A-Z]+')
    pattern_time = re.compile(r'\d{2}\.\d{2}\.\d+.\d{2}:\d+')

    matches_courses = pattern_courses.finditer(str(courses))
    matches_time = pattern_time.finditer(str(time))
    mathes_units = pattern_units.finditer(str(units))

    for unit, course_time in zip(mathes_units,
                                 gen_courses_time(list(matches_courses), matches_time)):
        data[unit.group(0)] = course_time
    print(data)
    return data


@logger
@slow_watch(n=float(input('input time in seconds for connection_db: ')))
def connection_db():
    con = connect(
        database="Currencies",
        user="username",
        password='911',
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
        except Exception as e:
            con.commit()
            print("Exception: ", e)
        cur.close()


def insert_into_tables(con, data):
    for key, value in data.items():
        cur = con.cursor()
        query = f"""Insert into {key}(purchase_course, sale_course, renew_date)
                values({value[0]}, {value[1]}, '{value[2]}')"""
        cur.execute(query)
        con.commit()
        cur.close()


try:
    url = 'https://www.banki.ru/products/currency/bank/mkb/moskva/'
    data = add_items(url)
    con = connection_db()
    cur = create_tables(con, data)
    insert_Tables = insert_into_tables(con, data)
    con.close()
except ConnectionError:
    print('Connection error. Check your internet connection')

print('connection_db has been called', connection_db.called, 'time(s)')

end = time()

dif = end - start
print(dif)

