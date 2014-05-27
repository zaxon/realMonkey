# realMonkey

标签（空格分隔）： android uiautomator test

---

realMonkey是一个轻量级的、跨平台运行的、基于uiautomator的android自动化测试工具，使用Python语言编写测试脚本，运行于android4.1以上的设备。
#优势
 - 不需要修改App的任何东西
 - 多平台编写、运行测试用例
 - 开源的
 - 跨应用
 - 不用编译
# 如何使用
确保你的PC已经配置好了android sdk和python开发环境
获取realMonkey，放置于PC上的任意位置
*注意：路径最好不要带中文*

下载地址：https://github.com/zaxon/realMonkey
### 编写测试脚本
```python
#testCase.py
import os,sys
sys.path.append(r'E:\realMonkey') #这是realMonkey在PC上的位置
from automatormonkey.monkeyrunnercore.MonkeyRunner import rMonkeyRunner
from automatormonkey.monkeyrunnercore.info.Enum import *

deviceName=['1','VVA5C3'] #选择回放脚本的设备
device=rMonkeyRunner(__file__,deviceName)

device.click(UIELEMENT.TEXT, '关闭')
device.sleep(5.0)
device.drag(DIRECTION.RIGHT)
```
### 回放脚本
    $ python testCase.py




