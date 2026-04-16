##########################
创建 Composer 包
##########################

你可以将创建的 :doc:`../general/modules` 制作成 Composer 包，
或为 CodeIgniter 4 创建 Composer 包。

.. contents::
    :local:
    :depth: 2

****************
目录结构
****************

Composer 包的典型目录结构如下::

    your-package-name/
    ├── .gitattributes
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    ├── composer.json
    ├── src/
    │   └── YourClass.php
    └── tests/
        └── YourClassTest.php

**********************
创建 composer.json
**********************

在包目录的根目录下，创建一个 **composer.json** 文件。该文件定义了有关包及其依赖项的元数据。

``composer init`` 命令可帮助你创建它。

例如，**composer.json** 可能如下所示::

    {
        "name": "your-vendor/your-package",
        "description": "Your package description",
        "type": "library",
        "license": "MIT",
        "autoload": {
            "psr-4": {
                "YourVendor\\YourPackage\\": "src/"
            }
        },
        "authors": [
            {
                "name": "Your Name",
                "email": "yourname@example.com"
            }
        ],
        "require": {
            // 在此处添加你的包所需的任何依赖项
        },
        "require-dev": {
            // 在此处添加开发所需的任何依赖项（例如 PHPUnit）
        }
    }

包名称
============

``name`` 字段在此很重要。包名称通常以全小写格式
"vendor-name/package-name" 书写。以下是一个常见的例子：

- ``your-vendor-name``：标识供应商（包的创建者）的名称，
  例如你的姓名或你的组织。
- ``your-package-name``：你正在创建的包的名称。

因此，使名称具有唯一性以区别于其他包非常重要。
在发布时，唯一性尤为重要。

命名空间
=========

包名称随后决定了 ``autoload.psr4`` 中的供应商命名空间。

如果你的包名称是 ``your-vendor/your-package``，则供应商命名空间必须
是 ``YourVendor``。因此你可以如下编写::

    "autoload": {
        "psr-4": {
            "YourVendor\\YourPackage\\": "src/"
        }
    },

这个设置指示 Composer 自动加载你的包的源代码。

选择许可证
================

如果不熟悉开源许可证，请参阅 https://choosealicense.com/。
许多 PHP 包，包括 CodeIgniter，都使用 MIT 许可证。

***************************
准备开发工具
***************************

有许多工具可帮助确保代码质量。因此你应该使用它们。
你可以通过 `CodeIgniter DevKit <https://github.com/codeigniter4/devkit>`_
轻松安装和配置这些工具。

安装 DevKit
=================

在包目录的根目录下，运行以下命令：

.. code-block:: console

    composer config minimum-stability dev
    composer config prefer-stable true
    composer require --dev codeigniter4/devkit

DevKit 会安装各种有助于开发的 Composer 包，并在 **vendor/codeigniter4/devkit/src/Template** 中为它们安装模板。将其中的文件复制到项目根目录，并根据需要进行编辑。

配置编码标准修复工具
==================================

DevKit 提供了基于 `PHP-CS-Fixer <https://github.com/PHP-CS-Fixer/PHP-CS-Fixer>`_
的 `CodeIgniter 编码标准 <https://github.com/CodeIgniter/coding-standard>`_ 修复工具。

将 **vendor/codeigniter4/devkit/src/Template/.php-cs-fixer.dist.php** 复制到
项目根目录。

为缓存文件创建 **build** 目录::

    your-package-name/
    ├── .php-cs-fixer.dist.php
    ├── build/

在编辑器中打开 **.php-cs-fixer.dist.php**，并修正文件夹路径::

    --- a/.php-cs-fixer.dist.php
    +++ b/.php-cs-fixer.dist.php
    @@ -7,7 +7,7 @@ use PhpCsFixer\Finder;
     $finder = Finder::create()
         ->files()
         ->in([
    -        __DIR__ . '/app/',
    +        __DIR__ . '/src/',
             __DIR__ . '/tests/',
         ])
         ->exclude([

就是这样。现在你可以运行编码标准修复工具：

.. code-block:: console

    vendor/bin/php-cs-fixer fix --ansi --verbose --diff

如果在 **composer.json** 中添加 ``scripts.cs-fix``，你就可以用
``composer cs-fix`` 命令运行它::

    {
        // ...
        },
        "scripts": {
            "cs-fix": "php-cs-fixer fix --ansi --verbose --diff"
        }
    }

************
配置文件
************

允许用户覆盖设置
===================================

如果你的包有配置文件，并且希望用户能够覆盖设置，请使用 :php:func:`config()` 和短类名，如 ``config('YourConfig')``
来调用配置文件。

然后，用户可以通过在 **app/Config** 中放置一个具有相同短类名的配置类来覆盖包配置，
该类继承自包的 Config 类，如 ``YourVendor\YourPackage\Config\YourConfig``。

在 app/Config 中覆盖设置
=================================

如果需要在 **app/Config** 目录中覆盖或添加已知配置，
可以使用 :ref:`隐式注册器 <registrars>`。

**********
参考
**********

我们已发布了一些官方包。在创建自己的包时，
你可以将这些包作为参考：

- https://github.com/codeigniter4/shield
- https://github.com/codeigniter4/settings
- https://github.com/codeigniter4/tasks
- https://github.com/codeigniter4/cache
