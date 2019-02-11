from flask import Flask
from flask_restful import Resource, Api
import csv
import json
from datetime import datetime
import psycopg2 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from models.AppRating import AppRating;
from models.Summary import Summary;
from extensions.CustomEncoder import CustomEncoder;

# Instantiate the app
app = Flask(__name__)
api = Api(app)

connection = psycopg2.connect("user='postgres' host='db' password='postgres'")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()

class Observatory(Resource):
    def get(self):
        genres = ['News', 'Book', 'Music']
        apps = []

        with open('./data/AppleStore.csv') as csvFile:
            reader = csv.DictReader(csvFile)
            for row in reader:
                apps.append(AppRating(row))

        filteredGenres = list(filter(lambda x: x.genre in genres, apps))
        filteredGenres.sort(key=lambda x: x.rating_amount, reverse=True)

        summaries = []

        for summary in filteredGenres[:10]:
            summaries.append(Summary(summary.id, summary.name, summary.rating_amount,
                                     summary.size, summary.currency, summary.genre))
        

        cursor.execute('DROP TABLE summary')
        cursor.execute('DROP DATABASE IF EXISTS cognitivodb')
        
        cursor.execute("CREATE DATABASE cognitivodb");                           
        cursor.execute("CREATE TABLE IF NOT EXISTS summary (id int primary key, name varchar, rating_amount int, size int, currency varchar, genre varchar)");        
        sql = "INSERT INTO summary (id, name, rating_amount, size, currency, genre) VALUES (%s, %s, %s, %s, %s, %s)"
        csv.register_dialect('myDialect', delimiter='|',
                             quoting=csv.QUOTE_NONE, quotechar='')
        titles =['id', 'name', 'rating_amount', 'size', 'currency', 'genre']
        myFile = open('./data/Summary.csv', 'w')        
        with myFile:
            writer = csv.writer(myFile, dialect='myDialect')
            writer.writerow(titles);
            for s in summaries:
                writer.writerow([s.id, s.track_name, s.n_citacoes, s.size_bytes, s.price, s.prime_genre])
                cursor.execute(sql, (s.id, s.track_name, s.n_citacoes, s.size_bytes, s.price, s.prime_genre));

        

        cursor.execute("SELECT * FROM summary")
        myresult = cursor.fetchall();

        serialized = json.dumps(myresult, cls=CustomEncoder)

        connection.close()        

        return serialized


# Create routes
api.add_resource(Observatory, '/')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
