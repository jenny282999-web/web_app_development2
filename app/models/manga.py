import sqlite3
import os

DATABASE = os.path.join('instance', 'database.db')

class Manga:
    """
    漫畫模型：負責處理漫畫基本資訊的 CRUD 與篩選邏輯。
    """
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
        """
        建立並傳回資料庫連線。
        """
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, title, description, cover_image, language, content_type, gender_pref, author):
        """
        新增一筆漫畫記錄。
        """
        try:
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
        except Exception as e:
            print(f"Error creating manga: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有漫畫記錄。
        """
        try:
            conn = cls.get_db_connection()
            mangas = conn.execute('SELECT * FROM mangas').fetchall()
            conn.close()
            return [dict(m) for m in mangas]
        except Exception as e:
            print(f"Error fetching all mangas: {e}")
            return []

    @classmethod
    def get_by_id(cls, manga_id):
        """
        根據 ID 取得單筆漫畫記錄。
        """
        try:
            conn = cls.get_db_connection()
            manga = conn.execute('SELECT * FROM mangas WHERE id = ?', (manga_id,)).fetchone()
            conn.close()
            return dict(manga) if manga else None
        except Exception as e:
            print(f"Error fetching manga by id {manga_id}: {e}")
            return None

    @classmethod
    def search(cls, query):
        """
        根據書名關鍵字搜尋漫畫。
        """
        try:
            conn = cls.get_db_connection()
            mangas = conn.execute('SELECT * FROM mangas WHERE title LIKE ?', ('%' + query + '%',)).fetchall()
            conn.close()
            return [dict(m) for m in mangas]
        except Exception as e:
            print(f"Error searching mangas with query '{query}': {e}")
            return []

    @classmethod
    def filter(cls, language=None, content_type=None, gender_pref=None):
        """
        根據分類條件篩選漫畫。
        """
        try:
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
        except Exception as e:
            print(f"Error filtering mangas: {e}")
            return []

    @classmethod
    def update(cls, manga_id, **kwargs):
        """
        更新漫畫資訊。
        """
        try:
            conn = cls.get_db_connection()
            keys = kwargs.keys()
            query = f"UPDATE mangas SET {', '.join([f'{k} = ?' for k in keys])} WHERE id = ?"
            params = list(kwargs.values()) + [manga_id]
            conn.execute(query, params)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating manga {manga_id}: {e}")
            return False

    @classmethod
    def delete(cls, manga_id):
        """
        刪除漫畫記錄。
        """
        try:
            conn = cls.get_db_connection()
            conn.execute('DELETE FROM mangas WHERE id = ?', (manga_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting manga {manga_id}: {e}")
            return False
