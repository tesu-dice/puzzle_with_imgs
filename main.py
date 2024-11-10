"""
#更新履歴
20240920    とりあえずのパズル機能実装
20241003    パズルをウィンドウの中心に配置、完成したら枠線を削除
20241021    指定ファイルをポップアップから追加できるように変更。


#仕様
済  パズルとしての機能
済  指定フォルダから複数の画像を取り込んで選べる機能
済  ファイルの指定をGUIからポップアップでできるようにする。


#今実装中の機能に関するメモ
ラベル及びコンボボックスの準備、初期値は一番最初のファイルにする。





"""


import tkinter as tk #GUIの作成
import tkinter.ttk as ttk #コンボボックスの表示
import tkinter.filedialog #ファイル追加時に使用
import tkinter.messagebox
from PIL import Image, ImageTk #画像のサイズ変更
import pyautogui #画面サイズの統一で必要
import os #ファイルの読み込み
import random #シャッフルで利用





#スクリーンのサイズを取得
def get_ScreenSize():
    return pyautogui.size()



#menu選択

    #引数フォルダのpng,jpgファイルをすべて読み込み、ファイル名：パスの辞書で返す
    #           game\images\ -> hogehoge: images\hogehoge の辞書
def read_imglist(_folder_path):
    #ファイルの読み込み
    _img_dict ={}
    for file in os.listdir(_folder_path):
        if file.endswith(".png") or file.endswith(".jpg"):
            _img_dict[os.path.os.path.basename(file)] = os.path.join(_folder_path, file)
    print(_img_dict)
    return _img_dict

#入力用の欄設置
def set_inputs(_objects = {}):
    
    #ラベル
    _w_label = tk.Label(root, text="横の分割数", font=myfont)
    _h_label = tk.Label(root, text="縦の分割数", font=myfont)
    _file_label = tk.Label(root, text="ファイル名", font=myfont)
        #配置/ 辞書に追加
    _w_label.place(x=10, y=10);     _objects["W_label"] = _w_label
    _h_label.place(x=300, y=10);    _objects["H_label"] = _h_label
    _file_label.place(x=600, y=10); _objects["F_label"] = _file_label

    #コンボボックス
    _cb_w_get = ttk.Combobox(root, values=[1,2,3,4,5,6,7], width=5, height=10, font= myfont)
    _cb_h_get = ttk.Combobox(root, values=[1,2,3,4,5,6,7], width=5, height=10, font=myfont)
    _cb_file_labels = list( imgdict.keys() )
    _cb_file_get = ttk.Combobox(root, values=_cb_file_labels, height=10, font=myfont)
        #配置と初期設定 / 辞書に追加
    _cb_w_get.place(x=120, y=10); _cb_h_get.place(x=410, y=10); _cb_file_get.place(x=710, y=10)
    _cb_w_get.set(4); _cb_h_get.set(4); _cb_file_get.set( _cb_file_labels[-1])
    _objects["横分割入力"] = _cb_w_get; _objects["縦分割入力"] = _cb_h_get; _objects["ファイル入力"]=_cb_file_get
        #イベントの設定
    _cb_w_get.bind("<<ComboboxSelected>>", update_sample)  # イベントをバインド
    _cb_h_get.bind("<<ComboboxSelected>>", update_sample)  # イベントをバインド
    _cb_file_get.bind("<<ComboboxSelected>>", update_sample)  # イベントをバインド
    
    #ファイルの追加ボタン
    _AddFile_button = tk.Button(root, text="ファイルの追加", font =myfont, command =(AddImageFile) )
        #配置と辞書に追加
    _AddFile_button.place(x=1100, y=0);   _objects["AddFileButton"] = _AddFile_button
    #開始ボタン
    _start_button = tk.Button(root, text="start", font=myfont, command= puzzlestart)
        #配置と辞書に追加
    _start_button.place(x=1600, y=0);   _objects["StartButon"] = _start_button


    return _objects

def AddImageFile():
    _filetypes =[("すべての対応ファイル","*jpg;*.jpeg;*png"),
                 ("JPEG形式", "*.jpg;*.jpeg;"),
                 ("PNG形式","*.png")]
    _target_path = tkinter.filedialog.askopenfilename(filetypes=_filetypes)
    if _target_path == "":#ファイル指定に失敗したとき
        return
    #画像ファイルの追加処理
    global imgdict
    if(_target_path.split("/")[-1] in imgdict):
        imgdict.pop(_target_path.split("/")[-1])
    imgdict[_target_path.split("/")[-1]] = _target_path
    

    clear_inputs()
    set_inputs()
    update_sample()
    

