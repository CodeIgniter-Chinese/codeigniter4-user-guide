##########################
创建 Composer 包
##########################

可将创建的 :doc:`../general/modules` 转化为 Composer 包，也可为 CodeIgniter 4 创建专属 Composer 包。

.. contents::
    :local:
    :depth: 2

****************
目录结构
****************

以下是 Composer 包的标准目录结构::

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

在包目录根路径下创建 **composer.json** 文件。此文件定义了包的元数据及其依赖项。

可使用 ``composer init`` 命令辅助创建。

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
            // 此处列出包所需的依赖项
        },
        "require-dev": {
            // 此处列出开发依赖项（如 PHPUnit）
        }
    }

包名
============

``name`` 字段至关重要。包名通常采用“vendor-name/package-name”格式且全部小写。常见示例如下：

- ``your-vendor-name``：标识供应商（包创建者）的名称，如个人姓名或组织名。
- ``your-package-name``：所创建包的名称。

因此，务必确保名称唯一，以便与其他包区分。在发布时，唯一性尤为重要。

命名空间
=========

包名决定了 ``autoload.psr4`` 中的供应商命名空间。

如果包名为 ``your-vendor/your-package``，则供应商命名空间必须为 ``YourVendor``。编写方式如下::

    "autoload": {
        "psr-4": {
            "YourVendor\\YourPackage\\": "src/"
        }
    },

此设置指示 Composer 自动加载包的源代码。

选择授权协议
================

如不熟悉开源授权协议，请参阅 https://choosealicense.com/。包括 CodeIgniter 在内的许多 PHP 包都使用 MIT 协议。

***************************
准备开发工具
***************************

许多工具可协助确保代码质量，建议使用。通过 `CodeIgniter DevKit <https://github.com/codeigniter4/devkit>`_ 可轻松安装并配置此类工具。

安装 DevKit
=================

在包根目录下运行以下命令：

.. code-block:: console

    composer config minimum-stability dev
    composer config prefer-stable true
    composer require --dev codeigniter4/devkit

DevKit 会安装各种有助于开发的 Composer 包，并在 **vendor/codeigniter4/devkit/src/Template** 中提供对应的模板。将该目录下的文件复制到项目根目录，并根据需求进行修改。

配置代码规范修复工具
==================================

DevKit 提供了基于 `PHP-CS-Fixer <https://github.com/PHP-CS-Fixer/PHP-CS-Fixer>`_ 的代码规范修复工具，并遵循 `CodeIgniter 代码规范 <https://github.com/CodeIgniter/coding-standard>`_。

将 **vendor/codeigniter4/devkit/src/Template/.php-cs-fixer.dist.php** 复制到项目根目录。

创建用于存放缓存文件的 **build** 目录::

    your-package-name/
    ├── .php-cs-fixer.dist.php
    ├── build/

使用编辑器打开 **.php-cs-fixer.dist.php** 并修正目录路径::

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

配置完成。现在可运行代码规范修复工具：

.. code-block:: console

    vendor/bin/php-cs-fixer fix --ansi --verbose --diff

如果在 **composer.json** 中添加了 ``scripts.cs-fix``，则可通过 ``composer cs-fix`` 命令运行::

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

如果包中包含配置文件，且希望允许用户覆盖这些设置，请使用 :php:func:`config()` 并传入短类名（如 ``config('YourConfig')``）来调用该配置文件。

随后，用户只需在 **app/Config** 中放置一个同名短类名的配置类，并继承包的配置类（如 ``YourVendor\YourPackage\Config\YourConfig``），即可覆盖包配置。

覆盖 app/Config 中的设置
=================================

如需覆盖或补充 **app/Config** 目录下的已知配置，可使用 :ref:`隐式注册器 <registrars>`。

**********
参考资料
**********

官方已发布多个包。在创建自己的包时，可将这些包作为参考：

- https://github.com/codeigniter4/shield
- https://github.com/codeigniter4/settings
- https://github.com/codeigniter4/tasks
- https://github.com/codeigniter4/cache
