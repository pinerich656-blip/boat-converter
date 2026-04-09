import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

def get_all_races_tamano(place_code="01"):
    today = datetime.now().strftime("%Y%m%d")
    print(f"--- {today} 玉野競輪 全レースデータ作成開始 ---")
    
    all_data = {}
    
    # 1Rから12Rまでループ
    for race_num in range(1, 13):
        race_key = str(race_num)
        print(f"第{race_key}レースのデータを生成中...")
        
        # 本格的なスクレイピング・ロジックの土台
        # 将来的にはここで各レースの個別URL（netkeirin等）を叩く
        race_players = []
        for car_id in range(1, 10):
            # テスト用にレース毎・車番毎に少しずつ違う得点を作るロジック
            # レース番号(race_num)と車番(car_id)を計算に入れて「変化」を見やすくしたよ
            base_score = 85.0 + (race_num * 0.5) 
            adjustment = (car_id * 1.2)
            
            race_players.append({
                "id": car_id,
                "s": round(base_score + adjustment, 1),
                "n": f"玉野{race_key}R {car_id}番車"
            })
        
        all_data[race_key] = race_players
        
        # 連続アクセスで負荷をかけないための待機（本物サイトを叩く時用）
        # time.sleep(0.5) 

    # 12レース分まとまったデータを保存
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"--- 全12レースの data.json 書き出し完了 ---")

if __name__ == "__main__":
    # 玉野(01)を指定して実行
    get_all_races_tamano("01")
