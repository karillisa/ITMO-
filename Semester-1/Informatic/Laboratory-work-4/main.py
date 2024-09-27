from SQLite import *

connection = create_connection("library.sqlite")
create_persons_table = """
CREATE TABLE IF NOT EXISTS persons (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  surname TEXT NOT NULL,
  number_group INTEGER
);
"""
execute_query(connection, create_persons_table)

create_genres_table = """
CREATE TABLE IF NOT EXISTS genres (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);
"""
execute_query(connection, create_genres_table)

create_books_table = """
CREATE TABLE IF NOT EXISTS books (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  year INTEGER NOT NULL,
  genre_id INTEGER NOT NULL,
  FOREIGN KEY (genre_id) REFERENCES genres (id)
);
"""
execute_query(connection, create_books_table)

create_issued_books_table = """
CREATE TABLE IF NOT EXISTS issued_books (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id INTEGER NOT NULL,
  person_id INTEGER NOT NULL,
  FOREIGN KEY (book_id) REFERENCES books (id),
  FOREIGN KEY (person_id) REFERENCES persons (id)
);
"""
execute_query(connection, create_issued_books_table)

create_persons = """
INSERT INTO
  persons (first_name, surname, number_group)
VALUES
  ('James', 'Hype', 1),
  ('Leila', 'Corr', 1),
  ('Brigitte', 'Blue', 2),
  ('Mike', 'Cin', 2),
  ('Elizabeth', 'Viola', 3)
"""
execute_query(connection, create_persons)

create_books = """
INSERT INTO
  books (name, year, genre_id)
VALUES
  ('Crazy Town', 2010, 1),
  ('Charlie Gehringer', 2013, 2),
  ('Childbed Fever', 2015, 3),
  ('Hitler Made Me', 2010, 2),
  ('My Dirty Little', 2020, 5)
"""
execute_query(connection, create_books)

create_genres = """
INSERT INTO
  genres (name)
VALUES
  ('Classic'),
  ('Mystic'),
  ('Fantasy'),
  ('Detective'),
  ('Comedy')
"""
execute_query(connection, create_genres)

create_issued_books = """
INSERT INTO
  issued_books (book_id, person_id)
VALUES
  (1, 1),
  (1, 2),
  (2, 1),
  (2, 3),
  (3, 4),
  (4, 4),
  (5, 5)
"""
execute_query(connection, create_issued_books)

# 1. Выбор всех записей из таблиц
select_all_persons = """
SELECT * FROM persons;
"""

print('1.', execute_query(connection, select_all_persons, fetch_result=True))

select_all_genres = """
SELECT * FROM genres;
"""

print('2.', execute_query(connection,select_all_genres,fetch_result=True))

select_all_books = """
SELECT * FROM books;
"""

print('3.', execute_query(connection,select_all_books,fetch_result=True))

select_all_issued_books = """
SELECT * FROM issued_books;
"""

print('4.', execute_query(connection,select_all_issued_books,fetch_result=True))

# 2. Запрос по извлечению данных с использованием JOIN
select_issued_books_info = """
SELECT persons.first_name, persons.surname, books.name, books.year
FROM issued_books
JOIN persons ON issued_books.person_id = persons.id
JOIN books ON issued_books.book_id = books.id;
"""
print('5.', execute_query(connection, select_issued_books_info, True))


# 3. Запрос по извлечению данных с использованием WHERE и GROUP BY
select_books_count_by_genre = """
SELECT genres.name, COUNT(books.id) as book_count
FROM books
JOIN genres ON books.genre_id = genres.id
WHERE books.year > 2010
GROUP BY genres.name;
"""
print('6.', execute_query(connection, select_books_count_by_genre, True))

# 4. Два запроса с вложенным SELECT-запросом (вложение с помощью WHERE)
select_authors_of_books_after_2010 = """
SELECT first_name, surname
FROM persons
WHERE id IN (SELECT person_id FROM issued_books 
             JOIN books ON issued_books.book_id = books.id 
             WHERE books.year > 2010);
"""
print('7.', execute_query(connection, select_authors_of_books_after_2010, True))

# 5. Два запроса с использованием UNION (объединение запросов):

union_query = """
SELECT first_name, surname FROM persons WHERE number_group = 1
UNION
SELECT first_name, surname FROM persons WHERE number_group = 2
"""
print('8.', execute_query(connection, union_query, fetch_result=True))


# 6. Запрос с использованием DISTINCT
select_distinct_genres = """
SELECT name FROM genres;
"""

print('9.', execute_query(connection, select_distinct_genres, fetch_result=True))

# 7. Обновление двух записей в двух разных таблицах
update_person_name = """
UPDATE persons SET first_name = 'John' WHERE id = 1;
"""
update_book_year = """
UPDATE books SET year = 2012 WHERE id = 1;
"""
execute_query(connection, update_person_name)
execute_query(connection, update_book_year)

# 8. Удаление по одной записи из каждой таблицы
delete_person = """
DELETE FROM persons WHERE id = 2;
"""
delete_book = """
DELETE FROM books WHERE id = 3;
"""
execute_query(connection, delete_person)
execute_query(connection, delete_book)

# 9. Удаление всех записей в одной из таблиц
delete_all_genres = """
DELETE FROM genres;
"""
execute_query(connection, delete_all_genres)

# 10. Формирование отчета
report_query = """
SELECT persons.first_name, persons.surname, GROUP_CONCAT(books.name, ', ') AS issued_books
FROM issued_books
JOIN persons ON issued_books.person_id = persons.id
JOIN books ON issued_books.book_id = books.id
GROUP BY persons.first_name, persons.surname;
"""
execute_query(connection, report_query)

# Закрываем соединение с базой данных
if connection:
    connection.close()
