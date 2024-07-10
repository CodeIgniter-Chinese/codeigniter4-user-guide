#################
自动加载文件
#################

.. contents::
    :local:
    :depth: 2

每个应用程序由许多不同位置的大量类组成。
框架为核心功能提供类。你的应用程序将具有许多库、模型和其他实体才能正常工作。你可能会使用第三方类。跟踪每个文件的位置,并在一系列 ``require()`` 中硬编码该位置是一个巨大的头疼且极易出错。这就是自动加载器的用武之地。

***********************
CodeIgniter4 自动加载器
***********************

CodeIgniter 提供了一个非常灵活的自动加载器，只需进行很少的配置即可使用。它可以定位符合 `PSR-4`_ 自动加载目录结构的各个命名空间类。

.. _PSR-4: https://www.php-fig.org/psr/psr-4/

自动加载器本身工作良好,但也可以与其他自动加载器(如 `Composer <https://getcomposer.org>`_)一起使用,如果需要的话,甚至可以与你自己的自定义自动加载器一起使用。
因为它们都通过 `spl_autoload_register <https://www.php.net/manual/en/function.spl-autoload-register.php>`_ 注册,所以它们顺序工作,不会相互干扰。

自动加载器始终处于活动状态,在框架执行开始时通过 ``spl_autoload_register()`` 注册。

.. important:: 你应该始终小心文件名的大小写。许多开发人员在 Windows 或 macOS 上使用不区分大小写的文件系统开发。
    然而,大多数服务器环境使用区分大小写的文件系统。如果文件名大小写不正确,自动加载程序无法在服务器上找到该文件。

*************
配置
*************

初始配置在 **app/Config/Autoload.php** 中完成。该文件包含两个主要数组:一个用于类映射,一个用于 PSR-4 兼容命名空间。

.. _autoloader-namespaces:

命名空间
==========

组织类的推荐方法是为应用程序文件创建一个或多个命名空间。

配置文件中的 ``$psr4`` 数组允许你将命名空间映射到可以找到这些类的目录:

.. literalinclude:: autoloader/001.php

每行的键是命名空间本身。这个不需要尾部反斜杠。
值是可以找到类的目录位置。

默认情况下，命名空间 ``App`` 位于 **app** 目录中，命名空间 ``Config`` 位于 **app/Config** 目录中。

如果你在这些位置根据 `PSR-4`_ 创建类文件，自动加载器将自动加载它们。

.. _confirming-namespaces:

确认命名空间
=====================

你可以使用 ``spark namespaces`` 命令检查命名空间配置:

.. code-block:: console

    php spark namespaces

.. _autoloader-application-namespace:

应用程序命名空间
=====================

默认情况下,应用程序目录被映射到 ``App`` 命名空间。你必须为应用程序目录中的控制器、库或模型添加命名空间,它们将在 ``App`` 命名空间下被找到。

Config 命名空间
----------------

配置文件位于 ``Config`` 命名空间中，而不是你可能预期的 ``App\Config`` 中。这使得核心系统文件即使在应用命名空间发生变化时也能始终找到它们。

.. note:: 自 v4.5.3 appstarter 版本起，``Config\\`` 命名空间已被添加到 **composer.json** 的 ``autoload.psr-4`` 中。

更改应用命名空间
----------------------

你可以通过编辑 **app/Config/Constants.php** 文件并在 ``APP_NAMESPACE`` 设置下设置新的命名空间值来更改此命名空间:

.. literalinclude:: autoloader/002.php
   :lines: 2-

如果你使用 Composer 自动加载器，你还需要在 **composer.json** 中更改 ``App`` 命名空间，然后运行 ``composer dump-autoload``。

.. code-block:: text

    {
        ...
        "autoload": {
            "psr-4": {
                "App\\": "app/"    <-- Change
            },
            ...
        },
        ...
    }

.. note:: 自 v4.5.0 appstarter 起，``App\\`` 命名空间已被添加到 **composer.json** 的 ``autoload.psr-4`` 中。如果你的 **composer.json** 中没有此项，添加它可能会提升你应用的自动加载性能。

你需要修改引用当前命名空间的所有现有文件。

类映射
========

CodeIgniter 通过不通过文件系统进行额外的 ``is_file()`` 调用来获取系统最后的性能,广泛使用类映射。你可以使用类映射链接到未使用命名空间的第三方库:

如果你使用的第三方库不是 Composer 包且没有命名空间，你可以使用类映射（classmap）来加载这些类：

.. literalinclude:: autoloader/003.php

每行的键是你要定位的类的名称。值是定位它的路径。

****************
Composer 支持
****************

默认情况下会自动初始化 Composer 支持。

默认情况下,它会在 ``ROOTPATH . 'vendor/autoload.php'`` 查找 Composer 的自动加载文件。如果由于任何原因需要更改该文件的位置,可以修改 **app/Config/Constants.php** 中定义的值。

加载器的优先级
=======================

如果同一个命名空间在 CodeIgniter 和 Composer 中同时定义，Composer 的自动加载器将优先尝试定位文件。

.. note:: 在 v4.5.0 之前，如果同一个命名空间在 CodeIgniter 和 Composer 中同时定义，CodeIgniter 的自动加载器会优先尝试定位文件。

.. _file-locator-caching:

*******************
FileLocator 缓存
*******************

.. versionadded:: 4.5.0

**FileLocator** 负责查找文件或从文件中获取类名，这无法通过 PHP 自动加载来实现。

为了提高其性能，FileLocator 缓存已经被实现。

工作原理
============

- 在析构时，如果缓存数据已更新，则将 FileLocator 找到的所有数据保存到缓存文件中。
- 如果有缓存数据可用，则在实例化时恢复缓存数据。

缓存数据会永久使用。

如何删除缓存数据
=========================

一旦存储，缓存数据将永不过期。

因此，如果你添加或删除文件，或者更改现有文件路径或命名空间，旧的缓存数据将被返回，你的应用可能无法正常工作。

在这种情况下，你必须手动删除缓存文件。如果你通过 Composer 添加了 CodeIgniter 包，你也需要删除缓存文件。

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

或者你可以使用 ``spark optimize`` 命令来启用它。

.. note::
    此属性无法通过
    :ref:`环境变量 <configuration-classes-and-environment-variables>` 重写。
