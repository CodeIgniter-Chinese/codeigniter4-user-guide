Composer 安装
#####################

.. contents::
    :local:
    :depth: 2

Composer 可以通过几种方式在你的系统上安装 CodeIgniter4。

.. important:: CodeIgniter4 需要 Composer 2.0.14 或更高版本。

.. note:: 如果你不熟悉 Composer,我们建议你先阅读
    `基本用法 <https://getcomposer.org/doc/01-basic-usage.md>`_。

第一种技术描述了使用 CodeIgniter4 创建骨架项目的方法,然后你可以将其用作新 Web 应用程序的基础。
下面描述的第二种技术允许你将 CodeIgniter4 添加到现有的 Web 应用程序中。

.. note:: 如果你使用 Git 仓库存储代码或与他人协作,那么 **vendor** 文件夹通常会被“git 忽略”。在这种情况下,当你将仓库克隆到新系统时,需要运行 ``composer update``。

App Starter
===========

`CodeIgniter 4 app starter <https://github.com/codeigniter4/appstarter>`_
仓库包含一个骨架应用程序,其中包含对最新版本框架的 Composer 依赖项。

此安装技术适用于希望启动基于 CodeIgniter4 的新项目的开发人员。

安装
------------

在项目根目录上层文件夹中::

    > composer create-project codeigniter4/appstarter 项目根目录

上述命令将创建一个**项目根目录**文件夹。

如果省略“项目根目录”参数,该命令将创建一个“appstarter”文件夹,可以根据需要重命名。

.. note:: CodeIgniter 自动加载程序不允许特殊字符,这些字符在某些操作系统中的文件名中是非法的。
    可以使用的符号是 ``/``, ``_``, ``.``, ``:``, ``\`` 和空格。
    因此,如果在包含特殊字符的文件夹下安装 CodeIgniter,比如 ``(``, ``)`` 等,CodeIgniter 将无法工作。

.. important:: 当你将应用部署到生产服务器时,不要忘记运行以下命令::

    > composer install --no-dev

    上述命令将只移除开发环境下的 Composer 软件包,这些软件包在生产环境中不需要。这将大大减少 vendor 文件夹的大小。

初始配置
---------------------

安装后,需要进行一些初始配置。有关详细信息,请参阅 :ref:`initial-configuration`。

.. _app-starter-upgrading:

升级
---------

每当有新版本发布时,在项目根目录的命令行中运行::

    > composer update

阅读 :doc:`升级说明 <upgrading>`,并查看已破坏的更改和增强功能。

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
----------

App Starter 仓库带有 ``builds`` 脚本,可在当前稳定版本和框架的最新开发分支之间切换 Composer 源。此脚本适用于愿意使用最新的未发布更改(可能不稳定)的开发者。

`开发用户指南 <https://codeigniter4.github.io/CodeIgniter4/>`_ 可以在线访问。
请注意,这与已发布的用户指南不同,并将明确适用于 develop 分支。

在项目根目录中::

    > php builds development

上述命令将更新 **composer.json** 以指向工作仓库的 ``develop`` 分支,并更新配置和 XML 文件中的相应路径。要还原这些更改,请运行::

    > php builds release

使用 ``builds`` 命令后,请务必运行 ``composer update`` 以使用最新目标构建同步 vendor 文件夹。

将 CodeIgniter4 添加到现有项目中
==========================================

“手动安装”中描述的相同 `CodeIgniter 4 框架 <https://github.com/codeigniter4/framework>`_
仓库也可以使用 Composer 添加到现有项目中。

安装
------------

在 ``app`` 文件夹中开发你的应用程序,``public`` 文件夹将是你的文档根目录。

在项目根目录中::

    > composer require codeigniter4/framework

.. important:: 将应用程序部署到生产服务器时,不要忘记运行以下命令::

    > composer install --no-dev

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

每当有新版本发布时,在项目根目录的命令行中运行::

    > composer update

阅读 :doc:`升级说明 <upgrading>`,并查看已破坏的更改和增强功能。

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

在项目根目录的命令行中::

    > composer require codeigniter4/translations

每次执行 ``composer update`` 时,这些都会与框架一起更新。
