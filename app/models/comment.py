import sqlite3

class CommentModel:
    def __init__(self, db_path='instance/database.db'):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, user_id, comic_id, content, rating, warning_tags=None):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO comments (user_id, comic_id, content, rating, warning_tags) VALUES (?, ?, ?, ?, ?)",
            (user_id, comic_id, content, rating, warning_tags)
        )
        conn.commit()
        comment_id = cursor.lastrowid
        conn.close()
        return comment_id

    def get_by_comic(self, comic_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        query = """
            SELECT co.*, u.username 
            FROM comments co
            JOIN users u ON co.user_id = u.id
            WHERE co.comic_id = ?
            ORDER BY co.created_at DESC
        """
        cursor.execute(query, (comic_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def delete(self, comment_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        conn.commit()
        count = cursor.rowcount
        conn.close()
        return count > 0
