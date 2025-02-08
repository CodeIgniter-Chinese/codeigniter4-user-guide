#########
Publisher
#########

Publisher 类库提供了一种在项目内复制文件的方法，具备强大的检测和错误检查功能。

.. contents::
    :local:
    :depth: 2

*******************
加载类库
*******************

由于 Publisher 实例与其源路径和目标路径相关联，因此该类库不通过 ``Services`` 提供，而应直接实例化或扩展。例如：

.. literalinclude:: publisher/001.php

*****************
概念与用法
*****************

``Publisher`` 解决了在后端框架中工作时的一些常见问题：

* 如何维护具有版本依赖关系的项目资源？
* 如何管理需要 Web 访问的上传文件和其他"动态"文件？
* 当框架或模块变更时如何更新项目？
* 组件如何将新内容注入现有项目？

本质上，发布操作等同于将文件复制到项目中。``Publisher`` 扩展了 ``FileCollection``，通过流式方法链来读取、过滤和处理输入文件，然后将它们复制或合并到目标路径。你可以在控制器或其他组件中按需使用 ``Publisher``，也可以通过扩展类并利用 ``spark publish`` 的发现机制来分阶段执行发布操作。

按需使用
=========

通过直接实例化类来使用 ``Publisher``：

.. literalinclude:: publisher/002.php

默认情况下，源路径和目标路径分别设置为 ``ROOTPATH`` 和 ``FCPATH``，这使得 ``Publisher`` 可以轻松访问项目中的任何文件并使其可通过 Web 访问。你也可以在构造函数中传入新的源路径或同时传入源路径和目标路径：

.. literalinclude:: publisher/003.php

当所有文件准备就绪后，使用输出命令（**copy()** 或 **merge()**）将暂存文件处理到目标路径：

.. literalinclude:: publisher/004.php

完整方法描述请参阅 :ref:`reference`。

自动化与发现
========================

你可能需要在应用部署或维护时执行定期发布任务。``Publisher`` 利用强大的 ``Autoloader`` 来定位所有准备发布的子类：

.. literalinclude:: publisher/005.php

默认情况下 ``discover()`` 会在所有命名空间中搜索 "Publishers" 目录，但你可以指定其他目录来返回找到的子类：

.. literalinclude:: publisher/006.php

大多数情况下你无需自行处理发现机制，直接使用提供的 "publish" 命令即可：

.. code-block:: console

    php spark publish

默认情况下，类扩展中的 ``publish()`` 会从 ``$source`` 添加所有文件并将其合并到目标路径，遇到冲突时覆盖。

.. _discovery-in-a-specific-namespace:

在指定命名空间中发现
---------------------------------

.. versionadded:: 4.6.0

自 v4.6.0 起，你还可以扫描特定命名空间。这不仅减少了需要扫描的文件数量，也避免了重新运行 Publisher 的需求。只需在 ``discover()`` 方法的第二个参数中指定目标根命名空间：

.. literalinclude:: publisher/016.php

指定的命名空间必须已注册到 CodeIgniter。你可以使用 "spark namespaces" 命令查看所有命名空间列表：

.. code-block:: console

    php spark namespaces

"publish" 命令也提供 ``--namespace`` 选项来定义搜索 Publisher 的命名空间，适用于来自库的情况：

.. code-block:: console

    php spark publish --namespace Namespace\Vendor\Package

安全性
========

