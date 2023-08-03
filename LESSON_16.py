import sqlite3

con = sqlite3.connect('dbairbnb.db')
conn = con.cursor()

conn.execute(
    """
    CREATE TABLE host (
        id_host INTEGER PRIMARY KEY,
        name_host TEXT NOT NULL,
        mail_host TEXT NOT NULL,
        date_of_birth DATE NOT NULL,
        phone_number INTEGER NOT NULL
    );
""")

conn.execute(
    """
    CREATE TABLE guests (
        id_guest INTEGER PRIMARY KEY,
        name_guest TEXT NOT NULL,
        mail_guest TEXT NOT NULL,
        date_of_birth DATE NOT NULL,
        phone_number INTEGER NOT NULL
    );
""")

conn.execute(
    """
    CREATE TABLE appart (
        id_appart INTEGER PRIMARY KEY,
        id_host INTEGER NOT NULL,
        price_per_day REAL NOT NULL,
        adress TEXT NOT NULL,
        a_c TEXT NOT NULL,
        amount_of_residence INTEGER NOT NULL,
        FOREIGN KEY (id_host) REFERENCES host (id)
    );
""")

conn.execute(
    """
    CREATE TABLE reservation (
        id_reservation INTEGER PRIMARY KEY,
        id_appart INTEGER NOT NULL,
        id_guest INTEGER NOT NULL,
        date_from DATE NOT NULL,
        date_to DATE NOT NULL,
        price REAL NOT NULL,
        payment_status TEXT NOT NULL,
        FOREIGN KEY (id_appart) REFERENCES appart (id_appart),
        FOREIGN KEY (id_guest) REFERENCES guest (id_guest)
    );
""")

conn.execute(
    """
    CREATE TABLE review (
        id_review INTEGER PRIMARY KEY,
        id_reservation INTEGER NOT NULL,
        stars INTEGER NOT NULL,
        text_review TEXT NOT NULL,
        FOREIGN KEY (id_reservation) REFERENCES reservation (id_reservation)
    );
""")

conn.execute("INSERT INTO host (name_host, mail_host, date_of_birth, phone_number) VALUES ('Kate', 'kateryna@gmail.com', '1997-04-20', 380993847722)")
conn.execute("INSERT INTO host (name_host, mail_host, date_of_birth, phone_number) VALUES ('July', 'julia@gmail.com', '1997-06-19', 380996320912)")
conn.execute("INSERT INTO host (name_host, mail_host, date_of_birth, phone_number) VALUES ('Artem', 'artem@gmail.com', '1998-08-03', 380958192093)")

conn.execute("INSERT INTO guests (name_guest, mail_guest, date_of_birth, phone_number) VALUES ('Igor', 'igorbrag@gmail.com', '1993-01-27', 380992453322)")
conn.execute("INSERT INTO guests (name_guest, mail_guest, date_of_birth, phone_number) VALUES ('Pavlo', 'pavlo@gmail.com', '1992-04-14', 380998167201)")
conn.execute("INSERT INTO guests (name_guest, mail_guest, date_of_birth, phone_number) VALUES ('Veronika', 'veronika@gmail.com', '1990-10-17', 380972917482)")

conn.execute("INSERT INTO appart (id_host, price_per_day, adress, a_c, amount_of_residence) VALUES (1, 250, 'Shevchenka 76', 'yes', 4)")
conn.execute("INSERT INTO appart (id_host, price_per_day, adress, a_c, amount_of_residence) VALUES (2, 400, 'Reytarska 21', 'yes', 2)")
conn.execute("INSERT INTO appart (id_host, price_per_day, adress, a_c, amount_of_residence) VALUES (3, 200, 'Rylleva 35', 'no', 6)")

conn.execute("INSERT INTO reservation (id_appart, id_guest, date_from, date_to, price, payment_status) VALUES (3, 3, '2023-09-01', '2023-09-10', 2500, 'PAID')")
conn.execute("INSERT INTO reservation (id_appart, id_guest, date_from, date_to, price, payment_status) VALUES (3, 2, '2023-10-10', '2023-10-15', 4500, 'NOT PAID')")
conn.execute("INSERT INTO reservation (id_appart, id_guest, date_from, date_to, price, payment_status) VALUES (3, 1, '2023-08-20', '2023-08-23', 600, 'PAID')")

conn.execute("INSERT INTO review (id_reservation, stars, text_review) VALUES (3, 4, 'Had a great vacation here!')")
conn.execute("INSERT INTO review (id_reservation, stars, text_review) VALUES (2, 5, 'Best place!')")
conn.execute("INSERT INTO review (id_reservation, stars, text_review) VALUES (1, 3, 'Cant recommend this place')")


# 1. Find a user who had the biggest amount of reservations. Return user name and user_id

conn.execute('''
SELECT g.name_guest, g.id_guest, COUNT(r.id_reservation) AS counters
FROM guests g
LEFT JOIN reservation r ON g.id_guest = r.id_guest
GROUP BY g.name_guest, g.id_guest
ORDER BY counters DESC
LIMIT 1
''')
res = conn.fetchone()
print("Guest with the most reservations:", res)

# 2. (Optional) Find a host who earned the biggest amount of money for the last month. Return hostname and host_id
conn.execute('''
SELECT h.name_host, h.id_host, SUM(r.price) AS money
FROM host h
LEFT JOIN appart app ON h.id_host = app.id_host
LEFT JOIN reservation r ON app.id_appart = r.id_appart
WHERE r.date_from >= date('now', '-1 month')
GROUP BY h.name_host, h.id_host
ORDER BY money DESC
LIMIT 1
''')
res2 = conn.fetchone()
print("Host with the most earnings last month:", res2)

# (Optional) Find a host with the best average rating. Return hostname and host_id

conn.execute('''
SELECT h.name_host, h.id_host, AVG(rev.stars) AS avg_star
FROM host h
LEFT JOIN appart app ON h.id_host = app.id_host
LEFT JOIN reservation r ON app.id_appart = r.id_appart      
LEFT JOIN review rev ON r.id_reservation = rev.id_reservation
GROUP BY h.name_host, h.id_host
ORDER BY avg_star DESC
LIMIT 1
''')
res3 = conn.fetchone()
print("Host with the best star:", res3)

conn.close()

