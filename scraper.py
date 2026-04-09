import requests
from bs4 import BeautifulSoup
import json
import time

def get_all_races(place_code="01"):
    all_data = {}
    
    for race_num in range(1, 13):
        print(f"{race_num}Rを取得中...")
        # 本来はここで各レースのURLにアクセス
        # 取得できたと仮定したシミュレーションデータを入れるよ
        race_players = []
        for i in range(1, 10):
            race_players.append({
                "id": i,
                "s": 80.0 + (race_num * 0.5) + i, # レース毎に変える
                "n": f"玉野 {race_num}R {i}番車"
            })
        all_data[str(race_num)] = race_players
        time.sleep(1) # サイトに負荷をかけないためのマナー

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_all_races("01")
