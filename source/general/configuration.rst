#############
配置
#############

每个框架都使用配置文件来定义许多参数和初始设置。CodeIgniter 配置文件定义了简单的类,其中所需的设置是公共属性。

与许多其他框架不同,CodeIgniter 的可配置项不包含在单个文件中。相反,每个需要可配置项的类都有一个与使用它的类同名的配置文件。你可以在 **app/Config** 文件夹中找到应用程序配置文件。

.. contents::
    :local:
    :depth: 2

什么是配置类？
*******************************

配置类用于定义系统默认配置值。系统配置值通常是*静态*的。配置类旨在保留配置应用程序操作方式的设置，而不是响应每个用户的个别设置。

不建议在配置类实例化后，在执行期间修改值。换句话说，建议将配置类视为不可变或只读的类。这尤其重要，如果你使用 :ref:`factories-config-caching`。

配置值可以在类文件中硬编码，也可以在实例化时从环境变量中获取。

使用配置文件
**********************************

获取配置对象
=======================

你可以通过几种不同的方式访问类的配置文件。

使用 new 关键字
---------------

使用 ``new`` 关键字创建一个实例:

.. literalinclude:: configuration/001.php

.. _configuration-config:

config()
--------

使用 :php:func:`config()` 函数:

.. literalinclude:: configuration/002.php

如果未提供命名空间，它将首先在 **app/Config** 文件夹中查找文件，如果找不到，则在所有定义的命名空间的 **Config** 文件夹中查找。

CodeIgniter 提供的所有配置文件都使用 ``Config`` 命名空间。在你的应用程序中使用这个命名空间将提供最佳性能,因为它确切知道在哪里可以找到这些文件。

你可以通过使用不同的命名空间将配置文件放在任何你想要的文件夹中。这允许你在生产服务器上将配置文件放在一个不可公开访问的文件夹中,同时在开发期间保持其位于 **/app** 下方便访问。

