#############
配置
#############

每个框架都使用配置文件来定义众多参数和初始设置。CodeIgniter 的配置文件定义了简单的类，其中所需的设置是公共属性。

与许多其他框架不同，CodeIgniter 的可配置项并不包含在单个文件中。相反，每个需要可配置项的类都会有一个与其使用的类同名的配置文件。你可以在 **app/Config** 文件夹中找到应用程序的配置文件。

.. contents::
    :local:
    :depth: 2


什么是配置类？
*******************************

配置类用于定义系统默认的配置值。系统配置值通常是 *静态的*。配置类旨在保留配置应用程序运行方式的设置，而不是响应每个用户的个人设置。

不建议在配置类实例化期间设置的值在后续执行过程中进行修改。换句话说，建议将配置类视为不可变或只读类。如果你使用 :ref:`factories-config-caching`，这一点尤为重要。

配置值可以在类文件中硬编码，也可以在实例化时从环境变量中获取。

使用配置文件
********************************

获取配置对象
=======================

你可以通过几种不同的方式访问类的配置文件。

new 关键字
-----------

通过使用 ``new`` 关键字创建实例：

.. literalinclude:: configuration/001.php

.. _configuration-config:

config()
--------

通过使用 :php:func:`config()` 函数：

.. literalinclude:: configuration/002.php

如果没有提供命名空间，它会首先在 **app/Config** 文件夹中查找文件，如果未找到，则在所有已定义命名空间的 **Config** 文件夹中查找。

所有随 CodeIgniter 一起提供的配置文件都使用 ``Config`` 命名空间。在应用程序中使用此命名空间将提供最佳性能，因为它确切知道在哪里找到文件。

