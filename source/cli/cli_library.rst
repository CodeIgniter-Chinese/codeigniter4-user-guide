###########
命令行界面（CLI）类库
###########

Codeigniter 的 CLI 类库构造简单的设计交互式的命令行脚本，包括:

* 提示用户获取更多信息
* 著述多彩的文本终端
* 报警声（要友好！）
* 在长时间任务期间显示进度条
* 去配合窗口换行长文本。


.. contents::
    :local:
    :depth: 2

初始化类
======================

你不需要创建 CLI 类库的接口，此后它的所有方法是静态的。反而在你的类上，你要简单地确保你的的控制器通过 ``use`` 声明能找出它::


	<?php namespace App\Controllers;

	use CodeIgniter\CLI\CLI;

	class MyController extends \CodeIgniter\Controller
	{
		. . .
	}

当文件第一时间被加载时，类是自动地被初始化的。



从用户获取输入信息
===========================

因为更多信息有时候你需要询问用户。他们也许不会提供可选择的命令行参数数组，要不然脚本在改写以前也许会遭遇一个现存的文件并需要确认。用 ``prompt()`` 方法是易于操作的。

通过 ``prompt()`` 方法你可以规定一个问题作为第一参数::

	$color = CLI::prompt('What is your favorite color?');

在第二参数值里，通过默认值如果用户仅按回车键，则你能规定一个要被使用的默认答案::

	$color = CLI::prompt('What is your favorite color?', 'blue');
	
通过允许回答的数组你能约束可以接受的问题作为第二参数::

	$overwrite = CLI::prompt('File exists. Overwrite?', ['y','n']);

最终，你能通过合法授权规范去应答输入并作为第三个参数::

	$email = CLI::prompt('What is your email?', null, 'required|valid_email');


提供反馈
==================

**write()**

为了给你的用户你要提供反馈，一些方法要被提供。
这些方法能被简单的做为单一的状态更新或者适应用户终端窗口换行的一个复杂信息的表格。
在这个 ``write()`` 方法的核心里，该方法要输出字符串作为第一参数::

	CLI::write('The rain in Spain falls mainly on the plains.');
	
通过一个颜色名称你能改变文本的颜色作为第二参数::	

	CLI::write('File created.', 'green');

根据状况，这个方法能被使用在差异的信息中，或者通过使用不同的颜色创建 'headers'。
你能通过颜色名字设置背景颜色作为第三参数::

	CLI::write('File overwritten.', 'light_red', 'dark_gray');

接下来的前景颜色是可用的:

* 黑色
* 灰色
* 蓝色
* 深蓝色
* 浅蓝色
* 绿色
* 浅绿色
* 青色
* 浅青色
* 红色
* 浅红色
* 紫色
* 浅紫色
* 浅黄色
* 黄色
* 浅灰色
* 白色

并且做为背景色更小的数字是可用的:

* 黑色
* 蓝色
* 绿色
* 青色
* 红色
* 黄色
* 浅灰色
* 洋红


**print()**

打印功能完全同等地对待 ``write()`` 方法，除非它不会在换行符前或换行符后阻止打印。
更换它，打印它到屏幕里的任何地方指针是当前地。
这个方法允许你在同一行，来自不同调用函数打印所有混合项。
当你想展示一个状态，做某事，然后在同一行打印 "Done" 这个方法是特别有帮助的::


    for ($i = 0; $i <= 10; $i++)
    {
        CLI::print($i);
    }

**color()**

当 ``write()`` 命令将写到终端的单独行时，用项目终止字符 （EOL） 结束它，你能用 ``color()`` 方法改变字符碎片，
并且字符碎片能以相同的方式使用，除非该字符碎片会在打印后阻止终止字符。
这个方法允许你在相同的列上创造多行输出信息。或者，更一般地，你能用它在 ``write()`` 方法内去创建不同颜色里的字符::


	CLI::write("fileA \t". CLI::color('/path/to/file', 'white'), 'yellow');

这个示例将会写单独行到窗口，以 ``fileA`` 用黄色，遵循跳格键，然后 ``/path/to/file`` 用白色文本。


**error()**

