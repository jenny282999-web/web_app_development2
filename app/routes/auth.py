from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.user import UserModel

auth_bp = Blueprint('auth', __name__)
user_model = UserModel()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    顯示註冊頁面或處理使用者註冊邏輯。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # 基本驗證
        if not username or not email or not password:
            flash('請填寫所有欄位', 'error')
            return render_template('auth/register.html')

        # 檢查使用者是否已存在
        if user_model.get_by_username(username):
            flash('此使用者名稱已被使用', 'error')
            return render_template('auth/register.html')

        # 建立使用者 (此處暫用明文，建議後續加入雜湊)
        user_id = user_model.create(username, email, password)
        if user_id:
            flash('註冊成功！請登入', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('註冊失敗，請稍後再試', 'error')

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    顯示登入頁面或驗證使用者登入資訊。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('請輸入帳號與密碼', 'error')
            return render_template('auth/login.html')

        user = user_model.get_by_username(username)
        if user and user['password_hash'] == password: # 簡易驗證
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'歡迎回來，{username}！', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('帳號或密碼錯誤', 'error')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """
    處理使用者登出並清除 session。
    """
    session.clear()
    flash('你已成功登出', 'info')
    return redirect(url_for('main.index'))

