from flask import Blueprint, render_template, request, redirect, url_for, flash, session

library_bp = Blueprint('library', __name__)

@library_bp.route('/')
def index():
    """
    顯示使用者的個人跨平台書櫃列表。
    """
    pass

@library_bp.route('/add', methods=['POST'])
def add():
    """
    將指定漫畫加入個人書櫃。
    """
    pass

@library_bp.route('/update', methods=['POST'])
def update():
    """
    更新閱讀進度、狀態或平台資訊。
    """
    pass

@library_bp.route('/delete', methods=['POST'])
def delete():
    """
    從書櫃中移除指定的漫畫紀錄。
    """
    pass
