############
Publisher 类
############

Publisher 类提供稳健的检测和错误检查机制，用于在项目内复制文件。

.. contents::
    :local:
    :depth: 2

*******************
加载类
*******************

由于 Publisher 实例与源目录和目标目录绑定，该类不通过 ``Services`` 提供，
而应直接实例化或继承。例如：

.. literalinclude:: publisher/001.php

*****************
概念与用法
*****************

``Publisher`` 解决了使用后端框架时遇到的几个常见问题：

* 如何管理带有版本依赖的项目资源？
* 如何管理上传等需要 Web 可访问的“动态”文件？
* 框架或模块更新时如何同步项目？
* 组件如何向现有项目注入新内容？

最基本的发布操作就是将一个或多个文件复制到项目中。``Publisher`` 继承 ``FileCollection``，
支持以链式调用的流畅风格读取、过滤和处理输入文件，然后将其复制或合并到目标目录。
可在控制器或其他组件中按需使用 ``Publisher``，也可通过继承该类并利用 ``spark publish`` 发现机制来预置发布任务。

按需使用
=========

直接实例化 ``Publisher`` 类即可使用：

.. literalinclude:: publisher/002.php

默认情况下，源目录和目标目录分别设为 ``ROOTPATH`` 和 ``FCPATH``，
便于 ``Publisher`` 从项目中取出任意文件并使其可通过 Web 访问。
也可在构造函数中传入新的源目录，或同时传入源目录和目标目录：

.. literalinclude:: publisher/003.php

文件暂存完成后，使用输出命令（**copy()** 或 **merge()**）将暂存文件处理到目标目录：

.. literalinclude:: publisher/004.php

可用方法的完整说明参见 :ref:`reference`。

自动化与发现
========================

项目中可能有常规发布的任务需要嵌入到部署或维护流程中。``Publisher`` 利用强大的 ``Autoloader``
来定位任何已就绪的子类：

.. literalinclude:: publisher/005.php

默认情况下，``discover()`` 会在所有命名空间中搜索 "Publishers" 目录，
也可指定不同的目录，将返回找到的所有子类：

.. literalinclude:: publisher/006.php

大多数情况下无需自行处理发现逻辑，直接使用内置的 "publish" 命令即可：

.. code-block:: console

    php spark publish

默认情况下，继承类的 ``publish()`` 会将 ``$source`` 中的所有文件合并到目标目录，
发生冲突时覆盖。

.. _discovery-in-a-specific-namespace:

在指定命名空间中发现
---------------------------------

.. versionadded:: 4.6.0

自 v4.6.0 起，还可以扫描指定的命名空间。这不仅能减少扫描的文件数量，
还能避免重复运行 Publisher。只需在 ``discover()`` 方法的第二个参数中指定目标根命名空间即可。

.. literalinclude:: publisher/016.php

指定的命名空间必须是 CodeIgniter 已知的。可使用 "spark namespaces" 命令查看所有命名空间列表：

.. code-block:: console

    php spark namespaces

"publish" 命令还提供 ``--namespace`` 选项，用于在搜索可能来自库的 Publisher 时指定命名空间。

.. code-block:: console

    php spark publish --namespace Namespace\Vendor\Package

安全性
========

