import sqlite3
from sqlite3 import Error

DATABASE_PATH = "./"

#######################################################
### :desc: create a database connection to the SQLite
###        database specified by db_file.
### :param db_file: database file
### :return: Connection object or None
#######################################################


class DBConnector:
    seed_executed = False

    def create_connection(self, db_file):
        conn = None
        db_file = DATABASE_PATH + db_file
        try:
            conn = sqlite3.connect(db_file)
            create_database(conn)
            if not self.seed_executed:
                seed_database(conn)
                self.seed_executed = True
            return conn
        except Error as e:
            print(e)

        return conn

    def create_seedless_connection(self, db_file):
        conn = None
        db_file = DATABASE_PATH + db_file
        try:
            conn = sqlite3.connect(db_file)
            create_database(conn)
            return conn
        except Error as e:
            print(e)

        return conn


#######################################################
### :desc: create a table from the create_table_sql
###        statement.
### :param conn: Connection object
### :param create_table_sql: a CREATE TABLE statement
### :return: None
#######################################################
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def seed_database(conn):
    seed_insert = """ 
        INSERT INTO consorcium(name) VALUES
        ('TransNit'),
        ('TransOceanica');

        INSERT INTO bus_trip_compliance(consorcium, trips_scheduled, trips_completed, conclusion_percentage, subsidy, date) VALUES
        ('TransNit', 1000, 850, 85.0, 85.0, '2021-10-01'),
        ('TransOceanica', 800, 720, 90.0, 95.0, '2021-10-01'),
        ('TransNit', 1000, 850, 85.0, 85.0, '2021-11-01'),
        ('TransOceanica', 800, 720, 90.0, 95.0, '2021-11-01');

        INSERT INTO bus_km_compliance(consorcium, km_scheduled, km_completed, conclusion_percentage, subsidy, date) VALUES
        ('TransNit', 400.0, 390.0, 97.5, 100.0, '2021-10-01'),
        ('TransOceanica', 350.0, 100.0, 28.57, 0.0, '2021-10-01'),
        ('TransNit', 400.0, 390.0, 97.5, 100.0, '2021-11-01'),
        ('TransOceanica', 350.0, 100.0, 28.57, 0.0, '2021-11-01');

        INSERT INTO bus_climatization_compliance(consorcium, total_busses, busses_without_climatization, conclusion_percentage, subsidy, date) VALUES
        ('TransNit', 100, 10, 90.0, 95.0, '2021-10-01'),
        ('TransOceanica', 50, 40, 80.0, 70.0, '2021-10-01'),
        ('TransNit', 100, 10, 90.0, 95.0, '2021-11-01'),
        ('TransOceanica', 50, 40, 80.0, 70.0, '2021-11-01');

        INSERT INTO bus_amount_compliance(consorcium, scheduled_fleets, recorded_fleets, conclusion_percentage, subsidy, date) VALUES
        ('TransNit', 100, 90, 90.0, 100.0, '2021-10-01'),
        ('TransOceanica', 50, 40, 80.0, 70.0, '2021-10-01'),
        ('TransNit', 100, 90, 90.0, 100.0, '2021-11-01'),
        ('TransOceanica', 50, 40, 80.0, 70.0, '2021-11-01');
    """
    cursor = conn.cursor()

    try:
        cursor.executescript(seed_insert)
        conn.commit()
    except Error as e:
        print(e)


