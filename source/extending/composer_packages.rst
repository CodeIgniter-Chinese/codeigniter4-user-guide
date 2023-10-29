##########################
创建 Composer 包
##########################

你可以将你创建的 :doc:`../general/modules` 转换为 Composer 包，或者为 CodeIgniter 4 创建一个 Composer 包。

.. contents::
    :local:
    :depth: 2

****************
文件夹结构
****************

下面是一个典型的 Composer 包的目录结构示例::

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

在你的包目录的根目录中，创建一个 **composer.json** 文件。该文件定义了关于你的包及其依赖项的元数据。

使用 ``composer init`` 命令可以帮助你创建它。

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

``name`` 字段在这里非常重要。包名称通常以 "vendor-name/package-name" 的格式书写，全部小写。以下是一个常见的示例：

- ``your-vendor-name``：标识供应商（包的创建者）的名称，例如你的姓名或组织名称。
- ``your-package-name``：你正在创建的包的名称。

因此，为了使名称唯一以区分其它包，使其与其他包区分开是非常重要的，尤其是在发布时。

命名空间
=========

包名称决定了 ``autoload.psr4`` 中的供应商命名空间。

如果你的包名称是 ``your-vendor/your-package``，那么供应商命名空间必须是 ``YourVendor``。因此，你需要像下面这样编写::

    "autoload": {
        "psr-4": {
            "YourVendor\\YourPackage\\": "src/"
        }
    }

这个设置指示 Composer 自动加载你的包的源代码。

选择许可证
================

如果你对开源许可证不熟悉，请参考 https://choosealicense.com/。许多 PHP 包，包括 CodeIgniter，使用 MIT 许可证。

***************************
准备开发工具
***************************

有许多工具可以帮助确保代码质量。因此，你应该使用它们。你可以使用 `CodeIgniter DevKit <https://github.com/codeigniter4/devkit>`_ 轻松安装和配置此类工具。

安装 DevKit
=================

在你的包目录的根目录中，运行以下命令：

.. code-block:: console

    composer config minimum-stability dev
    composer config prefer-stable true
    composer require --dev codeigniter4/devkit

DevKit 安装了各种 Composer 包，帮助你进行开发，并在 **vendor/codeigniter4/devkit/src/Template** 中为它们安装了模板。将其中的文件复制到你的项目根目录，并根据你的需求进行编辑。

配置 Coding Standards Fixer
==================================

DevKit 提供了基于 `PHP-CS-Fixer <https://github.com/PHP-CS-Fixer/PHP-CS-Fixer>`_ 的 `CodeIgniter Coding Standard <https://github.com/CodeIgniter/coding-standard>`_ 的 Coding Standards Fixer。

将 **vendor/codeigniter4/devkit/src/Template/.php-cs-fixer.dist.php** 复制到你的项目根目录。

为缓存文件创建 **build** 文件夹::

    your-package-name/
    ├── .php-cs-fixer.dist.php
    ├── build/

打开你的编辑器中的 **.php-cs-fixer.dist.php** 文件，并修复文件夹路径::

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

完成后，你可以运行 Coding Standards Fixer：

.. code-block:: console

    vendor/bin/php-cs-fixer fix --ansi --verbose --diff

如果你在 **composer.json** 中添加了 ``scripts.cs-fix``，则可以使用 ``composer cs-fix`` 命令运行它::

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

如果你的包有一个配置文件，并且你希望用户能够覆盖设置，可以使用 :php:func:`config()` 函数与短类名（例如 ``config('YourConfig')``）来调用配置文件。

然后，用户可以通过在 **app/Config** 中放置一个与短类名相同且扩展了包配置类的配置类（例如 ``YourVendor\YourPackage\Config\YourConfig``）来覆盖包配置。

在 app/Config 中覆盖设置
=================================

如果你需要在 **app/Config** 文件夹中覆盖或添加已知配置，可以使用 :ref:`隐式注册器 <registrars>`。

**********
参考资料
**********

我们已经发布了一些官方包。你可以在创建自己的包时使用这些包作为参考：

- https://github.com/codeigniter4/shield
- https://github.com/codeigniter4/settings
- https://github.com/codeigniter4/tasks
- https://github.com/codeigniter4/cache