def update_sample(event =None):
    _f = imgdict[input_objects["ファイル入力"].get()]
    _w = input_objects["横分割入力"].get()
    _h = input_objects["縦分割入力"].get()
    print(_f, _w, _h)
    clear_labels()
    split_img(_f, _w, _h)

# 既存のラベルを削除する関数
def clear_labels():
    for widget in frame.winfo_children():
        widget.destroy()

#
def clear_inputs():
    # コンボボックスとスタートボタンを削除
    for widget in input_objects.values():
        widget.destroy()

def puzzlestart():
    update_sample()
    #ピースをランダムにシャッフル
    global puzzle
    puzzle = shuffle_pieces(puzzle)
    clear_inputs()
    global puzzlestate
    puzzlestate = True












#デバックを表示
def print_debug(list):
    return
    if(list == "start"):
        labels =[]
        for i in range( 5 ):        #表示したいラベルの数だけ作る
            labels.append(tk.Label())
            labels[i].place(x=50, y=50*i)
        root.after(1000, print_debug(labels))
    else:
        list[0]["text"] = get_ScreenSize()
        list[1]["text"] = root.geometry()
        list[2]["text"] = root.winfo_screenwidth()
        list[3]["text"] = root.winfo_screenheight()
        root.after(1000, lambda: print_debug(list))

#PILで画像を分割して2次配列の辞書として返す
# str:ファイルパス, int:分割数2つ -> 分割した画像群の辞書
def split_img(_img_path, _width_int=5, _height_int=5 ):
    _width_int = int(_width_int); _height_int = int(_height_int) #int型にキャスト
    if (int(_width_int) < 1 or int(_height_int) < 1 or img ==None):#例外処理
        return
    _i = read_img(_img_path)
    _splited_img = [[] for _ in range(_height_int)]  #二次配列に画像と初期位置の辞書を記憶
    piece_width = _i.width / _width_int
    piece_height = _i.height / _height_int
    for i in range(_height_int):
        for j in range(_width_int):
            #ピースを追加
            clip = _i.crop((j*piece_width, i*piece_height, (j+1)*piece_width, (i+1)*piece_height))
            new = {"img": clip, "n_h": i, "n_w": j, "correct": False, "relief": "solid","border": 5}  # 画像、正しい位置、正解フラグ、リリーフタイプ
            _splited_img[i].append(new)
    
    global puzzle
    puzzle = _splited_img  # 生成されたパズルをグローバル変数に代入
    set_labels(puzzle)  # パズルをセットして表示

    return puzzle

#2次配列の辞書リストからパネル配置
def set_labels(_p, complete=False):
    clear_labels()
    print_pieces(_p)
    for i in range(len(_p)):
        for j in range(len(_p[0])):
            # reliefの状態に応じて変更
            relief_style = _p[i][j]["relief"]
            ij_image = ImageTk.PhotoImage(_p[i][j]["img"])

            label = tk.Label(frame, image=ij_image, relief=relief_style, border=_p[i][j]["border"])
            label.image = ij_image
            label.grid(row=i, column=j)
            if not _p[i][j]["correct"]:  # 正解のピースは動かせないようにする
                label.bind("<Button-1>", lambda event, r=i, c=j: swap_pieces(event, r, c, _p))  # クリックイベントをバインド
            else:
                # 正しい位置にあるピースはバインドを解除する
                label.unbind("<Button-1>")

# ピース（辞書の二次配列）をランダムにシャッフルする関数
def shuffle_pieces(_p):
    flat_list = [item for sublist in _p for item in sublist]
    random.shuffle(flat_list)
    
    shuffled_puzzle = [[] for _ in range(len(_p))]
    idx = 0
    for i in range(len(_p)):
        for j in range(len(_p[0])):
            shuffled_puzzle[i].append(flat_list[idx])
            idx += 1
    
    set_labels(shuffled_puzzle)
    return shuffled_puzzle

