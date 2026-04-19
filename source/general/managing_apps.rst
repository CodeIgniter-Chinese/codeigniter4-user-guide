##########################
管理应用程序
##########################

默认情况下，CodeIgniter 假定仅用于管理一个应用程序（即在 **app** 目录下构建的应用）。不过，也可以让多个应用程序集共用同一个 CodeIgniter 安装，或者重命名及移动应用程序目录。

.. contents::
    :local:
    :depth: 2

.. _renaming-app-directory:

重命名或移动应用程序目录
================================================

如果需要重命名应用程序目录，或者将其移至服务器中项目根目录以外的其他位置，请打开主 **app/Config/Paths.php** 文件，并在 ``$appDirectory`` 变量中设置 *服务器完整路径* （约在第 44 行）：

.. literalinclude:: managing_apps/001.php

此外，还需要修改项目根目录下的两个文件，以便程序能够找到 **Paths** 配置文件：

- **spark**：运行命令行应用。

  .. literalinclude:: managing_apps/002.php
      :lines: 2-

- **public/index.php**：Web 应用的前端控制器。

  .. literalinclude:: managing_apps/003.php
      :lines: 2-

.. _running-multiple-app:

使用一套 CodeIgniter 安装运行多个应用
===============================================================

如果希望共用同一个 CodeIgniter 框架来管理多个不同的应用程序，只需将原应用程序目录下的所有目录放入各自的（子）目录中即可。

例如，假设要创建两个分别名为 **foo** 和 **bar** 的应用程序。可以按如下方式组织项目目录结构：

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

.. note:: 如果是通过 Zip 文件安装的 CodeIgniter，目录结构如下：

    .. code-block:: text

        foo/
        bar/
        codeigniter4/system/

在此结构下，**foo** 和 **bar** 两个应用都拥有标准的应用程序目录和 **public** 文件夹，并共用同一个 **codeigniter4/framework**。

每个应用下的 **app/Config/Paths.php** 需要将 ``$systemDirectory`` 变量设置为指向共用的 **codeigniter4/framework** 文件夹：

.. literalinclude:: managing_apps/005.php

.. note:: 如果是通过 Zip 文件安装的 CodeIgniter，``$systemDirectory`` 应设置为 ``__DIR__ . '/../../../codeigniter4/system'``。

同时，需要修改每个应用下 **app/Config/Constants.php** 中的 ``COMPOSER_PATH`` 常量：

.. literalinclude:: managing_apps/004.php

仅在更改了应用程序目录时，请参阅 :ref:`renaming-app-directory` 并修改 **index.php** 与 **spark** 中的路径。

更改 .env 文件位置
======================================

如有必要，可以通过调整 ``app/Config/Paths.php`` 中的 ``$envDirectory`` 属性来更改 ``.env`` 文件的位置。

默认情况下，框架会从 ``app/`` 目录上一级（即 ``ROOTPATH``）的 ``.env`` 文件中加载环境设置。按照建议将域名正确指向 ``public/`` 目录时，该位置是安全的。

但在实际操作中，某些应用是通过子目录（例如 ``http://example.com/myapp``）而非主域名提供服务的。在这种情况下，如果 ``.htaccess`` 或其他保护措施配置不当，将 ``.env`` 文件留在 ``ROOTPATH`` 可能会泄露敏感配置数据。

为了避免此类风险，建议确保 ``.env`` 文件位于任何 Web 可访问目录之外。

.. warning::

   如果更改了 ``.env`` 文件的位置，请务必确保其无法通过公共访问。该文件一旦泄露，可能会导致凭据被盗，并使数据库、邮件服务器或第三方 API 等关键服务面临风险。
