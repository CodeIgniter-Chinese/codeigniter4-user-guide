#################
自动加载文件
#################

.. contents::
    :local:
    :depth: 2

每个应用程序都由位于不同位置的大量类组成。框架提供了核心功能类，而应用程序则通过一系列类、模型及其它实体来实现具体功能。此外，项目还可能使用第三方类。手动追踪每个文件的位置，并在代码中通过一系列 ``requires()`` 硬编码这些路径既麻烦又容易出错。自动加载器正是为了解决这一问题而生。

***********************
CodeIgniter4 自动加载器
***********************

CodeIgniter 提供了一个配置极其灵活的自动加载器，只需极少配置即可使用。它可以定位符合 `PSR-4`_ 自动加载目录结构的命名空间类。

.. _PSR-4: https://www.php-fig.org/psr/psr-4/

该自动加载器既可以独立运行，也能根据需要与 `Composer <https://getcomposer.org>`_ 或自定义加载器协同工作。由于它们都通过 `spl_autoload_register <https://www.php.net/manual/zh/function.spl-autoload-register.php>`_ 注册，因此可以按序工作，互不干扰。

自动加载器始终处于激活状态，在框架执行之初便已通过 ``spl_autoload_register()`` 完成注册。

.. important:: 务必注意文件名的大小写。许多开发者在 Windows 或 macOS 等不区分大小写的文件系统中进行开发，但大多数服务器环境是区分大小写的。如果文件名大小写不正确，自动加载器将无法在服务器上找到对应文件。

*************
配置
*************

初始配置位于 **app/Config/Autoload.php**。该文件包含两个主要数组：一个用于类映射（classmap），另一个用于兼容 PSR-4 的命名空间。

.. _autoloader-namespaces:

命名空间
==========

建议为应用程序创建一或多个命名空间来组织类文件。

通过配置文件中的 ``$psr4`` 数组，可将命名空间映射到类文件所在的目录：

.. literalinclude:: autoloader/001.php

每一行的键名为命名空间本身，末尾无需反斜杠。对应的值为类文件所在的目录路径。

默认情况下，``App`` 命名空间对应 **app** 目录，``Config`` 命名空间对应 **app/Config** 目录。

只要在对应位置按照 `PSR-4`_ 标准创建类文件，自动加载器就会对其进行自动加载。

.. _confirming-namespaces:

确认命名空间
=====================

可通过 ``spark namespaces`` 命令检查命名空间配置：

.. code-block:: console

    php spark namespaces

.. _autoloader-application-namespace:

应用程序命名空间
=====================

默认情况下，应用程序目录被映射到 ``App`` 命名空间。必须为应用程序目录下的控制器、类或模型设置命名空间，这样即可在 ``App`` 命名空间下找到它们。

Config 命名空间
----------------

配置文件使用 ``Config`` 命名空间，而非预想中的 ``App\Config``。这确保了即便修改了应用程序命名空间，系统核心文件依然能够找到它们。

.. note:: 自 v4.5.3 版本的 appstarter 起，``Config\\`` 命名空间已添加到 **composer.json** 的 ``autoload.psr-4`` 中。

修改 App 命名空间
----------------------

如需修改此命名空间，可编辑 **app/Config/Constants.php** 文件，并在 ``APP_NAMESPACE`` 设置项中定义新值：

.. literalinclude:: autoloader/002.php
   :lines: 2-

如果使用了 Composer 自动加载，还需修改 **composer.json** 中的 ``App`` 命名空间，并执行 ``composer dump-autoload``。

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

.. note:: 自 v4.5.0 版本的 appstarter 起，``App\\`` 命名空间已添加到 **composer.json** 的 ``autoload.psr-4`` 中。如果 **composer.json** 中没有该项，手动添加可提升应用的自动加载性能。

此外，还需要同步修改所有引用了旧命名空间的现有文件。

类映射
========

如果使用了非 Composer 包且未定义命名空间的第三方库，可以通过类映射加载这些类：

.. literalinclude:: autoloader/003.php

每一行的键名是要定位的类名，对应的值则是该类所在的路径。

****************
Composer 支持
****************

默认会自动初始化 Composer 支持。

框架默认在 ``ROOTPATH . 'vendor/autoload.php'`` 查找 Composer 的自动加载文件。如需更改此文件路径，可修改 **app/Config/Constants.php** 中定义的值。

自动加载器的优先级
=======================

如果在 CodeIgniter 和 Composer 中定义了相同的命名空间，Composer 自动加载器将优先尝试定位文件。

.. note:: 在 v4.5.0 之前的版本中，如果定义了相同的命名空间，CodeIgniter 自动加载器会优先尝试定位文件。

.. _file-locator-caching:

*******************
FileLocator 缓存
*******************

.. versionadded:: 4.5.0

**FileLocator** 负责查找文件或从文件中获取类名，这些功能无法通过 PHP 原生自动加载实现。

为提升性能，框架引入了 FileLocator 缓存机制。

工作原理
============

- 如果缓存数据有更新，在析构时将 FileLocator 找到的所有数据保存到缓存文件中。
- 实例化时，如果缓存可用，则从中恢复数据。

缓存数据将永久生效。

如何删除缓存数据
=========================

缓存数据一旦存储便永不过期。

因此，如果增删文件，或者修改了现有的文件路径及命名空间，旧的缓存数据将导致应用运行异常。在这种情况下，必须手动删除缓存文件。此外，通过 Composer 添加 CodeIgniter 包后，也需要删除缓存文件。

可使用 ``spark cache:clear`` 命令：

.. code-block:: console

    php spark cache:clear

或者直接删除 **writable/cache/FileLocatorCache** 文件。

.. note::
    执行 ``spark optimize`` 命令也会清除缓存。

如何启用 FileLocator 缓存
=================================

在 **app/Config/Optimize.php** 中将以下属性设置为 ``true``：

    public bool $locatorCacheEnabled = true;

或者通过 ``spark optimize`` 命令启用。

.. note::
    该属性无法通过 :ref:`环境变量 <configuration-classes-and-environment-variables>` 覆盖。

.. warning:: 在 :doc:`Worker 模式 </installation/worker_mode>` 下运行应用时，请勿使用此选项。
