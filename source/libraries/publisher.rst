#########
Publisher
#########

Publisher 库提供了使用强大的检测和错误检查在项目内复制文件的方法。

.. contents::
    :local:
    :depth: 2

*******************
加载库
*******************

因为 Publisher 实例针对其源和目标,所以这个库不通过 ``Services`` 提供,而应该直接实例化或扩展。例如:

.. literalinclude:: publisher/001.php

*****************
概念和用法
*****************

``Publisher`` 解决了在后端框架中工作时的一些常见问题:

* 我如何维护具有版本依赖性的项目资产?
* 我如何管理上传和其他需要网络访问的“动态”文件?
* 当框架或模块发生更改时,我如何更新我的项目?
* 组件如何向现有项目注入新内容?

最基本意义上,发布就是将一个或多个文件复制到项目中。``Publisher`` 扩展了 ``FileCollection`` 来执行流式样式的命令链,以读取、过滤和处理输入文件,然后将它们复制或合并到目标目标中。你可以根据需要在控制器或其他组件中使用 ``Publisher``,或者通过扩展类并利用 ``spark publish`` 进行发现来规划发布。

按需使用
=========

通过实例化该类的新实例直接访问 ``Publisher``:

.. literalinclude:: publisher/002.php

默认情况下,源和目标分别设置为 ``ROOTPATH`` 和 ``FCPATH``,使 ``Publisher`` 可以轻松获取项目中的任何文件并使其可通过 Web 访问。或者,你可以在构造函数中传递一个新的源或源和目标:

.. literalinclude:: publisher/003.php

一旦所有文件都准备就绪,使用输出命令之一(**copy()** 或 **merge()**)将暂存的文件处理到它们的目标位置:

.. literalinclude:: publisher/004.php

请参阅 :ref:`reference` 以获取可用方法的完整描述。

自动化和发现
========================

你可能有在应用程序部署或维护的一部分中嵌入了定期发布任务。``Publisher`` 利用强大的 ``Autoloader`` 来定位任何准备发布的子类:

.. literalinclude:: publisher/005.php

默认情况下, ``discover()`` 将在所有命名空间中搜索“Publishers”目录,但你可以指定不同的目录,它将返回找到的任何子类:

.. literalinclude:: publisher/006.php

大多数时候你不需要自己处理发现,只需使用提供的“publish”命令:

.. code-block:: console

    php spark publish

默认情况下,在你的类扩展上 ``publish()`` 将从你的 ``$source`` 添加所有文件并合并到你的目标位置,在冲突时覆盖。

安全性
========

为了防止模块向你的项目注入恶意代码, ``Publisher`` 包含一个配置文件,其中定义了允许作为目标的目录和文件模式。默认情况下,文件只能发布到你的项目中(以防止访问文件系统的其余部分), ``public/`` 文件夹 (``FCPATH``) 只会接收以下扩展名的文件:

* Web 资源:css、scss、js、map
* 非可执行 Web 文件:htm、html、xml、json、webmanifest
* 字体:ttf、eot、woff、woff2
* 图像:gif、jpg、jpeg、tif、tiff、png、webp、bmp、ico、svg

如果你需要为项目添加或调整安全性,请更改 ``app/Config/Publisher.php`` 中的 ``Config\Publisher`` 的 ``$restrictions`` 属性。

********
示例
********

这里有一些示例用例及其实现来帮助你开始发布。

文件同步示例
=================

你想在主页上显示“每日照片”图像。你有每日照片的订阅源,但你需要将实际文件放入项目中可以浏览的位置,如 **public/images/daily_photo.jpg**。你可以设置 :doc:`自定义命令 </cli/cli_commands>` 每天运行一次来处理此操作:

.. literalinclude:: publisher/007.php

现在运行 ``spark publish:daily`` 将使你的主页图像保持更新。如果照片来自外部 API 呢?你可以使用 ``addUri()`` 代替 ``addPath()`` 来下载远程资源并发布它:

.. literalinclude:: publisher/008.php

资产依赖项示例
==========================

你想将前端库“Bootstrap”集成到你的项目中,但频繁的更新使跟踪它变得很麻烦。你可以在项目中创建发布定义来通过扩展 ``Publisher`` 来同步前端资产。所以 **app/Publishers/BootstrapPublisher.php** 可能如下所示:

.. literalinclude:: publisher/009.php

.. note:: 在执行命令之前，必须先创建目录 ``$destination``。

现在通过 Composer 添加依赖项并调用 ``spark publish`` 来运行发布:

.. code-block:: console

    composer require twbs/bootstrap
    php spark publish

... 然后你会在项目中得到类似下面的结果::

    public/.htaccess
    public/favicon.ico
    public/index.php
    public/robots.txt
    public/
        bootstrap/
            css/
                bootstrap.min.css
                bootstrap-utilities.min.css.map
                bootstrap-grid.min.css
                bootstrap.rtl.min.css
                bootstrap.min.css.map
                bootstrap-reboot.min.css
                bootstrap-utilities.min.css
                bootstrap-reboot.rtl.min.css
                bootstrap-grid.min.css.map
            js/
                bootstrap.esm.min.js
                bootstrap.bundle.min.js.map
                bootstrap.bundle.min.js
                bootstrap.min.js
                bootstrap.esm.min.js.map
                bootstrap.min.js.map