#######################################################
### :desc: create database and database file if it not
###        exists.
### :param DATABASE: file
### :param conn: Connection object
### :return: None
#######################################################
def create_database(conn):
    sql_consorcium_table = """ CREATE TABLE IF NOT EXISTS consorcium (
                                id INTEGER PRIMARY KEY,
                                name VARCHAR(20) NOT NULL UNIQUE
                            ); """

    sql_bus_trip_compliance = """ CREATE TABLE IF NOT EXISTS bus_trip_compliance (
                                        id INTEGER PRIMARY KEY,
                                        consorcium VARCHAR(20),
                                        trips_scheduled INT,
                                        trips_completed INT,
                                        conclusion_percentage FLOAT,
                                        subsidy FLOAT,
                                        date DATE,
                                        FOREIGN KEY(consorcium) REFERENCES consorcium(name)
                                    ); """

    sql_bus_km_compliance = """ CREATE TABLE IF NOT EXISTS bus_km_compliance (
                                    id INTEGER PRIMARY KEY,
                                    consorcium VARCHAR(20),
                                    km_scheduled FLOAT,
                                    km_completed FLOAT,
                                    conclusion_percentage FLOAT,
                                    subsidy FLOAT,
                                    date DATE,
                                    FOREIGN KEY(consorcium) REFERENCES consorcium(name)
                                ); """

    sql_bus_climatization_compliance = """ CREATE TABLE IF NOT EXISTS bus_climatization_compliance (
                                            id INTEGER PRIMARY KEY,
                                            consorcium VARCHAR(20),
                                            total_busses FLOAT,
                                            busses_without_climatization FLOAT,
                                            conclusion_percentage FLOAT,
                                            subsidy FLOAT,
                                            date DATE,
                                            FOREIGN KEY(consorcium) REFERENCES consorcium(name)
                                        ); """

    sql_bus_amount_compliance = """ CREATE TABLE IF NOT EXISTS bus_amount_compliance (
                                        id INTEGER PRIMARY KEY,
                                        consorcium VARCHAR(20),
                                        scheduled_fleets FLOAT,
                                        recorded_fleets FLOAT,
                                        conclusion_percentage FLOAT,
                                        subsidy FLOAT,
                                        date DATE,
                                        FOREIGN KEY(consorcium) REFERENCES consorcium(name)
                                    ); """

    sql_total_subsidy = """ CREATE TABLE IF NOT EXISTS total_subsidy (
                                id INTEGER PRIMARY KEY,
                                consorcium VARCHAR(20),
                                total_subsidy FLOAT,
                                date DATE,
                                FOREIGN KEY(consorcium) REFERENCES consorcium(name)
                            ); """

    # create tables
    create_table(conn, sql_consorcium_table)
    create_table(conn, sql_bus_trip_compliance)
    create_table(conn, sql_bus_km_compliance)
    create_table(conn, sql_bus_climatization_compliance)
    create_table(conn, sql_bus_amount_compliance)
    create_table(conn, sql_total_subsidy)


###################################################################
#                                                                 #
#                         AUX FUNCTIONS                           #
#                                                                 #
###################################################################
def str_to_coords(coords_str: str):
    coords = coords_str.split(";")

    for i in range(len(coords)):
        coords[i] = list(map(float, coords[i].split(",")))

    return coords


def list_to_str(my_list: list):
    s = ""
    if type(my_list[0]) == list:  # coordinates list: [[lat0, lon0], [lat1, lon1],...]
        for coord in my_list:
            s += f"{coord[0]},{coord[1]};"  # lat0,lon1;lat1,lon1;lat2,lon2
    else:  # schedule list: ['07:45:0', '07:46:0',...]
        for ts in my_list:
            s += f"{ts};"

    return s[:-1]  # remove last ";"


###################################################################
#                                                                 #
#                            INSERTS                              #
#                                                                 #
###################################################################
def insert_consorcium(conn, name):
    sql = f"""
        INSERT INTO consorcium(name) VALUES
        (?)
    """
    cur = conn.cursor()
    try:
        cur.execute(sql, name)
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(e)
        return False

    return True


