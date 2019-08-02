# Python
## "樹莓派" 在 /home/pi/.config 下找到名為autostart的資料夾,如果沒有就新建立一個。在該資料夾下建立一個xxx.desktop檔案,檔名自擬,字尾必須是desktop,檔案內容如下:
### [Desktop Entry] 
### Name=test 
### Comment=Python Program 
### Exec=python /home/pi/test.py 
### Icon=/home/pi/python_games/4row_black.png 
### Terminal=false 
### MultipleArgs=false 
### Type=Application 
### Categories=Application;Development; 
### StartupNotify=true
### Name、Comment、Icon 可以自定,表示啟動項的名稱、備註和圖示。Exec 表示呼叫的指令,和在終端輸入執行指令碼的指令格式一致。如果你的樹莓派沒有png圖示,那麼就和我一樣,找到python_game資料夾,那裡有幾個簡單的圖示可以現成拿來使用。


### sudo reboot 
### 重啟, test.py 就開機自動運行了。
[!https://github.com/tsaiminghsu/Python/blob/master/TwoDigitsCounter_74595.png)
