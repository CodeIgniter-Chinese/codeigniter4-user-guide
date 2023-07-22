#####################
自定义函数调用
#####################

.. contents::
    :local:
    :depth: 2

$db->callFunction()
===================

此函数使你可以以与平台无关的方式调用 PHP 数据库函数,这些函数不是 CodeIgniter 原生支持的。
例如,假设你想调用 ``mysql_get_client_info()`` 函数,CodeIgniter 原生不支持此函数。你可以这样做:

.. literalinclude:: call_function/001.php

你必须在第一个参数中提供函数名称,不带 ``mysql_`` 前缀。前缀会根据当前使用的数据库驱动自动添加。这允许你在不同的数据库平台上运行相同的函数。显然,并非所有函数调用在所有平台上都是相同的,所以就可移植性而言,此函数的用途有限。

被调用函数需要的任何参数都将添加到第二个参数中。

.. literalinclude:: call_function/002.php

你通常需要提供数据库连接 ID 或数据库结果 ID。可以使用以下方式访问连接 ID:

.. literalinclude:: call_function/003.php

可以从结果对象内部访问结果 ID,如下所示:

.. literalinclude:: call_function/004.php
