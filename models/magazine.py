from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category=""):
        self._id = id
        self._name = name
        self._category = category
        self.create_in_db()

    def create_in_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO magazines (id, name, category) VALUES (?, ?, ?)",
            (self._id, self._name, self._category)
        )
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    def __str__(self):
        return f"Magazine: {self._name}, Category: {self._category}, ID: {self._id}"
