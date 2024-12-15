from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self._id = id
        self._name = name
        self.create_in_db()

    def create_in_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO authors (id, name) VALUES (?, ?)", (self._id, self._name))
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def articles(self):
        from models.article import Article  # Local import to avoid circular import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(row[0], row[1], row[2], self, row[4]) for row in rows]

    def magazines(self):
        from models.magazine import Magazine  # Local import
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT DISTINCT magazines.* 
            FROM magazines 
            JOIN articles ON magazines.id = articles.magazine_id 
            WHERE articles.author_id = ?
        """
        cursor.execute(query, (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(row[0], row[1], row[2]) for row in rows]

    def __str__(self):
        return f"Author: {self._name}, ID: {self._id}"
