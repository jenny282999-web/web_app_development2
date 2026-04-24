from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.progress import ProgressModel

library_bp = Blueprint('library', __name__)
progress_model = ProgressModel()

@library_bp.route('/')
def index():
    """
    顯示使用者的個人跨平台書櫃列表。
    """
    user_id = session.get('user_id')
    if not user_id:
        flash('請先登入以查看書櫃', 'warning')
        return redirect(url_for('auth.login'))
        
    library = progress_model.get_user_library(user_id)
    return render_template('library/index.html', library=library)

@library_bp.route('/add', methods=['POST'])
def add():
    """
    將指定漫畫加入個人書櫃。
    """
    user_id = session.get('user_id')
    comic_id = request.form.get('comic_id')
    platform = request.form.get('platform', 'Webtoon')
    
    if not user_id:
        flash('請先登入', 'warning')
        return redirect(url_for('auth.login'))
        
    res = progress_model.create_or_update(user_id, int(comic_id), platform=platform)
    if res:
        flash('已成功加入書櫃', 'success')
    return redirect(url_for('library.index'))

@library_bp.route('/update', methods=['POST'])
def update():
    """
    更新閱讀進度、狀態或平台資訊。
    """
    user_id = session.get('user_id')
    comic_id = request.form.get('comic_id')
    chapter = request.form.get('chapter')
    status = request.form.get('status')
    platform = request.form.get('platform')
    
    if user_id:
        progress_model.create_or_update(
            user_id, int(comic_id), 
            current_chapter=chapter, 
            status=status, 
            platform=platform
        )
        flash('進度已更新', 'success')
    return redirect(url_for('library.index'))

@library_bp.route('/delete', methods=['POST'])
def delete():
    """
    從書櫃中移除指定的漫畫紀錄。
    """
    progress_id = request.form.get('progress_id')
    if progress_model.delete(int(progress_id)):
        flash('已從書櫃移除', 'info')
    return redirect(url_for('library.index'))