.. note:: 在 v4.4.0 之前，``config()`` 会在有与 shortname 相同的类时，在 **app/Config/** 中查找文件，即使你指定了完全限定的类名，如 ``config(\Acme\Blog\Config\Blog::class)``。在 v4.4.0 中修复了此行为，并返回指定的实例。

获取配置属性
=========================

所有配置对象属性都是公共的,所以你可以像访问任何其他属性一样访问设置:

.. literalinclude:: configuration/003.php

创建配置文件
****************************

当你需要一个新的配置时,首先在所需位置创建一个新文件。默认文件位置(大多数情况下推荐)是 **app/Config**。该类应使用适当的命名空间,并且它应扩展 ``CodeIgniter\Config\BaseConfig`` 以确保它可以接收特定环境的设置。

你可以通过使用不同的命名空间将配置文件放置在任何 **Config** 文件夹中。

该类应使用适当的命名空间，并应扩展 ``CodeIgniter\Config\BaseConfig`` 以确保它可以接收特定于环境的设置。

定义类并用代表你的设置的公共属性填充它:

.. literalinclude:: configuration/004.php

环境变量
*********************

今天应用程序设置的最佳实践之一是使用环境变量。原因之一是环境变量可以在不更改任何代码的情况下在部署之间轻松更改。配置在部署之间可能会有很大变化,但代码不会。例如,多个环境(如开发者的本地机器和生产服务器)通常需要针对每个特定设置配置不同的值。

环境变量也应该用于任何私人信息,如密码、API 密钥或其他敏感数据。

.. _dotenv-file:

Dotenv 文件
===========

CodeIgniter 通过使用 “dotenv” 文件使设置环境变量变得简单轻松。该术语来源于文件名,文件名以点号开头,然后是 “env”文本。

创建 Dotenv 文件
--------------------

CodeIgniter 期望 **.env** 文件与 **app** 目录一起位于项目的根目录中。 CodeIgniter 中分发了一个位于项目根目录 named 的模板文件 **env** (注意开头没有点号(``.``)?)。

它包含了项目可能会使用的大量变量,并分配了空、虚拟或默认值。你可以通过重命名模板为 **.env** 或复制为名为 **.env** 的副本,将此文件用作应用程序的起点。

.. warning:: 确保 **.env** 文件NOT被你的版本控制系统跟踪。 对于 *git* 来说,这意味着将其添加到 **.gitignore**。 否则可能会导致敏感证书被公开。

设置变量
-----------------

设置以简单的名称/值对的集合存储在 **.env** 文件中,用等号分隔。
::

    S3_BUCKET = dotenv
    SECRET_KEY = super_secret_key
    CI_ENVIRONMENT = development

当你的应用程序运行时, **.env** 将自动加载,并将变量放入环境中。如果环境中已经存在一个变量,它将不会被覆盖。

获取变量
-----------------

加载的环境变量可以使用下列任意一种访问:
``getenv()``、``$_SERVER`` 或 ``$_ENV``。

.. literalinclude:: configuration/005.php

.. warning:: 请注意,来自 **.env** 文件的设置会添加到 ``$_SERVER`` and ``$_ENV`` 中。由此带来的一个副作用是,如果你的 CodeIgniter 应用程序生成一个 ``var_dump($_ENV)`` 或 ``phpinfo()`` (用于调试或其他有效原因) ，或者在 ``development`` 环境中显示了详细的错误报告，**你的安全凭据可能会公开暴露**。

嵌套变量
-----------------

为了省去输入,你可以通过在 ``${...}`` 内包装变量名来重用已经在文件中指定的变量:

::

    BASE_DIR = "/var/webroot/project-root"
    CACHE_DIR = "${BASE_DIR}/cache"
    TMP_DIR = "${BASE_DIR}/tmp"

命名空间变量
--------------------

有时你会有多个同名变量。系统需要一种方法来确定应使用的正确设置。这通过为变量“命名空间”来解决这个问题。

命名空间变量使用点表示法来限定变量名,以便在合并到环境时它们是唯一的。这是通过在变量名称前面包含区别前缀和点号(.)来完成的。

::

    // 非命名空间变量
    name = "George"
    db = my_db

    // 命名空间变量
    address.city = "Berlin"
    address.country = "Germany"
    frontend.db = sales
    backend.db = admin
    BackEnd.db = admin

.. _env-var-namespace-separator:

命名空间分隔符
-------------------

某些环境,例如 Docker、CloudFormation 不允许带点号(``.``)的变量名。在这种情况下,从 v4.1.5 开始,你也可以使用下划线 (``_``) 作为分隔符。

::

    // 使用下划线的命名空间变量
    app_forceGlobalSecureRequests = true
    app_CSPEnabled = true

.. _configuration-classes-and-environment-variables:

配置类和环境变量
***********************************************

当你实例化一个配置类时,任何 *命名空间* 环境变量都会被考虑合并到配置对象的属性中。

.. important:: 你无法通过设置环境变量来添加新属性,也不能将标量值改变为数组。请参见 :ref:`env-var-replacements-for-data`。

.. note:: 此功能是在 ``CodeIgniter\Config\BaseConfig`` 类中实现的。因此，它不适用于 **app/Config** 文件夹中的一些文件，这些文件不扩展该类。

如果命名空间变量的前缀正好匹配配置类的命名空间,那么设置的尾部(点之后)将被视为配置属性。如果它与现有的配置属性匹配,环境变量的值将替换配置文件中相应的值。如果没有匹配,配置类属性保持不变。在此用法中,前缀必须是类的完整(区分大小写)命名空间。

::

    Config\App.forceGlobalSecureRequests = true
    Config\App.CSPEnabled = true

.. note:: 命名空间前缀和属性名均区分大小写。它们必须完全匹配配置类文件中定义的完整命名空间和属性名称。

使用仅包含配置类名称的小写版本的 *短前缀* 相同。如果短前缀匹配类名,则 **.env** 中的值将替换配置文件中的值。

::

    app.forceGlobalSecureRequests = true
    app.CSPEnabled = true

从 v4.1.5 开始,你也可以使用下划线::

    app_forceGlobalSecureRequests = true
    app_CSPEnabled = true

.. note:: 使用 *短前缀* 时,属性名称仍必须完全匹配类中定义的名称。

.. _env-var-replacements-for-data:

作为数据的环境变量
==============================================

务必要始终记住，你的 **.env** 文件中的环境变量**只是现有标量值的替代**。

简单来说，你只能通过在 **.env** 文件中设置来更改 Config 类中存在的属性的标量值。

    1. 你不能添加 Config 类中未定义的属性。
    2. 你不能将属性中的标量值更改为数组。
    3. 你不能向现有数组中添加元素。

例如,你不能只是在 **.env** 中放置 ``app.myNewConfig = foo`` 并期望你的 ``Config\App`` 在运行时神奇地拥有该属性和值。

当你在 ``Config\Database`` 中有属性 ``$default = ['encrypt' => false]`` 时,即使你在 **.env** 中放置 ``database.default.encrypt.ssl_verify = true``,也不能将 ``encrypt`` 值更改为数组。如果你想这样做，请参阅 :ref:`Database Configuration <database-config-with-env-file>`。

将环境变量视为数组
========================================

可以进一步将命名空间环境变量视为数组。
如果前缀与配置类匹配,则环境变量名称的其余部分在也包含点时将被视为数组引用。

::

    // 常规命名空间变量
    Config\SimpleConfig.name = George

    // 数组命名空间变量
    Config\SimpleConfig.address.city = "Berlin"
    Config\SimpleConfig.address.country = "Germany"

如果这是指向 SimpleConfig 配置对象,那么上面的示例将被视为:

.. literalinclude:: configuration/006.php

``$address`` 属性的任何其他元素保持不变。

你也可以使用数组属性名称作为前缀。如果环境文件包含以下内容,结果与上面相同。

::

    // 数组命名空间变量
    Config\SimpleConfig.address.city = "Berlin"
    address.country = "Germany"

处理不同环境
*******************************

通过使用带有修改后的值来满足该环境需求的单独 **.env** 文件,可以轻松配置多个环境。

该文件不应包含应用程序使用的每个可能的配置类的每一个可能设置。事实上,它应该只包含特定于该环境的项目,以及密码、API 密钥等不应公开暴露的敏感详细信息。但是任何在部署之间更改的都很合适。

在每个环境中,将 **.env** 文件放在项目的根目录中。对于大多数设置来说,这将与 ``app`` 目录处于同一级别。

不要使用版本控制系统跟踪 **.env** 文件。如果这样做,并且存储库被公开,你将在所有人都可以找到的地方放置敏感信息。

.. _registrars:

注册器
**********

“注册器”是可以在命名空间和文件之间在运行时提供其他配置属性的任何其他类。
注册器提供了一种在运行时跨命名空间和文件更改配置的方法。

如果在 :doc:`模块 </general/modules>` 中启用了 :ref:`auto-discovery`，则注册器可以在命名空间和文件之间在运行时更改配置属性。

有两种实现注册器的方法: **隐式** 和 **显式**。

.. note:: 来自 **.env** 的值始终优先于注册器。

隐式注册器
===================

隐式注册器可以更改任何配置类的属性。

任何命名空间都可以通过使用 **Config/Registrar.php** 文件定义隐式注册器。这些文件是类，其方法的名称与你希望扩展的每个配置类的名称相同。

例如，第三方模块或 Composer 包可能希望为 ``Config\Pager`` 提供额外的模板，而不会覆盖开发人员已经配置的内容。在 **src/Config/Registrar.php** 中，将有一个名为 ``Registrar`` 的类，其中只有一个 ``Pager()`` 方法（注意大小写敏感）：

.. literalinclude:: configuration/007.php

注册方法必须始终返回一个数组,其中的键对应目标配置文件中的属性。存在的值被合并,注册器属性具有覆盖优先级。

显式注册器
===================

显式注册器只能更改其注册的配置类属性。

配置文件还可以显式指定任意数量的注册器。
这是通过在配置文件中添加一个 ``$registrars`` 属性来完成的,其中包含候选注册器的名称数组:

.. literalinclude:: configuration/008.php

为了充当“注册器”,标识的类必须具有一个与配置类同名的静态函数,它应返回一个关联数组的属性设置。

在实例化配置对象时,它将循环遍历 ``$registrars`` 中指定的类。对于这些类中的每个类,它都会调用以配置类命名的方法,并合并任何返回的属性。

针对此设置的配置类示例:

.. literalinclude:: configuration/009.php

... 相关的区域销售模型可能如下所示:

.. literalinclude:: configuration/010.php

通过上面的示例,在实例化 ``MySalesConfig`` 时,它将最终具有声明的三个属性,但 ``$target`` 属性的值将通过将 ``RegionalSales`` 视为“注册器”来覆盖。生成的配置属性:

.. literalinclude:: configuration/011.php

.. _confirming-config-values:

确认配置值
************************

实际的 Config 对象属性值在运行时由 :ref:`registrars`、:ref:`环境变量 <configuration-classes-and-environment-variables>` 和 :ref:`factories-config-caching` 进行更改。

CodeIgniter 有以下 :doc:`命令 <../cli/spark_commands>` 来检查实际的配置值。

.. _spark-config-check:

config:check
============

.. versionadded:: 4.5.0

例如，如果你想检查 ``Config\App`` 实例：

.. code-block:: console

    php spark config:check App

输出结果如下：

.. code-block:: none

    Config\App#6 (12) (
        public 'baseURL' -> string (22) "http://localhost:8080/"
        public 'allowedHostnames' -> array (0) []
        public 'indexPage' -> string (9) "index.php"
        public 'uriProtocol' -> string (11) "REQUEST_URI"
        public 'defaultLocale' -> string (2) "en"
        public 'negotiateLocale' -> boolean false
        public 'supportedLocales' -> array (1) [
            0 => string (2) "en"
        ]
        public 'appTimezone' -> string (3) "UTC"
        public 'charset' -> string (5) "UTF-8"
        public 'forceGlobalSecureRequests' -> boolean false
        public 'proxyIPs' -> array (0) []
        public 'CSPEnabled' -> boolean false
    )

    Config Caching: Disabled

你可以看到配置缓存是否已启用。

.. note:: 如果启用了配置缓存，则始终使用缓存的值。有关详情，请参阅 :ref:`factories-config-caching`。
