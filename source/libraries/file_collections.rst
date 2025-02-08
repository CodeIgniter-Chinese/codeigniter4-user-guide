################
文件集合
################

处理文件组可能很繁琐，因此框架提供了 ``FileCollection`` 类来简化跨文件系统的文件组定位和操作。

.. contents::
    :local:
    :depth: 2

***********
基本用法
***********

在最基础的用法中，``FileCollection`` 是一个由你设置或构建的文件数组：

.. literalinclude:: files/011.php

在你输入要处理的文件后，可以移除文件或使用过滤命令来删除/保留匹配特定正则表达式或 glob 风格模式的文件：

.. literalinclude:: files/012.php

当集合构建完成后，可以使用 ``get()`` 获取最终文件路径列表，或利用 ``FileCollection`` 的可计数和可迭代特性直接操作每个 ``File``：

.. literalinclude:: files/013.php

以下是操作 ``FileCollection`` 的具体方法。

*********************
创建集合
*********************

__construct(string[] $files = [])
=================================

构造函数接受一个可选的文件路径数组作为初始集合。这些路径会传递给 ``add()`` 方法，因此子类通过 ``$files`` 提供的文件会保留。

define()
========

允许子类定义自己的初始文件。此方法由构造函数调用，支持预定义集合而无需重复调用其方法。

示例：

.. literalinclude:: files/014.php

现在你可以在项目任意位置使用 ``ConfigCollection`` 来访问 **app/Config/** 下的所有 PHP 文件，无需每次重新调用集合方法。

set(array $files)
=================

将输入文件列表设置为提供的文件路径字符串数组。这会移除集合中所有现有文件，因此 ``$collection->set([])`` 本质上是硬重置。

***************
输入文件
***************

add(string[]|string $paths, bool $recursive = true)
===================================================

添加路径或路径数组指示的所有文件。如果路径解析为目录，则 ``$recursive`` 会包含子目录。

addFile(string $file) / addFiles(array $files)
==============================================

将单个文件或多个文件添加到当前输入文件列表。文件必须是实际文件的绝对路径。

removeFile(string $file) / removeFiles(array $files)
====================================================

从当前输入文件列表中移除单个文件或多个文件。

addDirectory(string $directory, bool $recursive = false)
========================================================
addDirectories(array $directories, bool $recursive = false)
===========================================================

添加目录或多个目录中的所有文件，可选是否递归子目录。目录必须是实际目录的绝对路径。

***************
过滤文件
***************

removePattern(string $pattern, string $scope = null)
====================================================
retainPattern(string $pattern, string $scope = null)
====================================================

通过模式（和可选作用域）过滤当前文件列表，移除或保留匹配文件。

``$pattern`` 可以是完整正则表达式（如 ``'#\A[A-Za-z]+\.php\z#'``）或类似 ``glob()`` 的伪正则表达式（如 ``'*.css'``）。

如果提供 ``$scope``，则只有该目录下或其子目录中的文件会被考虑（即 ``$scope`` 外的文件始终保留）。未提供作用域时，所有文件都会参与过滤。

示例：

.. literalinclude:: files/015.php


.. _file-collections-retain-multiple-patterns:

retainMultiplePatterns(array $pattern, string $scope = null)
============================================================

提供与 ``retainPattern()`` 相同的功能，但接受模式数组来保留匹配所有模式的文件。

示例：

.. literalinclude:: files/016.php

****************
检索文件
****************

get(): string[]
===============

返回所有已加载输入文件的数组。

.. note:: ``FileCollection`` 实现了 ``IteratorAggregate`` 接口，因此可以直接操作（例如 ``foreach ($collection as $file)``）。