模块部署示例
=========================

你希望允许使用你流行的身份验证模块的开发者能够扩展 Migration、Controller 和 Model 的默认行为。你可以为应用程序创建自己的模块“发布”命令来注入这些组件以供使用:

.. literalinclude:: publisher/010.php

现在当你的模块用户运行 ``php spark auth:publish`` 时,会向他们的项目添加以下内容::

    app/Controllers/AuthController.php
    app/Database/Migrations/2017-11-20-223112_create_auth_tables.php.php
    app/Models/LoginModel.php
    app/Models/UserModel.php

.. _reference:

*****************
库参考
*****************

.. note:: ``Publisher`` 是 :doc:`FileCollection </libraries/files>` 的扩展,因此可以访问读取和过滤文件的所有这些方法。

支持方法
===============

[static] discover(string $directory = 'Publishers'): Publisher[]
----------------------------------------------------------------

发现指定命名空间目录中的所有 Publishers 并返回。例如,如果 **app/Publishers/FrameworkPublisher.php** 和 **myModule/src/Publishers/AssetPublisher.php** 都存在并扩展了 ``Publisher``,那么 ``Publisher::discover()`` 会返回每个的一个实例。

publish(): bool
---------------

处理完整的输入-过程-输出链。默认情况下,这相当于调用 ``addPath($source)`` 和 ``merge(true)``,但子类通常会提供自己的实现。在运行 ``spark publish`` 时,会在所有发现的 Publisher 上调用 ``publish()``。返回成功或失败。

getScratch(): string
--------------------

返回临时工作区,如有必要则创建它。某些操作使用中间存储来暂存文件和更改,这提供了一个瞬态的可写目录的路径,你也可以使用它。

getErrors(): array<string, Throwable>
-------------------------------------

返回最后一次写入操作的任何错误。数组的键是导致错误的文件,值是捕获的 Throwable。使用 Throwable 的 ``getMessage()`` 来获取错误消息。

addPath(string $path, bool $recursive = true)
---------------------------------------------

添加相对于 ``$source`` 的实际文件或目录指示的所有文件。如果相对路径解析为目录,则 ``$recursive`` 将包含子目录。

addPaths(array $paths, bool $recursive = true)
----------------------------------------------

添加相对于 ``$source`` 的实际文件或目录指示的所有文件。如果相对路径解析为目录,则 ``$recursive`` 将包含子目录。

addUri(string $uri)
-------------------

使用 ``CURLRequest`` 下载 URI 的内容到临时工作区,然后将结果文件添加到列表中。

addUris(array $uris)
--------------------

使用 ``CURLRequest`` 将 URI 的内容下载到临时工作区,然后将结果文件添加到列表中。

.. note:: 所做的 CURL 请求是一个简单的 ``GET``,并使用响应主体作为文件内容。某些远程文件可能需要自定义请求才能正确处理。

输出文件
================

wipe()
------

从 ``$destination`` 中删除所有文件、目录和子目录。

.. important:: 想清楚再使用。

copy(bool $replace = true): bool
--------------------------------

将所有文件复制到 ``$destination`` 中。这不会重新创建目录结构,因此来自当前列表的每个文件最终都会结束在同一目标目录中。使用 ``$replace`` 会导致文件在已经存在现有文件时被覆盖。返回成功或失败,使用 ``getPublished()`` 和 ``getErrors()`` 来排查故障。要注意基本名称冲突,例如:

.. literalinclude:: publisher/011.php

merge(bool $replace = true): bool
---------------------------------

将所有文件以适当的相对子目录复制到 ``$destination`` 中。与 ``$source`` 匹配的任何文件都将被放置到 ``$destination`` 中的等效目录中,从而有效地创建一个“镜像”或“rsync”操作。使用 ``$replace`` 会导致文件在已经存在现有文件时被覆盖;由于目录已合并,这不会影响目标中的其他文件。返回成功或失败,使用 ``getPublished()`` 和 ``getErrors()`` 来排查故障。

例子:

.. literalinclude:: publisher/012.php

.. _publisher-modifying-files:

修改文件
===============

replace(string $file, array $replaces): bool
--------------------------------------------

.. versionadded:: 4.3.0

替换 ``$file`` 内容。第二个参数 ``$replaces`` 数组指定要搜索的字符串作为键,替换为值。

.. literalinclude:: publisher/013.php

addLineAfter(string $file, string $line, string $after): bool
-------------------------------------------------------------

.. versionadded:: 4.3.0

在包含特定字符串 ``$after`` 的行之后添加 ``$line``。

.. literalinclude:: publisher/014.php

addLineBefore(string $file, string $line, string $after): bool
--------------------------------------------------------------

.. versionadded:: 4.3.0

在包含特定字符串 ``$after`` 的行之前添加 ``$line``。

.. literalinclude:: publisher/015.php
