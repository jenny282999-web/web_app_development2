from app import create_app, init_db
import sys

app = create_app()

if __name__ == '__main__':
    # 如果有命令列參數 'init'，則初始化資料庫
    if len(sys.argv) > 1 and sys.argv[1] == 'init':
        with app.app_context():
            init_db()
            print("資料庫初始化完成。")
    else:
        app.run(debug=True)
