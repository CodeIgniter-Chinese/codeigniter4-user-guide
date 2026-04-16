######################
数据库配置
######################

.. contents::
    :local:
    :depth: 3

.. note::
    有关当前支持的数据库驱动，请参阅 :ref:`requirements-supported-databases`。

***********
配置文件
***********

CodeIgniter 提供了一个配置文件，用于存储你的数据库连接信息（用户名、密码、数据库名等）。该配置文件位于 **app/Config/Database.php**。你也可以在 **.env** 文件中设置数据库连接值。更多详细信息，请参见下文。

设置默认数据库
========================

配置设置存储在一个类属性中，该属性是一个具有以下原型的数组：

.. literalinclude:: configuration/001.php

类属性的名称即为连接名，可以在连接时使用该名称来指定组名。

.. note:: SQLite3 数据库的默认位置是 **writable** 目录。
    如果要更改位置，必须设置新目录的完整路径（例如，'database' => WRITEPATH . 'db/database_name.db'）。

DSN
---

某些数据库驱动（如 Postgre、OCI8）需要完整的 DSN（数据源名称）字符串才能连接。
但如果对于需要 DSN 的驱动你未指定 DSN 字符串，CodeIgniter 将尝试使用其余提供的设置来构建它。

如果指定了 DSN，你应该使用 ``'DSN'`` 配置设置，就像使用驱动程序底层的原生 PHP 扩展一样，如下所示：

.. literalinclude:: configuration/002.php
    :lines: 11-15

通用 DSN 格式
^^^^^^^^^^^^^^^^^^^^^^^

你也可以以通用格式（类似 URL）设置 DSN。在这种情况下，DSN 必须具有以下原型：

.. literalinclude:: configuration/003.php
    :lines: 11-14

使用通用版本的 DSN 字符串连接时，若要覆盖默认的配置值，
请将配置变量作为查询字符串添加：

.. literalinclude:: configuration/004.php
    :lines: 11-15

.. literalinclude:: configuration/010.php
    :lines: 11-15

.. note:: 如果你提供了 DSN 字符串但缺少某些有效设置（例如，数据库字符集），而这些设置存在于其余的配置字段中，CodeIgniter 将会追加它们。

故障转移
---------

你也可以指定故障转移，以应对主连接因某种原因无法连接的情况。
这些故障转移可以通过为连接设置 failover 来指定，如下所示：

.. literalinclude:: configuration/005.php

你可以根据需要指定任意数量的故障转移。

设置多个数据库
==========================

你可以选择性地存储多组连接值。
例如，如果你在单个安装下运行多个环境（开发、生产、测试等），
可以为每个环境设置一个连接组，然后根据需要在各组之间切换。例如，要设置一个“test”环境，你可以这样做：

.. literalinclude:: configuration/006.php

然后，要全局告知系统使用该组，你需要设置配置文件中的这个变量：

.. literalinclude:: configuration/007.php

.. note:: 名称 ``test`` 是任意的，你可以将其设置为任何名称。
    默认情况下，我们为主连接使用了 ``default`` 这个词，
    但它也可以根据你的项目需求重命名为更相关的名称。

自动切换数据库
================================

你可以修改配置文件，通过在类的构造函数中添加必要的逻辑来检测环境，并自动将 ``defaultGroup`` 的值更新为正确的组：

.. literalinclude:: configuration/008.php

.. _database-config-with-env-file:

**************************
使用 .env 文件进行配置
**************************

你也可以在 **.env** 文件中保存配置值，并使用当前服务器的数据库设置。你只需要输入与默认组配置设置不同的值。这些值应遵循以下格式，其中 ``default`` 是组名::

    database.default.username = 'root';
    database.default.password = '';
    database.default.database = 'ci4';

但你不能通过设置环境变量来添加新属性，也不能将标量值更改为数组。详情请参阅 :ref:`env-var-replacements-for-data`。

因此，如果你想在 MySQL 中使用 SSL，需要一个变通方法。例如，在你的 **.env** 文件中将数组值设置为 JSON 字符串：

::

    database.default.encrypt = {"ssl_verify":true,"ssl_ca":"/var/www/html/BaltimoreCyberTrustRoot.crt.pem"}

然后在 Config 类的构造函数中解码：

.. literalinclude:: configuration/009.php

.. _database-config-explanation-of-values:

*********************
配置值说明
*********************

================ ===========================================================================================================
 配置名          说明
================ ===========================================================================================================
**DSN**          DSN 连接字符串（一个一体化的配置序列）。
**hostname**     你的数据库服务器的主机名。通常为 'localhost'。
**username**     用于连接数据库的用户名。（``SQLite3`` 不使用此选项。）
**password**     用于连接数据库的密码。（``SQLite3`` 不使用此选项。）
**database**     你要连接的数据库的名称。

                 .. note:: CodeIgniter 不支持在表名和列名中使用点（``.``）。
                    自 v4.5.0 起，支持包含点的数据库名。
