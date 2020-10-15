import sqlite3
from sqlite3 import Error
import requests 
import json

sql_create_birds_table = """ CREATE TABLE IF NOT EXISTS birds (
                                    id integer PRIMARY KEY,
                                    name text,
                                    license text,
                                    url text,
                                    image_width integer,
                                    image_height integer    
                                ); """

sql = ''' INSERT INTO birds(name,license,url,image_width,image_height)
            VALUES(?,?,?,?,?) '''

base_url = 'https://commons.wikimedia.org/w/rest.php/v1/'
endpoint = 'search/page'
headers = {'User-Agent': 'MediaWiki REST API docs examples/0.1 (https://meta.wikimedia.org/wiki/User:APaskulin_(WMF))'}

himalayan_birds = [
    "Robin accentor",
    "Rufous-breasted accentor",
    "Blue-throated barbet",
    "Great barbet",
    "Grey-winged blackbird",
    "White-collared blackbird",
    "Himalayan bluetail",
    "Black bulbul",
    "Himalayan bulbul",
    "Mountain bulbul",
    "Brown bullfinch",
    "Crested bunting",
    "Black-throated bushtit"
]

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def add_birds(birds, db_conn):
    for bird in birds:
        endpoint = 'search/page'
        search_query = bird
        limit = 1

        url = base_url + endpoint
        response = requests.get(url, headers=headers, params={'q': search_query, 'limit': limit},)
        response = json.loads(response.text)

        for page in response['pages']:
            file = page['title']
            endpoint = 'file/' + file

            url = base_url + endpoint
            response = requests.get(url, headers=headers)
            response = json.loads(response.text)

            print(bird)
            try:
                license =  'https:' + response['file_description_url']
                url = response['preferred']['url']
                name = bird
                width = response['preferred']['width']
                height = response['preferred']['height']
                himalayan_bird = (name, license, url, width, height)
                cur = db_conn.cursor()
                cur.execute(sql, himalayan_bird)
                print(himalayan_bird)
            except:
                print("Image not found")
            print()

db_connection = create_connection("sqlite.db")
create_table(db_connection, sql_create_birds_table)
add_birds(himalayan_birds, db_connection)

