import sqlite3
import os

DATABASE = os.path.join('instance', 'database.db')

class Manga:
    def __init__(self, id, title, description, cover_image, language, content_type, gender_pref, author, created_at):
        self.id = id
        self.title = title
        self.description = description
        self.cover_image = cover_image
        self.language = language
        self.content_type = content_type
        self.gender_pref = gender_pref
        self.author = author
        self.created_at = created_at

    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, title, description, cover_image, language, content_type, gender_pref, author):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mangas (title, description, cover_image, language, content_type, gender_pref, author)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, cover_image, language, content_type, gender_pref, author))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @classmethod
    def get_all(cls):
        conn = cls.get_db_connection()
        mangas = conn.execute('SELECT * FROM mangas').fetchall()
        conn.close()
        return [dict(m) for m in mangas]

    @classmethod
    def get_by_id(cls, manga_id):
        conn = cls.get_db_connection()
        manga = conn.execute('SELECT * FROM mangas WHERE id = ?', (manga_id,)).fetchone()
        conn.close()
        return dict(manga) if manga else None

    @classmethod
    def search(cls, query):
        conn = cls.get_db_connection()
        mangas = conn.execute('SELECT * FROM mangas WHERE title LIKE ?', ('%' + query + '%',)).fetchall()
        conn.close()
        return [dict(m) for m in mangas]

    @classmethod
    def filter(cls, language=None, content_type=None, gender_pref=None):
        conn = cls.get_db_connection()
        query = 'SELECT * FROM mangas WHERE 1=1'
        params = []
        if language:
            query += ' AND language = ?'
            params.append(language)
        if content_type:
            query += ' AND content_type = ?'
            params.append(content_type)
        if gender_pref:
            query += ' AND gender_pref = ?'
            params.append(gender_pref)
        
        mangas = conn.execute(query, params).fetchall()
        conn.close()
        return [dict(m) for m in mangas]

    @classmethod
    def update(cls, manga_id, **kwargs):
        conn = cls.get_db_connection()
        keys = kwargs.keys()
        query = f"UPDATE mangas SET {', '.join([f'{k} = ?' for k in keys])} WHERE id = ?"
        params = list(kwargs.values()) + [manga_id]
        conn.execute(query, params)
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, manga_id):
        conn = cls.get_db_connection()
        conn.execute('DELETE FROM mangas WHERE id = ?', (manga_id,))
        conn.commit()
        conn.close()
