import sqlite3
import os

DATABASE = os.path.join('instance', 'database.db')

class Comment:
    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, manga_id, chapter_id, user_name, content):
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

    @classmethod
    def get_by_chapter(cls, chapter_id):
        conn = cls.get_db_connection()
        comments = conn.execute('SELECT * FROM comments WHERE chapter_id = ? ORDER BY created_at DESC', (chapter_id,)).fetchall()
        conn.close()
        return [dict(c) for c in comments]

    @classmethod
    def get_by_manga(cls, manga_id):
        conn = cls.get_db_connection()
        comments = conn.execute('SELECT * FROM comments WHERE manga_id = ? ORDER BY created_at DESC', (manga_id,)).fetchall()
        conn.close()
        return [dict(c) for c in comments]

    @classmethod
    def delete(cls, comment_id):
        conn = cls.get_db_connection()
        conn.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
        conn.commit()
        conn.close()
