import numpy as np
import PySimpleGUI as sg
import cv2
from pathlib import Path

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

def file_read():
    '''
    ファイルを選択して読み込む
    '''
    fp = ""
    # GUIのレイアウト
    layout = [
        [
            sg.FileBrowse(key="file"),
            sg.Text("ファイル"),
            sg.InputText()
        ],
        [sg.Submit(key="submit"), sg.Cancel("Exit")]
    ]
    # WINDOWの生成
    # 全角文字が存在するとエラーになる->警告など、対処法を考える
    window = sg.Window("ファイル選択", layout)

    # イベントループ
    while True:
        event, values = window.read(timeout=100)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        elif event == 'submit':
            if values[0] == "":
                sg.popup("ファイルが入力されていません。")
                event = ""
            else:
                fp = values[0]
                break
    window.close()
    return Path(fp)

class Main:
    def __init__(self):
        self.fp=file_read()
        self.image=imread(str(self.fp))
        gaussian = cv2.GaussianBlur(self.image, ksize=(3,3), sigmaX=1.3)
        for i in range(10):
            gaussian = cv2.GaussianBlur(gaussian, ksize=(3,3), sigmaX=1.3)
        cv2.imwrite("Images/output/median.jpg", self.image)
        cv2.imwrite("Images/output/gaussian.jpg", gaussian)

if __name__=='__main__':
    Main()