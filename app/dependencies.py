from app.db.database import Database

class Dependency:
    def __init__(self, db: Database ):
        self.db = db

    def get_db(self):
        try:
            self.db.connect()
            yield self.db.database
        finally:
            self.db.close()
