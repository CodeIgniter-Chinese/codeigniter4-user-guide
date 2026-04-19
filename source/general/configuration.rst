#############
配置
#############

每个框架都使用配置文件来定义各项参数和初始设置。CodeIgniter 的配置文件定义了简单的类，所需设置均作为公共属性。

与许多其他框架不同，CodeIgniter 的配置项并不集中在单个文件中。相反，每个需要配置项的类都有一个同名的配置文件。应用程序配置文件位于 **app/Config** 目录下。

.. contents::
    :local:
    :depth: 2


什么是配置类？
*******************************

配置类用于定义系统默认配置值。系统配置值通常是 *静态* 的。配置类旨在保存配置应用运行方式的设置，而不是响应每个用户的个性化设置。

不建议在执行期间修改配置类实例化时设置的值。换言之，建议将配置类视为不可变类或只读类。如果使用了 :ref:`factories-config-caching`，这一点尤为重要。

配置值可以硬编码在类文件中，也可以在实例化时从环境变量中获取。

使用配置文件
********************************

获取 Config 对象
=======================

可以通过几种不同的方式访问类的配置文件。

new 关键字
-----------

使用 ``new`` 关键字创建实例：

.. literalinclude:: configuration/001.php

.. _configuration-config:

config()
--------

使用 :php:func:`config()` 函数：

.. literalinclude:: configuration/002.php

如果不提供命名空间，将首先在 **app/Config** 目录下查找文件；若未找到，则在所有定义的命名空间下的 **Config** 目录中查找。

CodeIgniter 自带的所有配置文件都使用了 ``Config`` 命名空间。在应用程序中使用此命名空间可获得最佳性能，因为系统能准确识别文件位置。

