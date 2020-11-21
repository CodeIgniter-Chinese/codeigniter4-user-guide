###########
CLI Library
###########

CodeIgniter 的 CLI 库，让创建命令行交互脚本变得简单。其中包括：

* 为用户提供更多信息
* 在终端上打印彩色文本
* Beeping (be nice!)
* 在长任务中显示进度条
* 让长文本行适应窗口

.. contents::
    :local:
    :depth: 2

初始化类
======================

你不需要创建 CLI 库的实例，因为它的所有方法都是静态方法。你只需要确保你的控制器可以通过 ``use`` 声明找到它： 
::

	<?php namespace App\Controllers;

	use CodeIgniter\CLI\CLI;

	class MyController extends \CodeIgniter\Controller
	{
		. . .
	}

首次加载该文件时，这个类会自动初始化。

获取用户输入
===========================

有时你需要询问用户更多的信息。他们可能没有提供可选的命令行参数，或者脚本遇到了存在的文件，在覆写前需要进行确认。
这时使用 ``prompt()`` 方法处理

你可以提供一个问题作为方法的第一个参数：
::

	$color = CLI::prompt('What is your favorite color?');

你可以提供一个默认的答案作为方法的第二个参数。如果用户没有任何输入，只是按下 Enter 键，则将使用该默认答案：
::

	$color = CLI::prompt('What is your favorite color?', 'blue');

你可以向第二个参数传入允许答案的数组，以限制可以接受的答案：
::

	$overwrite = CLI::prompt('File exists. Overwrite?', ['y','n']);

最后你可以将验证规则作为第三个参数，以限制输入的答案：
::

	$email = CLI::prompt('What is your email?', null, 'required|valid_email');

提供反馈
==================

**write()**

多个方法可以用来向用户提供反馈。它可以像更新单个状态一样简单，也可以包装复杂的信息表到用户终端。
其核心是 ``write()`` 方法，该方法将要输出的字符串作为第一个参数：
::

	CLI::write('The rain in Spain falls mainly on the plains.');

你可以输入颜色名称作为第二个参数来更改文本的颜色：
::

	CLI::write('File created.', 'green');

你可以向第三个参数输入颜色名称来设置背景颜色。这可以用于按状态区分消息，或使用其他颜色创建“标题”：
::

	CLI::write('File overwritten.', 'light_red', 'dark_gray');

可以使用以下前景色：

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

少数可以用作背景色：

* black
* blue
* green
* cyan
* red
* yellow
* light_gray
* magenta

**print()**

Print 方法的功能和 ``write`` 相同，不同的是它不会在行前或者行尾强制换行。它将信息打印到当前屏幕光标所在的位置上，
这让你可以在不同的代码位置，打印信息到屏幕的同一行上。当你显示状态，执行某些操作后在同一行打印 “Done”  时，这十分有用：
::

    for ($i = 0; $i <= 10; $i++)
    {
        CLI::print($i);
    }

**color()**

``write()`` 方法将单行文本打印到终端，并打印 EOL 标识符结尾。``color()`` 方法以相同的方式处理文本，不同的是它不会在结尾打印 EOL 标识符。
这可以让你在同一行创建多个输出。更常见的用法是在 ``write()`` 方法内部使用，以在同一行中显示不同颜色的文本：
::

	CLI::write("fileA \t". CLI::color('/path/to/file', 'white'), 'yellow');

该示例将打印一行文本到终端。首先用黄色打印 ``fileA`` ，接着打印一个制表符，最后用白色打印 ``/path/to/file``。

**error()**

如果你需要输出错误信息，则应该使用 ``error`` 方法。它会将浅红色的文本写入到 ``STDERR``，而不是像 ``write()`` 和 ``color()`` 一样写入到 ``STDOUT``。
如果你使用脚本监视错误信息，这样就可以只捕获到实际的错误信息，不必从所有信息中进行筛选：
::

	CLI::error('Cannot write to file: ' . $file);

**wrap()**

该方法将获取一个字符串，并开始在当前行开始打印。它将会根据设置的长度对字符串进行包装，每行只显示设置的长度的内容。
他可以用来显示带有说明的显示列表，避免过多内容显示在一行内，影响阅读：
::

	CLI::color("task1\t", 'yellow');
	CLI::wrap("Some long description goes here that might be longer than the current window.");

默认情况下，字符串将用终端宽度进行包装。Windows 目前无法提供确定的窗口大小，所以默认使用 80 个字符。如果你希望将宽度设置的更短一些，
可以将最大行长度作为第二个参数传递。这将在最接近该长度的单词处断开字符，以避免破坏单词：
::

	// Wrap the text at max 20 characters wide
	CLI::wrap($description, 20);

你会发现需要左边需要一列显示标题、文件或任务，而右边需要一列显示文本和他的说明。默认情况下，
这将换行到窗口的左边缘，即不允许信息按列排列。这时你可以用空格来填充第一行之后的每一行，
以便让左侧具有清晰的列边缘：
::

	// 确定所有标题的最大长度
	// 确定左列的宽度
	$maxlen = max(array_map('strlen', $titles));

	for ($i=0; $i < count($titles); $i++)
	{
		CLI::write(
			// 在行的左侧列显示标题
			$titles[$i] . '   ' .
			// 在行的右侧列包装信息
			// 与左侧最宽的内容间隔三个宽度
			CLI::wrap($descriptions[$i], 40, $maxlen + 3)
		);
	}

将创建以下内容：

.. code-block:: none

    task1a   Lorem Ipsum is simply dummy
               text of the printing and typesetting
               industry.
    task1abc   Lorem Ipsum has been the industry's
               standard dummy text ever since the

**newLine()**

``newLine()`` 方法向用户显示一个空行，它不需要任何参数：
::

	CLI::newLine();

**clearScreen()**

你可以使用 ``clearScreen()`` 方法清除当前窗口。在多数的 Windows 系统中，它将插入 40 行空白行，因为 Windows 不支持该功能。
Windows 10 bash 因该能改变这点：
::

	CLI::clearScreen();

**showProgress()**

如果你有一个长时间运行的任务，你希望让用户了解当前的执行进度，则可以使用 ``showProgress()`` 方法，它显示以下内容：

.. code-block:: none

	[####......] 40% Complete

该行将设置为动态显示，以获得良好的展示效果。

将当前的步骤作为第一个参数传入，并将总步骤作为第二个参数传入。完成的百分比和显示长度将根据该数字确认。当任务完成后，传递 false 
作为第一个参数，进度条将被删除：
::

	$totalSteps = count($tasks);
	$currStep   = 1;

	foreach ($tasks as $task)
	{
		CLI::showProgress($currStep++, $totalSteps);
		$task->run();
	}

	// Done, so erase it...
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

等待一定的秒数。可以选择显示等待消息，或等待按键：

::

        // 等待指定的时间间隔，并显示倒计时信息
        CLI::wait($seconds, true);

        // 显示等待输入的信息，并等待输入
        CLI::wait(0, false);

        // 等待指定的时间间隔，不显示任何信息
        CLI::wait($seconds, false);
