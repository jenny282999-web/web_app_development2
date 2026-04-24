import sqlite3

class ComicModel:
    def __init__(self, db_path='instance/database.db'):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, title, author, description=None, cover_url=None):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO comics (title, author, description, cover_url) VALUES (?, ?, ?, ?)",
            (title, author, description, cover_url)
        )
        conn.commit()
        comic_id = cursor.lastrowid
        conn.close()
        return comic_id

    def get_all(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM comics")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_by_id(self, comic_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM comics WHERE id = ?", (comic_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_by_tag(self, tag_name):
        conn = self._get_connection()
        cursor = conn.cursor()
        query = """
            SELECT c.* FROM comics c
            JOIN comic_tags ct ON c.id = ct.comic_id
            JOIN tags t ON ct.tag_id = t.id
            WHERE t.name = ?
        """
        cursor.execute(query, (tag_name,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def update(self, comic_id, title=None, author=None, description=None, cover_url=None):
        conn = self._get_connection()
        cursor = conn.cursor()
        fields = []
        params = []
        if title: fields.append("title = ?"); params.append(title)
        if author: fields.append("author = ?"); params.append(author)
        if description: fields.append("description = ?"); params.append(description)
        if cover_url: fields.append("cover_url = ?"); params.append(cover_url)
        
        if not fields: return False
        
        params.append(comic_id)
        query = f"UPDATE comics SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        count = cursor.rowcount
        conn.close()
        return count > 0

    def delete(self, comic_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM comics WHERE id = ?", (comic_id,))
        conn.commit()
        count = cursor.rowcount
        conn.close()
        return count > 0
