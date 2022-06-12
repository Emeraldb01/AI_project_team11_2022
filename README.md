# AI_project_team11_2022

## Requirements

Python版本：3.9.13

使用前需要先安裝module：
```
pip install -r requirements.txt
```

## 檔案說明
### app.py

可使用前鏡頭或單一影片進行測試，在執行過程中會有視窗畫面，可以即時了解當前所辨認之手勢。

---
### app_for_testing.py
一次對整個資料夾的影片進行測試，執行過程為了節省效能，不會有額外的視窗畫面。


---
### test.py
使用整支影片所判斷出的個別手勢資訊（array of 5, 4, 0, N），判斷是否包含連續的540手勢，會被app及app_for_test呼叫

---
### 10_sec_yes
test data: 10秒且有540手勢之影片共四十部

---
### 10_sec_no
test data: 10秒且沒有540手勢之影片共四十部

## 使用方法
### app.py
範例:

```
python app.py --video_source ./video.mp4 --output_frame 5
```

* --video_source <影片位置>: 若沒有指定arg，則使用電腦鏡頭

* --output_frame <想要每幾幀紀錄一個手勢>: 若沒有指定arg，則每五幀紀錄一幀

過程中若要退出，在視窗中按下Esc即可

---

### app_for_testing.py
範例:

```
python app_for_testing.py --video_dir 10_sec_no
```

* --video_dir <包含影片的資料夾位置>: 資料夾的名稱最後一定要標明 yes 或是 no，如同範例所寫的格式。

* --output_frame <想要每幾幀紀錄一個手勢>: 若沒有指定arg，則每五幀紀錄一幀

### baseline.ipynb
用dataset train兩個baseline model，並輸出各手勢分別正確率及整體正確率

將整個project folder upload至google drive，由內打開該檔案，應可以直接執行
或是至 AI_project_team11_2022/model/keypoint_classifier/ 中，下載"keypoint.csv"並上傳至drive，更改cell 2之路徑，即可執行


## 輸出
### app.py
範例：
```
Result = Y
```
說明:
* Result的結果只會有2種，{Y, N}，代表的意思為：
    - Y: 有偵測出5-4-0。
    - N: 沒有偵測出5-4-0。

---

### app_for_testing.py
範例：
```
1: Filename = 11.mp4, Answer = N, Result = N   ========>  Correct
2: Filename = 12.mp4, Answer = N, Result = N   ========>  Correct
3: Filename = 13.mp4, Answer = N, Result = N   ========>  Correct
4: Filename = 14.mp4, Answer = N, Result = N   ========>  Correct
Total cases: 4, Success: 4, Fail: 0
Accuracy = 100.0 %
```
說明:
* Answer及Result的結果只會有2種，{Y, N}，代表的意思為：
    - Y: 有偵測出5-4-0。
    - N: 沒有偵測出5-4-0。

若兩者相同，則表示該部影片預測正確，反之則預測失敗。
