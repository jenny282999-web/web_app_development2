from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    系統首頁，顯示熱門漫畫與情緒推薦入口。
    """
    pass
