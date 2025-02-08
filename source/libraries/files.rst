##################
文件处理
##################

CodeIgniter 提供了一个 File 类，它封装了 `SplFileInfo <https://www.php.net/manual/zh/class.splfileinfo.php>`_ 类并添加了一些便捷方法。该类是 :doc:`上传文件 </libraries/uploaded_files>` 和 :doc:`图像 </libraries/images>` 的基类。

.. contents::
    :local:
    :depth: 2

获取 File 实例
***********************

你可以通过将文件路径传入构造函数来创建新的 File 实例。

.. literalinclude:: files/001.php
    :lines: 2-

默认情况下，文件不需要存在。但是你可以传递额外的 ``true`` 参数来检查文件是否存在，如果不存在则会抛出 ``FileNotFoundException()``。

利用 Spl 特性
***********************

一旦获得实例，你就可以使用 SplFileInfo 类的全部功能，包括：

.. literalinclude:: files/002.php
    :lines: 2-

新增功能
************

除了 SplFileInfo 类的所有方法外，还提供了一些新工具。

getRandomName()
===============

你可以使用 ``getRandomName()`` 方法生成带有当前时间戳前缀的加密安全随机文件名。这在移动文件时重命名文件特别有用，可以使文件名不可猜测：

.. literalinclude:: files/003.php
    :lines: 2-

getSize()
=========

返回文件的大小（以字节为单位）：

.. literalinclude:: files/004.php
    :lines: 2-

如果文件不存在或发生错误，将抛出 ``RuntimeException``。

getSizeByUnit()
===============

.. deprecated:: 4.6.0

默认返回文件大小（以字节为单位）。你可以传入 ``'kb'`` 或 ``'mb'`` 作为第一个参数，分别以千字节或兆字节为单位获取结果：

.. literalinclude:: files/005.php
    :lines: 2-

如果文件不存在或发生错误，将抛出 ``RuntimeException``。

.. _file-get-size-by-binary-unit:

getSizeByBinaryUnit()
=====================

.. versionadded:: 4.6.0

默认返回文件大小（以字节为单位）。你可以传入不同的 FileSizeUnit 值作为第一个参数，分别以 KiB、MiB 等单位获取结果。可以通过第二个参数传入精度值来定义小数位数。

.. literalinclude:: files/017.php
    :lines: 4-

如果文件不存在或发生错误，将抛出 ``RuntimeException``。

.. _file-get-size-by-metric-unit:

getSizeByMetricUnit()
=====================

.. versionadded:: 4.6.0

默认返回文件大小（以字节为单位）。你可以传入不同的 FileSizeUnit 值作为第一个参数，分别以 KB、MB 等单位获取结果。可以通过第二个参数传入精度值来定义小数位数。

.. literalinclude:: files/018.php
    :lines: 4-

如果文件不存在或发生错误，将抛出 ``RuntimeException``。

getMimeType()
=============

检索文件的媒体类型（MIME 类型）。使用尽可能安全的方法来确定文件类型：

.. literalinclude:: files/006.php
    :lines: 2-

guessExtension()
================

尝试基于可信的 ``getMimeType()`` 方法确定文件扩展名。如果 MIME 类型未知，则返回 null。这通常比仅使用文件名提供的扩展名更可靠。使用 **app/Config/Mimes.php** 中的值来确定扩展名：

.. literalinclude:: files/007.php
    :lines: 2-

移动文件
============

每个文件都可以使用 ``move()`` 方法移动到新位置。第一个参数指定目标目录：

.. literalinclude:: files/008.php
    :lines: 2-

默认使用原始文件名。你可以通过第二个参数指定新文件名：

.. literalinclude:: files/009.php
    :lines: 2-

``move()`` 方法会返回移动后文件的新 File 实例，因此如果需要使用新位置，必须捕获结果：

.. literalinclude:: files/010.php
    :lines: 2-
