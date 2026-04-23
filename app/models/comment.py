import sqlite3
import os

DATABASE = os.path.join('instance', 'database.db')

class Comment:
    """
    留言模型：處理使用者評論的儲存與讀取。
    """
    @staticmethod
    def get_db_connection():
        """
        建立資料庫連線。
        """
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, manga_id, chapter_id, user_name, content):
        """
        新增留言。
        """
        try:
            conn = cls.get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO comments (manga_id, chapter_id, user_name, content)
                VALUES (?, ?, ?, ?)
            ''', (manga_id, chapter_id, user_name, content))
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except Exception as e:
            print(f"Error creating comment: {e}")
            return None

    @classmethod
    def get_by_chapter(cls, chapter_id):
        """
        取得特定章節的所有留言。
        """
        try:
            conn = cls.get_db_connection()
            comments = conn.execute('SELECT * FROM comments WHERE chapter_id = ? ORDER BY created_at DESC', (chapter_id,)).fetchall()
            conn.close()
            return [dict(c) for c in comments]
        except Exception as e:
            print(f"Error fetching comments for chapter {chapter_id}: {e}")
            return []

    @classmethod
    def get_by_manga(cls, manga_id):
        """
        取得特定漫畫的所有留言。
        """
        try:
            conn = cls.get_db_connection()
            comments = conn.execute('SELECT * FROM comments WHERE manga_id = ? ORDER BY created_at DESC', (manga_id,)).fetchall()
            conn.close()
            return [dict(c) for c in comments]
        except Exception as e:
            print(f"Error fetching comments for manga {manga_id}: {e}")
            return []

    @classmethod
    def delete(cls, comment_id):
        """
        刪除留言。
        """
        try:
            conn = cls.get_db_connection()
            conn.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting comment {comment_id}: {e}")
            return False