如果你需要输出错误，你应当使用适当的命名的 ``error()`` 方法。
这个方法用浅红色文本书写到 STDERR（标准错误输出设备），代替 STDOUT（标准输出），就像 ``write()`` 和 ``color()`` 做的。
对于错误如果你有脚本监视这个方法是有帮助的，因此他们不要通过所有信息去删选，仅要实际的错误信息。
你正确地使用它就像你用过的 ``write()`` 方法一样::

	CLI::error('Cannot write to file: ' . $file);

**wrap()**

这个命令将会取得一个字符串，开始打印它在最近的行上，并且按照设置的长度换到新行输出字符串。
当显示带你想在最近的窗口换行或者不要离开屏幕的描述选项列表时，这个方法是有用的::

	CLI::color("task1\t", 'yellow');
	CLI::wrap("Some long description goes here that might be longer than the current window.");

默认情况下，字符串将会在终端宽度上换行。
最近地窗口不提供到终端窗口的尺寸，因此我们默认 80 个字母。
如果你想对某个更短字符串制约宽度，并且你能相当确定适应窗口，通过最大行长度作为第二参数。
在附近的文字分界线里这将会破坏字符串以便破坏文字。
::

	// Wrap the text at max 20 characters wide
	CLI::wrap($description, 20);

当你想带描述的文本专栏在右侧时，你也许找到了你需要的专栏在左面的标题，文件或者任务上。
默认情况下，这个方法将会换行回到窗口的左边界，该方法不允许任何事件在专栏里排队。
万一出现上文叙述的情况，你能在第一行后通过一定数量的空格去填充每一行，以便你在左侧有一个干净利落的专栏边界::

	// 决定所有标题的最大长度
	// 去决定左面专栏的宽度
	$maxlen = max(array_map('strlen', $titles));

	for ($i=0; $i <= count($titles); $i++)
	{
		CLI::write(
			// 在列左面显示标题
			$title[$i] . '   ' .
			// 在右手专栏对叙述换行
			// 用它的左边更宽 3 个字母
			// 在左侧最长的项目
			CLI::wrap($descriptions[$i], 40, $maxlen + 3)
		);
	}

愿创建的事件像下面描述的一样:

.. code-block:: none

    task1a     Lorem Ipsum is simply dummy
               text of the printing and typesetting
               industry.
    task1abc   Lorem Ipsum has been the industry's
               standard dummy text ever since the

**newLine()**

 ``newLine()`` 方法显示到用户的空行。它不带任何参数::

	CLI::newLine();

**clearScreen()**

你能用  ``clearScreen()`` 方法清理最近的终端窗口。
在 Windows 的多数版本里，从 Windows 不支持这个特征以来这个方法将简单地插入 40 个空白行。
Windows 10 bash integration 能被改成下面的语句::

	CLI::clearScreen();

**showProgress()**

如果你有长期运行的任务并且你想要保持用户更新进度，你能使用 ``showProgress()`` 方法显示某些事像下面描述的一样:

.. code-block:: none

	[####......] 40% Complete

为了一个非常好的效果这块的位置是动态的。

使用进度，经过最近的步骤作为第一参数，并且步骤的总数字作为第二参数。
百分比完成和显示长度将会基于上面的数字被决定。
当你已经做完了，通过 ``false`` 作为第一参数并且进度条将会被移除。
::

	$totalSteps = count($tasks);
	$currStep   = 1;

	foreach ($tasks as $task)
	{
		CLI::showProgress($currStep++, $totalSteps);
		$task->run();
	}

	// 做完了，所以擦除它……
	CLI::showProgress(false);

**table()**

::

	$thead = ['ID', 'Title', 'Updated At', 'Active'];
	$tbody = [
		[7, 'A great item title', '2017-11-15 10:35:02', 1],
		[8, 'Another great item title', '2017-11-16 13:46:54', 0]
	];

	CLI::table($tbody, $thead);

.. code-block:: none

	+----+--------------------------+---------------------+--------+
	| ID | Title                    | Updated At          | Active |
	+----+--------------------------+---------------------+--------+
	| 7  | A great item title       | 2017-11-16 10:35:02 | 1      |
	| 8  | Another great item title | 2017-11-16 13:46:54 | 0      |
	+----+--------------------------+---------------------+--------+

**wait()**

等待确定的秒数，可选择地显示等待信息并且等待按键。
::

        // 等待具体指定的间隔，用倒数几秒显示
        CLI::wait($seconds, true);

        // 显示延长信息并且等待输入
        CLI::wait(0, false);

        // 等带具体指定的间隔
        CLI::wait($seconds, false);
