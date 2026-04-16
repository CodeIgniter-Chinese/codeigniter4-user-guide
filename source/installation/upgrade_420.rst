#############################
从 4.1.9 升级到 4.2.0
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

必须修改的文件
**********************

index.php 与 spark
===================

以下文件发生了重大变更，
**你必须将更新后的版本合并到你的应用中**：

* ``public/index.php``
* ``spark``

.. important:: 如果不更新以上两个文件，在运行 ``composer update`` 之后，
    CodeIgniter 将完全无法工作。

    例如，升级步骤如下：

    .. code-block:: console

        composer update
        cp vendor/codeigniter4/framework/public/index.php public/index.php
        cp vendor/codeigniter4/framework/spark .

Config/Constants.php
====================

常量 ``EVENT_PRIORITY_LOW``、``EVENT_PRIORITY_NORMAL`` 和 ``EVENT_PRIORITY_HIGH`` 已被弃用，
其定义已移至 ``app/Config/Constants.php``。
如果你使用了这些常量，请在 ``app/Config/Constants.php`` 中进行定义。
或者，使用新的类常量
``CodeIgniter\Events\Events::PRIORITY_LOW``、
``CodeIgniter\Events\Events::PRIORITY_NORMAL`` 和
``CodeIgniter\Events\Events::PRIORITY_HIGH``。

composer.json
=============

.. note:: 在 v4.5.0 或更高版本中不再需要此步骤。

如果你使用 Composer，并且在安装 CodeIgniter v4.1.9 或更早版本时，
在 ``/composer.json`` 的 ``autoload.psr-4`` 中包含 ``App\\`` 和 ``Config\\`` 命名空间，
如下所示，则需要移除这些行，并运行 ``composer dump-autoload``。

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

破坏性变更
****************

- ``system/bootstrap.php`` 文件不再返回 ``CodeIgniter`` 实例，
  并且也不再加载 ``.env`` 文件（现由 ``index.php`` 和 ``spark`` 处理）。
  如果你的代码依赖这些行为，将不再生效，必须进行修改。
  此变更是为了更方便地实现
  `预加载 <https://www.php.net/manual/zh/opcache.preloading.php>`_。

破坏性增强
*********************

- ``Validation::setRule()`` 的方法签名已更改，移除了 ``$rules`` 参数上的 ``string`` 类型提示。
  继承该方法的类同样应移除该类型提示，以避免破坏 LSP。
- ``CodeIgniter\Database\BaseBuilder::join()`` 和
  ``CodeIgniter\Database\*\Builder::join()`` 的方法签名已更改，
  移除了 ``$cond`` 参数上的 ``string`` 类型提示。
  继承该方法的类同样应移除该类型提示，以避免破坏 LSP。

项目文件
*************

**项目空间** （根目录、app、public、writable）中的部分文件已更新。
由于这些文件位于 **system** 范围之外，框架不会在没有你介入的情况下自动修改它们。

目前有一些第三方 CodeIgniter 模块可用于协助合并项目空间中的变更：
`在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

.. note:: 除极少数用于缺陷修复的情况外，对项目空间文件所做的任何修改都不会破坏你的应用。
    此处列出的所有变更在下一个主版本发布前都是可选的，
    任何强制性变更都会在上述章节中说明。

内容变更
===============

以下文件发生了较大的改动（包括弃用项或界面调整），建议将更新后的版本合并到你的应用中：

* ``app/Config/Routes.php``
    * 为提高默认配置的安全性，自动路由现已默认禁用。

所有变更
===========

以下是 **项目空间** 中所有发生变更的文件列表；
其中许多仅为注释或格式调整，不会影响运行时行为：

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
