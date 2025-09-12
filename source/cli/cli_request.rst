****************
CLIRequest 类
****************

如果请求来自命令行调用，请求对象实际上是
``CLIRequest``。它的行为与 :doc:`常规请求 </incoming/request>`
相同，但增加了一些方便使用的访问器方法。

====================
额外的访问器
====================

getSegments()
-------------

返回被视为路径一部分的命令行参数数组：

.. literalinclude:: cli_request/001.php

getPath()
---------

以字符串形式返回重建后的路径：

.. literalinclude:: cli_request/002.php

getOptions()
------------

返回被视为选项的命令行参数数组：

.. literalinclude:: cli_request/003.php

getOption($key)
-----------------

返回被视为选项的特定命令行参数的值：

.. literalinclude:: cli_request/004.php

getOptionString()
-----------------

返回选项的重建命令行字符串：

.. literalinclude:: cli_request/005.php

将 ``true`` 传递给第一个参数会尝试使用两个连字符来写长选项：

.. literalinclude:: cli_request/006.php
