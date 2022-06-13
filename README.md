
# AI_project_team11_2022

## Requirements

Python版本：3.9.13

使用前需要先安裝module：
```
pip install -r requirements.txt
```

## 檔案說明
### `app.py`
可使用前鏡頭或單一影片進行測試，在執行過程中會有視窗畫面，可以即時了解當前所辨認之手勢。

---
### `app_for_testing.py`
一次對整個資料夾的影片進行測試，執行過程為了節省效能，不會有額外的視窗畫面。

---
### `test.py`
使用整支影片所辨認出的個別手勢資訊（array of {5, 4, 0, N, X} ），判斷是否包含連續的5-4-0手勢。

會被`app.py`及`app_for_testing.py`呼叫

---
### `10_sec_yes`
作為Test data，內含40部長度10秒且有540手勢之影片。

---
### `10_sec_no`
作為Test data，內含40部長度10秒且沒有540手勢之影片。

---
### 其他Test data
另有各40部長度30秒，分別有540手勢、沒有540手勢的影片。

因檔案過大，所以不上傳至Repo，可至連結下載：[包含影片之Google Drive](https://drive.google.com/drive/folders/1g2w5Qxhu-ea007MQFYhMKN2DXqWD1VVc?usp=sharing)


## 使用方法
### `app.py`
範例:

```
python app.py --video_source ./video.mp4 --output_frame 5
```

* --video_source <影片位置>: 若沒有指定arg，則使用電腦鏡頭

* --output_frame <想要每幾幀紀錄一個手勢>: 若沒有指定arg，則每五幀紀錄一幀

過程中若要退出，在視窗中按下Esc即可

---

### `app_for_testing.py`
範例:

```
python app_for_testing.py --video_dir 10_sec_no
```

* --video_dir <包含影片的資料夾位置>: 資料夾的名稱最後一定要標明 yes 或是 no，如同範例所寫的格式。

* --output_frame <想要每幾幀紀錄一個手勢>: 若沒有指定arg，則每五幀紀錄一幀


## 輸出
### `app.py`
範例1：
```
hit1: Time of occurrence:2.5s spend time:2.5s
hit2: Time of occurrence:5.42s spend time:1.25s
hit3: Time of occurrence:8.54s spend time:1.46s
hit4: Time of occurrence:11.25s spend time:1.87s
Attention!
Result = Y
```
範例2：
```
Safe
Result = N
```
說明:
* Result的結果只會有2種，{Y, N}，代表的意思為：
    - Y: 有偵測出5-4-0手勢。
    - N: 沒有偵測出5-4-0手勢。
* 另有可能出現的輸出為：
	- `hit{x}: Time of occurrence: {t1}s spend time:{t2}s`
		- x: 這是該部影片第x次出現5-4-0手勢。
		- t1: 該次手勢出現在影片第t1秒
		- t2: 該次手勢總共花了t2秒比完
	- `Attention!`: 若該部影片偵測到 >= 3次5-4-0手勢，表示此人高機率在密集求助，需注意。
	- `Safe!`: 表示整部影片沒有偵測到任何一次5-4-0手勢，大致安全。
---

### `app_for_testing.py`
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
    - Y: 有偵測出5-4-0手勢。
    - N: 沒有偵測出5-4-0手勢。

若兩者相同，則表示該部影片預測正確，反之則預測失敗。
