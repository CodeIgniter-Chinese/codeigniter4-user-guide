############
安装
############

CodeIgniter4 可以手动安装,或使用 Composer 安装。

.. note:: 在使用 CodeIgniter 之前, 请确认你的服务器符合
          :doc:`要求 </intro/requirements>`.

手动安装
===================

CodeIgniter 通过手动下载并解压压缩包来安装。

Composer 安装
=====================

虽然不是必须的，但你可以通过 `composer <https://getcomposer.org>`_ create-project 命令来安装 CodeIgniter。

::

    composer create-project codeigniter4/framework

运行
=======

#. 将 CodeIgniter 的文件夹和文件上传到你的服务器上。 **index.php** 文件将会在你项目根目录的 **public** 文件夹里。
#. 使用文本编辑器打开 **application/Config/App.php** 文件来设置你的基本 URL。如果你打算使用加密或者 Session，请设置加密密钥。如果你需要更多的灵活性，可以在 .env 文件中将 baseURL 设置为 **app.baseURL="http://example.com"**。
#. 如果你打算使用数据库，使用文本编辑器打开 **application/Config/Database.php** 并配置你的数据库设置。

为了最大程度地保证安全性，系统目录以及任何应用程序的目录都在网站根目录之上，这样就无法通过浏览器直接访问到它们。默认情况下，每一个目录下都包含有 **.htaccess** 文件来防止直接访问，但因为服务器配置改变或服务器不支持 **.htaccess** ，因此最好还是将它们从公共访问目录中移除。

如果你想公开你的视图，你可以将 **views** 目录移动到 **application** 目录之外，移动到 **public** 目录下的相应文件夹中。如果你这样做，记住最好打开你的主 index.php 文件并将 ``$system_path``，``$application_folder`` 和 ``$view_folder`` 变量设置为全路径，例如：*/www/MyUser/system*。

在生产环境中所要做的一个额外操作是禁用 PHP 错误报告以及其它任何仅开发时所使用的功能。在 CodeIgniter 中，可以通过设置 ``ENVIRONMENT`` 常量来完成。这在 `环境页面 </general/environments>` 上有更详细的叙述。默认情况下，应用程序将会以“production”（生产）环境运行。如果要使用提供的调试工具，你需要将环境设置为 "develop"。

.. 警告:: 使用 PHP 的内置 Web 服务器可能会出现问题，因为它不会处理用于正确处理请求的 `.htaccess` 文件。

就是这样！

如果你是 CodeIgniter 新手, 请阅读用户指南的 :doc:`入门 <../intro/index>` 部分，开始学习如何构建静态 PHP 应用程序。祝你愉快！

.. toctree::
    :hidden:
    :titlesonly:

    downloads
    self
    upgrading
    troubleshooting
    local_server
