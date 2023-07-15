****************
CLIRequest 类
****************

如果请求来自命令行调用,则请求对象实际上是一个 ``CLIRequest``。它的行为与 :doc:`常规请求 </incoming/request>` 相同,但添加了一些方便的访问器方法。

====================
额外的访问器
====================

getSegments()
-------------

返回被视为路径一部分的命令行参数数组:

.. literalinclude:: cli_request/001.php

getPath()
---------

返回重构后的路径字符串:

.. literalinclude:: cli_request/002.php

getOptions()
------------

返回被视为选项的命令行参数数组:

.. literalinclude:: cli_request/003.php

getOption($which)
-----------------

返回被视为选项的特定命令行参数的值:

.. literalinclude:: cli_request/004.php

getOptionString()
-----------------

返回重构后的命令行选项字符串:

.. literalinclude:: cli_request/005.php

向第一个参数传递 ``true`` 将尝试使用两个破折号编写长选项:

.. literalinclude:: cli_request/006.php
