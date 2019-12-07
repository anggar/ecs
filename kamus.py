import pymysql

class Kamus:
    def __init__(self):
        self.db = pymysql.connect(host="localhost",
                    user="root",passwd="",db="ant")
        self.cur = self.db.cursor()
        self.cur.execute("SELECT * FROM KAMUS;")
        self.kata = set()

        for row in self.cur.fetchall():
            self.kata.add(row[0])


    def check(self, word: str):
        return word in self.kata

    @staticmethod
    def destroy():
        db.close()