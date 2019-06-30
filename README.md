# Python
## 在 /home/pi/.config 下找到名為autostart的資料夾,如果沒有就新建立一個。在該資料夾下建立一個xxx.desktop檔案,檔名自擬,字尾必須是desktop,檔案內容如下:
###[Desktop Entry] 
### Name=test 
### Comment=Python Program 
### Exec=python /home/pi/test.py 
### Icon=/home/pi/python_games/4row_black.png 
### Terminal=false 
### MultipleArgs=false 
### Type=Application 
### Categories=Application;Development; 
### StartupNotify=true
