from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    顯示註冊頁面或處理使用者註冊邏輯。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    顯示登入頁面或驗證使用者登入資訊。
    """
    pass

@auth_bp.route('/logout')
def logout():
    """
    處理使用者登出並清除 session。
    """
    pass
