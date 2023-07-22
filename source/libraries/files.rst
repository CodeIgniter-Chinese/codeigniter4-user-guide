##################
处理文件
##################

CodeIgniter 提供了一个 File 类,它封装了 `SplFileInfo <https://www.php.net/manual/en/class.splfileinfo.php>`_ 类,
并提供了一些额外的方便方法。这个类是 :doc:`上传文件 </libraries/uploaded_files>` 和 :doc:`图像 </libraries/images>` 的基类。

.. contents::
    :local:
    :depth: 2

获取 File 实例
***********************

通过在构造函数中传递文件的路径来创建一个新的 File 实例。默认情况下,文件不需要存在。但是,你可以传递一个额外的参数 “true” 来检查文件是否存在,如果文件不存在则抛出 ``FileNotFoundException()``。

.. literalinclude:: files/001.php

利用 Spl 的优势
***********************

一旦你有了一个实例,你就可以完全使用 SplFileInfo 类的功能,包括:

.. literalinclude:: files/002.php

新功能
************

除了 SplFileInfo 类中的所有方法,你还可以获取一些新工具。

getRandomName()
===============

你可以使用 ``getRandomName()`` 方法生成一个加密安全的随机文件名,文件名前面加上当前时间戳。当移动文件时,这对于使文件名不可猜测尤其有用:

.. literalinclude:: files/003.php

getSize()
=========

以字节为单位返回上传文件的大小:

.. literalinclude:: files/004.php

getSizeByUnit()
===============

以字节为单位返回上传文件的默认大小。你可以在第一个参数中传递 'kb' 或 'mb',以分别以千字节或兆字节获取结果:

.. literalinclude:: files/005.php

getMimeType()
=============

检索文件媒体类型(mime 类型)。在确定文件类型时,使用尽可能安全的方法:

.. literalinclude:: files/006.php

guessExtension()
================

尝试根据受信任的 ``getMimeType()`` 方法确定文件扩展名。如果 mime 类型未知,将返回 null。这通常是比仅使用文件名提供的扩展名更可信的来源。使用 **app/Config/Mimes.php** 中的值来确定扩展名:

.. literalinclude:: files/007.php

移动文件
============

每个文件都可以使用恰当命名的 ``move()`` 方法移动到新位置。第一个参数是要移动文件到的目录:

.. literalinclude:: files/008.php

默认情况下,使用了原始文件名。你可以通过作为第二个参数传递来指定一个新文件名:

.. literalinclude:: files/009.php

move() 方法返回重新定位文件的新的 File 实例,所以如果需要结果位置,必须捕获结果:

.. literalinclude:: files/010.php
