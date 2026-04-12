################
文件集合
################

成组处理文件往往比较繁琐，因此框架提供了 ``FileCollection``
类，便于在整个文件系统中定位并处理一组文件。

.. contents::
    :local:
    :depth: 2

***********
基本用法
***********

最基本的 ``FileCollection`` 是一个自行设置或构建的文件数组：

.. literalinclude:: files/011.php

输入要处理的文件后，可移除文件，或使用过滤命令移除或保留匹配特定正则表达式
或 glob 风格模式的文件：

.. literalinclude:: files/012.php

集合完成后，可使用 ``get()`` 获取最终的文件路径列表，也可利用
``FileCollection`` 具备可计数和可迭代特性，直接处理每个 ``File``：

.. literalinclude:: files/013.php

下面介绍使用 ``FileCollection`` 的具体方法。

*********************
创建集合
*********************

__construct(string[] $files = [])
=================================

构造函数接受一个可选的文件路径数组，作为初始集合。这些路径会传递给
``add()``，因此子类在 ``$files`` 中提供的任何文件都会保留。

define()
========

允许子类定义自己的初始文件。构造函数会调用此方法，从而无需调用这些方法
即可使用预定义的集合。

示例：

.. literalinclude:: files/014.php

这样一来，便可在项目任何位置使用 ``ConfigCollection`` 访问 **app/Config/**
中的所有 PHP 文件，而不必每次都重新调用集合方法。

set(array $files)
=================

将输入文件列表设置为提供的文件路径字符串数组。这会移除集合中的所有现有文
件，因此 ``$collection->set([])`` 本质上相当于一次硬重置。

***************
输入文件
***************

add(string[]|string $paths, bool $recursive = true)
===================================================

添加路径或路径数组指定的所有文件。如果路径解析为目录，则 ``$recursive``
会包含子目录。

addFile(string $file) / addFiles(array $files)
==============================================

将一个或多个文件添加到当前输入文件列表中。文件必须是实际存在文件的绝对路
径。

removeFile(string $file) / removeFiles(array $files)
====================================================

从当前输入文件列表中移除一个或多个文件。

addDirectory(string $directory, bool $recursive = false)
========================================================
addDirectories(array $directories, bool $recursive = false)
===========================================================

从一个或多个目录中添加所有文件，并可选择是否递归进入子目录。目录必须是实
际存在目录的绝对路径。

***************
过滤文件
***************

removePattern(string $pattern, string $scope = null)
====================================================
retainPattern(string $pattern, string $scope = null)
====================================================

使用模式（以及可选的作用域）过滤当前文件列表，移除或保留匹配的文件。

``$pattern`` 可以是完整的正则表达式（如 ``'#\A[A-Za-z]+\.php\z#'``），也可
以是类似 ``glob()`` 的伪正则表达式（如 ``'*.css'``）。

如果提供了 ``$scope``，则只会考虑该目录中或其下的文件（即位于 ``$scope``
之外的文件始终会被保留）。未提供作用域时，所有文件都会参与处理。

示例：

.. literalinclude:: files/015.php


.. _file-collections-retain-multiple-patterns:

retainMultiplePatterns(array $pattern, string $scope = null)
============================================================

提供与 ``retainPattern()`` 相同的功能，但接受一个模式数组，以保留匹配任一模
式的文件。

示例：

.. literalinclude:: files/016.php

****************
获取文件
****************

get(): string[]
===============

返回所有已加载输入文件的数组。

.. note:: ``FileCollection`` 是一个 ``IteratorAggregate``，因此可直接使用
    （例如 ``foreach ($collection as $file)``）。
