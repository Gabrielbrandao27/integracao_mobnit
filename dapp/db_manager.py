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
        INSERT INTO company(name) VALUES
            ('Peixoto Ltda');
        INSERT INTO line(route_name, required_bus_amount, required_travel_distance_km, required_round_trips, company_id) VALUES
            ('15', 4, 0, 0, 1),
            ('21', 5, 0, 0, 1),
            ('22', 4, 0, 0, 1);
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

    sql_company_table = """ CREATE TABLE IF NOT EXISTS company (
                                id INTEGER PRIMARY KEY,
                                name VARCHAR(50)
                            ); """

    sql_bus_line_table = """ CREATE TABLE IF NOT EXISTS line (
                                id INTEGER PRIMARY KEY,
                                route_name VARCHAR(5),
                                required_bus_amount INT,
                                required_travel_distance_km NUMERIC,
                                required_round_trips INT,
                                company_id INT,
                                FOREIGN KEY(company_id) REFERENCES company(id)
                            ); """

    # sql_bus_line_compliance = """ CREATE TABLE IF NOT EXISTS line_compliance (
    #                             id INTEGER PRIMARY KEY,
    #                             line_id INT,
    #                             expected_bus_amount INT,
    #                             recorded_bus_amount INT,
    #                             recorded_travel_distance_km NUMERIC,
    #                             recorded_round_trips INT,
    #                             date_recorded DATETIME DEFAULT CURRENT_TIMESTAMP,
    #                             FOREIGN KEY(line_id) REFERENCES line(id)
    #                         ); """

    sql_bus_line_compliance = """ CREATE TABLE IF NOT EXISTS line_compliance (
                                id INTEGER PRIMARY KEY,
                                line_id VARCHAR(5),
                                expected_bus_amount INT,
                                recorded_bus_amount INT,
                                FOREIGN KEY(line_id) REFERENCES line(id)
                            ); """

    sql_bus_table = """ CREATE TABLE IF NOT EXISTS bus (
                                id INTEGER PRIMARY KEY,
                                bus_code VARCHAR(50),
                                line_id INT,
                                has_air_conditioning INT,
                                FOREIGN KEY(line_id) REFERENCES line(id)
                    ); """ # no caso, has_air_conditioning pode ser 0 ou 1

    sql_bus_coordinate_table = """ CREATE TABLE IF NOT EXISTS bus_coordinates (
                                id INTEGER PRIMARY KEY,
                                bus_id INT,
                                latitude REAL,
                                longitude REAL,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY(bus_id) REFERENCES bus(id)
                            ); """

    # create tables
    create_table(conn, sql_company_table)
    create_table(conn, sql_bus_line_table)
    create_table(conn, sql_bus_line_compliance)
    create_table(conn, sql_bus_table)
    create_table(conn, sql_bus_coordinate_table)


###################################################################
#                                                                 #
#                         AUX FUNCTIONS                           #
#                                                                 #
###################################################################
def str_to_coords(coords_str:str):
    coords = coords_str.split(";")

    for i in range(len(coords)):
        coords[i] = list(map(float, coords[i].split(",")))
    
    return coords

def list_to_str(my_list:list):
    s = ""
    if type(my_list[0]) == list: # coordinates list: [[lat0, lon0], [lat1, lon1],...]
        for coord in my_list:
            s += f"{coord[0]},{coord[1]};" # lat0,lon1;lat1,lon1;lat2,lon2
    else: # schedule list: ['07:45:0', '07:46:0',...]
        for ts in my_list:
            s += f"{ts};"
    
    return s[:-1] # remove last ";"


###################################################################
#                                                                 #
#                            INSERTS                              #
#                                                                 #
###################################################################
def insert_bus_line(conn, info_linha):
    sql = f''' INSERT INTO line(route_name)
              VALUES('{info_linha}') '''
    cur = conn.cursor()
    
    try:
        cur.execute(sql)
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(e)
        return False
    
    return True

