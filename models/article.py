from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self._id = id
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id
        self.create_in_db()

    def create_in_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO articles (id, title, content, author_id, magazine_id) VALUES (?, ?, ?, ?, ?)",
            (self._id, self._title, self._content, self._author_id, self._magazine_id)
        )
        conn.commit()
        conn.close()

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    @property
    def author_id(self):
        return self._author_id

    @property
    def magazine_id(self):
        return self._magazine_id

    def __str__(self):
        return f"Article(id={self._id}, title={self._title}, content={self._content}, author_id={self._author_id}, magazine_id={self._magazine_id})"
