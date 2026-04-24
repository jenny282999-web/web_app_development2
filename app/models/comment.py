import sqlite3

class CommentModel:
    def __init__(self, db_path='instance/database.db'):
        self.db_path = db_path

    def _get_connection(self):
        """建立資料庫連線並設定 row_factory。"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, user_id, comic_id, content, rating, warning_tags=None):
        """新增一筆評論。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO comments (user_id, comic_id, content, rating, warning_tags) VALUES (?, ?, ?, ?, ?)",
                (user_id, comic_id, content, rating, warning_tags)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating comment: {e}")
            return None
        finally:
            conn.close()

    def get_by_comic(self, comic_id):
        """取得指定漫畫的所有評論。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            query = """
                SELECT co.*, u.username 
                FROM comments co
                JOIN users u ON co.user_id = u.id
                WHERE co.comic_id = ?
                ORDER BY co.created_at DESC
            """
            cursor.execute(query, (comic_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching comments: {e}")
            return []
        finally:
            conn.close()

    def delete(self, comment_id):
        """刪除指定評論。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting comment: {e}")
            return False
        finally:
            conn.close()

