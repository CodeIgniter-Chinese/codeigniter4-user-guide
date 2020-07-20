#####################
应用结构
#####################

为了可以充分利用 CodeIgniter，你需要了解应用程序的结构，默认情况下，你可以更改内容以满足你的应用程序的需求。

默认目录
===================

新安装的应用程序中有六个目录：``/app``，``/system``，``/public``， ``/writable``，``/tests`` 和 ``/docs``。这些目录中的每一个都有一个非常具体的使用规范。

app
-----------

``app`` 目录是你所有应用程序代码所在的目录。它带有一个默认的目录结构，适用于许多应用程序。以下文件夹构成基本内容：

.. code-block:: none

	/app
		/Config         Stores the configuration files
		/Controllers    Controllers determine the program flow
		/Database       Stores the database migrations and seeds files
		/Filters        Stores filter classes that can run before and after controller
		/Helpers        Helpers store collections of standalone functions
		/Language       Multiple language support reads the language strings from here
		/Libraries      Useful classes that don't fit in another category
		/Models         Models work with the database to represent the business entities.
		/ThirdParty     ThirdParty libraries that can be used in application
		/Views          Views make up the HTML that is displayed to the client.

由于app目录已经是命名空间，因此你可以随意修改此目录的结构以满足应用程序的需要。例如，你可能决定开始使用存储库模式和实体模型来处理数据。在这种情况下，你可以将Models目录重命名为 Repositories，并添加新Entities目录。

.. note:: 如果重命名 ``Controllers`` 目录，则无法使用路由到控制器的自动方法，并且需要在你的路由文件中定义所有路由。

此目录中的所有文件都位于 ``App`` 命名空间下，你可以在 **app/Config/Constants.php** 文件中自由更改 。

system
------
该目录存储构成框架的文件本身。虽然你在使用应用程序目录方面具有很大的灵活性，但系统目录中的文件永远不应该被修改。相反，你应该扩展类或创建新类，以提供所需的相应功能。

此目录中的所有文件都位于 ``CodeIgniter`` 命名空间下。

public
------
**public** 文件夹包含 Web应用程序的浏览器可以直接访问的地址，防止源代码的直接访问。它包含主要的 **.htaccess** 文件，**index.php** 以及其它你想要添加的样式文件地址，比如CSS，javascript或图像。

这个文件夹将成为你站点的"Web根目录"，并且你的Web服务器配置将指向它。

writable
--------
此目录包含在应用程序生命周期中可能需要写入的所有目录。包括用于存储缓存文件，日志和任何用户可能发送使用的目录。你可以在此处添加应用程序需要写入的任何其他目录。这允许你将其他主目录保持为不可写，作为附加的安全措施。

tests
-----
此目录设置为测试文件的存储地址。 ``_support`` 目录包含各种模拟类和其他在编写测试时可以使用的实用程序。该目录请在生产环境中忽略提交/传输到生产环境中。

docs
----
如果此目录是你项目中的一部分，那么此目录包含 CodeIgniter4 用户指南的本地副本。

修改目录位置
-----------------------------

如果你需要重定位任何主目录位置，可以在 ``app/Config/Paths`` 更改配置。

详情请参考 `管理你的应用 <../general/managing_apps.html>`_
