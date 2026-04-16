###########################
处理上传文件
###########################

相比直接使用 PHP 的 ``$_FILES`` 数组，CodeIgniter 处理表单上传文件更加简单、安全。该类扩展了 :doc:`File 类 </libraries/files>`，因此具备 File 类的全部功能。

.. note:: 这与 CodeIgniter 3 中的文件上传类不同。此类提供对上传文件的原始接口，附带少量便捷功能。

.. contents::
    :local:
    :depth: 2

.. _file-upload-form-tutorial:

*************************
文件上传教程
*************************

上传文件的一般流程如下：

-  显示上传表单，用户选择文件并上传。
-  表单提交后，文件上传到指定的目标位置。
-  上传过程中，文件会根据设定的偏好进行验证，确保允许上传。
-  上传成功后，向用户显示成功消息。

以下是一个简短的教程来演示此过程，后面附有参考信息。

创建上传表单
========================

使用文本编辑器创建名为 **upload_form.php** 的表单，将以下代码放入其中并保存到 **app/Views** 目录：

.. literalinclude:: uploaded_files/001.php

此处使用了表单辅助函数来创建表单起始标签。文件上传需要 multipart 表单，辅助函数会生成正确的语法。

同时可以看到 ``$errors`` 变量，用于在用户操作出错时显示错误消息。

成功页面
================

使用文本编辑器创建名为 **upload_success.php** 的表单，将以下代码放入其中并保存到 **app/Views** 目录::

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Upload Form</title>
    </head>
    <body>

    <h3>Your file was successfully uploaded!</h3>

    <ul>
        <li>name: <?= esc($uploaded_fileinfo->getBasename()) ?></li>
        <li>size: <?= esc($uploaded_fileinfo->getSizeByUnit('kb')) ?> KB</li>
        <li>extension: <?= esc($uploaded_fileinfo->guessExtension()) ?></li>
    </ul>

    <p><?= anchor('upload', 'Upload Another File!') ?></p>

    </body>
    </html>

控制器
==============

使用文本编辑器创建名为 **Upload.php** 的控制器，将以下代码放入其中并保存到 **app/Controllers** 目录：

.. literalinclude:: uploaded_files/002.php

只有 :ref:`rules-for-file-uploads` 可用于验证上传的文件。

因此也无法使用 ``required`` 规则，如果文件是必需的，应改用 ``uploaded`` 规则。

注意，传递给 ``$this->validateData()`` 的第一个参数是空数组（``[]``）。这是因为文件验证规则会直接从 Request 对象获取上传文件的数据。

如果表单中除文件上传外还有其他字段，将字段数据作为第一个参数传递即可。

路由
==========

使用文本编辑器打开 **app/Config/Routes.php**，添加以下两条路由：

.. literalinclude:: uploaded_files/021.php

上传目录
====================

