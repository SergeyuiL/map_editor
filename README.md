# 1、安装Python3
version >= 3.10

https://www.python.org/downloads/macos/

# 2、配置环境
```shell
pip3 install -r requirements.txt
```

# 3、运行脚本
```python
python3 map_editor.py
```

# 4、使用说明
- 启动时点击```Load Map```按钮选择地图目录（文件夹），选中目录后会自动导入栅格地图和配置文件
- 对话框中可以看到一个红色方框框选对应像素，通过键盘上、下、左、右按键移动方框，空格键翻转对应像素属性，白色为可行域，黑色为障碍物
- ```Save Map```按钮将更改应用于原地图，```Save Map As```另存地图