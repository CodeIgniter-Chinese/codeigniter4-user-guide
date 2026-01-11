##########################
管理应用程序
##########################

默认情况下，CodeIgniter 假定你只打算使用一个应用程序，该应用程序将在你的 **app** 目录中构建。然而，你也可以拥有多个共享同一个 CodeIgniter 安装的应用程序集合，甚至可以重命名或重新定位你的应用程序目录。

.. contents::
    :local:
    :depth: 2

.. _renaming-app-directory:

重命名或重新定位应用程序目录
================================================

如果你想重命名应用程序目录，甚至将其移动到服务器上除项目根目录外的不同位置，请打开你的主 **app/Config/Paths.php** 文件，并在 ``$appDirectory`` 变量中（大约在第 44 行）设置 *完整的服务器路径*：

.. literalinclude:: managing_apps/001.php

你还需要修改项目根目录中的两个额外文件，以便它们能够找到 **Paths** 配置文件：

- **spark** 运行命令行应用程序。

  .. literalinclude:: managing_apps/002.php
      :lines: 2-

- **public/index.php** 是你的 Web 应用程序的前端控制器。

  .. literalinclude:: managing_apps/003.php
      :lines: 2-

.. _running-multiple-app:

使用单个 CodeIgniter 安装运行多个应用程序
===============================================================

如果你想共享一个通用的 CodeIgniter 框架安装来管理几个不同的应用程序，只需将位于应用程序目录中的所有目录放入它们自己的（子）目录中。

例如，假设你要创建两个名为 **foo** 和 **bar** 的应用程序。你可以这样构建应用程序项目目录结构：

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

.. note:: 如果你从 Zip 文件安装 CodeIgniter，目录结构将如下所示：

    .. code-block:: text

        foo/
        bar/
        codeigniter4/system/

这样就有两个应用程序 **foo** 和 **bar**，它们都拥有标准的应用程序目录和一个 **public** 文件夹，并共享一个通用的 **codeigniter4/framework**。

每个应用程序内部 **app/Config/Paths.php** 文件中的 ``$systemDirectory`` 变量将被设置为指向共享的通用 **codeigniter4/framework** 文件夹：

.. literalinclude:: managing_apps/005.php

.. note:: 如果你从 Zip 文件安装 CodeIgniter，``$systemDirectory`` 将是 ``__DIR__ . '/../../../codeigniter4/system'``。

并且需要修改每个应用程序内部 **app/Config/Constants.php** 文件中的 ``COMPOSER_PATH`` 常量：

.. literalinclude:: managing_apps/004.php

仅当你更改应用程序目录时，请参考 :ref:`renaming-app-directory` 并修改 **index.php** 和 **spark** 中的路径。
