# Currency-parser
currency-parser project consists of 2 files
1) parser: This programm analyse https://www.banki.ru/products/currency/bank/mkb/moskva/
and grab data related to currencies' exchange rates. 
After that programm creates tables in PostgreSQL local server(installed beforehand),
putting taken data into created tables
2)graphs: This programm connects to postgre local sertver and take data from related tables.
After that it builds graphs both sale-course and purchase-course of a selected currency.
    