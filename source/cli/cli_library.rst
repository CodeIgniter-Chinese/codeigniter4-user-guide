###########
CLI 库
###########

CodeIgniter 的 CLI 库可以轻松创建交互式命令行脚本,包括:

* 提示用户提供更多信息
* 在终端上写入多彩文本
* 蜂鸣声(要友好!)
* 在长时间任务期间显示进度条
* 将过长的文本行包装以适应窗口

.. contents::
    :local:
    :depth: 2

初始化类
**********************

你不需要创建 CLI 库的实例,因为它的所有方法都是静态的。相反,你只需要通过控制器顶部的 ``use`` 语句确保控制器可以定位它:

.. literalinclude:: cli_library/001.php

该类在首次加载文件时会自动初始化。

获取用户输入
***************************

有时你需要询问用户更多信息。他们可能没有提供可选的命令行参数,或者脚本可能遇到现有文件并需要确认才能覆盖。这通过 ``prompt()`` 或 ``promptByKey()`` 方法来处理。

.. note:: 从 v4.3.0 开始,你可以用 ``PhpStreamWrapper`` 为这些方法编写测试。
    请参阅 :ref:`testing-cli-input`。

prompt()
========

你可以通过作为第一个参数传递问题来提供一个问题:

.. literalinclude:: cli_library/002.php

你可以通过在第二个参数中传递默认值,为用户只需按 Enter 提供默认答案:

.. literalinclude:: cli_library/003.php

你可以通过作为第二个参数传递允许答案的数组来限制可接受的答案:

.. literalinclude:: cli_library/004.php

最后,你可以将答案输入的 :ref:`验证 <validation>` 规则作为第三个参数传递:

.. literalinclude:: cli_library/005.php

验证规则也可以以数组语法编写:

.. literalinclude:: cli_library/006.php

promptByKey()
=============

预定义的提示答案(选项)有时需要描述或过于复杂,无法通过其值进行选择。``promptByKey()`` 允许用户通过其键而不是值来选择选项:

.. literalinclude:: cli_library/007.php

命名键也是可能的:

.. literalinclude:: cli_library/008.php

最后,你可以将答案输入的 :ref:`验证 <validation>` 规则作为第三个参数传递,可接受的答案会自动限制为传入的选项。

.. _prompt-by-multiple-keys:

promptByMultipleKeys()
======================

.. versionadded:: 4.3.0

这个方法与 ``promptByKey()`` 相同,但它支持多个值。

.. literalinclude:: cli_library/023.php

.. important:: 与 ``promptByKey()`` 不同, ``promptByMultipleKeys()`` 方法不支持命名键或验证。

提供反馈
******************

write()
=======

提供了几种方法来向用户提供反馈。这可以是简单的单个状态更新,也可以是复杂的信息表格,会换行到用户的终端窗口。这其核心是 ``write()`` 方法,它以要输出的字符串作为第一个参数:

.. literalinclude:: cli_library/009.php

你可以通过在第二个参数中传递颜色名称来更改文本颜色:

.. literalinclude:: cli_library/010.php

这可以用来按状态区分消息,或通过使用不同的颜色创建“标题”。你甚至可以通过将颜色名称作为第三个参数传递来设置背景颜色:

.. literalinclude:: cli_library/011.php

以下前景色可用:

* black
* dark_gray
* blue
* dark_blue
* light_blue
* green
* light_green
* cyan
* light_cyan
* red
* light_red
* purple
* light_purple
* light_yellow
* yellow
* light_gray
* white

并且有更小数量的背景色可用:

* black
* blue
* green
* cyan
* red
* yellow
* light_gray
* magenta

print()
=======

``print()`` 的作用与 ``write()`` 方法相同,只是它不会在前后强制换行。相反,它会将内容打印到光标当前所在的屏幕上。这允许你从不同的调用中在同一行上打印多个项目。当你想显示一个状态,执行一些操作,然后在同一行上打印“Done”时,这特别有用:

.. literalinclude:: cli_library/012.php

.. _cli-library-color:

color()
=======

虽然 ``write()`` 命令会将单行写入终端,并在结束时带有 EOL 字符,但你可以使用 ``color()`` 方法来制作一个字符串片段,可以以相同的方式使用,不同之处在于打印后不会强制 EOL。这允许你在同一行上创建多个输出。或者,更常见的是,你可以在 ``write()`` 方法中使用它来创建不同颜色的字符串:

.. literalinclude:: cli_library/013.php

这个示例将在窗口中写入一行, ``fileA`` 为黄色,后跟一个制表符,然后是白色的 ``/path/to/file``。

error()
=======

如果需要输出错误,你应该使用适当命名的 ``error()`` 方法。这会将浅红色文本写入 STDERR,而不是像 ``write()`` 和 ``color()`` 那样写入 STDOUT。如果你有监视错误的脚本,这样可以方便它们不必筛选所有信息,而只提取实际的错误消息。你可以像使用 ``write()`` 方法一样使用它:

.. literalinclude:: cli_library/014.php

wrap()
======

这个命令将获取一个字符串,开始在当前行打印它,并将其换行到设置的长度。当显示你想要在当前窗口中换行而不是超出屏幕的选项及其描述时,这可能很有用:

.. literalinclude:: cli_library/015.php

默认情况下,字符串将换行到终端宽度。Windows 当前没有提供确定窗口大小的方法,因此我们默认为 80 个字符。如果你想将宽度限制为一些可以相当确定适合窗口的较短长度,请将最大行长度作为第二个参数传递。这将在最接近的词边界处中断字符串,以免单词被断开。

.. literalinclude:: cli_library/016.php

你可能会发现,你想要标题、文件或任务的左边有一列,而右边有描述文本的一列。默认情况下,这将回绕到窗口的左边缘,这不允许项目按列对齐。在这种情况下,你可以传入换行后要填充的空格数,以便在左边有一个整齐的列边界:

.. literalinclude:: cli_library/017.php

这将创建类似如下的内容:

.. code-block:: none

    task1a     Lorem Ipsum 只是印刷和排版
               行业的虚构文字
    task1abc   Lorem Ipsum 从1500年代起
               就一直是行业的标准虚构文字

newLine()
=========

``newLine()`` 方法向用户显示一个空行。它不接受任何参数:

.. literalinclude:: cli_library/018.php

clearScreen()
=============

你可以使用 ``clearScreen()`` 方法清除当前的终端窗口。在大多数 Windows 版本中,这只会插入 40 行空白行,因为 Windows 不支持此功能。Windows 10 bash 集成应该会改变这一点:

.. literalinclude:: cli_library/019.php

showProgress()
==============

如果你有一个长时间运行的任务,希望保持用户了解进度,可以使用 ``showProgress()`` 方法,它会显示类似以下内容:

.. code-block:: none

    [####......] 40% Complete

此块会就地进行动画以产生非常好的效果。

使用时,请将当前步骤作为第一个参数传递,将总步骤数作为第二个参数。完成百分比和显示长度将根据该数字确定。完成时,请将 ``false`` 作为第一个参数传入,进度条将被删除。

.. literalinclude:: cli_library/020.php

table()
=======

.. literalinclude:: cli_library/021.php

.. code-block:: none

    +----+--------------------------+---------------------+--------+
    | ID | Title                    | Updated At          | Active |
    +----+--------------------------+---------------------+--------+
    | 7  | A great item title       | 2017-11-15 10:35:02 | 1      |
    | 8  | Another great item title | 2017-11-16 13:46:54 | 0      |
    +----+--------------------------+---------------------+--------+

wait()
======

等待一定的秒数,可选择显示等待消息并等待按键。

.. literalinclude:: cli_library/022.php