# ピースの配置が正しいかを判定する関数
def check_correct(_p):
    all_correct = True
    for i in range(len(_p)):
        for j in range(len(_p[0])):
            if _p[i][j]["n_h"] == i and _p[i][j]["n_w"] == j:
                _p[i][j]["correct"] = True
                _p[i][j]["relief"] = "flat"  # 正しいピースはフラットにする
                _p[i][j]["border"] = 0
            else:
                _p[i][j]["correct"] = False
                _p[i][j]["relief"] = "solid"  # 間違っているピースはソリッドにする
                all_correct = False
    set_labels(_p)
    return all_correct

#クリックしたラベルを入れ替える関数
first_click = None
def swap_pieces(event, row, col, _p):
    if not puzzlestate:  # puzzlestateがFalseなら操作を無効化
        return

    global first_click
    if first_click is None:
        # 最初にクリックしたピースを保存
        first_click = (row, col)
        highlight_piece(row, col, _p, highlight=True)  # ピースを浮き上がらせる
    else:
        # 2回目にクリックしたピースと交換
        r1, c1 = first_click
        r2, c2 = row, col

        # 入れ替え処理
        _p[r1][c1], _p[r2][c2] = _p[r2][c2], _p[r1][c1]
        
        # 再度ラベルを表示
        set_labels(_p)
        
        # 正しいか判定
        if check_correct(_p):
            set_labels(_p, True)
            display_completion_message()  # パズル完成時にメッセージを表示
        
        first_click = None  # リセット

# ピースの浮き上がりを制御する関数
def highlight_piece(row, col, _p, highlight=False):
    if highlight:
        _p[row][col]["relief"] = "raised"  # ピースを浮き上がらせる
    else:
        _p[row][col]["relief"] = "solid"  # 通常のピースに戻す
    set_labels(_p)

# パズル完成時にメッセージを表示する関数
def display_completion_message():
    tkinter.messagebox.showinfo("パズル完成","Good Job!!!")

#各ピースのステータスを確認する関数
def print_pieces(p):
    return 
    for i in range(len(p)):
        for j in range(len(p[0])):
            print(puzzle[i][j],end=" , ")
            if(puzzle[i][j].get("label")):
                print(puzzle[i][j]["label"]["border"])



#ウィンドウの作成
def make_win(_w=1800,_h=1000):
    _win = tk.Tk()
    _win.title("sample")
    _win.config(background="#a0a0a0")
    _win.geometry(str(_w)+"x"+str(_h)+"+200+100")
    _win.resizable(False, False)  # リサイズ不可に設定
    #win.attributes('-fullscreen', True)
    return _win


#引数のパスの画像ファイルのサイズを収まるように変更して返す
def read_img(filepath, w=1700, h=900):
    w -= 100; h -= 100
    if filepath =="":
        return
    _img = Image.open(filepath)



    #画像のリサイズ
    img_w , img_h = _img.size
    _img = _img.resize((w, int(img_h * w/ img_w) ))#横幅を1600に
    if(_img.size[1] > h):#高さが大きくなりすぎたなら縮小
        _img = _img.resize(( int(img_w * h/ img_h), h))


    """
    while(1):
        img_w , img_h = _img.size
        print("read_img()", _img.size)

        if(img_w > w ):
            _img = _img.resize((w, int(img_h * w/ img_w) ))
        elif(img_h > h):
            
        if(img_h > h):#横幅補正しても縦幅がオーバーの時
            _img = _img.resize(( int(img_w * h/ img_h), h))
        #サイズチェック
        if(_img.size[0]< w+100 and _img.size[1] < h+100):
            break
    """
    return _img


#main
    #変数定義
win_w , win_h = 1800, 1000
myfont = ("メイリオ",10,"bold")
backcolor="#a0a0a0"
puzzlestate = False #パズルの状態
puzzle = {} #パズルピースの辞書
l_w, l_h = 0, 0


    #関数実行
root = make_win(win_w, win_h)
    #フレームを作成して中央に配置
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


imgdict = read_imglist("imgs")
input_objects = set_inputs()
#画像を分割
print("debug")
print(imgdict[input_objects["ファイル入力"].get()])
img = read_img(imgdict[input_objects["ファイル入力"].get()],win_w, win_h)
puzzle = split_img(imgdict[input_objects["ファイル入力"].get()], input_objects["横分割入力"].get(), input_objects["縦分割入力"].get())


#デバック用テキスト出力
print_debug("start")





#メインループ
root.mainloop()
