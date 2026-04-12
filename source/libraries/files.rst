##################
处理文件
##################

CodeIgniter 提供了一个 File 类，用于封装 `SplFileInfo <https://www.php.net/manual/zh/class.splfileinfo.php>`_ 类，
并提供一些额外的便捷方法。这个类也是 :doc:`上传文件 </libraries/uploaded_files>`
和 :doc:`图像 </libraries/images>` 的基类。

.. contents::
    :local:
    :depth: 2

获取 File 实例
***********************

通过在构造函数中传入文件路径，即可创建新的 File 实例。

.. literalinclude:: files/001.php
    :lines: 2-

默认情况下，文件不需要实际存在。不过，可额外传入参数 ``true`` 来检查文件是否存在；
如果不存在，则抛出 ``FileNotFoundException()``。

利用 Spl 的能力
***********************

获得实例后，即可使用 ``SplFileInfo`` 类的完整功能，包括：

.. literalinclude:: files/002.php
    :lines: 2-

新增功能
************

除了 SplFileInfo 类的全部方法外，File 还提供了一些新工具。

getRandomName()
===============

通过 ``getRandomName()`` 方法，可生成一个密码学安全的随机文件名，并在前面附加当前时间戳。
在移动文件时，这对于重命名文件特别有用，因为文件名将无法被猜测：

.. literalinclude:: files/003.php
    :lines: 2-

getSize()
=========

返回文件大小，单位为字节：

.. literalinclude:: files/004.php
    :lines: 2-

如果文件不存在或发生错误，将抛出 ``RuntimeException``。

getSizeByUnit()
===============

.. deprecated:: 4.6.0

默认以字节为单位返回文件大小。第一个参数可传入 ``'kb'`` 或 ``'mb'``，
分别以 KiB 或 MiB 返回结果：

.. literalinclude:: files/005.php
    :lines: 2-

如果文件不存在或发生错误，将抛出 ``RuntimeException``。


.. _file-get-size-by-binary-unit:

getSizeByBinaryUnit()
=====================

.. versionadded:: 4.6.0

默认以字节为单位返回文件大小。第一个参数可传入不同的 FileSizeUnit 值，
分别以 KiB、MiB 等单位返回结果。第二个参数可传入精度值，用于定义小数位数。

.. literalinclude:: files/017.php
    :lines: 4-

如果文件不存在或发生错误，将抛出 ``RuntimeException``。


.. _file-get-size-by-metric-unit:

getSizeByMetricUnit()
=====================

.. versionadded:: 4.6.0

默认以字节为单位返回文件大小。第一个参数可传入不同的 FileSizeUnit 值，
分别以 kB、MB 等单位返回结果。第二个参数可传入精度值，用于定义小数位数。

.. literalinclude:: files/018.php
    :lines: 4-

如果文件不存在或发生错误，将抛出 ``RuntimeException``。

getMimeType()
=============

获取文件的媒体类型（MIME 类型）。在判定文件类型时，会尽可能使用被认为更安全的方
法：

.. literalinclude:: files/006.php
    :lines: 2-

guessExtension()
================

尝试基于可信的 ``getMimeType()`` 方法判断文件扩展名。如果 MIME 类型未知，则返回
null。与直接使用文件扩展名相比，这通常更可信。扩展名的判断依据为
**app/Config/Mimes.php** 中的值：

.. literalinclude:: files/007.php
    :lines: 2-

移动文件
============

每个文件都可以使用 ``move()`` 方法移动到新位置。第一个参数为要移
动到的目录：

.. literalinclude:: files/008.php
    :lines: 2-

默认使用原始文件名。第二个参数可传入新的文件名：

.. literalinclude:: files/009.php
    :lines: 2-

``move()`` 方法会返回一个新的 File 实例，表示已重新定位的文件。因此，如需使
用新位置，必须保存返回结果：

.. literalinclude:: files/010.php
    :lines: 2-
