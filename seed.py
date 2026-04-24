import sqlite3
import os

db_path = 'instance/database.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Insert dummy comics
comics = [
    ('葬送的芙莉蓮', '山田鐘人 / 阿部司', '打倒魔王之後的故事。', 'https://upload.wikimedia.org/wikipedia/zh/thumb/3/30/Sousou_no_Frieren_volume_1.jpg/220px-Sousou_no_Frieren_volume_1.jpg'),
    ('我推的孩子', '赤坂明 / 橫槍萌果', '演藝圈的暗部與轉生。', 'https://upload.wikimedia.org/wikipedia/zh/thumb/d/d6/Oshi_no_Ko_Volume_1.jpg/220px-Oshi_no_Ko_Volume_1.jpg'),
    ('SPY×FAMILY 間諜家家酒', '遠藤達哉', '間諜、殺手與超能力者的家庭喜劇。', 'https://upload.wikimedia.org/wikipedia/zh/thumb/1/1b/Spy_x_Family_Volume_1.jpg/220px-Spy_x_Family_Volume_1.jpg'),
    ('藍色監獄', '金城宗幸 / 諾村優介', '為了誕生世界第一前鋒的計畫。', 'https://upload.wikimedia.org/wikipedia/zh/thumb/0/05/Blue_Lock_Volume_1.jpg/220px-Blue_Lock_Volume_1.jpg')
]

cursor.executemany(
    "INSERT INTO comics (title, author, description, cover_url) VALUES (?, ?, ?, ?)",
    comics
)

conn.commit()
conn.close()
print("測試數據注入完成。")