def insert_compliance_data(conn, info_linha):
    line_id_query = "SELECT route_name FROM line WHERE route_name = ?"
    sql = """ 
        INSERT INTO line_compliance(line_id, expected_bus_amount, recorded_bus_amount) VALUES
        (?, ?, ?)          
    """
    cur = conn.cursor()
    try:
        cur.execute(line_id_query, (info_linha['linha'],))
        line_id = cur.fetchone()[0]
        cur.execute(sql, (line_id, info_linha['frotaProgramada'], info_linha['frotaDisponivel']))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(e)
        return False

def insert_trip_schedule(conn, trip_id, bus_line_id, schedule:list):
    sql = ''' INSERT INTO trip_schedule(id, bus_line_id, schedule)
              VALUES(?, ?, ?) '''
    cur = conn.cursor()

    schedule_str = list_to_str(schedule)

    try:
        cur.execute(sql, (trip_id, bus_line_id, schedule_str))    
        conn.commit()
    except sqlite3.IntegrityError as e:
        return False
    
    return True


def insert_stop(conn, stop_order, bus_line_id, coord:list):
    sql = ''' INSERT INTO stop(stop_order, bus_line_id, lat, lon)
              VALUES(?, ?, ?, ?) '''
    cur = conn.cursor()

    lat, lon = coord

    try:
        cur.execute(sql, (stop_order, bus_line_id, lat, lon))
        conn.commit()
    except sqlite3.IntegrityError as e:
        return False
    
    return True

###################################################################
#                                                                 #
#                            QUERIES                              #
#                                                                 #
###################################################################
def select_lines(conn):
    sql = ''' SELECT * FROM line '''
    cur = conn.cursor()
    cur.execute(sql)

    return cur.fetchall()

def select_compliance_data(conn):
    sql = ''' SELECT * FROM line_compliance '''
    cur = conn.cursor()
    cur.execute(sql)

    return cur.fetchall()

def select_lines_id(conn):
    sql = ''' SELECT id FROM line '''
    cur = conn.cursor()
    cur.execute(sql)

    result = []
    for item in cur.fetchall(): # fetchall = [(id0,), (id1,), (id2,), ...]
        result.append(item[0])
    
    return result


def select_line(conn, id):
    sql = ''' SELECT * FROM line WHERE id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (id,))

    result = list(cur.fetchone()) # [id. route_str]
    
    coords_str = result[1]

    result[1] = str_to_coords(coords_str)

    return result


def select_route_of_line(conn, id):
    sql = ''' SELECT route FROM line WHERE id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (id,))

    try:
        coords_str = cur.fetchone()[0]
        route = str_to_coords(coords_str)
    except TypeError as e:
        return None
    
    return route


def select_trip_schedule(conn, trip_id):
    sql = ''' SELECT schedule FROM trip_schedule WHERE id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (trip_id,))

    return cur.fetchone()[0].split(";")


def count_trips(conn, bus_line):
    sql = ''' SELECT COUNT(*) FROM trip_schedule WHERE bus_line_id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (bus_line,))

    return cur.fetchone()[0]

def select_stop_schedule(conn, next_stop, bus_line_id, trip_id):
    result = [None, None]
    
    sql = ''' SELECT lat,lon FROM stop WHERE stop_order = ? AND bus_line_id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (next_stop, bus_line_id))

    result[0] = cur.fetchone()

    sql = ''' SELECT schedule FROM trip_schedule WHERE id = ? '''
    cur = conn.cursor()

    try:
        cur.execute(sql, (trip_id,))
        result[1] = cur.fetchone()[0].split(";")[next_stop-1]
    except TypeError as e:
        return None

    return result
    
    
def select_stops(conn, bus_line_id):    
    sql = ''' SELECT lat,lon,stop_order FROM stop WHERE bus_line_id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (bus_line_id,))

    return cur.fetchall()


if __name__ == "__main__":
    db_connector = DBConnector()
    conn = db_connector.create_connection("integracao_mobnit.db")
    if conn:
        create_database(conn)