****************
CLI 请求类
****************

如果对象来自命令行的调用，请求的对象实际上是 ``CLIRequest``.
它表现得如同 :doc:`conventional request </incoming/request>` , 但是为了便捷添加了一些访问函数方法。


====================
附加函数方法
====================

**getSegments()**

返回命令行实参的一组数组视为路径的部分::

    // command line: php index.php users 21 profile -foo bar
    echo $request->getSegments();  // ['users', '21', 'profile']

**getPath()**

以字符串返回重组的路径::


    // command line: php index.php users 21 profile -foo bar
    echo $request->getPath();  // users/21/profile

**getOptions()**

返回命令行实参的一组数组视为选项::

    // command line: php index.php users 21 profile -foo bar
    echo $request->getOptions();  // ['foo' => 'bar']

**getOption($which)**

返回一个特殊的命令行实参的值视为一个选项::


    // command line: php index.php users 21 profile -foo bar
    echo $request->getOption('foo');  // bar
    echo $request->getOption('notthere'); // NULL

**getOptionString()**

为选项返回重组的命令行字符串::

    // command line: php index.php users 21 profile -foo bar
    echo $request->getOptionPath();  // -foo bar