.. note:: 在 v4.4.0 之前，即使你指定了完全限定的类名（如 ``config(\Acme\Blog\Config\Blog::class)``），``config()`` 也会在 **app/Config/** 中查找具有相同短名称的类的文件。此行为已在 v4.4.0 中修复，并返回指定的实例。

获取配置属性
=========================

所有配置对象属性都是公共的，因此你可以像访问其他任何属性一样访问这些设置：

.. literalinclude:: configuration/003.php

创建配置文件
****************************

当你需要新的配置时，首先在所需位置创建一个新文件。默认文件位置（大多数情况下推荐）是 **app/Config**。

你可以通过使用不同的命名空间将配置文件放在任何 **Config** 文件夹中。

该类应使用适当的命名空间，并且应继承 ``CodeIgniter\Config\BaseConfig`` 以确保它能够接收特定于环境的设置。

定义类并用代表你设置的公共属性填充它：

.. literalinclude:: configuration/004.php

环境变量
*********************

使用环境变量是当今应用程序设置的最佳实践之一。主要原因是，环境变量可以在不同部署环境之间轻松更改，无需修改任何代码。配置会因部署环境而异，但代码保持不变。例如，开发者的本地机器和生产服务器等不同环境，通常需要为每个特定环境使用不同的配置值。

环境变量还应该用于任何私密信息，如密码、API 密钥或其他敏感数据。

.. _dotenv-file:

Dotenv 文件
===========

CodeIgniter 通过使用 "dotenv" 文件使设置环境变量变得简单无痛。这个术语来自文件名，它在 "env" 文本前以点号开头。

创建 Dotenv 文件
--------------------

CodeIgniter 期望 **.env** 文件位于项目根目录中，与 **app** 目录并列。CodeIgniter 分发了一个模板文件，位于项目根目录，名为 **env**（注意开头没有点号（``.``）？）。

它包含大量你的项目可能使用的变量，这些变量已被分配为空值、虚拟值或默认值。你可以将此文件作为应用程序的起点，方法是将模板重命名为 **.env**，或者复制一份名为 **.env** 的文件。

.. warning:: 确保 **.env** 文件未被你的版本控制系统跟踪。对于 *git*，这意味着将其添加到 **.gitignore** 中。如果不这样做，可能会导致敏感凭据暴露给公众。

设置变量
-----------------

设置在 **.env** 文件中以简单的名称/值对集合形式存储，用等号分隔。
::

    S3_BUCKET = dotenv
    SECRET_KEY = super_secret_key
    CI_ENVIRONMENT = development

当你的应用程序运行时，**.env** 将自动加载，变量将被放入环境中。如果环境中已存在变量，则不会被覆盖。

获取变量
-----------------

加载的环境变量可以通过以下任一方式访问：
``getenv()``、``$_SERVER`` 或 ``$_ENV``。

.. literalinclude:: configuration/005.php

.. warning:: 注意，你的 **.env** 文件中的设置会被添加到 ``$_SERVER`` 和 ``$_ENV`` 中。作为副作用，这意味着如果你的 CodeIgniter 应用程序（例如）生成 ``var_dump($_ENV)`` 或 ``phpinfo()``（用于调试或其他有效原因），或在 ``development`` 环境中显示详细的错误报告，**你的安全凭据将被公开暴露**。

嵌套变量
-----------------

为了减少输入，你可以通过将变量名包装在 ``${...}`` 中来重用文件中已指定的变量：

::

    BASE_DIR = "/var/webroot/project-root"
    CACHE_DIR = "${BASE_DIR}/cache"
    TMP_DIR = "${BASE_DIR}/tmp"

命名空间变量
--------------------

有时你会有多个同名的变量。系统需要一种方法来知道正确的设置应该是什么。这个问题通过 "*命名空间*" 变量来解决。

命名空间变量使用点符号来限定变量名，使它们在合并到环境变量时保持唯一。这是通过包含一个区分前缀，后跟一个点（.），然后是变量名本身来完成的。

::

    // 未命名空间的变量
    name = "George"
    db = my_db

    // 命名空间的变量
    address.city = "Berlin"
    address.country = "Germany"
    frontend.db = sales
    backend.db = admin
    BackEnd.db = admin

.. _env-var-namespace-separator:

命名空间分隔符
-------------------

某些环境（例如 Docker、CloudFormation）不允许变量名包含点号（``.``）。在这种情况下，从 v4.1.5 开始，你也可以使用下划线（``_``）作为分隔符。

::

    // 使用下划线的命名空间变量
    app_forceGlobalSecureRequests = true
    app_CSPEnabled = true

.. _configuration-classes-and-environment-variables:

配置类和环境变量
***********************************************

当你实例化配置类时，任何 *命名空间* 的环境变量都会被考虑合并到配置对象的属性中。

.. important:: 你不能通过设置环境变量来添加新属性，也不能将标量值更改为数组。请参阅 :ref:`env-var-replacements-for-data`。

.. note:: 此功能在 ``CodeIgniter\Config\BaseConfig`` 类中实现。因此，对于 **app/Config** 文件夹中不继承该类的少数文件，它将不起作用。

如果命名空间变量的前缀与配置类的命名空间完全匹配，则设置的尾部部分（点号之后）将被视为配置属性。如果它与现有的配置属性匹配，环境变量的值将替换配置文件中的相应值。如果没有匹配，配置类属性将保持不变。在此用法中，前缀必须是类的完整（区分大小写）命名空间。

::

    Config\App.forceGlobalSecureRequests = true
    Config\App.CSPEnabled = true

.. note:: 命名空间前缀和属性名都是区分大小写的。它们必须与配置类文件中定义的完整命名空间和属性名完全匹配。

对于 *短前缀*（即仅使用配置类名的小写版本的命名空间）也是如此。如果短前缀与类名匹配，**.env** 中的值将替换配置文件中的值。

::

    app.forceGlobalSecureRequests = true
    app.CSPEnabled = true

从 v4.1.5 开始，你也可以使用下划线编写：

::

    app_forceGlobalSecureRequests = true
    app_CSPEnabled = true

.. note:: 使用 *短前缀* 时，属性名仍必须与类中定义的名称完全匹配。

.. _env-var-replacements-for-data:

环境变量作为数据的替换
==============================================

始终牢记，**.env** 中包含的环境变量 **仅用于替换现有的标量值**。

简单来说，你只能通过在 **.env** 中设置来更改 Config 类中存在的属性的标量值。

    1. 你不能添加 Config 类中未定义的属性。
    2. 你不能将属性中的标量值更改为数组。
    3. 你不能向现有数组中添加元素。

例如，你不能在 **.env** 中放入 ``app.myNewConfig = foo`` 并期望你的 ``Config\App`` 在运行时神奇地拥有该属性和值。

当你的 ``Config\Database`` 中有属性 ``$default = ['encrypt' => false]`` 时，即使你在 **.env** 中放入 ``database.default.encrypt.ssl_verify = true``，也不能将 ``encrypt`` 值更改为数组。如果你想这样做，请参阅 :ref:`Database Configuration <database-config-with-env-file>`。

将环境变量视为数组
========================================

命名空间环境变量可以进一步被视为数组。如果前缀与配置类匹配，则环境变量名称的其余部分如果也包含点号，则被视为数组引用。

::

    // 普通命名空间变量
    Config\SimpleConfig.name = George

    // 数组命名空间变量
    Config\SimpleConfig.address.city = "Berlin"
    Config\SimpleConfig.address.country = "Germany"

如果这是引用 SimpleConfig 配置对象，上述示例将被视为：

.. literalinclude:: configuration/006.php

``$address`` 属性的任何其他元素将保持不变。

你也可以使用数组属性名作为前缀。如果环境文件包含以下内容，则结果将与上述相同。

::

    // 数组命名空间变量
    Config\SimpleConfig.address.city = "Berlin"
    address.country = "Germany"

处理不同环境
*******************************

通过使用单独的 **.env** 文件（其值已修改以满足该环境的需求），可以轻松完成多环境配置。

该文件不应包含应用程序使用的所有配置类的每个可能设置。实际上，它应该只包含特定于环境的项目，或者是密码、API 密钥和其他不应暴露的敏感详细信息。但任何在部署之间发生变化的内容都是合理的。

在每个环境中，将 **.env** 文件放在项目的根文件夹中。对于大多数设置，这将与 ``app`` 目录处于同一级别。

不要使用版本控制系统跟踪 **.env** 文件。如果你这样做，并且存储库是公开的，你就会将敏感信息放在每个人都能找到的地方。

.. _registrars:

注册器
**********

"注册器" 是任何可能提供额外配置属性的其他类。注册器提供了一种在运行时跨命名空间和文件更改配置的方法。

如果在 :doc:`Modules </general/modules>` 中启用了 :ref:`auto-discovery`，注册器就会工作。它在 Config 对象实例化时更改配置属性。

.. note:: 此功能在 ``CodeIgniter\Config\BaseConfig`` 类中实现。因此，对于 **app/Config** 文件夹中不继承该类的少数文件，它将不起作用。

有两种实现注册器的方法：**隐式** 和 **显式**。

.. note:: **.env** 中的值始终优先于注册器。

隐式注册器
===================

隐式注册器可以更改任何 Config 类属性。

任何命名空间都可以通过使用 **Config/Registrar.php** 文件定义隐式注册器。这些文件是类，其方法以你希望扩展的每个配置类命名。

例如，第三方模块或 Composer 包可能希望向 ``Config\Pager`` 提供额外的模板，而不会覆盖开发者已经配置的任何内容。在 **src/Config/Registrar.php** 中会有一个 ``Registrar`` 类，其中包含单个 ``Pager()`` 方法（注意大小写敏感）：

.. literalinclude:: configuration/007.php

注册器方法必须始终返回一个数组，其键对应于目标配置文件的属性。现有值将被合并，注册器属性具有覆盖优先级。

显式注册器
===================

显式注册器只能更改它们注册的 Config 类属性。

配置文件还可以显式指定任意数量的注册器。这是通过在配置文件中添加一个 ``$registrars`` 属性来完成的，该属性包含候选注册器名称的数组：

.. literalinclude:: configuration/008.php

为了充当 "注册器"，所标识的类必须具有与配置类同名的静态函数，并且应该返回属性设置的关联数组。

当你的配置对象被实例化时，它将遍历 ``$registrars`` 中指定的类。对于这些类中的每一个，它将调用以配置类命名的方法并合并任何返回的属性。

为此设置的示例配置类：

.. literalinclude:: configuration/009.php

... 相关的区域销售模型可能如下所示：

.. literalinclude:: configuration/010.php

在上述示例中，当 ``MySalesConfig`` 被实例化时，它将最终拥有声明的三个属性，但 ``$target`` 属性的值将通过将 ``RegionalSales`` 视为 "注册器" 而被覆盖。结果配置属性：

.. literalinclude:: configuration/011.php

.. _confirming-config-values:

确认配置值
************************

实际的 Config 对象属性值在运行时由 :ref:`registrars` 和 :ref:`Environment Variables <configuration-classes-and-environment-variables>` 以及 :ref:`factories-config-caching` 更改。

CodeIgniter 具有以下 :doc:`命令 <../cli/spark_commands>` 来检查实际的 Config 值。

.. _spark-config-check:

config:check
============

.. versionadded:: 4.5.0

例如，如果你想检查 ``Config\App`` 实例：

.. code-block:: console

    php spark config:check App

输出如下所示：

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

你可以看到 Config Caching 是否启用。

.. note:: 如果启用了 Config Caching，则会永久使用缓存的值。有关详细信息，请参阅 :ref:`factories-config-caching`。