**DBDriver**     数据库驱动名称。大小写必须与驱动名称匹配。
                 你可以设置一个完全限定的类名来使用自定义驱动。
                 支持的驱动：``MySQLi``、``Postgre``、``SQLite3``、``SQLSRV`` 和 ``OCI8``。
**DBPrefix**     一个可选的表前缀，当运行
                 :doc:`查询构建器 <query_builder>` 查询时将被添加到表名前。这允许多个 CodeIgniter
                 安装共享一个数据库。
**pConnect**     true/false（布尔值）- 是否使用持久连接。
**DBDebug**      true/false（布尔值）- 当数据库发生错误时是否抛出异常。
**charset**      与数据库通信时使用的字符集。
**DBCollat**     （仅 ``MySQLi``）与数据库通信时使用的字符排序规则。
**swapPre**      一个默认的表前缀，应被 ``DBPrefix`` 替换。这对于分布式
                 应用程序很有用，在这种应用程序中你可能会运行手动编写的查询，并且需要前缀
                 仍可由最终用户自定义。
**schema**       （仅 ``Postgre`` 和 ``SQLSRV``）数据库模式，不同驱动程序的默认值不同。
**encrypt**      （仅 ``MySQLi`` 和 ``SQLSRV``）是否使用加密连接。
                 有关 ``MySQLi`` 设置，请参阅 :ref:`MySQLi encrypt <mysqli-encrypt>`。
                 ``SQLSRV`` 驱动接受 true/false。
**compress**     （仅 ``MySQLi``）是否使用客户端压缩。
**strictOn**     （仅 ``MySQLi``）true/false（布尔值）- 是否强制使用“严格模式”连接，这有助于在
                 开发应用程序时确保使用严格的 SQL。
**port**         数据库端口号 - 默认端口使用空字符串 ``''`` （或 ``SQLSRV`` 的动态端口）。
**foreignKeys**  （仅 ``SQLite3``）true/false（布尔值）- 是否启用外键约束。

                 .. important:: SQLite3 外键约束默认是禁用的。
                     请参阅 `SQLite 文档 <https://www.sqlite.org/pragma.html#pragma_foreign_keys>`_。
                     要强制启用外键约束，请将此配置项设置为 true。
**busyTimeout**  （仅 ``SQLite3``）毫秒（int）- 当表被锁定时，休眠指定的时间。
**synchronous**  （仅 ``SQLite3``）标志（int）- 事务期间 SQLite 写入磁盘的严格程度。
                 使用 `null` 以保持默认设置。此选项自 v4.6.0 起可用。
**numberNative** （仅 ``MySQLi``）true/false（布尔值）- 是否启用 MYSQLI_OPT_INT_AND_FLOAT_NATIVE。
**foundRows**    （仅 ``MySQLi``）true/false（布尔值）- 是否启用 MYSQLI_CLIENT_FOUND_ROWS。
**dateFormat**   默认的日期/时间格式，遵循 PHP 的 `DateTime format`_。
                 * ``date``        - 日期格式
                 * ``datetime``    - 日期和时间格式
                 * ``datetime-ms`` - 带毫秒的日期和时间格式
                 * ``datetime-us`` - 带微秒的日期和时间格式
                 * ``time``        - 时间格式
                 此选项自 v4.5.0 起可用，你可以通过 ``$db->dateFormat['datetime']`` 获取其值。
                 目前，数据库驱动不直接使用这些值，
                 但 :ref:`模型 <model-saving-dates>` 会使用它们。
================ ===========================================================================================================

.. _DateTime format: https://www.php.net/manual/en/datetime.format.php

.. note:: 根据你使用的数据库驱动（``MySQLi``、``Postgre`` 等），并非所有值都是必需的。例如，使用 ``SQLite3`` 时，
    你不需要提供用户名或密码，数据库名将是数据库文件的路径。

MySQLi
======

hostname
--------

配置套接字连接
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

要通过文件系统套接字连接到 MySQL 服务器，应将套接字的路径指定在
``'hostname'`` 设置中。CodeIgniter 的 MySQLi 驱动将检测到此设置并正确配置连接。

.. literalinclude:: configuration/011.php
    :lines: 11-18

.. _mysqli-encrypt:

encrypt
-------

MySQLi 驱动接受一个包含以下选项的数组：

* ``ssl_key``    - 私钥文件的路径
* ``ssl_cert``   - 公钥证书文件的路径
* ``ssl_ca``     - 证书颁发机构文件的路径
* ``ssl_capath`` - 包含以 PEM 格式存储的受信任 CA 证书的目录路径
* ``ssl_cipher`` - 用于加密的*允许*密码列表，以冒号（``:``）分隔
* ``ssl_verify`` - true/false（布尔值）- 是否验证服务器证书
