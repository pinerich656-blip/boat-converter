import requests
import json
import time
from datetime import datetime

def get_all_active_stadiums():
    # 本来はここで「今日の開催一覧ページ」をスクレイピングする
    # 今回は例として、今日開催の可能性がある場を複数リストアップ
    # ※本物にする際はここを自動取得に変更します
    active_stadiums = {
        "01": "玉野",
        "71": "松山",
        "81": "小倉",
        "42": "大垣"
    }
    
    master_data = {}

    for code, name in active_stadiums.items():
        print(f"【{name}】データを収集中...")
        stadium_races = {}
        
        for r in range(1, 13):
            race_players = []
            for i in range(1, 10):
                # 場名とレース番号がわかるように名前を生成
                race_players.append({
                    "id": i,
                    "s": round(80.0 + (int(code)*0.1) + r + i, 1),
                    "n": f"{name}{r}R {i}番車"
                })
            stadium_races[str(r)] = race_players
        
        master_data[name] = stadium_races
        time.sleep(0.1) # サーバーに優しく

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(master_data, f, ensure_ascii=False, indent=2)
    print("全場データのパッキングが完了しました！")

if __name__ == "__main__":
    get_all_active_stadiums()
