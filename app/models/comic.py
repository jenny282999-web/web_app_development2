import sqlite3

class ComicModel:
    def __init__(self, db_path='instance/database.db'):
        self.db_path = db_path

    def _get_connection(self):
        """建立資料庫連線並設定 row_factory。"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, title, author, description=None, cover_url=None):
        """新增一筆漫畫作品。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO comics (title, author, description, cover_url) VALUES (?, ?, ?, ?)",
                (title, author, description, cover_url)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating comic: {e}")
            return None
        finally:
            conn.close()

    def get_all(self):
        """取得所有漫畫作品。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM comics")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching comics: {e}")
            return []
        finally:
            conn.close()

    def get_by_id(self, comic_id):
        """根據 ID 取得單筆漫畫。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM comics WHERE id = ?", (comic_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error fetching comic by id: {e}")
            return None
        finally:
            conn.close()

    def get_by_tag(self, tag_name):
        """根據標籤名稱取得所有相關漫畫。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            query = """
                SELECT c.* FROM comics c
                JOIN comic_tags ct ON c.id = ct.comic_id
                JOIN tags t ON ct.tag_id = t.id
                WHERE t.name = ?
            """
            cursor.execute(query, (tag_name,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching comics by tag: {e}")
            return []
        finally:
            conn.close()

    def update(self, comic_id, title=None, author=None, description=None, cover_url=None):
        """更新漫畫作品資料。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
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
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating comic: {e}")
            return False
        finally:
            conn.close()

    def delete(self, comic_id):
        """刪除指定漫畫。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM comics WHERE id = ?", (comic_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting comic: {e}")
            return False
        finally:
            conn.close()

