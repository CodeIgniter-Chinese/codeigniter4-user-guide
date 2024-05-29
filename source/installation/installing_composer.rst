Composer 安装
#####################

.. contents::
    :local:
    :depth: 2

Composer 可以通过两种方式在你的系统上安装 CodeIgniter4。

.. important:: CodeIgniter4 需要 Composer 2.0.14 或更高版本。

.. note:: 如果你不熟悉 Composer,我们建议你先阅读
    `基本用法 <https://getcomposer.org/doc/01-basic-usage.md>`_。

第一个方法描述了如何使用 CodeIgniter4 创建一个项目骨架（App Starter），你可以将其作为新 Web 应用的基础。下面描述的第二个方法允许你将 CodeIgniter4 添加到已有的 Web 应用中。

.. note:: 如果你使用 Git 仓库来存储代码或与他人协作，那么 **vendor** 文件夹通常会被 “git 忽略”。在这种情况下，当你将仓库克隆到一个新系统时，你需要执行 ``composer install``（如果你想更新所有 Composer 依赖项，则执行 ``composer update``）。

App Starter
===========

`CodeIgniter 4 app starter <https://github.com/codeigniter4/appstarter>`_
仓库包含一个骨架应用程序,其中包含对最新版本框架的 Composer 依赖项。

此安装技术适用于希望启动基于 CodeIgniter4 的新项目的开发人员。

安装
------------

在项目根目录上层文件夹中:

.. code-block:: console

    composer create-project codeigniter4/appstarter 项目根目录

上述命令将创建一个 **项目根目录** 文件夹。

如果省略“项目根目录”参数,该命令将创建一个“appstarter”文件夹,可以根据需要重命名。

.. note:: 在 v4.4.0 之前，CodeIgniter 的自动加载器不允许在某些操作系统上的文件名中使用非法的特殊字符。可以使用的符号包括 ``/``、``_``、``.``、``:``、``\`` 和空格。因此，如果你将 CodeIgniter 安装在包含特殊字符（如 ``(``、``)`` 等）的文件夹中，CodeIgniter 将无法正常工作。从 v4.4.0 开始，这个限制已经被移除。

.. important:: 当你将应用部署到生产服务器时,不要忘记运行以下命令:

    .. code-block:: console

        composer install --no-dev

    上述命令将只移除开发环境下的 Composer 软件包,这些软件包在生产环境中不需要。这将大大减少 vendor 文件夹的大小。

安装先前版本
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

例如，你可能希望在 v4.5.0 发布后安装 v4.4.8。

在这种情况下，在命令中指定版本：

.. code-block:: console

    composer create-project codeigniter4/appstarter:4.4.8 project-root

然后，在项目根文件夹中打开 **composer.json**，并指定框架版本：

.. code-block:: text

    "require": {
        ...
        "codeigniter4/framework": "4.4.8"
    },

然后，运行 ``composer update`` 命令。

.. note:: 当你在 **composer.json** 中使用固定版本号如 ``"codeigniter4/framework": "4.4.8"`` 时，``composer update`` 命令将不会更新框架到最新版本。请参见 `Writing Version Constraints`_ 了解如何指定版本。

.. _Writing Version Constraints: https://getcomposer.org/doc/articles/versions.md#writing-version-constraints

初始配置
---------------------

安装后,需要进行一些初始配置。有关详细信息,请参阅 :ref:`initial-configuration`。

.. _app-starter-upgrading:

升级
---------

每当有新版本发布时,在项目根目录的命令行中运行:

.. code-block:: console

    composer update

阅读 :doc:`升级说明 <upgrading>` 和 :doc:`变更日志 <../changelogs/index>`，并检查重大变更和增强功能。

升级到指定版本
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

例如，你可能希望在 v4.5.0 发布后从 v4.4.7 升级到 v4.4.8。

在这种情况下，在项目根文件夹中打开 **composer.json**，并指定框架版本：

.. code-block:: text

    "require": {
        ...
        "codeigniter4/framework": "4.4.8"
    },

然后，运行 ``composer update`` 命令。

.. note:: 当你在 **composer.json** 中使用固定版本号如 ``"codeigniter4/framework": "4.4.8"`` 时，``composer update`` 命令将不会更新框架到最新版本。请参见 `Writing Version Constraints`_ 了解如何指定版本。

优点
----

安装简单;易于更新。

缺点
----

更新后,你仍然需要检查 **项目空间** 中的文件更改(根目录、app、public、writable),并合并它们。

