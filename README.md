# Currency-parser
This project consists of 2 files(parts):

1) Parser: This program analyses https://www.banki.ru/products/currency/bank/mkb/moskva/
and grabs data related to currencies' exchange rates. 
After that, program creates tables on PostgreSQL local server(established beforehand),
putting taken data into created tables.

2) Graphs: This program connects to postgre local server and takes data from related tables.
After that, on the basis of matplotlib module it builds graphs both sale-course and purchase-course of a selected currency.
    
