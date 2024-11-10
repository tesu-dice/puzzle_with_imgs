import os
import re
import tkinter.filedialog #ファイル追加時に使用
import tkinter as tk

#対象フォルダの選択
def AddFile():
    global folder_path
    folder_path = tkinter.filedialog.askdirectory()
    update_UI("フォルダが指定されました。:")
    update_UI(folder_path)



#指定フォルダの古いファイルを削除
def delete_old_files():
    global folder_path
    if(folder_path ==None or folder_path ==""):
        update_UI("指定フォルダがありません。")
        return 
    # ファイル名のパターンにマッチさせる正規表現
    _pattern = re.compile(r"(.+?)\.(\w+)\.(\d+)$")

    # 各ファイル種別の最新ファイルを保持する辞書
    _latest_files = {}

    # フォルダ内のファイルを取得
    for filename in os.listdir(folder_path):
        match = _pattern.match(filename)
        if match:
            base_name = f"{match.group(1)}.{match.group(2)}"  # 拡張子までの部分
            version = int(match.group(3))  # 数値部分を整数に変換

            # 最新バージョンがなければ追加、または更新
            if base_name not in _latest_files or _latest_files[base_name][1] < version:
                # 既存の古いファイルがあれば削除
                if base_name in _latest_files:
                    old_file = _latest_files[base_name][0]
                    os.remove(os.path.join(folder_path, old_file))
                    update_UI(f"Deleted old file: {old_file}")
                
                # 最新のファイルを辞書に登録
                _latest_files[base_name] = (filename, version)
            else:
                # 最新でないファイルは削除
                os.remove(os.path.join(folder_path, filename))
                update_UI(f"Deleted old file: {filename}")

    update_UI("削除処理が完了しました。")
#UI関連

#ウィンドウの作成
def make_win(_w, _h):
    _win = tk.Tk()
    _win.title("sample")
    _win.config(background=backcolor)
    _win.geometry(str(_w)+"x"+str(_h)+"+200+100")
    _win.resizable(False, False)  # リサイズ不可に設定
    #win.attributes('-fullscreen', True)
    return _win

#UIの設置
def set_UI(_master):
    _UIs ={}#UI用のライブラリ
    
    #説明文1
    _exp1_text =    "1. [ フォルダの指定 ]ボタンから対象フォルダを指定してください。\n2. [ 実行 ]ボタンを押すと古いCAD用ファイルを削除します。\n3. 削除ファイルのログが表示されるので見たければどうぞ"
    _exp1_label = tk.Label(_master, text=_exp1_text, font=("メイリオ",12,"bold"), justify='left')
    _exp1_label.place(x=200, y=25);    _UIs["exp1_label"] = _exp1_label

    #ファイルの追加ボタン
    _AddFile_button = tk.Button(_master, text="フォルダの指定", font =myfont, command =(AddFile) ,width=10)
    _AddFile_button.place(x=50, y=20);     _UIs["AddFileButton"] = _AddFile_button
    #実行ボタン
    _act_button = tk.Button(_master, text="実行", font =myfont, command =(delete_old_files) ,width=10)
    _act_button.place(x=50, y=70);   _UIs["AddFileButton"] = _AddFile_button

    #メッセージ用テキストボックス
    # メッセージ用のフレームを作成し、その中にTextとScrollbarを配置
    frame = tk.Frame(_master, width=100, height=20)
    frame.place(x=50, y=120)
    
    # メッセージ用のテキストボックス
    message_text = tk.Text(frame, wrap="word", width=100, height=20)
    message_text.configure(state="disabled")  # 編集不可に設定
    message_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    _UIs["message_text"] = message_text

    # 縦スクロールバー
    bar_vertical_scroll = tk.Scrollbar(frame, orient=tk.VERTICAL, command=message_text.yview)
    bar_vertical_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    message_text["yscrollcommand"] = bar_vertical_scroll.set

    return _UIs


def update_UI(_message=""):
    if(_message != ""):
        #UI_objects["message_text"].insert(tk.END , _message + "\n")

        # 編集可能に設定
        UI_objects["message_text"].configure(state="normal")
        
        # メッセージを追加して改行
        UI_objects["message_text"].insert("end", _message + "\n")
        
        # 最新メッセージが表示されるようにスクロール
        UI_objects["message_text"].see("end")
        
        # 再び編集不可に設定
        UI_objects["message_text"].configure(state="disabled")


    #root.after(500,update_UI) #一度始めたら1秒ごとに繰り返すように設定


#main処理-------------------------------------------
    #変数定義
win_w , win_h = 800, 400
myfont = ("メイリオ",10,"bold")
backcolor="#a0a0a0"
folder_path = ""

    #関数実行
root = make_win(win_w, win_h)
UI_objects = set_UI(root)

update_UI()
root.mainloop()

