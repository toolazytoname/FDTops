# FDTops
## 由来

批量给类增加前缀，替换前缀。

我是不是与这种事有缘啊，批量重命名类，改个前缀，加个前缀，Xcode自带的Refactor是好用，但是同时只能更改一个类的名字，不能批量操作。于是就有了这么个脚本。

之前用shell 写过一个简单的脚本，主要原理就是调用苹果自带的命令行工具tops,重新捡起来发现确实是不太习惯，于是用Python3 重新写了一个。这个命令就是用来批量重命名方法名，类等，使用过程中碰到一个问题，它不会自动把文件名改掉，自然也不会把文件头中的 #import “className.h”给替换掉。不知道是工具本身就不支持，还是我没有设置好某个参数，反正遍寻man中的介绍，最终也没有找到。只能用脚本暴力重命名文件，替换。



## 如何使用

cd到FDTops.py脚本所在目录，苹果自带的Python版本是2.7，你首先得安一个Python3

~~~shell
python3 FDTops.py（脚本命令位置） /Users/yiche/Code/yiche/yiche4iOS/autoPrice/App/Mine/MessageCenter（目标类所在目录）  replace（操作符，目前只支持replace 和add） YC（原始前缀名） FD（目标前缀名） 

python3 FDTops.py /Users/yiche/Code/yiche/yiche4iOS/autoPrice/App/Mine/MessageCenter  replace YC FD 

python3 FDTops.py /Users/yiche/Code/yiche/yiche4iOS/autoPrice/App/Mine/MessageCenter add FD（增加的前缀） 

~~~



## 原理 

1. 递归便利目标目录下的文件， 通过文件名获得类名
2. 用tops 命令替换 
3. 替换import 进来的的类名 "{classname}.h” 
4. 重命名目标目录下的.h. 和 .m文件



## 待优化

1. 因为对Python 不太熟悉，PyCharm 也用得不太熟，全程有很多warning没有解决。
2. 为了代码结构逻辑清晰，递归遍历了好多次，熟了再优化吧
3. 是不是可以把这些操作，全放到一个模块里面，然后import 进来 



## 灵感之源

[iOS SDKs: Renaming a lot of classes](https://stackoverflow.com/questions/16645726/ios-sdks-renaming-a-lot-of-classes)]