#!/usr/bin/env python3
import os
import time
import psutil
import json
import configparser
from datetime import datetime

# デフォルト設定
DEFAULT_CONFIG = {
    "dummy_size_gb": 4,
    "check_interval": 1,
    "chunk_mb": 100,
    "emergency_threshold": 0.90,
    "log_enabled": True,
    "log_dir": "/var/log/dynamic-dummy-mem",
    "status_path": "/var/log/dynamic-dummy-mem/status.json"
}

CONFIG_PATH = "/etc/dynamic-dummy-mem/config.ini"

# 設定読み込み
def load_config(path):
    cfg = DEFAULT_CONFIG.copy()
    parser = configparser.ConfigParser()
    if os.path.exists(path):
        parser.read(path)
        section = parser["dynamic-dummy-mem"] if "dynamic-dummy-mem" in parser else parser["DEFAULT"]
        for k in cfg:
            if k in section:
                v = section[k]
                if isinstance(DEFAULT_CONFIG[k], bool):
                    cfg[k] = v.lower() in ("yes","true","1")
                elif isinstance(DEFAULT_CONFIG[k], int):
                    cfg[k] = int(v)
                elif isinstance(DEFAULT_CONFIG[k], float):
                    cfg[k] = float(v)
                else:
                    cfg[k] = v
    return cfg

def log_event(msg, log_dir, log_enabled=True):
    if not log_enabled: return
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, "dummy_mem.log"), "a") as f:
        f.write(f"[{now}] {msg}\n")

def total_dummy_gb(dummy_chunks, chunk_mb):
    return len(dummy_chunks) * chunk_mb / 1024

def alloc_chunks(dummy_chunks, chunk_mb, num):
    for _ in range(num):
        dummy_chunks.append(bytearray(chunk_mb * 1024 * 1024))

def free_chunks(dummy_chunks, num):
    for _ in range(num):
        if dummy_chunks:
            dummy_chunks.pop()

def get_my_memory_gb():
    proc = psutil.Process(os.getpid())
    mem = proc.memory_info().rss / (1024 ** 3)
    return mem

def emergency_release(dummy_chunks):
    if dummy_chunks:
        print("!!! EMERGENCY: Releasing ALL dummy memory!")
        dummy_chunks.clear()

def save_status_json(status, status_path):
    os.makedirs(os.path.dirname(status_path), exist_ok=True)
    with open(status_path, "w") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)

def main():
    cfg = load_config(CONFIG_PATH)
    dummy_size_gb = cfg["dummy_size_gb"]
    check_interval = cfg["check_interval"]
    chunk_mb = cfg["chunk_mb"]
    emergency_threshold = cfg["emergency_threshold"]
    log_enabled = cfg["log_enabled"]
    log_dir = cfg["log_dir"]
    status_path = cfg["status_path"]

    dummy_chunks = []
    last_dummy = 0

    while True:
        mem = psutil.virtual_memory()
        used_gb = (mem.total - mem.available) / (1024 ** 3)
        my_gb = get_my_memory_gb()
        other_used_gb = used_gb - my_gb
        need_dummy = max(0, dummy_size_gb - other_used_gb)
        curr_dummy = total_dummy_gb(dummy_chunks, chunk_mb)
        diff_gb = need_dummy - curr_dummy

        # ステータスjson出力
        status = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_memory_gb": round(mem.total / (1024 ** 3), 2),
            "used_gb": round(used_gb, 2),
            "dummy_gb": round(curr_dummy, 2),
            "other_gb": round(other_used_gb, 2),
            "percent": round(mem.percent, 1)
        }
        save_status_json(status, status_path)

        # コンソール表示（任意：systemd時は消す）
        os.system('clear')
        print(f"=== ダミーメモリ監視 ===")
        print(f"合計メモリ        : {status['total_memory_gb']} GB")
        print(f"現在の使用量      : {status['used_gb']} GB")
        print(f"他プロセスの使用  : {status['other_gb']} GB")
        print(f"ダミー確保        : {status['dummy_gb']} GB")
        print(f"使用率            : {status['percent']} %")
        print(f"(次回チェックまで {check_interval} 秒)")

        # 非常時解放
        if mem.percent > emergency_threshold * 100:
            emergency_release(dummy_chunks)
            log_event("!!! EMERGENCY: Releasing ALL dummy memory!", log_dir, log_enabled)
        else:
            chunk_diff = int(diff_gb * 1024 / chunk_mb)
            if chunk_diff > 0:
                alloc_chunks(dummy_chunks, chunk_mb, chunk_diff)
            elif chunk_diff < 0:
                free_chunks(dummy_chunks, -chunk_diff)

        # ダミー量変化時のみログ
        if abs(curr_dummy - last_dummy) > 0.05:
            log_event(f"ダミー確保を {curr_dummy:.2f} GB に調整", log_dir, log_enabled)
            last_dummy = curr_dummy

        time.sleep(check_interval)

if __name__ == "__main__":
    main()
