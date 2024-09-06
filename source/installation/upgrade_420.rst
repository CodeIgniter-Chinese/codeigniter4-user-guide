#############################
从 4.1.9 升级到 4.2.0
#############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

必备文件变更
**********************

index.php 和 spark
===================

以下文件进行了重大更改,
**你必须将更新后的版本** 与应用程序合并:

* ``public/index.php``
* ``spark``

.. important:: 如果你不更新以上两个文件,在运行 ``composer update`` 后 CodeIgniter 将完全无法工作。

    升级过程例如如下:

    .. code-block:: console

        composer update
        cp vendor/codeigniter4/framework/public/index.php public/index.php
        cp vendor/codeigniter4/framework/spark .

Config/Constants.php
====================

常量 ``EVENT_PRIORITY_LOW``、``EVENT_PRIORITY_NORMAL`` 和 ``EVENT_PRIORITY_HIGH`` 已被废弃,定义移至 ``app/Config/Constants.php``。如果你使用这些常量,请在 ``app/Config/Constants.php`` 中定义它们。或者使用新的类常量 ``CodeIgniter\Events\Events::PRIORITY_LOW``、``CodeIgniter\Events\Events::PRIORITY_NORMAL`` 和 ``CodeIgniter\Events\Events::PRIORITY_HIGH``。

composer.json
=============

.. note:: 此步骤在 v4.5.0 或更高版本中不再需要。

如果你使用 Composer,在安装 CodeIgniter v4.1.9 或更早版本时,如果 ``/composer.json`` 的 ``autoload.psr-4`` 中存在类似下面的 ``App\\`` 和 ``Config\\`` 命名空间,你需要删除这些行并运行 ``composer dump-autoload``。

.. code-block:: text

    {
        ...
        "autoload": {
            "psr-4": {
                "App\\": "app",             <-- 移除此行
                "Config\\": "app/Config"    <-- 移除此行
            }
        },
        ...
    }

重大变更
****************

- ``system/bootstrap.php`` 文件不再返回 ``CodeIgniter`` 实例,也不再加载 ``.env`` 文件(现在在 ``index.php`` 和 ``spark`` 中处理)。如果你的代码依赖这些行为则不再起作用,必须进行修改。这已更改是为了更易实现 `预加载 <https://www.php.net/manual/zh/opcache.preloading.php>`_。

重大增强
*********************

- ``Validation::setRule()`` 的方法签名已更改。``$rules`` 参数上的 ``string`` 类型提示已移除。扩展类同样应移除参数类型声明,以避免违反LSP。
- ``CodeIgniter\Database\BaseBuilder::join()`` 和 ``CodeIgniter\Database\*\Builder::join()`` 的方法签名已更改。``$cond`` 参数上的 ``string`` 类型提示已移除。扩展类同样应移除参数类型声明,以避免违反LSP。

项目文件
*************

**项目空间** 中的许多文件(根目录、app、public、writable)都已更新。由于这些文件超出 **系统** 范围,如果不进行干预,它们将不会更改。有一些第三方 CodeIgniter 模块可以协助合并项目空间的更改: `在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

.. note:: 除非极少数情况进行错误修复,否则对项目空间文件的任何更改都不会破坏你的应用程序。在下一个主要版本之前,这里注明的所有更改都是可选的,强制性更改将在上面部分介绍。

内容更改
===============

以下文件已作出重大更改(包括弃用或视觉调整),建议你将更新版本与应用程序合并:

* ``app/Config/Routes.php``
    * 为了使默认配置更安全,默认情况下自动路由已更改为禁用。

所有更改
===========

这是 **项目空间** 中已更改的所有文件的列表;其中许多仅为注释或格式更改,不会影响运行时:

* app/Config/App.php
* app/Config/Constants.php
* app/Config/ContentSecurityPolicy.php
* app/Config/Database.php
* app/Config/Events.php
* app/Config/Feature.php
* app/Config/Filters.php
* app/Config/Format.php
* app/Config/Logger.php
* app/Config/Mimes.php
* app/Config/Publisher.php
* app/Config/Routes.php
* app/Config/Security.php
* app/Config/Validation.php
* app/Config/View.php
* app/Controllers/BaseController.php
* app/Views/errors/html/debug.css
* app/Views/errors/html/debug.js
* app/Views/errors/html/error_404.php
* app/Views/errors/html/error_exception.php
* app/Views/errors/html/production.php
* app/Views/welcome_message.php
* app/index.html
* preload.php
* public/index.php
* spark
