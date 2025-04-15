import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['institutions', 'positions', 'experiences', 'skills','feedback', 'users']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def createTables(self, purge=False, data_path='flask_app/database/'):
        '''Creates or drops database tables.'''

        # Drop tables in reverse order if purge is True
        if purge:
            # Disable foreign key checks
            self.query("SET FOREIGN_KEY_CHECKS = 0;")

            # Drop tables
            self.query(f"""DROP TABLE IF EXISTS skills""")
            self.query(f"""DROP TABLE IF EXISTS experiences""")
            self.query(f"""DROP TABLE IF EXISTS positions""")
            self.query(f"""DROP TABLE IF EXISTS institutions""")
            self.query(f"""DROP TABLE IF EXISTS feedback""")
            self.query(f"""DROP TABLE IF EXISTS users""")

            # Enable foreign key checks
            self.query("SET FOREIGN_KEY_CHECKS = 1;")

        # Create each table from the SQL file
        # Ensure the order respects foreign key dependencies
        table_creation_order = ['institutions', 'positions', 'experiences', 'feedback', 'skills', 'users']

        for table in table_creation_order:
            with open(f"{data_path}create_tables/{table}.sql") as read_file:
                create_statement = read_file.read()
            self.query(create_statement)

            # Import initial data if available
            try:
                params = []
                with open(f"{data_path}initial_data/{table}.csv") as read_file:
                    scsv = read_file.read()
                for row in csv.reader(StringIO(scsv), delimiter=','):
                    params.append(row)

                # Insert the data
                cols = params[0]
                params = params[1:]
                self.insertRows(table=table, columns=cols, parameters=params)
            except FileNotFoundError:
                print(f'No initial data for table {table}')

    def insertRows(self, table='table', columns=['x', 'y'], parameters=[['v11', 'v12'], ['v21', 'v22']]):
        """
        Inserts rows into the specified table.

        :param table: Name of the table to insert data into.
        :param columns: List of column names corresponding to the parameters.
        :param parameters: List of values to insert, either as a single row or multiple rows.
        :return: Last inserted ID or a list of last inserted IDs for multiple rows.
        """
        # Prepare keys and values for the SQL query
        keys = ', '.join(columns)
        values_placeholder = ', '.join(['%s'] * len(columns))

        # Construct the query for multiple rows
        if any(isinstance(el, list) for el in parameters):
            # Handle multiple rows
            query = f"INSERT IGNORE INTO {table} ({keys}) VALUES "
            query += ', '.join([f"({values_placeholder})"] * len(parameters))
            flattened_parameters = list(itertools.chain(*parameters))
        else:
            # Handle a single row
            query = f"INSERT IGNORE INTO {table} ({keys}) VALUES ({values_placeholder})"
            flattened_parameters = parameters

        try:
            # Execute the query
            self.query(query, flattened_parameters)

            # Fetch the last inserted ID(s)
            last_id_query = "SELECT LAST_INSERT_ID()"
            result = self.query(last_id_query)

            if isinstance(parameters[0], list):
                # If multiple rows were inserted, return a list of IDs
                return [result[0]['LAST_INSERT_ID()'] + i for i in range(len(parameters))]
            else:
                # For a single row, return the single ID
                return result[0]['LAST_INSERT_ID()']
        except mysql.connector.Error as err:
            print(f"Error while inserting rows into {table}: {err}")
            return None

    def getResumeData(self):
        # Prepare to collect data
        resume_data = {}

        # Load institutions from CSV
        institutions_file = 'flask_app/database/initial_data/institutions.csv'
        try:
            with open(institutions_file, newline='') as csvfile:
                institution_reader = csv.DictReader(csvfile)
                for row in institution_reader:
                    inst_id = int(row['inst_id'])
                    resume_data[inst_id] = {
                        'address': row['address'] if row['address'] else 'NULL',
                        'city': row['city'],
                        'state': row['state'],
                        'type': row['type'],
                        'zip': row['zip'] if row['zip'] else 'NULL',
                        'department': row['department'],
                        'name': row['name'],
                        'positions': {}
                    }
        except FileNotFoundError:
            print(f"Error: File {institutions_file} not found.")

        # Load positions from CSV
        positions_file = 'flask_app/database/initial_data/positions.csv'
        try:
            with open(positions_file, newline='') as csvfile:
                position_reader = csv.DictReader(csvfile)
                for row in position_reader:
                    position_id = int(row['position_id'])
                    inst_id = int(row['inst_id'])
                    if inst_id in resume_data:
                        resume_data[inst_id]['positions'][position_id] = {
                            'title': row['title'],
                            'responsibilities': row['responsibilities'],
                            'start_date': row['start_date'],
                            'end_date': row['end_date'],
                            'experiences': {}
                        }
        except FileNotFoundError:
            print(f"Error: File {positions_file} not found.")

        # Load experiences from CSV
        experiences_file = 'flask_app/database/initial_data/experiences.csv'
        try:
            with open(experiences_file, newline='') as csvfile:
                experience_reader = csv.DictReader(csvfile)
                for row in experience_reader:
                    experience_id = int(row['experience_id'])
                    position_id = int(row['position_id'])
                    # Find the corresponding position
                    for inst_id, institution in resume_data.items():
                        for pos_id, position in institution['positions'].items():
                            if pos_id == position_id:
                                position['experiences'][experience_id] = {
                                    'description': row['description'],
                                    'hyperlink': row['hyperlink'],
                                    'name': row['name'],
                                    'start_date': row['start_date'],
                                    'end_date': row['end_date'],
                                    'skills': {}
                                }
        except FileNotFoundError:
            print(f"Error: File {experiences_file} not found.")

        # Load skills from CSV
        skills_file = 'flask_app/database/initial_data/skills.csv'
        try:
            with open(skills_file, newline='') as csvfile:
                skill_reader = csv.DictReader(csvfile)
                for row in skill_reader:
                    skill_id = int(row['skill_id'])
                    experience_id = int(row['experience_id'])
                    # Find the corresponding experience
                    for inst_id, institution in resume_data.items():
                        for pos_id, position in institution['positions'].items():
                            for exp_id, experience in position['experiences'].items():
                                if exp_id == experience_id:
                                    experience['skills'][skill_id] = {
                                        'name': row['name'],
                                        'skill_level': int(row['skill_level'])
                                    }
        except FileNotFoundError:
            print(f"Error: File {skills_file} not found.")

        return resume_data

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    def createUser(self, email='me@email.com', password='password', role='guest'):
        """
        Creates a new user in the database with encrypted password if user does not already exist.

        :param email: Email of the new user.
        :param password: Password of the new user.
        :param role: Role of the user, either 'guest' or 'owner'.
        :return: Dictionary indicating success (1) or failure (0) and a message.
        """
        # Check if user already exists
        existing_user = self.query("SELECT * FROM users WHERE email = %s", (email,))
        if existing_user:
            return {'success': 0, 'message': 'User already exists'}

        # Encrypt the password using scrypt
        encrypted_password = self.onewayEncrypt(password)

        # Insert the new user into the database
        try:
            self.query("INSERT INTO users (email, password, role) VALUES (%s, %s, %s)",
                       (email, encrypted_password, role))
            return {'success': 1, 'message': 'User created successfully'}
        except mysql.connector.Error as err:
            print(f"Error while creating user: {err}")
            return {'success': 0, 'message': 'Failed to create user due to database error'}

    def authenticate(self, email='me@email.com', password='password'):
        """
        Authenticates an existing user, or creates a new user if the email does not exist.

        :param email: Email of the user attempting to login.
        :param password: Password of the user.
        :return: Dictionary indicating success (1) or failure (0) and a message.
        """
        # Fetch the user from the database using their email
        user = self.query("SELECT * FROM users WHERE email = %s", (email,))

        if not user:
            # If user does not exist, create a new user
            creation_result = self.createUser(email=email, password=password)
            if creation_result['success'] == 1:
                return {'success': 1, 'message': 'New user created and logged in successfully'}
            else:
                return {'success': 0, 'message': 'Failed to create new user'}

        # If user exists, check the password
        stored_password = user[0]['password']
        if self.onewayEncrypt(password) == stored_password:
            # Authentication successful
            return {'success': 1, 'message': 'Authentication successful'}
        else:
            # Password does not match
            return {'success': 0, 'message': 'Incorrect password'}

    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message


