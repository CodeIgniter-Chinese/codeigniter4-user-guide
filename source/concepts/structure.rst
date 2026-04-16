#####################
应用程序结构
#####################

要充分使用 CodeIgniter，你需要了解应用程序的默认结构，以及可以根据你的应用需求进行哪些更改。

.. contents::
    :local:
    :depth: 2

默认目录
*******************

一个全新的安装包含五个目录：

- **app**
- **public**
- **writable**
- **tests**
- **vendor** 或 **system**

每个目录都有非常具体的作用。

app
===

**app** 目录是应用程序代码存放的地方。它自带一个默认的目录结构，适用于大多数应用程序。

以下目录构成了其基本内容：

.. code-block:: none

    app/
        Config/         存储配置文件
        Controllers/    控制器决定程序流程
        Database/       存储数据库迁移和数据填充文件
        Filters/        存储可在控制器前后运行的过滤器类
        Helpers/        辅助函数存储独立函数的集合
        Language/       多语言支持从这里读取语言字符串
        Libraries/      存放不适合其他类别的有用类
        Models/         模型与数据库交互，代表业务实体
        ThirdParty/     可在应用中使用的第三方库
        Views/          视图组成要向客户端显示的 HTML

因为 **app** 目录已经具备命名空间，你可以根据应用程序的需要自由修改此目录的结构。

例如，你可能决定开始使用 Repository 模式和实体（Entities）来处理数据。在这种情况下，你可以将 **Models** 目录重命名为 **Repositories**，并添加一个新的 **Entities** 目录。

此目录中的所有文件都位于 ``App`` 命名空间下，尽管你可以通过修改 **app/Config/Constants.php** 来更改它。

system
======

.. note:: 如果你使用 Composer 安装 CodeIgniter，则 **system** 目录位于 **vendor/codeigniter4/framework/system**。

此目录存储了构成框架本身的文件。虽然你对如何使用应用程序目录有很高的灵活性，但绝不应修改 system 目录中的文件。相反，你应该通过扩展类或创建新类来提供所需的功能。

此目录中的所有文件都位于 ``CodeIgniter`` 命名空间下。

.. _application-structure-public:

public
======

**public** 目录存放了 Web 应用程序中可被浏览器访问的部分，防止对源代码的直接访问。

它包含主 **.htaccess** 文件、**index.php** 以及你添加的任何应用程序资源，如 CSS、JavaScript 或图片。

此目录旨在作为你网站的 "web root"，你的 Web 服务器将被配置为指向它。

writable
========

此目录用于存放应用程序在其生命周期中可能需要写入的任何目录。这包括用于存储缓存文件、日志以及用户可能上传的文件的目录。

你应该将应用程序需要写入的其他任何目录都添加到这里。这允许你将其他主要目录保持为不可写状态，作为一种附加的安全措施。

tests
=====

此目录用于存放你的测试文件。**_support** 目录存放了各种模拟类和你在编写测试时可以使用的其他工具。

此目录无需转移到你的生产服务器上。

修改目录位置
*****************************

如果你已经移动了任何主要目录，可以在 **app/Config/Paths.php** 内更改配置设置。

请阅读 :doc:`管理你的应用程序 <../general/managing_apps>`。