def insert_bus_trip_compliance_data(conn, date, payload):
    sql = """ 
        INSERT INTO bus_trip_compliance(consorcium, trips_scheduled, trips_completed, conclusion_percentage, subsidy, date) VALUES
        (?, ?, ?, ?, ?, ?)          
    """
    cur = conn.cursor()
    try:
        cur.execute(
            sql,
            (
                payload["dados"]["consorcio"],
                payload["dados"]["compliance"]["meta_viagens_realizadas"],
                payload["dados"]["compliance"]["total_viagens_realizadas"],
                payload["dados"]["porcentagem_conclusao"],
                payload["dados"]["subsidio_concedido"],
                date
            ),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(e)
        return False


def insert_bus_km_compliance_data(conn, date, payload):
    sql = """ 
        INSERT INTO bus_km_compliance(consorcium, km_scheduled, km_completed, conclusion_percentage, subsidy, date) VALUES
        (?, ?, ?, ?, ?, ?)          
    """
    cur = conn.cursor()
    try:
        cur.execute(
            sql,
            (
                payload["dados"]["consorcio"],
                payload["dados"]["compliance"]["total_programada"],
                payload["dados"]["compliance"]["total_realizada"],
                payload["dados"]["porcentagem_conclusao"],
                payload["dados"]["subsidio_concedido"],
                date
            ),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(e)
        return False


def insert_bus_climatization_compliance_data(conn, date, payload):
    sql = """ 
        INSERT INTO bus_climatization_compliance(consorcium, total_busses, busses_without_climatization, conclusion_percentage, subsidy, date) VALUES
        (?, ?, ?, ?, ?, ?)          
    """
    cur = conn.cursor()
    try:
        cur.execute(
            sql,
            (
                payload["dados"]["consorcio"],
                payload["dados"]["compliance"]["total_onibus"],
                payload["dados"]["compliance"]["nao_climatizados"],
                payload["dados"]["porcentagem_conclusao"],
                payload["dados"]["subsidio_concedido"],
                date
            ),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(e)
        return False


def insert_bus_amount_compliance_data(conn, date, payload):
    sql = """ 
        INSERT INTO bus_amount_compliance(consorcium, scheduled_fleets, recorded_fleets, conclusion_percentage, subsidy, date) VALUES
        (?, ?, ?, ?, ?, ?)          
    """
    cur = conn.cursor()
    try:
        cur.execute(
            sql,
            (
                payload["dados"]["consorcio"],
                payload["dados"]["compliance"]["total_frotas_programadas"],
                payload["dados"]["compliance"]["total_frotas_disponiveis"],
                payload["dados"]["porcentagem_conclusao"],
                payload["dados"]["subsidio_concedido"],
                date
            ),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(e)
        return False


def insert_total_subsidy_data(conn, consorcio, total_subsidy, date):
    sql = """ 
        INSERT INTO total_subsidy(consorcium, total_subsidy, date) VALUES
        (?, ?, ?)          
    """
    cur = conn.cursor()
    try:
        cur.execute(sql, (consorcio, total_subsidy, date))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(e)
        return False


###################################################################
#                                                                 #
#                            QUERIES                              #
#                                                                 #
###################################################################
def select_consorcium(conn):
    sql = """ SELECT * FROM consorcium """
    cur = conn.cursor()
    cur.execute(sql)

    return cur.fetchall()


def select_bus_trip_compliance_data(conn):
    sql = """ SELECT * FROM bus_trip_compliance """
    cur = conn.cursor()
    cur.execute(sql)

    return cur.fetchall()


def select_bus_km_compliance_data(conn):
    sql = """ SELECT * FROM bus_km_compliance """
    cur = conn.cursor()
    cur.execute(sql)

    return cur.fetchall()


def select_bus_climatization_compliance_data(conn):
    sql = """ SELECT * FROM bus_climatization_compliance """
    cur = conn.cursor()
    cur.execute(sql)

    return cur.fetchall()


def select_bus_amount_compliance_data(conn):
    sql = """ SELECT * FROM bus_amount_compliance """
    cur = conn.cursor()
    cur.execute(sql)

    return cur.fetchall()


if __name__ == "__main__":
    db_connector = DBConnector()
    conn = db_connector.create_seedless_connection("integracao_mobnit.db")
    if conn:
        create_database(conn)
