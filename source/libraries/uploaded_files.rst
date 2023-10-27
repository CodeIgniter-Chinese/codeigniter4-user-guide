###########################
处理上传的文件
###########################

在 CodeIgniter 中通过表单使用文件上传功能将会比直接使用 PHP 的 ``$_FILES`` 数组更加简单和安全。这是 :doc:`文件类 </libraries/files>` 的扩展,因此获得了该类所有的特性。

.. note:: 这和 CodeIgniter v3.x 中的文件上传类不太一样。这里提供了一个访问上传文件的原始接口和一些小特性。

.. contents::
    :local:
    :depth: 2

***********
过程
***********

上传一个文件涉及以下一般过程:

- 显示一个上传表单,允许用户选择一个文件并上传。
- 当表单提交时,文件被上传到你指定的目的地。
- 在上传过程中,会验证文件是否被允许上传,基于你设置的首选项。
- 一旦上传完成,用户将看到一个成功的消息。

为了演示这个过程,这里是一个简单的教程。之后你会找到参考信息。

创建上传表单
========================

使用文本编辑器,创建一个名为 **upload_form.php** 的表单。在其中放入下面的代码,并保存到你的 **app/Views/** 目录:

.. literalinclude:: uploaded_files/001.php

你会注意到我们使用了一个表单辅助函数来创建表单开标签。文件上传需要一个多部分表单,所以辅助函数帮我们创建了正确的语法。你也会注意到我们有一个 ``$errors`` 变量。这是为了在用户做错事时显示错误信息。

成功页面
================

使用文本编辑器,创建一个名为 **upload_success.php** 的页面。在其中放入下面的代码,并保存到你的 **app/Views/** 目录:

.. code-block:: html

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>上传表单</title>
    </head>
    <body>

    <h3>你的文件上传成功!</h3>

    <ul>
        <li>名称:<?= esc($uploaded_fileinfo->getBasename()) ?></li>
        <li>大小:<?= esc($uploaded_fileinfo->getSizeByUnit('kb')) ?> KB</li>
        <li>扩展名:<?= esc($uploaded_fileinfo->guessExtension()) ?></li>
    </ul>

    <p><?= anchor('upload', '上传另一个文件!') ?></p>

    </body>
    </html>

控制器
==============

使用文本编辑器,创建一个名为 **Upload.php** 的控制器。在其中放入下面的代码,并保存到你的 **app/Controllers/** 目录:

.. literalinclude:: uploaded_files/002.php

.. note:: 由于 HTML 文件上传字段的值不存在,它存储在 ``$_FILES`` 全局变量中,所以只能使用 :ref:`文件上传规则 <rules-for-file-uploads>` 来验证上传的文件,不能使用 :doc:`验证器 </libraries/validation>`。
    ``required`` 规则也不能使用,请使用 ``uploaded`` 代替。

路由
==========

使用文本编辑器,打开 **app/Config/Routes.php**。在其中添加以下两个路由:

.. literalinclude:: uploaded_files/021.php

上传目录
====================

上传的文件存储在 **writable/uploads/** 目录下。

试一试!
=======

要测试你的表单,使用类似这样的 URL 访问你的网站::

    example.com/index.php/upload/

你应该可以看到一个上传表单。尝试上传一个图像文件(可以是 **jpg**、**gif**、**png** 或 **webp**)。如果控制器中的路径正确,它应该可以工作。

.. _uploaded-files-accessing-files:

***************
访问文件
***************

所有文件
=========

当你上传文件时,可以通过 PHP 的 ``$_FILES`` 超全局变量以原生方式访问它们。当处理一次上传的多个文件时,这个数组有一些重大缺陷,也存在许多开发者可能不知道的潜在安全问题。CodeIgniter 通过把文件操作标准化到一个通用接口后面,可以帮助解决这两个问题。

文件是通过当前的 ``IncomingRequest`` 实例访问的。要检索与这个请求一起上传的所有文件,使用 ``getFiles()``。它将返回一个由 ``CodeIgniter\HTTP\Files\UploadedFile`` 实例表示的文件数组:

.. literalinclude:: uploaded_files/003.php

当然,文件输入有多种命名方式,任何不简单的都会产生奇怪的结果。数组的返回方式和你期望的一样。使用最简单的方式,单个文件可能像这样提交:

.. code-block:: html

    <input type="file" name="avatar">

它将返回一个简单的像这样的数组:

.. code-block:: php

    [
        'avatar' => // 上传的文件实例
    ];

.. note:: UploadedFile 实例对应 ``$_FILES`` 。即使用户只是点击提交按钮而没有上传任何文件,该实例也仍然存在。你可以通过 UploadedFile 的 ``isValid()`` 方法检查文件是否真的被上传。参见 :ref:`verify-a-file`。

如果你为名称使用了数组表示法,输入看起来像这样:

.. code-block:: html

    <input type="file" name="my-form[details][avatar]">

``getFiles()`` 返回的数组看起来更像这样:

.. code-block:: php

    [
         'my-form' => [
            'details' => [
                'avatar' => // 上传的文件实例
            ],
        ],
    ]

在某些情况下,你可以指定一个文件数组来上传:

.. code-block:: html

    上传头像: <input type="file" name="my-form[details][avatars][]">
    上传头像: <input type="file" name="my-form[details][avatars][]">

在这种情况下,返回的文件数组更像是:

.. code-block:: php

    [
        'my-form' => [
            'details' => [
                'avatar' => [
                    0 => // 上传的文件实例,
                    1 => // 上传的文件实例,
                ],
            ],
        ],
    ]

单个文件
===========

如果你只需要访问单个文件,可以使用 ``getFile()`` 直接获取文件实例。它将返回一个 ``CodeIgniter\HTTP\Files\UploadedFile`` 实例:

最简单的用法
--------------

使用最简单的方式,单个文件可能这样提交:

.. code-block:: html

    <input type="file" name="userfile">

它将返回一个简单的文件实例,像这样:

.. literalinclude:: uploaded_files/004.php

数组表示法
--------------

如果你为名称使用数组表示法,输入看起来像这样:

.. code-block:: html

    <input type="file" name="my-form[details][avatar]">

获取文件实例:

.. literalinclude:: uploaded_files/005.php

多个文件
==============

.. code-block:: html

    <input type="file" name="images[]" multiple>

在控制器中:

.. literalinclude:: uploaded_files/006.php

其中 ``images`` 是表单字段名称的循环。

如果有多个相同名称的文件,你可以使用 ``getFile()`` 来单独获取每个文件。

在控制器中:

.. literalinclude:: uploaded_files/007.php

你可能会发现使用 ``getFileMultiple()`` 更方便,它可以获取一个具有相同名称的上传文件数组:

.. literalinclude:: uploaded_files/008.php

另一个例子:

.. code-block:: html

    上传头像: <input type="file" name="my-form[details][avatars][]">
    上传头像: <input type="file" name="my-form[details][avatars][]">

在控制器中:

.. literalinclude:: uploaded_files/009.php

.. note:: 使用 ``getFiles()`` 更合适。

*********************
处理文件
*********************

一旦你获取到 UploadedFile 实例,你就可以以安全的方式检索关于文件的信息,也可以将文件移动到新位置。

.. _verify-a-file:

验证文件
=============

你可以通过调用 ``isValid()`` 方法来检查文件是否真的通过 HTTP 上传且没有错误:

.. literalinclude:: uploaded_files/010.php

如这个例子所示,如果文件有上传错误,你可以通过 ``getError()`` 和 ``getErrorString()`` 方法获取错误码(整数)和错误消息。可以通过这个方法发现以下错误:

* 文件超过了你的 ``upload_max_filesize`` ini 设置。
* 文件超过了表单中定义的上传限制。
* 文件只被部分上传。
* 没有文件被上传。
* 文件无法写入磁盘。
* 文件上传失败:缺少临时目录。
* 文件上传被 PHP 扩展停止。

文件名
==========

getName()
---------

你可以使用 ``getName()`` 方法获取客户提供的原始文件名。这通常是客户端发送的文件名,不应该相信它。如果文件已经移动,这将返回移动后的文件的最终名称:

.. literalinclude:: uploaded_files/011.php

getClientName()
---------------

即使文件已经移动,也总是返回上传文件的原始名称,就是客户端发送的名称:

.. literalinclude:: uploaded_files/012.php

getTempName()
-------------

要获取上传过程中创建的临时文件的完整路径,你可以使用 ``getTempName()`` 方法:

.. literalinclude:: uploaded_files/013.php

其他文件信息
===============

getClientExtension()
--------------------

根据上传的文件名返回原始文件扩展名:

.. literalinclude:: uploaded_files/014.php

.. warning:: 这不是可信的来源。要获取可信的版本,请改用 ``guessExtension()``。

getClientMimeType()
-------------------

返回客户端提供的文件的 MIME 类型。这不是可信的值。要获取可信版本,请使用 ``getMimeType()`` :

.. literalinclude:: uploaded_files/015.php

getClientPath()
---------------

.. versionadded:: 4.4.0

当客户端通过目录上传方式上传文件时，返回上传文件的 `webkit 相对路径 <https://developer.mozilla.org/en-US/docs/Web/API/File/webkitRelativePath>`_。
在 PHP 8.1 以下的版本中，返回 ``null``。

.. literalinclude:: uploaded_files/023.php

移动文件
============

使用原始文件名
----------------------

每个文件都可以使用贴切的 ``move()`` 方法移动到新位置。第一个参数是要移动文件的目录:

.. literalinclude:: uploaded_files/016.php

默认情况下,使用原始文件名。

指定新文件名
-----------------

你可以通过第二个参数指定一个新文件名:

.. literalinclude:: uploaded_files/017.php

覆盖现有文件
-------------------------

默认情况下,如果目标文件已经存在,会使用一个新的文件名。
例如,如果 **image_name.jpg** 已经存在于目录中,
那么文件名会自动设置为 **image_name_1.jpg**。

你可以传入 ``true`` 作为第三个参数来覆盖现有文件:

.. literalinclude:: uploaded_files/022.php

检查文件是否移动
-----------------------

一旦临时文件被删除,表示文件已经移动。你可以使用返回布尔值的 ``hasMoved()`` 方法来检查文件是否已经移动:

.. literalinclude:: uploaded_files/018.php

移动失败时
-----------------

在几种情况下,移动上传的文件可能会失败,并抛出一个 HTTPException:

- 文件已经移动过
- 文件上传不成功
- 文件移动操作失败(例如权限不正确)

存储文件
===========

每个文件都可以使用同名的 ``store()`` 方法移动到新位置。

使用最简单的用法,单个文件可能这样提交:

.. code-block:: html

    <input type="file" name="userfile">

默认情况下,上传的文件将保存在 **writable/uploads** 目录下。会创建 **YYYYMMDD** 文件夹
和随机文件名。返回文件路径:

.. literalinclude:: uploaded_files/019.php

你可以指定一个目录作为第一个参数来移动文件。通过第二个参数指定一个新文件名:

.. literalinclude:: uploaded_files/020.php

在几种情况下,移动上传的文件可能会失败,并抛出一个 ``HTTPException``:

- 文件已经移动过
- 文件上传不成功
- 文件移动操作失败(例如权限不正确)
