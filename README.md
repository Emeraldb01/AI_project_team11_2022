# AI_project_team11_2022

## Requirements

Python版本：3.9.13

使用前需要先安裝module：
```
pip install -r requirements.txt
```

在requirements.txt中，只有放執行app.py所需的module。

## 使用方法

範例:

```
python app.py --video_source ./video.mp4 --output_frame 5
```

--video_souce <影片位置>: 若沒有指定arg，則使用電腦鏡頭

--output_frame <想要每幾幀輸出一個手勢>: 若沒有指定arg，則每一幀都輸出

過程中若要退出，在視窗中按下Esc即可

## 輸出

結果將會記錄到"./result.csv"內，格式範例為

```
L: 5 5 4 X N N
R: 4 4 0 0 0 X
```

## 結果解釋

開頭L及R代表左或右手。

可能的結果有5種，{5, 4, 0, N, X}，代表的意思為:

* 5：辨認出5

* 4：辨認出4

* 0：辨認出0

* N：非5, 4, 0的其他手勢

* X：該隻手並沒有出現在影像內

## Training

若要使用Google Colab進行Training，請將該資料夾上傳至Google Drive。

開啟`keypoint_classification_EN.ipynb`後，僅需在Runtime中按下`Restart and run all`，即可進行Training。