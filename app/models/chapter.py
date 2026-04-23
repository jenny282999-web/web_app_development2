import sqlite3
import os

DATABASE = os.path.join('instance', 'database.db')

class Chapter:
    """
    章節模型：負責處理漫畫章節的存取。
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
    def create(cls, manga_id, chapter_num, title, content_url):
        """
        新增章節。
        """
        try:
            conn = cls.get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO chapters (manga_id, chapter_num, title, content_url)
                VALUES (?, ?, ?, ?)
            ''', (manga_id, chapter_num, title, content_url))
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except Exception as e:
            print(f"Error creating chapter: {e}")
            return None

    @classmethod
    def get_by_manga(cls, manga_id):
        """
        取得指定漫畫的所有章節。
        """
        try:
            conn = cls.get_db_connection()
            chapters = conn.execute('SELECT * FROM chapters WHERE manga_id = ? ORDER BY chapter_num ASC', (manga_id,)).fetchall()
            conn.close()
            return [dict(c) for c in chapters]
        except Exception as e:
            print(f"Error fetching chapters for manga {manga_id}: {e}")
            return []

    @classmethod
    def get_by_id(cls, chapter_id):
        """
        取得特定 ID 的章節資訊。
        """
        try:
            conn = cls.get_db_connection()
            chapter = conn.execute('SELECT * FROM chapters WHERE id = ?', (chapter_id,)).fetchone()
            conn.close()
            return dict(chapter) if chapter else None
        except Exception as e:
            print(f"Error fetching chapter {chapter_id}: {e}")
            return None

    @classmethod
    def delete(cls, chapter_id):
        """
        刪除章節。
        """
        try:
            conn = cls.get_db_connection()
            conn.execute('DELETE FROM chapters WHERE id = ?', (chapter_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting chapter {chapter_id}: {e}")
            return False
