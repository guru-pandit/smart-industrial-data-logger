import sqlite3

class Database:

    creating_table = """
    DROP TABLE IF EXISTS Temperature_Data;
    CREATE TABLE Temperature_Data (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Temperature FLOAT,
    Date TIMESTAMP,
    Time TIMESTAMP
    );

    DROP TABLE IF EXISTS Current_Data;  
    CREATE TABLE Current_Data (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Current FLOAT,
    Date TIMESTAMP,
    Time TIMESTAMP
    );

    DROP TABLE IF EXISTS RPM_Data;
    CREATE TABLE RPM_Data (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    RPM FLOAT,
    Date TIMESTAMP,
    Time TIMESTAMP
    );

    DROP TABLE IF EXISTS Vibration_Data;
    CREATE TABLE Vibration_Data (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Vibration FLOAT,
    Date TIMESTAMP,
    Time TIMESTAMP
    );
    """

    def __init__(self, filename):
        # Connect or create Database
        self.db = sqlite3.connect(filename)
        self.cursor = self.db.cursor()

        # Creating table
        sqlite3.complete_statement(self.creating_table)
        self.cursor.executescript(self.creating_table)

        # Close database
        self.cursor.close()
        # self.db.close()

#---- Functions to save data to the database-----
    # Function to save current data
    def temp_data_handler(self, data):
        self.inserting_data = """INSERT INTO 'Temperature_Data'('temperature', 'Date', 'Time') VALUES(?,?,?);"""
        self.db.cursor().execute(self.inserting_data, data)
        self.db.commit()


    # Function to save current data
    def current_data_handler(self, data):
        self.inserting_data = """INSERT INTO 'Current_Data'('Current', 'Date', 'Time') VALUES(?,?,?);"""
        self.db.cursor().execute(self.inserting_data, data)
        self.db.commit()

    # Function to save RPM data
    def rpm_data_handler(self, data):
        self.inserting_data = """INSERT INTO 'RPM_Data'('RPM', 'Date', 'Time') VALUES(?,?,?);"""
        self.db.cursor().execute(self.inserting_data, data)
        self.db.commit()

    # Function to save vibration data
    def vibration_data_handler(self, data):
        self.inserting_data = """INSERT INTO 'Vibration_Data'('Vibration', 'Date', 'Time') VALUES(?,?,?);"""
        self.db.cursor().execute(self.inserting_data, data)
        self.db.commit()

    # Function to select sensor data as per MQTT Topic
    def sensor_data_handler(self, topic, data):
        if topic == "/SIDL/temperature":
            self.temp_data_handler(data)
        if topic == "/SIDL/current":
            self.current_data_handler(data)
        if topic == "/SIDL/rpm":
            self.rpm_data_handler(data)
        if topic == "/SIDL/vibration":
            self.vibration_data_handler(data)

