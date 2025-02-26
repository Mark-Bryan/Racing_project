import mysql.connector


def get_db_conn():
    conn = mysql.connector.connect(
        host="localhost",
        user="Banyeh_Akika",
        password="#Capalot1900",  # provides a reusable database connection
        database="amc_se",
    )
    return conn


# cursor = conn.cursor()


# sql = "SELECT * FROM cars"
# cursor.execute(sql)
# cars = cursor.fetchall()

# for car in cars:
#     print(car)

# car_sql = "INSERT INTO `cars` (`Car_ID`, `Title`, `Description`, `Cover_Image`) VALUES ('3', 'Ferrari Monza SP1', 'Lightening Bolt', '') "

# cursor.execute(car_sql)
# conn.commit()

# cursor.execute(car_sql)
# cars = cursor.fetchall()
# for car in cars:
#     print(car)


# cursor.close()
# conn.close()
