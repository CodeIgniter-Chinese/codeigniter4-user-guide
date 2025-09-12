###########
CLI 库
###########

CodeIgniter 的 CLI 库让创建交互式命令行脚本变得简单，包括：

* 向用户提示更多信息
* 在终端中写入多色文本
* 发出提示音（请友好使用！）
* 在长时间任务期间显示进度条
* 将长文本行换行以适应窗口宽度。

.. contents::
    :local:
    :depth: 2

初始化类
**********************

由于 CLI 库的所有方法都是静态的，你无需创建其实例。相反，你只需确保控制器可以通过类上方的 ``use`` 语句找到它：

.. literalinclude:: cli_library/001.php

该类在文件首次加载时会自动初始化。

从用户获取输入
***************************

有时你需要向用户询问更多信息。他们可能没有提供可选的命令行参数，或者脚本可能遇到了一个已存在的文件，需要在覆盖前进行确认。这可以通过 ``prompt()`` 或 ``promptByKey()`` 方法来处理。

.. note:: 从 v4.3.0 版本开始，你可以使用 ``PhpStreamWrapper`` 为这些方法编写测试。
    参见 :ref:`testing-cli-input`。

prompt()
========

你可以通过将问题作为第一个参数传入来提供：

.. literalinclude:: cli_library/002.php

你可以通过将默认值作为第二个参数传入，来提供一个默认答案，当用户直接按回车键时会使用该答案：

.. literalinclude:: cli_library/003.php

你可以通过将允许的答案数组作为第二个参数传入，来限制可接受的答案：

.. literalinclude:: cli_library/004.php

最后，你可以将 :ref:`验证 <validation>` 规则作为第三个参数传入答案输入：

.. literalinclude:: cli_library/005.php

验证规则也可以用数组语法编写：

.. literalinclude:: cli_library/006.php

promptByKey()
=============

对于提示，预定义的答案（选项）有时需要描述，或者过于复杂而无法通过其值来选择。
``promptByKey()`` 允许用户通过键而不是值来选择选项：

.. literalinclude:: cli_library/007.php

命名键也是可能的：

.. literalinclude:: cli_library/008.php

最后，你可以将 :ref:`验证 <validation>` 规则作为第三个参数传入答案输入，可接受的答案会自动限制为传入的选项。

.. _prompt-by-multiple-keys:

promptByMultipleKeys()
======================

.. versionadded:: 4.3.0

此方法与 ``promptByKey()`` 相同，但支持多个值。

.. literalinclude:: cli_library/023.php

.. important:: 方法 ``promptByMultipleKeys()`` 与 ``promptByKey()`` 不同，不支持命名键或验证。

提供反馈
******************

write()
=======

提供了几种方法，让你可以向用户提供反馈。这可以是简单的状态更新，也可以是适应用户终端窗口宽度的复杂信息表。核心是 ``write()`` 方法，它将要输出的字符串作为第一个参数：

.. literalinclude:: cli_library/009.php

你可以通过将颜色名称作为第二个参数传入来更改文本颜色：

.. literalinclude:: cli_library/010.php

这可用于区分不同状态的消息，或通过使用不同颜色创建“标题”。你甚至可以通过将颜色名称作为第三个参数传入来设置背景色：

.. literalinclude:: cli_library/011.php

以下前景色可用：

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

背景色可用的种类较少：

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

print() 的功能与 ``write()`` 方法完全相同，只是它不会在前后强制换行。
相反，它会将内容打印到光标当前所在的位置。这允许你通过不同的调用在同一行上打印多个项目。当你想要显示一个状态，执行某个操作，然后在同一行上打印“Done”时，这尤其有用：

.. literalinclude:: cli_library/012.php

.. _cli-library-color:

color()
=======

虽然 ``write()`` 命令会将单行写入终端，并以 EOL 字符结尾，但你可以使用 ``color()`` 方法创建一个字符串片段，其使用方式相同，只是它不会在打印后强制换行。这允许你在同一行上创建多个输出。或者，更常见的是，你可以在 ``write()`` 方法内部使用它来创建内部不同颜色的字符串：

.. literalinclude:: cli_library/013.php

此示例会将单行写入窗口，其中 ``fileA`` 为黄色，后跟一个制表符，然后是白色文本的 ``/path/to/file``。

error()
=======

如果需要输出错误，你应该使用相应的 ``error()`` 方法。它会将浅红色文本写入 STDERR，而不是像 ``write()`` 和 ``color()`` 那样写入 STDOUT。如果你有脚本在监视错误，这会很有用，这样它们就不必筛选所有信息，只需关注实际的错误消息。你使用它的方式与使用 ``write()`` 方法完全相同：

.. literalinclude:: cli_library/014.php

wrap()
======

此命令将获取一个字符串，从当前行开始打印，并在新行上将其换行到设定的长度。
当你需要显示一个带有描述的选项列表，并希望这些描述在当前窗口内换行而不超出屏幕时，这可能会很有用：

.. literalinclude:: cli_library/015.php

默认情况下，字符串将在终端宽度处换行。Windows 当前无法确定窗口大小，因此我们默认为 80 个字符。如果你想将宽度限制为更短的长度，以确保其能适应窗口，请将最大行长度作为第二个参数传入。这会在最近的单词边界处断开字符串，以避免单词被拆分。

.. literalinclude:: cli_library/016.php

你可能会发现，你希望左侧有一列标题、文件或任务，而在右侧有一列对应的描述文本。默认情况下，换行会回到窗口的左边缘，这不允许内容在列中对齐。在这种情况下，你可以传入一定数量的空格来填充第一行之后的每一行，这样左侧就会有一个清晰的列边缘：

.. literalinclude:: cli_library/017.php

将创建类似以下内容：

.. code-block:: none

    task1a     Lorem Ipsum is simply dummy
               text of the printing and
               typesetting industry.
    task1abc   Lorem Ipsum has been the
               industry's standard dummy
               text ever since the

newLine()
=========

``newLine()`` 方法会向用户显示一个空白行。它不接受任何参数：

.. literalinclude:: cli_library/018.php

clearScreen()
=============

你可以使用 ``clearScreen()`` 方法清空当前终端窗口。在大多数 Windows 版本中，这只会插入 40 个空白行，因为 Windows 不支持此功能。Windows 10 的 bash 集成可能会改变这一点：

.. literalinclude:: cli_library/019.php

showProgress()
==============

如果你有一个长时间运行的任务，并希望向用户实时更新进度，可以使用 ``showProgress()`` 方法，它会显示类似以下内容：

.. code-block:: none

    [####......] 40% Complete

该方块在原位置进行动画，效果非常不错。

使用时，将当前步骤作为第一个参数传入，将总步骤数作为第二个参数传入。完成百分比和显示长度将基于该数字确定。完成后，将第一个参数传为 ``false``，进度条将被移除。

.. literalinclude:: cli_library/020.php

table()
=======

.. literalinclude:: cli_library/021.php

.. code-block:: none

    +----+--------------------------+---------------------+--------+
    | ID | Title                    | Updated At          | Active |
    +----+--------------------------+---------------------+--------+
    | 7  | A great item title       | 2017-11-16 10:35:02 | 1      |
    | 8  | Another great item title | 2017-11-16 13:46:54 | 0      |
    +----+--------------------------+---------------------+--------+

wait()
======

等待一定数量的秒数，可选择性地显示等待消息并等待按键。

.. literalinclude:: cli_library/022.php