上传的文件存储在 **writable/uploads/** 目录中。

试一试！
========

要尝试此表单，访问类似以下 URL 的地址::

    example.com/index.php/upload/

应该会看到一个上传表单。尝试上传一个图片文件（**jpg**、**gif**、**png** 或 **webp** 均可）。如果控制器中的路径正确，应该就能成功上传。

.. _uploaded-files-accessing-files:

***************
访问文件
***************

所有文件
=========

上传的文件可以通过 PHP 的 ``$_FILES`` 超全局变量直接访问。这个数组在处理多个文件同时上传时存在重大缺陷，并且存在许多开发者不了解的潜在安全漏洞。CodeIgniter 通过统一接口来标准化文件的使用，解决了这两个问题。

通过当前的 ``IncomingRequest`` 实例访问文件。要检索此请求中上传的所有文件，使用 ``getFiles()``。将返回一个由 ``CodeIgniter\HTTP\Files\UploadedFile`` 实例表示的文件数组：

.. literalinclude:: uploaded_files/003.php

当然，文件 input 标签的命名方式有多种，除最简单的情况外，其他都可能产生奇怪的结果。数组的返回方式和你期望的一样。对于最简单的用法，可能只提交一个文件::

    <input type="file" name="avatar">

将返回一个简单的数组::

    [
        'avatar' => // UploadedFile 实例,
    ];

.. note:: UploadedFile 实例对应 ``$_FILES``。即使用户仅点击提交按钮而未上传任何文件，该实例仍然存在。可通过 UploadedFile 的 ``isValid()`` 方法检查文件是否真正上传。详见 :ref:`verify-a-file`。

如果使用了数组表示法命名，输入字段类似::

    <input type="file" name="my-form[details][avatar]">

``getFiles()`` 返回的数组类似::

    [
         'my-form' => [
            'details' => [
                'avatar' => // UploadedFile 实例
            ],
        ],
    ]


在某些情况下，可以指定一个文件数组进行上传::

    Upload an avatar: <input type="file" name="my-form[details][avatars][]">
    Upload an avatar: <input type="file" name="my-form[details][avatars][]">

此时返回的文件数组类似::

    [
        'my-form' => [
            'details' => [
                'avatar' => [
                    0 => // UploadedFile 实例,
                    1 => // UploadedFile 实例,
                ],
            ],
        ],
    ]

单个文件
===========

如果只需访问单个文件，可以使用 ``getFile()`` 直接获取文件实例。将返回一个 ``CodeIgniter\HTTP\Files\UploadedFile`` 实例：

最简单的用法
--------------

最简单的用法，可能只提交一个文件::

    <input type="file" name="userfile">

将返回一个简单的文件实例：

.. literalinclude:: uploaded_files/004.php

数组表示法
--------------

如果使用了数组表示法来命名，input 标签类似::

    <input type="file" name="my-form[details][avatar]">

获取文件实例：

.. literalinclude:: uploaded_files/005.php

多个文件
==============

::

    <input type="file" name="images[]" multiple>

在控制器中：

.. literalinclude:: uploaded_files/006.php

其中 ``images`` 是表单字段名称。

如果有多个文件使用相同的名称，可以使用 ``getFile()`` 逐个检索每个文件。

在控制器中：

.. literalinclude:: uploaded_files/007.php

也可以使用 ``getFileMultiple()``，获取同名的上传文件数组：

.. literalinclude:: uploaded_files/008.php

另一个示例::

    Upload an avatar: <input type="file" name="my-form[details][avatars][]">
    Upload an avatar: <input type="file" name="my-form[details][avatars][]">

在控制器中：

.. literalinclude:: uploaded_files/009.php

.. note:: 使用 ``getFiles()`` 更为合适。

*********************
文件操作
*********************

获取 UploadedFile 实例后，即可安全地获取文件信息，并将文件移动到新位置。

.. _verify-a-file:

验证文件
=============

调用 ``isValid()`` 方法检查文件是否通过 HTTP 上传且无错误：

.. literalinclude:: uploaded_files/010.php

如上例所示，如果文件上传出错，可通过 ``getError()`` 和 ``getErrorString()`` 方法获取错误代码（整数）和错误消息。通过此方法可以发现以下错误：

* 文件超出 ``upload_max_filesize`` ini 指令限制。
* 文件超出表单定义的上传限制。
* 文件仅部分上传。
* 未上传任何文件。
* 文件无法写入磁盘。
* 文件无法上传：缺少临时目录。
* 文件上传被 PHP 扩展停止。

文件名
==========

getName()
---------

使用 ``getName()`` 方法获取客户端提供的原始文件名。通常是客户端发送的文件名，不应完全信任。如果文件已被移动，将返回移动后的最终文件名：

.. literalinclude:: uploaded_files/011.php

getClientName()
---------------

始终返回客户端上传文件的原始名称，即使文件已被移动：

.. literalinclude:: uploaded_files/012.php

getTempName()
-------------

要获取上传时创建的临时文件的完整路径，可以使用 ``getTempName()`` 方法：

.. literalinclude:: uploaded_files/013.php

其他文件信息
===============

getClientExtension()
--------------------

根据上传的文件名返回原始文件扩展名：

.. literalinclude:: uploaded_files/014.php

.. warning:: 这不是可信来源。如需可信版本，请改用 ``guessExtension()``。

getClientMimeType()
-------------------

返回客户端提供的文件 MIME 类型。这不是可信值。如需可信版本，请改用 ``getMimeType()``：

.. literalinclude:: uploaded_files/015.php

getClientPath()
---------------

.. versionadded:: 4.4.0

当客户端通过目录上传文件时，返回 `webkitRelativePath <https://developer.mozilla.org/zh-CN/docs/Web/API/File/webkitRelativePath>`_。在 PHP 8.1 以下版本中，返回 ``null``。

.. literalinclude:: uploaded_files/023.php

移动文件
============

使用原始文件名
----------------------

每个文件都可以通过 ``move()`` 方法移动到新位置。第一个参数指定目标目录：

.. literalinclude:: uploaded_files/016.php

默认情况下使用原始文件名。

使用新文件名
-----------------

可以将新文件名作为第二个参数传入：

.. literalinclude:: uploaded_files/017.php

覆盖现有文件
-------------------------

默认情况下，如果目标文件已存在，将使用新文件名。例如，如果目录中已存在 **image_name.jpg**，则文件名会自动变为 **image_name_1.jpg**。

要将第三个参数设为 ``true`` 即可覆盖现有文件：

.. literalinclude:: uploaded_files/022.php

检查文件是否已被移动
-----------------------

文件移动后会删除临时文件。通过 ``hasMoved()`` 方法检查文件是否已被移动，返回布尔值：

.. literalinclude:: uploaded_files/018.php

移动失败时
-----------------

在以下情况下，移动上传文件可能会失败并抛出 ``HTTPException``：

- 文件已被移动
- 文件未成功上传
- 文件移动操作失败（如权限不足）

存储文件
===========

每个文件都可通过 ``store()`` 方法移动到新位置。

最简单的用法，可能只提交一个文件::

    <input type="file" name="userfile">

默认情况下，上传文件保存在 **writable/uploads** 目录中。会自动创建 **YYYYMMDD** 文件夹和随机文件名。返回文件路径：

.. literalinclude:: uploaded_files/019.php

可以将目标目录作为第一个参数传入。将新文件名作为第二个参数传入：

.. literalinclude:: uploaded_files/020.php

在以下情况下，移动上传文件可能会失败并抛出 ``HTTPException``：

- 文件已被移动
- 文件未成功上传
- 文件移动操作失败（如权限不足）
