################
文件集合
################

处理文件组可能很麻烦,所以框架提供了 ``FileCollection`` 类来方便跨文件系统定位和处理文件组。

.. contents::
    :local:
    :depth: 2

***********
基本用法
***********

在最基本的级别上,``FileCollection`` 是一个你设置或构建的文件索引:

.. literalinclude:: files/011.php

在你输入要处理的文件后,可以删除文件或使用过滤命令删除或保留匹配某个正则表达式或 glob 样式模式的文件:

.. literalinclude:: files/012.php

当你的集合完成后,可以使用 ``get()`` 来检索最终的文件路径列表,或者利用 ``FileCollection`` 可数和可迭代的特性直接与每个 ``File`` 一起工作:

.. literalinclude:: files/013.php

下面是使用 ``FileCollection`` 的具体方法。

*********************
启动一个集合
*********************

__construct(string[] $files = [])
=================================

构造函数接受一个可选的文件路径数组,用作初始集合。这些通过 ``add()`` 传递,所以任何子类在 ``$files`` 中提供的文件仍将保留。

define()
========

允许子类定义自己的初始文件。这个方法由构造函数调用,允许预定义集合而不必使用它们的方法。例如:

.. literalinclude:: files/014.php

现在你可以在项目的任何地方使用 ``ConfigCollection`` 来访问所有 App 配置文件,而不必每次都重新调用集合方法。

set(array $files)
=================

将输入文件设置为提供的文件路径字符串数组。这将从集合中删除任何现有文件,所以 ``$collection->set([])`` 本质上是一个硬重置。

***************
输入文件
***************

add(string[]|string $paths, bool $recursive = true)
===================================================

添加路径或路径数组指示的所有文件。如果路径解析为目录,则 ``$recursive`` 将包含子目录。

addFile(string $file) / addFiles(array $files)
==============================================

将文件或文件添加到当前的输入文件列表中。文件是实际文件的绝对路径。

removeFile(string $file) / removeFiles(array $files)
====================================================

从当前的输入文件列表中删除文件。

addDirectory(string $directory, bool $recursive = false)
========================================================
addDirectories(array $directories, bool $recursive = false)
===========================================================

从目录或目录中添加所有文件,可选地递归进入子目录。目录是实际目录的绝对路径。

***************
过滤文件
***************

removePattern(string $pattern, string $scope = null)
====================================================
retainPattern(string $pattern, string $scope = null)
====================================================

通过模式(和可选作用域)过滤当前文件列表,删除或保留匹配的文件。``$pattern`` 可以是一个完整的正则表达式(如 ``'#[A-Za-z]+\.php#'``),也可以是类似 ``glob()`` 的伪正则表达式(如 ``*.css``)。
如果提供了 ``$scope``,则只考虑该目录中的文件(即 ``$scope`` 之外的文件总是保留)。如果没有提供作用域,则所有文件都将被考虑。

例子:

.. literalinclude:: files/015.php

****************
检索文件
****************

get(): string[]
===============

返回加载的所有输入文件的数组。

.. note:: ``FileCollection`` 是一个 ``IteratorAggregate``,所以你可以直接使用它(例如 ``foreach ($collection as $file)``)。
