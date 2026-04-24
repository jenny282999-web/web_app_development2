import sqlite3
from datetime import datetime

class UserModel:
    def __init__(self, db_path='instance/database.db'):
        self.db_path = db_path

    def _get_connection(self):
        """建立資料庫連線並設定 row_factory。"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, username, email, password_hash):
        """新增一筆使用者記錄。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Error creating user: {e}")
            return None
        finally:
            conn.close()

    def get_all(self):
        """取得所有使用者。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching users: {e}")
            return []
        finally:
            conn.close()

    def get_by_id(self, user_id):
        """根據 ID 取得單筆使用者。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error fetching user by id: {e}")
            return None
        finally:
            conn.close()

    def get_by_username(self, username):
        """根據使用者名稱取得使用者。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error fetching user by username: {e}")
            return None
        finally:
            conn.close()

    def update(self, user_id, email=None, password_hash=None):
        """更新使用者資料。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            if email:
                cursor.execute("UPDATE users SET email = ? WHERE id = ?", (email, user_id))
            if password_hash:
                cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating user: {e}")
            return False
        finally:
            conn.close()

    def delete(self, user_id):
        """刪除指定使用者。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")
            return False
        finally:
            conn.close()

