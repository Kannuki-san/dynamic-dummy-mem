#!/usr/bin/env python3
import json
import os

STATUS_PATH = "/var/log/dynamic-dummy-mem/status.json"

def main():
    if os.path.exists(STATUS_PATH):
        with open(STATUS_PATH) as f:
            s = json.load(f)
        print("=== ダミーメモリ監視状況 ===")
        print(f"時刻              : {s['timestamp']}")
        print(f"合計メモリ        : {s['total_memory_gb']} GB")
        print(f"現在の使用量      : {s['used_gb']:.2f} GB")
        print(f"ダミー確保        : {s['dummy_gb']:.2f} GB")
        print(f"他プロセスの使用  : {s['other_gb']:.2f} GB")
        print(f"使用率            : {s['percent']:.1f} %")
    else:
        print("ステータスファイルが見つかりません")

if __name__ == "__main__":
    main()
