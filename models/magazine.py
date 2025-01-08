from database.connection import get_db_connection

class Magazine:
    def __init__(self, id=None, name="", category=""):
        if not name or not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Magazine name must be a non-empty string.")
        self._id = id
        self._name = name
        self._category = category
        self.save()

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()

       
        if self._id is None:
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self._name, self._category)
            )
            self._id = cursor.lastrowid
        else:
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

    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(*row) for row in rows]

    def contributors(self):
        from models.author import Author
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT DISTINCT authors.* 
            FROM authors 
            JOIN articles ON authors.id = articles.author_id 
            WHERE articles.magazine_id = ?
        """
        cursor.execute(query, (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(*row) for row in rows]

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]

    def contributing_authors(self):
        return self.contributors()

    def __str__(self):
        return f"Magazine: {self._name}, Category: {self._category}, ID: {self._id}"