.. note:: 在 v4.4.0 之前，即使指定了完全限定类名（如 ``config(\Acme\Blog\Config\Blog::class)``），只要存在同名的短类名，``config()`` 也会优先在 **app/Config/** 中查找文件。该行为已在 v4.4.0 中修复，现在会返回指定的实例。

获取 Config 属性
=========================

所有配置对象的属性都是公共的，因此可以像访问其他属性一样访问设置：

.. literalinclude:: configuration/003.php

创建配置文件
****************************

需要新配置时，首先在所需位置创建新文件。默认文件位置（大多数情况下的推荐位置）为 **app/Config**。

通过使用不同的命名空间，可以将配置文件放置在任何 **Config** 目录下。

类应使用适当的命名空间，并扩展 ``CodeIgniter\Config\BaseConfig``，以确保其能够接收特定环境的设置。

定义类并填充代表设置的公共属性：

.. literalinclude:: configuration/004.php

环境变量
*********************

使用环境变量是目前应用程序设置的最佳实践之一。原因之一是环境变量易于在部署之间更改而无需改动任何代码。配置在部署过程中可能会频繁变动，但代码不会。例如，开发者的本地机器和生产服务器等多个环境，通常需要针对每个特定的设置采用不同的配置值。

环境变量还应用于处理私密信息，如密码、API 密钥或其他敏感数据。

.. _dotenv-file:

Dotenv 文件
===========

CodeIgniter 通过使用 “dotenv” 文件，使设置环境变量变得简单且无痛。该术语源于文件名：在文本 “env” 前面有一个点。

创建 Dotenv 文件
--------------------

CodeIgniter 要求 **.env** 文件位于项目根目录，即 **app** 目录同级。CodeIgniter 分发了一个位于项目根目录的模板文件，名为 **env** （注意开头没有点 ``.`` ）。

该文件包含项目可能使用的大量变量，并已分配了空值、虚拟值或默认值。可以通过将模板重命名为 **.env** 或将其副本命名为 **.env**，作为应用程序的起点。

.. warning:: 务必确保 **.env** 文件未被版本控制系统跟踪。对于 *git*，这意味着将其添加到 **.gitignore**。否则可能导致敏感凭据泄露到公网。

设置变量
-----------------

设置以简单的键值对形式存储在 **.env** 文件中，中间用等号分隔。
::

    S3_BUCKET = dotenv
    SECRET_KEY = super_secret_key
    CI_ENVIRONMENT = development

应用程序运行时会自动加载 **.env**，并将变量放入环境中。如果环境中已存在某个变量，则不会被覆盖。

获取变量
-----------------

可使用以下任何方式访问加载的环境变量：``getenv()``、``$_SERVER`` 或 ``$_ENV``。

.. literalinclude:: configuration/005.php

.. warning:: 请注意，**.env** 文件中的设置会添加到 ``$_SERVER`` 和 ``$_ENV`` 中。由此带来的副作用是，如果 CodeIgniter 应用程序生成 `var_dump($_ENV)`、`phpinfo()`（出于调试或其他正当理由），或在 ``development`` 环境下显示详细错误报告，**安全凭据将会公开暴露**。

嵌套变量
-----------------

为了节省输入，可以通过将变量名包装在 ``${...}`` 中，重用文件中已指定的变量：

::

    BASE_DIR = "/var/webroot/project-root"
    CACHE_DIR = "${BASE_DIR}/cache"
    TMP_DIR = "${BASE_DIR}/tmp"

带命名空间的变量
--------------------

有时会出现多个同名变量的情况。系统需要一种方式来识别正确的设置。这个问题可以通过为变量设置 “命名空间” 来解决。

带命名空间的变量使用点号表示法来限定变量名，确保并入环境时是唯一的。具体做法是包含一个区分前缀，后跟一个点号（.），然后是变量名本身。

::

    // 不带命名空间的变量
    name = "George"
    db = my_db

    // 带命名空间的变量
    address.city = "Berlin"
    address.country = "Germany"
    frontend.db = sales
    backend.db = admin
    BackEnd.db = admin

.. _env-var-namespace-separator:

命名空间分隔符
-------------------

某些环境（如 Docker、CloudFormation）不允许变量名包含点号（``.``）。在这种情况下，自 v4.1.5 起，也可以使用下划线（``_``）作为分隔符。

::

    // 使用下划线的带命名空间的变量
    app_forceGlobalSecureRequests = true
    app_CSPEnabled = true

.. _configuration-classes-and-environment-variables:

配置类与环境变量
***********************************************

实例化配置类时，系统会考虑将任何 *带命名空间* 的环境变量合并到配置对象的属性中。

.. important:: 无法通过设置环境变量来添加新属性，也无法将标量值更改为数组。请参阅 :ref:`env-var-replacements-for-data`。

.. note:: 此功能在 ``CodeIgniter\Config\BaseConfig`` 类中实现。因此，对于 **app/Config** 目录下少数未扩展该类的文件，此功能将不起作用。

如果带命名空间变量的前缀与配置类的命名空间完全匹配，则设置的后续部分（点号之后）将被视为配置属性。如果匹配现有配置属性，环境变量的值将替换配置文件中的相应值。如果不匹配，配置类的属性将保持不变。在此用法中，前缀必须是类的完整命名空间（区分大小写）。

::

    Config\App.forceGlobalSecureRequests = true
    Config\App.CSPEnabled = true

.. note:: 命名空间前缀和属性名均区分大小写。必须与配置类文件中定义的完整命名空间和属性名完全匹配。

*短前缀* 同样适用，即仅使用配置类名的小写形式作为命名空间。如果短前缀与类名匹配，**.env** 中的值将替换配置文件中的值。

::

    app.forceGlobalSecureRequests = true
    app.CSPEnabled = true

自 v4.1.5 起，也可以使用下划线写法::

    app_forceGlobalSecureRequests = true
    app_CSPEnabled = true

.. note:: 使用 *短前缀* 时，属性名仍必须与类中定义的名称完全匹配。

.. _env-var-replacements-for-data:

环境变量作为数据替换
==============================================

务必牢记，**.env** 中的环境变量 **仅作为现有标量值的替换**。

简单来说，只能通过在 **.env** 中进行设置，来更改 Config 类中已存在的标量属性值。

    1. 无法添加 Config 类中未定义的属性。
    2. 无法将属性中的标量值更改为数组。
    3. 无法向现有数组添加元素。

例如，不能直接在 **.env** 中设置 ``app.myNewConfig = foo``，并指望 ``Config\App`` 在运行时神奇地拥有该属性和值。

当 ``Config\Database`` 中存在属性 ``$default = ['encrypt' => false]`` 时，即使在 **.env** 中设置了 ``database.default.encrypt.ssl_verify = true``，也无法将 ``encrypt`` 的值更改为数组。如需此类操作，请参阅 :ref:`数据库配置 <database-config-with-env-file>`。

将环境变量视为数组
========================================

带命名空间的环境变量可以进一步被视为数组。如果前缀与配置类匹配，且环境变量名的其余部分也包含点号，则该部分将被视为数组引用。

::

    // 普通带命名空间的变量
    Config\SimpleConfig.name = George

    // 数组带命名空间的变量
    Config\SimpleConfig.address.city = "Berlin"
    Config\SimpleConfig.address.country = "Germany"

如果上述变量引用的是 SimpleConfig 配置对象，则会按如下方式处理：

.. literalinclude:: configuration/006.php

``$address`` 属性的其他任何元素都将保持不变。

也可以使用数组属性名作为前缀。如果环境文件中包含以下内容，结果将与上述相同。

::

    // 数组带命名空间的变量
    Config\SimpleConfig.address.city = "Berlin"
    address.country = "Germany"

处理不同环境
*******************************

通过使用单独的 **.env** 文件并根据环境需求修改其中的值，可以轻松配置多个环境。

该文件不应包含应用程序所使用的每个配置类的所有可能设置。实际上，它应仅包含特定于环境的项目，或者诸如密码、API 密钥等不应公开的敏感细节。不过，任何在部署之间发生变化的内容都可以包含在内。

在每个环境中，将 **.env** 文件放置在项目的根目录下。对于大多数设置，这与 ``app`` 目录同级。

不要使用版本控制系统跟踪 **.env** 文件。如果这样做且存储库被公开，敏感信息将会暴露给所有人。

.. _registrars:

注册器
**********

“注册器”是指任何可能提供额外配置属性的其他类。注册器提供了一种在运行时跨命名空间和文件更改配置的方法。

如果在 :doc:`模块 </general/modules>` 中启用了 :ref:`auto-discovery`，注册器即可工作。它会在实例化 Config 对象时修改配置属性。

.. note:: 此功能在 ``CodeIgniter\Config\BaseConfig`` 类中实现。因此，对于 **app/Config** 目录下少数未扩展该类的文件，此功能将不起作用。

实现注册器有两种方式：**隐式** 和 **显式**。

.. note:: **.env** 中的值始终优先于注册器。

隐式注册器
===================

隐式注册器可以更改任何配置类的属性。

任何命名空间都可以通过使用 **Config/Registrar.php** 文件来定义隐式注册器。这些文件是类，其方法以希望扩展的每个配置类命名。

例如，第三方模块或 Composer 包可能希望向 ``Config\Pager`` 提供额外的模板，而不覆盖开发者已经配置的内容。在 **src/Config/Registrar.php** 中会有一个 ``Registrar`` 类，其中包含单个 ``Pager()`` 方法（注意区分大小写）：

.. literalinclude:: configuration/007.php

注册器方法必须始终返回一个数组，其键与目标配置文件的属性相对应。现有值会被合并，且注册器属性具有覆盖优先级。

显式注册器
===================

显式注册器只能更改其注册所在的配置类的属性。

配置文件也可以显式指定任意数量的注册器。通过在配置文件中添加一个 ``$registrars`` 属性来实现，该属性包含一个候选注册器名称数组：

.. literalinclude:: configuration/008.php

为了充当“注册器”，所确定的类必须具有一个与配置类同名的静态函数，并应返回属性设置的关联数组。

实例化配置对象时，它将遍历 ``$registrars`` 中指定的类。对于这些类中的每一个，它将调用以配置类命名的方法，并合并返回的任何属性。

此示例配置类设置如下：

.. literalinclude:: configuration/009.php

... 相关的区域销售模型可能如下所示：

.. literalinclude:: configuration/010.php

在上述示例中，当 ``MySalesConfig`` 实例化时，最终将拥有三个声明的属性，但 ``$target`` 属性的值将被覆盖，因为 ``RegionalSales`` 被视为“注册器”。生成的配置属性如下：

.. literalinclude:: configuration/011.php

.. _confirming-config-values:

确认配置值
************************

实际的 Config 对象属性值在运行时由 :ref:`registrars`、:ref:`环境变量 <configuration-classes-and-environment-variables>` 以及 :ref:`factories-config-caching` 进行更改。

CodeIgniter 提供了以下 :doc:`命令 <../cli/spark_commands>` 来检查实际的配置值。

.. _spark-config-check:

config:check
============

.. versionadded:: 4.5.0

例如，如果要检查 ``Config\App`` 实例：

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

可以查看配置缓存是否已启用。

.. note:: 如果启用了配置缓存，将永久使用缓存值。有关详情，请参阅 :ref:`factories-config-caching`。
