#####################
自定义函数调用
#####################

.. contents::
    :local:
    :depth: 2

$db->callFunction()
===================

此函数允许你以独立于平台的方式调用 CodeIgniter 未原生支持的 PHP 数据库函数。例如，假设你想调用 CodeIgniter **未原生支持** 的 ``mysql_get_client_info()`` 函数，你可以这样做：

.. literalinclude:: call_function/001.php

在第一个参数中，你必须提供函数名称，但**不需要**包含 ``mysql_`` 前缀。前缀会根据当前使用的数据库驱动程序自动添加。这允许你在不同的数据库平台上运行相同的函数。显然，并非所有函数调用在不同平台之间都是相同的，因此该函数在可移植性方面的有用性是有限的。

你调用的函数所需的任何参数都将添加到第二个参数中。

.. literalinclude:: call_function/002.php

通常，你需要提供数据库连接 ID 或数据库结果 ID。连接 ID 可以通过以下方式访问：

.. literalinclude:: call_function/003.php

结果 ID 可以从结果对象中访问，如下所示：

.. literalinclude:: call_function/004.php
