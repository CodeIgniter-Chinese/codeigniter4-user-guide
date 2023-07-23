##########################
管理应用程序
##########################

默认情况下,假设你只打算在 **app** 目录中使用 CodeIgniter 来管理一个应用程序。但是,可以拥有多个共享单个 CodeIgniter 安装的应用程序集,或者重命名或重新定位你的应用程序目录。

.. important:: 如果你安装了 CodeIgniter v4.1.9 或更早版本,并且在 ``/composer.json`` 的 ``autoload.psr-4`` 中有像下面这样的 ``App\\`` 和 ``Config\\`` 命名空间,你需要删除这些行并运行 ``composer dump-autoload``。

    .. code-block:: text

        {
            ...
            "autoload": {
                "psr-4": {
                    "App\\": "app",             <-- 移除这行
                    "Config\\": "app/Config"    <-- 移除这行
                }
            },
            ...
        }

.. contents::
    :local:
    :depth: 2

.. _renaming-app-directory:

重命名或重新定位应用程序目录
================================================

如果你想要重命名应用程序目录或者甚至将其移动到服务器上的项目根目录之外的其他位置,请打开主 **app/Config/Paths.php** 文件,并在 ``$appDirectory`` 变量中设置一个*完整的服务器路径*(约第44行):

.. literalinclude:: managing_apps/001.php

你需要修改项目根目录中的另外两个文件,以便它们可以找到 **Paths** 配置文件:

- **/spark** 运行命令行应用程序。

  .. literalinclude:: managing_apps/002.php

- **/public/index.php** 是你的 Web 应用程序的前端控制器。

  .. literalinclude:: managing_apps/003.php

使用一个 CodeIgniter 安装运行多个应用程序
===============================================================

如果你想共享一个公共的 CodeIgniter 框架安装来管理几个不同的应用程序,只需将位于应用程序目录内的所有目录都放入自己的(子)目录即可。

例如,假设你要创建两个名为 **foo** 和 **bar** 的应用程序。你可以像这样组织应用程序项目目录:

.. code-block:: text

    foo/
        app/
        public/
        tests/
        writable/
        env
        phpunit.xml.dist
        spark
    bar/
        app/
        public/
        tests/
        writable/
        env
        phpunit.xml.dist
        spark
    vendor/
        autoload.php
        codeigniter4/framework/
    composer.json
    composer.lock

.. note:: 如果你从 Zip 文件安装 CodeIgniter,目录结构将是:

    .. code-block:: text

        foo/
        bar/
        codeigniter4/system/

这将有两个应用程序 **foo** 和 **bar**,都有标准的应用程序目录和 **public** 文件夹,并共享一个公共的 **codeigniter4/framework**。

每个应用程序内部的 **app/Config/Paths.php** 中的 ``$systemDirectory`` 变量将被设置为指向共享的公共 **codeigniter4/framework** 文件夹:

.. literalinclude:: managing_apps/005.php

.. note:: 如果你从 Zip 文件安装 CodeIgniter, ``$systemDirectory`` 将是 ``__DIR__ . '/../../../codeigniter4/system'``。

并修改每个应用程序内部的 **app/Config/Constants.php** 中的 ``COMPOSER_PATH`` 常量:

.. literalinclude:: managing_apps/004.php

只有在你更改应用程序目录时,请参阅 :ref:`renaming-app-directory` 并修改 **index.php** 和 **spark** 中的路径。
