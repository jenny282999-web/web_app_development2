from flask import Blueprint, render_template, request, redirect, url_for

comic_bp = Blueprint('comic', __name__)

@comic_bp.route('/<int:id>')
def detail(id):
    """
    顯示漫畫詳情頁面，包含標籤與評論。
    """
    pass

@comic_bp.route('/<int:id>/comment', methods=['POST'])
def add_comment(id):
    """
    為指定漫畫發表評論與雷點標籤。
    """
    pass
