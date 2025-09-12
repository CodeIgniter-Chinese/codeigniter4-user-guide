#################
自动加载文件
#################

.. contents::
    :local:
    :depth: 2

每个应用程序都包含大量位于不同位置的类。框架为核心功能提供了类，你的应用程序需要
许多库、模型和其他实体来正常工作，项目中可能还会用到第三方类。追踪每个文件
的确切位置，并在代码中通过一系列 ``require()`` 硬编码这些位置，
这会带来巨大的麻烦且极易出错。自动加载器（autoloader）正是为了解决这个问题而生。

***********************
CodeIgniter4 自动加载器
***********************

CodeIgniter 提供了一个非常灵活的自动加载器，几乎无需配置即可使用。
它能够定位遵循 `PSR-4`_ 自动加载目录结构的独立命名空间类。

.. _PSR-4: https://www.php-fig.org/psr/psr-4/

自动加载器可以独立工作，也可以与其他自动加载器（如 `Composer <https://getcomposer.org>`_）
或你自定义的自动加载器协同工作。因为它们都通过
`spl_autoload_register <https://www.php.net/manual/zh/function.spl-autoload-register.php>`_
进行注册，所以会按顺序执行，互不干扰。

自动加载器始终处于激活状态，在框架执行开始时就通过 ``spl_autoload_register()`` 进行了注册。

.. important:: 你应始终注意文件名的大小写。许多开发者在 Windows 或 macOS 的
    大小写不敏感的文件系统上开发，但大多数服务器环境使用的是大小写敏感的文件系统。
    如果文件名大小写错误，自动加载器将无法在服务器上找到文件。

*************
配置
*************

初始配置在 **app/Config/Autoload.php** 文件中完成。该文件包含两个主要数组：
一个用于类映射（classmap），另一个用于 PSR-4 兼容的命名空间。

.. _autoloader-namespaces:

命名空间
==========

组织类文件的推荐方法是为你的应用程序文件创建一个或多个命名空间。

配置文件中的 ``$psr4`` 数组允许你将命名空间映射到类文件所在目录：

.. literalinclude:: autoloader/001.php

每一行的键是命名空间本身，不需要末尾的反斜杠。
值是类文件所在目录的路径。

默认情况下，``App`` 命名空间位于 **app** 目录，
``Config`` 命名空间位于 **app/Config** 目录。

如果按照 `PSR-4`_ 规范在指定位置创建类文件，自动加载器会自动加载它们。

.. _confirming-namespaces:

确认命名空间
=====================

你可以通过 ``spark namespaces`` 命令检查命名空间配置：

.. code-block:: console

    php spark namespaces

.. _autoloader-application-namespace:

应用程序命名空间
=====================

默认情况下，应用程序目录对应 ``App`` 命名空间。你必须为应用程序目录中的控制器、
库或模型指定命名空间，它们将位于 ``App`` 命名空间下。

Config 命名空间
----------------

配置文件位于 ``Config`` 命名空间，而不是你可能预期的 ``App\Config``。
这使得核心系统文件总能找到它们，即使应用命名空间发生了改变。

.. note:: 自 v4.5.3 版本的 appstarter 起，已将 ``Config\\`` 命名空间添加到
    **composer.json** 的 ``autoload.psr-4`` 中。

更改 App 命名空间
----------------------

你可以通过编辑 **app/Config/Constants.php** 文件，在 ``APP_NAMESPACE`` 设置下
修改新的命名空间值来更改此命名空间：

.. literalinclude:: autoloader/002.php
   :lines: 2-

如果你使用 Composer 自动加载器，还需要修改 **composer.json** 中的 ``App`` 命名空间，
并运行 ``composer dump-autoload``。

.. code-block:: text

    {
        ...
        "autoload": {
            "psr-4": {
                "App\\": "app/"    <-- 修改此处
            },
            ...
        },
        ...
    }

.. note:: 自 v4.5.0 版本的 appstarter 起，已将 ``App\\`` 命名空间添加到
    **composer.json** 的 ``autoload.psr-4`` 中。如果你的 **composer.json** 没有
    包含此项，添加它可能会提升应用程序的自动加载性能。

你将需要修改任何引用当前命名空间的现有文件。

类映射
========

如果你使用非 Composer 包且未命名空间化的第三方库，
可以使用类映射来加载这些类：

.. literalinclude:: autoloader/003.php

每一行的键是你想定位的类名，值是该类的路径。

****************
Composer 支持
****************

Composer 支持默认情况下会自动初始化。

默认情况下，它会在 ``ROOTPATH . 'vendor/autoload.php'`` 处查找 Composer 的自动加载文件。
如果因任何原因需要更改该文件的位置，可以修改 **app/Config/Constants.php** 中定义的值。

自动加载器的优先级
=======================

如果同一个命名空间在 CodeIgniter 和 Composer 中都有定义，
Composer 的自动加载器将优先尝试定位文件。

.. note:: 在 v4.5.0 之前，如果同一个命名空间在 CodeIgniter 和 Composer 中都有定义，
    CodeIgniter 的自动加载器会优先尝试定位文件。

.. _file-locator-caching:

*******************
FileLocator 缓存
*******************

.. versionadded:: 4.5.0

**FileLocator** 负责查找文件或从文件中获取类名，
这是 PHP 自动加载无法实现的功能。

为了提高其性能，已实现 FileLocator 缓存。

工作原理
============

- 如果缓存数据已更新，在析构时将 FileLocator 找到的所有数据保存到缓存文件中。

- 实例化时，如果缓存数据可用，则恢复缓存数据。

缓存数据将永久使用。

如何删除缓存数据
=========================

一旦存储，缓存数据永不失效。

因此，如果你添加或删除了文件，或更改了现有文件路径或命名空间，
旧的缓存数据将被返回，导致应用程序无法正常工作。

在这种情况下，你必须手动删除缓存文件。如果你通过 Composer 添加了 CodeIgniter 包，
也需要删除缓存文件。

你可以使用 ``spark cache:clear`` 命令：

.. code-block:: console

    php spark cache:clear

或者直接删除 **writable/cache/FileLocatorCache** 文件。

.. note::
    ``spark optimize`` 命令会清除缓存。

如何启用 FileLocator 缓存
=================================

在 **app/Config/Optimize.php** 中将以下属性设置为 ``true``：

    public bool $locatorCacheEnabled = true;

或者你可以使用 ``spark optimize`` 命令来启用。

.. note::
    此属性不能被
    :ref:`环境变量 <configuration-classes-and-environment-variables>` 覆盖。
