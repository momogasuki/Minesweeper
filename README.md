## Minesweeper ##

代码的功能是输入一张扫雷截图，输出当前局面下所有未确定格子的有雷的概率，并可视化显示出来。

The function of the code is: given a snapshot of a Minesweeper game, output the probability of 'is mine' of each unknowned grid, and visualize it.

### 使用方法 Usage ###

首先模仿match文件夹下的样例，运行你的扫雷，把012345678,旗子什么的截好图，替换match文件夹下的图片，并按相同方式命好名（如empty_xxx.jpg)

Firstly, replace pictures in 'match' directory with grids in your own Minesweeper game, and name it with the same pattern (e.g. empty_xxx.jpg)

随意开启一局扫雷，截取游戏中的某个局面保存，记好它的路径。然后打开`test.py`，把倒数第四行和倒数第三行分别改成截图的路径和截图的局面下的剩余雷数。

Secondly, start a game and save a snapshot in the middle of the game. Change the fourth and the third line of `test.py` with the path of your snapshot and the remaining number of mines in the snapshot, respectively.

最后运行`python test.py`即可。运行后会弹出一张可视化概率的图片，按‘S'可以保存，按其他任何键可以直接退出。

Finally, simply run `python test.py` and you will get a picture with visualized probability. Press 'S' to save the picture and otherwise quit directly.

### 随便说些啥 ###

记得自己先装上cv2！

算法现在基本上是无脑DFS，遇到难以判断的局面这个算法复杂度一下子就爆了。。。后面再考虑能不能先分割什么的。。。或者采用一些强化学习的思路并不需要求出精确概率？暂时还没太多想法。。。

关于这个从截图复原出局面的问题。。。现在是假定格子的边缘颜色都特别深，其他地方颜色都不是特别深。。。因为也没在其它电脑的扫雷上测试过，也不知道性能怎么样==出了问题再说吧==