为防止恶意代码注入项目，``Publisher`` 包含一个配置文件，用于定义允许的目录和文件模式作为目标。
默认情况下，文件只能发布到项目内（防止访问文件系统的其他部分），而 **public/** 目录
（``FCPATH``）仅接收以下扩展名的文件：

* Web 资源：css、scss、js、map
* 非可执行 Web 文件：htm、html、xml、json、webmanifest
* 字体：ttf、eot、woff、woff2
* 图像：gif、jpg、jpeg、tif、tiff、png、webp、bmp、ico、svg

如需添加或调整项目的安全性设置，请修改 **app/Config/Publisher.php** 中 ``Config\Publisher`` 的 ``$restrictions`` 属性。

********
示例
********

以下是一些示例用例及其实现，帮助快速上手发布功能。

文件同步示例
=================

你希望在首页展示“每日图片”。虽然已有每日图片的订阅源，
但需要将实际文件放入项目的 Web 可访问的位置 **public/images/daily_photo.jpg**。
可设置一个每日运行的 :doc:`自定义命令 </cli/cli_commands>` 来处理此任务：

.. literalinclude:: publisher/007.php

运行 ``spark publish:daily`` 即可保持首页图片为最新状态。
如果图片来自外部 API 呢？可使用 ``addUri()`` 替代 ``addPath()`` 来下载远程资源并发布：

.. literalinclude:: publisher/008.php

资源依赖示例
==========================

想将前端库 "Bootstrap" 集成到项目中，但频繁更新令人难以跟进。
可在项目中通过继承 ``Publisher`` 来创建发布定义，以同步前端资源。
**app/Publishers/BootstrapPublisher.php** 可能如下所示：

.. literalinclude:: publisher/009.php

.. note:: 执行命令前必须先创建 ``$destination`` 目录。

然后通过 Composer 添加依赖并调用 ``spark publish`` 执行发布：

.. code-block:: console

    composer require twbs/bootstrap
    php spark publish

... 最终会得到类似这样的结构::

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

希望使用热门认证模块的开发者能够扩展现有的迁移、控制器和模型的默认行为。
可创建模块专属的 "publish" 命令，以向应用注入这些组件供使用：

.. literalinclude:: publisher/010.php

模块用户运行 ``php spark auth:publish`` 后，项目中会添加以下文件::

    app/Controllers/AuthController.php
    app/Database/Migrations/2017-11-20-223112_create_auth_tables.php.php
    app/Models/LoginModel.php
    app/Models/UserModel.php

.. _reference:

*****************
库参考
*****************

.. note:: ``Publisher`` 继承自 :doc:`FileCollection </libraries/files>`，因此可以使用其所有方法来读取和过滤文件。

辅助方法
===============

[static] discover(string $directory = 'Publishers'): Publisher[]
----------------------------------------------------------------

发现并返回指定命名空间目录中的所有 Publisher。例如，如果
**app/Publishers/FrameworkPublisher.php** 和 **myModule/src/Publishers/AssetPublisher.php** 都存在且为
``Publisher`` 的子类，则 ``Publisher::discover()`` 将分别返回各自的实例。

publish(): bool
---------------

处理完整的输入-处理-输出链。默认情况下等价于调用 ``addPath($source)``
和 ``merge(true)``，但子类通常会提供自己的实现。运行 ``spark publish`` 时，
会在所有发现的 Publisher 上调用 ``publish()``。
返回成功或失败状态。

getScratch(): string
--------------------

返回临时工作区路径，如不存在则创建。某些操作使用中间存储来暂存
文件和更改，此方法提供一个临时的可写目录路径，也可供使用。

getErrors(): array<string, Throwable>
-------------------------------------

返回上次写入操作的所有错误。数组键为导致错误的文件，
值为捕获到的 Throwable。可在 Throwable 上调用 ``getMessage()`` 获取错误消息。

addPath(string $path, bool $recursive = true)
---------------------------------------------

添加相对路径指定的所有文件。路径为相对于 ``$source`` 的实际文件或目录引用。
如果相对路径解析为目录，``$recursive`` 将包含子目录。

addPaths(array $paths, bool $recursive = true)
----------------------------------------------

添加相对路径数组指定的所有文件。路径为相对于 ``$source`` 的实际文件或目录引用。
如果相对路径解析为目录，``$recursive`` 将包含子目录。

addUri(string $uri)
-------------------

使用 ``CURLRequest`` 将 URI 内容下载到临时工作区，然后将结果文件添加到列表中。

addUris(array $uris)
--------------------

使用 ``CURLRequest`` 将多个 URI 内容下载到临时工作区，然后将结果文件添加到列表中。

.. note:: 发起的 CURL 请求是简单的 ``GET`` 请求，使用响应体作为文件内容。某些
    远程文件可能需要自定义请求才能正确处理。

文件输出方法
================

wipe()
------

从 ``$destination`` 中删除所有文件、目录和子目录。

.. important:: 谨慎使用。

copy(bool $replace = true): bool
--------------------------------

将所有文件复制到 ``$destination``。此方法不会重建目录结构，因此当前列表中的每个文件
都会落入同一目标目录。使用 ``$replace`` 时，若文件已存在则会覆盖。返回成功或失败状态，
可使用 ``getPublished()`` 和 ``getErrors()`` 排查失败原因。
注意同名文件可能导致的冲突，例如：

.. literalinclude:: publisher/011.php

merge(bool $replace = true): bool
---------------------------------

将所有文件复制到 ``$destination`` 中相应的相对子目录中。
匹配 ``$source`` 的文件会被放置到 ``$destination`` 中等价的目录中，
实际上实现了"镜像"或 "rsync" 操作。使用 ``$replace`` 时，
若文件已存在则会覆盖；由于目录是合并而非替换，这不会影响目标目录中的其他文件。
返回成功或失败状态，可使用 ``getPublished()`` 和 ``getErrors()`` 排查失败原因。

示例：

.. literalinclude:: publisher/012.php

.. _publisher-modifying-files:

文件修改方法
===============

replace(string $file, array $replaces): bool
--------------------------------------------

.. versionadded:: 4.3.0

替换 ``$file`` 的内容。第二个参数 ``$replaces`` 数组指定搜索字符串作为键，替换内容作为值。

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