.. note:: 有一些第三方 CodeIgniter 模块可用于协助合并项目空间的更改:
    `在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

结构
---------

设置后项目中的文件夹:

- app、public、tests、writable
- vendor/codeigniter4/framework/system

最新开发版本
--------------

App Starter 仓库带有 ``builds`` 脚本,可在当前稳定版本和框架的最新开发分支之间切换 Composer 源。此脚本适用于愿意使用最新的未发布更改(可能不稳定)的开发者。

`开发用户指南 <https://codeigniter4.github.io/CodeIgniter4/>`_ 可以在线访问。
请注意,这与已发布的用户指南不同,并将明确适用于 develop 分支。

最新开发版更新
^^^^^^^^^^^^^^^^^^^^^

在你的项目根目录中执行以下命令：

.. code-block:: console

    php builds development

上述命令将更新 **composer.json**，将其指向工作仓库的 ``develop`` 分支，并更新配置文件和 XML 文件中的相应路径。

使用 ``builds`` 命令后，请确保运行 ``composer update``，以使你的 vendor 文件夹与最新的目标构建同步。然后，根据需要检查 :doc:`upgrading` 并更新项目文件。

下一个次要版本
^^^^^^^^^^^^^^^^^^

如果你想使用下一个次要版本的分支，在使用 ``builds`` 命令后手动编辑 **composer.json**。

如果你尝试使用 ``4.6`` 分支，请将版本更改为 ``4.6.x-dev``::

    "require": {
        "php": "^8.1",
        "codeigniter4/codeigniter4": "4.6.x-dev"
    },

然后运行 ``composer update``，以使你的 vendor 文件夹与最新的目标构建同步。然后，根据需要检查升级指南（**user_guide_src/source/installation/upgrade_{version}.rst**）并更新项目文件。

恢复到稳定版本
^^^^^^^^^^^^^^^^^^^^^^^^

要恢复更改，请运行：

.. code-block:: console

    php builds release

将 CodeIgniter4 添加到现有项目中
==========================================

“手动安装”中描述的相同 `CodeIgniter 4 框架 <https://github.com/codeigniter4/framework>`_
仓库也可以使用 Composer 添加到现有项目中。

安装
------------

在 ``app`` 文件夹中开发你的应用程序, ``public`` 文件夹将是你的文档根目录。

在项目根目录中:

.. code-block:: console

    composer require codeigniter4/framework

.. important:: 将应用程序部署到生产服务器时,不要忘记运行以下命令:

    .. code-block:: console

        composer install --no-dev

    上述命令将只移除开发环境下的 Composer 软件包,这些软件包在生产环境中不需要。这将大大减少 vendor 文件夹的大小。

设置
----------

    1. 从 **vendor/codeigniter4/framework** 复制 **app**、**public**、**tests** 和 **writable** 文件夹到项目根目录
    2. 从 **vendor/codeigniter4/framework** 复制 **env**、**phpunit.xml.dist** 和 **spark** 文件到项目根目录
    3. 你将必须调整 **app/Config/Paths.php** 中的 ``$systemDirectory`` 属性,以引用 vendor 目录,例如 ``__DIR__ . '/../../vendor/codeigniter4/framework/system'``。

初始配置
---------------------

需要进行一些初始配置。有关详细信息,请参阅 :ref:`initial-configuration`。

.. _adding-codeigniter4-upgrading:

升级
---------

每当有新版本发布时,在项目根目录的命令行中运行:

.. code-block:: console

    composer update

阅读 :doc:`升级说明 <upgrading>` 和 :doc:`变更日志 <../changelogs/index>`，并检查重大变更和增强功能。

升级到指定版本
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

例如，你可能希望在 v4.5.0 发布后从 v4.4.7 升级到 v4.4.8。

在这种情况下，在项目根文件夹中打开 **composer.json**，并指定框架版本：

.. code-block:: text

    "require": {
        ...
        "codeigniter4/framework": "4.4.8"
    },

然后，运行 ``composer update`` 命令。

优点
----

相对简单的安装;易于更新。

缺点
----

更新后,你仍需检查 **项目空间** 中的文件更改(根目录、app、public、writable)。

.. note:: 有一些第三方 CodeIgniter 模块可用于协助合并项目空间的更改:
    `在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

结构
---------

设置后项目中的文件夹:

- app、public、tests、writable
- vendor/codeigniter4/framework/system

翻译安装
=========================

如果你想利用系统消息翻译,可以以类似的方式将它们添加到项目中。

在项目根目录的命令行中:

.. code-block:: console

    composer require codeigniter4/translations

每次执行 ``composer update`` 时,这些都会与框架一起更新。
