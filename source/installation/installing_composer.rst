Composer 安装
#####################

.. contents::
    :local:
    :depth: 2

可以通过两种方式使用 Composer 在系统中安装 CodeIgniter4。

.. important:: CodeIgniter4 需要 Composer 2.0.14 或更高版本。

.. note:: 如果不熟悉 Composer，建议先阅读
    `Basic usage <https://getcomposer.org/doc/01-basic-usage.md>`_。

第一种方式是使用 CodeIgniter4 创建一个骨架项目（app starter），作为新 Web 应用的基础。
第二种方式是将 CodeIgniter4 添加到现有的 Web 应用中。

.. note:: 如果使用 Git 仓库来存储代码，或与他人协作，通常会将 **vendor** 文件夹加入 “git 忽略”。
    在这种情况下，当你将仓库克隆到新的系统时，需要运行 ``composer install``
    （如果希望更新所有 Composer 依赖，则运行 ``composer update``）。

App Starter
===========

`CodeIgniter 4 app starter <https://github.com/codeigniter4/appstarter>`_
仓库包含一个骨架应用，并通过 Composer 依赖于框架的最新正式版本。

这种安装方式适合希望启动一个新的、基于 CodeIgniter4 的项目的开发者。

安装
------------

在项目根目录的上一级目录中执行：

.. code-block:: console

    composer create-project codeigniter4/appstarter project-root

上述命令将创建一个 **project-root** 文件夹。

如果省略 ``project-root`` 参数，则会创建一个名为 ``appstarter`` 的文件夹，
之后可以按需要重命名。

.. note:: 在 v4.4.0 之前，CodeIgniter 自动加载器不允许使用在某些操作系统中，
    导致文件名非法的特殊字符。允许使用的符号包括 ``/``、``_``、``.``、``:``、``\`` 和空格。
    因此，如果将 CodeIgniter 安装在包含 ``(``、``)`` 等特殊字符的目录下，
    CodeIgniter 将无法运行。从 v4.4.0 起，这一限制已被移除。

.. important:: 部署到生产服务器时，别忘了运行以下命令：

    .. code-block:: console

        composer install --no-dev

    上述命令会移除仅用于开发环境、在生产环境中不需要的 Composer 包，
    从而大幅减小 **vendor** 文件夹的体积。

安装旧版本
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

例如，在 v4.5.0 发布之后，可能希望安装 v4.4.8。

这种情况下，需要在命令中指定版本号：

.. code-block:: console

    composer create-project codeigniter4/appstarter:4.4.8 project-root

然后，打开项目根目录中的 **composer.json**，并指定框架版本：

.. code-block:: text

    "require": {
        ...
        "codeigniter4/framework": "4.4.8"
    },

接着运行 ``composer update`` 命令。

.. note:: 当在 **composer.json** 中使用固定版本号（如 ``"codeigniter4/framework": "4.4.8"``）时，
    ``composer update`` 命令不会将框架更新到最新版本。
    有关如何指定版本范围，请参阅 `编写版本约束`_。

.. _编写版本约束: https://getcomposer.org/doc/articles/versions.md#writing-version-constraints

初始配置
---------------------

安装完成后，需要进行一些初始配置。
详情请参阅 :ref:`initial-configuration`。

.. _app-starter-upgrading:

升级
---------

每当有新版本发布时，在项目根目录中运行：

.. code-block:: console

    composer update

请阅读 :doc:`升级说明 <upgrading>` 和 :doc:`更新日志 <../changelogs/index>`，
并检查其中的重大变更和增强内容。

升级到指定版本
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

例如，在 v4.5.0 发布之后，可能希望从 v4.4.7 升级到 v4.4.8。

这种情况下，打开项目根目录中的 **composer.json**，并指定框架版本：

.. code-block:: text

    "require": {
        ...
        "codeigniter4/framework": "4.4.8"
    },

然后运行 ``composer update`` 命令。

.. note:: 当在 **composer.json** 中使用固定版本号（如 ``"codeigniter4/framework": "4.4.8"``）时，
    ``composer update`` 命令不会将框架更新到最新版本。
    有关如何指定版本范围，请参阅 `编写版本约束`_。

优点
----

安装简单；升级方便。

缺点
----

升级后，仍需要检查 **项目空间**
（root、app、public、writable）中的文件变更，并手动合并。