为防止模块向项目注入恶意代码，``Publisher`` 包含一个配置文件来定义允许的目标目录和文件模式。默认情况下，文件只能发布到项目内（防止访问文件系统其他部分），且 **public/** 文件夹（``FCPATH``）仅接收以下扩展名的文件：

* Web 资源：css, scss, js, map
* 非可执行 Web 文件：htm, html, xml, json, webmanifest
* 字体：ttf, eot, woff, woff2
* 图像：gif, jpg, jpeg, tif, tiff, png, webp, bmp, ico, svg

如需调整项目安全设置，请修改 **app/Config/Publisher.php** 中 ``Config\Publisher`` 的 ``$restrictions`` 属性。

********
示例
********

以下是几个典型用例及其实现，帮助你快速上手发布操作。

文件同步示例
=================

你希望在首页展示"每日图片"。虽然已有每日图片源，但需要将实际文件同步到项目的可浏览位置 **public/images/daily_photo.jpg**。可以设置每日运行的 :doc:`自定义命令 </cli/cli_commands>` 来处理：

.. literalinclude:: publisher/007.php

现在运行 ``spark publish:daily`` 即可保持首页图片更新。如果图片来自外部 API 怎么办？可以使用 ``addUri()`` 替代 ``addPath()`` 来下载远程资源并发布：

.. literalinclude:: publisher/008.php

资源依赖示例
==========================

你想在项目中集成前端库"Bootstrap"，但频繁更新带来维护难题。可以通过扩展 ``Publisher`` 创建发布定义来同步前端资源。例如 **app/Publishers/BootstrapPublisher.php** 可能如下：

.. literalinclude:: publisher/009.php

.. note:: 目录 ``$destination`` 必须在执行命令前创建。

现在通过 Composer 添加依赖并调用 ``spark publish`` 执行发布：

.. code-block:: console

    composer require twbs/bootstrap
    php spark publish

最终会生成如下结构::

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

你希望让使用流行认证模块的开发者能够扩展默认的 Migration、Controller 和 Model 行为。可以创建模块专属的"publish"命令来向应用中注入这些组件：

.. literalinclude:: publisher/010.php

现在当模块用户运行 ``php spark auth:publish`` 时，项目中会添加以下文件::

    app/Controllers/AuthController.php
    app/Database/Migrations/2017-11-20-223112_create_auth_tables.php.php
    app/Models/LoginModel.php
    app/Models/UserModel.php

.. _reference:

*****************
类库参考
*****************

.. note:: ``Publisher`` 继承自 :doc:`FileCollection </libraries/files>`，因此可以使用该类的所有文件读取和过滤方法。

支持方法
===============

[static] discover(string $directory = 'Publishers'): Publisher[]
----------------------------------------------------------------

发现并返回指定命名空间目录中的所有 Publisher。例如，如果同时存在 **app/Publishers/FrameworkPublisher.php** 和 **myModule/src/Publishers/AssetPublisher.php** 且都是 ``Publisher`` 的扩展，则 ``Publisher::discover()`` 会返回每个实例。

publish(): bool
---------------

处理完整的输入-处理-输出链。默认情况下等同于调用 ``addPath($source)`` 和 ``merge(true)``，但子类通常提供自己的实现。运行 ``spark publish`` 时会对所有发现的 Publisher 调用 ``publish()``。返回成功或失败状态。

getScratch(): string
--------------------

返回临时工作区路径（必要时创建）。某些操作使用中间存储来暂存文件和变更，此方法提供可写入的临时目录路径。

getErrors(): array<string, Throwable>
-------------------------------------

返回上次写入操作的错误信息。数组键是引发错误的文件路径，值是对应的 Throwable 对象。使用 Throwable 的 ``getMessage()`` 获取错误信息。

addPath(string $path, bool $recursive = true)
---------------------------------------------

添加相对路径指示的所有文件。路径是相对于 ``$source`` 的实际文件或目录引用。如果相对路径解析为目录，则 ``$recursive`` 会包含子目录。

addPaths(array $paths, bool $recursive = true)
----------------------------------------------

添加多个相对路径指示的所有文件。路径是相对于 ``$source`` 的实际文件或目录引用。如果相对路径解析为目录，则 ``$recursive`` 会包含子目录。

addUri(string $uri)
-------------------

使用 ``CURLRequest`` 将 URI 内容下载到临时工作区，然后将结果文件添加到列表。

addUris(array $uris)
--------------------

使用 ``CURLRequest`` 将多个 URI 内容下载到临时工作区，然后将结果文件添加到列表。

.. note:: CURL 请求是简单的 ``GET`` 请求并使用响应体作为文件内容。某些远程文件可能需要自定义请求处理。

文件输出方法
================

wipe()
------

删除 ``$destination`` 中的所有文件、目录和子目录。

.. important:: 谨慎使用。

copy(bool $replace = true): bool
--------------------------------

将所有文件复制到 ``$destination``。不重建目录结构，所有文件将置于同一目标目录。``$replace`` 为 true 时会覆盖现有文件。返回成功或失败状态，使用 ``getPublished()`` 和 ``getErrors()`` 排查故障。注意同名文件冲突，例如：

.. literalinclude:: publisher/011.php

merge(bool $replace = true): bool
---------------------------------

将所有文件按相对子目录结构复制到 ``$destination``。匹配 ``$source`` 的文件会置于 ``$destination`` 的对应目录，实现"镜像"或"rsync"操作。``$replace`` 为 true 时覆盖现有文件（不影响目标目录其他文件）。返回成功或失败状态，使用 ``getPublished()`` 和 ``getErrors()`` 排查故障。

示例：

.. literalinclude:: publisher/012.php

.. _publisher-modifying-files:

文件修改方法
===============

replace(string $file, array $replaces): bool
--------------------------------------------

.. versionadded:: 4.3.0

替换 ``$file`` 文件内容。第二个参数 ``$replaces`` 数组以搜索字符串为键，替换内容为值。

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
