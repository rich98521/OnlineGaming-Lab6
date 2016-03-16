from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import mysql.connector

class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = { 'version': '3.5.1',
                     'last_build':  date.today().isoformat() }
        self.write(response)
 
class GetGameByIdHandler(tornado.web.RequestHandler):
    def get(self, id):
        response = { 'id': int(id),
                     'name': 'Crazy Game',
                     'release_date': date.today().isoformat() }
        self.write(response)
 
class GetScoreHandler(tornado.web.RequestHandler):
    def get(self, name):
        cnx = mysql.connector.connect(user='root', password='98521',
                              host='127.0.0.1',
                              database='database1')
        cursor = cnx.cursor()
        query = ("SELECT Score FROM Scores WHERE Name = '"+ name +"'")

        cursor.execute(query, (name))
        data = cursor.fetchone()

        response = { 'name': name,
                     'score': data[0] }

        cursor.close()
        cnx.close()
        self.write(response)

class UpdateScoreHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "149.153.102.59")
        name = self.get_argument('name', '')
        score = self.get_argument('score', '')

        cnx = mysql.connector.connect(user='root', password='98521',
                              host='127.0.0.1',
                              database='database1')
        cursor = cnx.cursor()

        updateScore = ("DELETE FROM Scores WHERE Name = '"+ name +"'; INSERT INTO Scores (name, score) VALUES ('"+ name +"', "+ score +")")
        for result in cursor.execute(updateScore, multi = True):
            pass
        cnx.commit()
        cursor.close()
        cnx.close()

        response = { 'name': name,
                     'score': score }

        self.write(response)
 
application = tornado.web.Application([
    (r"/getgamebyid/([0-9]+)", GetGameByIdHandler),
    (r"/score/([a-z0-9]+)", GetScoreHandler),
    (r"/version", VersionHandler),
    (r"/updatescore", UpdateScoreHandler)
])
 
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()