.. note:: 有一些第三方 CodeIgniter 模块可以帮助合并项目空间中的变更：
    `在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

结构
---------

安装完成后的项目目录结构：

- app、public、tests、writable
- vendor/codeigniter4/framework/system

最新开发版
----------

App Starter 仓库包含一个 ``builds`` 脚本，可在当前稳定版本和框架最新开发分支之间切换 Composer 源。
该脚本适合愿意使用尚未发布、可能不稳定的最新变更的开发者。

`开发版用户指南 <https://codeigniter4.github.io/CodeIgniter4/>`_ 可在线访问。
请注意，它与正式发布的用户指南不同，内容明确针对 develop 分支。

更新到最新开发版
^^^^^^^^^^^^^^^^^^^^^

在项目根目录中执行：

.. code-block:: console

    php builds development

上述命令会更新 **composer.json**，使其指向工作仓库的 ``develop`` 分支，
并更新配置文件和 XML 文件中对应的路径。

使用 ``builds`` 命令后，请务必运行 ``composer update``，
以将 vendor 文件夹同步到最新的目标构建。
随后，如有需要，请查阅 :doc:`upgrading` 并更新项目文件。

下一个次要版本
^^^^^^^^^^^^^^^^^^

如果希望使用下一个次要版本分支，可以在使用 ``builds`` 命令后，
手动编辑 **composer.json**。

例如，尝试 ``4.6`` 分支时，将版本改为 ``4.6.x-dev``::

    "require": {
        "php": "^8.1",
        "codeigniter4/codeigniter4": "4.6.x-dev"
    },

然后运行 ``composer update``，
以将 vendor 文件夹同步到最新的目标构建。
接着，查阅升级指南
（**user_guide_src/source/installation/upgrade_{version}.rst**），
并在必要时更新项目文件。

恢复到稳定版本
^^^^^^^^^^^^^^^^^^^^^^^^

如需恢复更改，请运行：

.. code-block:: console

    php builds release

将 CodeIgniter4 添加到现有项目
==========================================

与“手动安装”中描述的相同，
`CodeIgniter 4 框架 <https://github.com/codeigniter4/framework>`_
仓库也可以通过 Composer 添加到现有项目中。

安装
------------

在 ``app`` 文件夹中开发应用，``public`` 文件夹作为文档根目录。

在项目根目录中执行：

.. code-block:: console

    composer require codeigniter4/framework

.. important:: 部署到生产服务器时，别忘了运行以下命令：

    .. code-block:: console

        composer install --no-dev

    上述命令会移除仅用于开发环境、在生产环境中不需要的 Composer 包，
    从而大幅减小 **vendor** 文件夹的体积。

设置
----------

    1. 将 **vendor/codeigniter4/framework** 中的 **app**、**public**、**tests** 和 **writable** 文件夹复制到项目根目录
    2. 将 **vendor/codeigniter4/framework** 中的 **env**、**phpunit.xml.dist** 和 **spark** 文件复制到项目根目录
    3. 需要调整 **app/Config/Paths.php** 中的 ``$systemDirectory`` 属性，使其指向 vendor 中的路径，例如 ``__DIR__ . '/../../vendor/codeigniter4/framework/system'``。

初始配置
---------------------

需要进行一些初始配置。
详情请参阅 :ref:`initial-configuration`。

.. _adding-codeigniter4-upgrading:

升级
---------

每当有新版本发布时，在项目根目录中运行：

.. code-block:: console

    composer update

请阅读 :doc:`升级说明 <upgrading>` 和 :doc:`更新日志 <../changelogs/index>`，
并检查其中的重大变更和增强内容。

升级到指定版本
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

例如，在 v4.5.0 发布之后，可能希望从 v4.4.7 升级到 v4.4.8。

这种情况下，打开项目根目录中的 **composer.json**，并指定框架版本：

.. code-block:: text

    "require": {
        ...
        "codeigniter4/framework": "4.4.8"
    },

然后运行 ``composer update`` 命令。

优点
----

安装相对简单；升级方便。

缺点
----

升级后，仍需要检查 **项目空间**
（root、app、public、writable）中的文件变更。

.. note:: 有一些第三方 CodeIgniter 模块可以帮助合并项目空间中的变更：
    `在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

结构
---------

安装完成后的项目目录结构：

- app、public、tests、writable
- vendor/codeigniter4/framework/system

语言包安装
=========================

如果希望使用系统消息的翻译，可以通过类似方式将其添加到项目中。

在项目根目录中执行：

.. code-block:: console

    composer require codeigniter4/translations

之后，每次运行 ``composer update`` 时，这些语言包都会与框架一同更新。
