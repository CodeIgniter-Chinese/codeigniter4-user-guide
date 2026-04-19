###############
Session 类
###############

Session 类用于维护用户"状态"，并追踪用户在浏览站点时的活动。

CodeIgniter 提供若干 Session 存储驱动程序，可在最后一节中查看：

.. contents::
    :local:
    :depth: 2

使用 Session 类
***********************

初始化 Session
======================

Session 通常在每次页面加载时全局运行，因此 Session 类会自动初始化。

访问并初始化 Session：

.. literalinclude:: sessions/001.php

``$config`` 参数为可选——应用配置。如未提供，服务注册器将实例化默认配置。

加载后，即可通过 ``$session`` 访问 Session 类对象。

或者，可使用辅助函数，它将使用默认配置选项。此版本更易读，但不接受配置参数。

.. literalinclude:: sessions/002.php

Session 如何工作？
=====================

页面加载时，Session 类会检查用户的浏览器是否发送了有效的 Session Cookie。如果 **不** 存在 Session Cookie（或与服务器存储的不匹配，或已过期），将创建新 Session 并保存。

如果存在有效的 Session，其信息将被更新。每次更新时，如已配置，Session ID 可能会被重新生成。

需理解的是，Session 类一旦初始化就会自动运行。无需任何操作即可触发上述行为。如下文所述，可处理 Session 数据，但读取、写入和更新 Session 的过程是自动的。

.. note:: 在 CLI 环境下，Session 类会自动停止运行，因为这是完全基于 HTTP 协议的概念。

关于并发的说明
------------------------

除非开发大量使用 AJAX 的网站，否则可跳过此节。如果正在开发此类应用且遇到性能问题，那么此节内容正是你需要的。

CodeIgniter v2.x 的 Session 未实现锁定，这意味着使用同一 Session 的两个 HTTP 请求可以同时运行。用更准确的技术术语来说——请求是非阻塞的。

然而，在 Session 语境下，非阻塞请求也意味着不安全，因为一个请求中对 Session 数据（或 Session ID 重新生成）的修改可能干扰第二个并发请求的执行。此细节是许多问题的根源，也是 CodeIgniter 3 完全重写 Session 类的主要原因。

为何说明这一点？因为在排查性能问题后，你可能会认为锁定是问题所在，进而寻找移除锁定的方法……

切勿这样做！移除锁定是 **错误** 的做法，会引发更多问题！

锁定不是问题，而是解决方案。真正的问题在于：已经处理完 Session 数据却未关闭，而实际上已不再需要它。因此，正确的做法是在不再需要 Session 时，为当前请求关闭它。

.. literalinclude:: sessions/003.php

什么是 Session 数据？
=====================

Session 数据即为与特定 Session ID（Cookie）关联的数组。

如果之前使用过 PHP 的 Session，应该熟悉 PHP 的 `$_SESSION 超全局变量 <https://www.php.net/manual/zh/reserved.variables.session.php>`_ （如果不熟悉，请阅读该链接的内容）。

CodeIgniter 通过相同方式提供对 Session 数据的访问，因为它使用 PHP 提供的 Session 处理机制。使用 Session 数据就像操作（读取、设置和取消设置值） ``$_SESSION`` 数组一样简单。

.. note:: 一般而言，使用全局变量是不好的做法。因此不建议直接使用超全局变量 ``$_SESSION``。

此外，CodeIgniter 还提供 2 种特殊类型的 Session 数据，下文将进一步说明：`Flashdata`_ 和 `Tempdata`_。

.. note:: 出于历史原因，我们将不包含 Flashdata 和 Tempdata 的 Session 数据称为"userdata"。

获取 Session 数据
=======================

Session 数组中的任何信息均可通过 ``$_SESSION`` 超全局变量访问。例如，若要将此前存储的 ``name`` 项赋值给 ``$name`` 变量，操作如下：

.. literalinclude:: sessions/004.php

或通过传统的访问器方法：

.. literalinclude:: sessions/005.php

或通过魔术 getter：

.. literalinclude:: sessions/006.php

甚至可通过 Session 辅助函数：

.. literalinclude:: sessions/007.php

.. note:: 如果要访问的项不存在，``get()`` 方法返回 null。

要获取所有现有的 Session 数据，只需省略项键（魔术 getter 仅适用于单个属性值）：

.. literalinclude:: sessions/009.php

.. important:: 按键获取单个项时，``get()`` 方法 **会** 返回 flashdata 或 tempdata 项。但获取 Session 中的所有数据时则不会。

添加 Session 数据
===================

假设特定用户登录站点。验证身份后，可将用户名和电子邮件地址添加到 Session，使这些数据全局可用，无需在需要时运行数据库查询。

可像其他变量一样将数据赋值给 ``$_SESSION`` 数组，或作为 ``$session`` 的属性。

可将包含新 Session 数据的数组传递给 ``set()`` 方法：

.. literalinclude:: sessions/010.php

其中 ``$array`` 是包含新数据的关联数组。示例：

.. literalinclude:: sessions/011.php

如需一次添加一个 Session 值，``set()`` 也支持以下语法：

.. literalinclude:: sessions/012.php

要验证 Session 值是否存在，使用 ``isset()`` 检查即可：

.. literalinclude:: sessions/013.php

或调用 ``has()``：

.. literalinclude:: sessions/014.php

向 Session 数据推送新值
=================================

如果 Session 值是数组，可使用 ``push()`` 方法追加新元素。例如，若 ``hobbies`` 键包含一个兴趣爱好数组，可按如下方式向该数组添加新值：

.. literalinclude:: sessions/015.php

删除 Session 数据
=====================

与其他变量一样，可通过 ``unset()`` 取消设置 ``$_SESSION`` 中的值：

.. literalinclude:: sessions/016.php

同样，``set()`` 用于向 Session 添加信息，``remove()`` 则用于删除，传入 Session 键即可。例如，要从 Session 数据数组中移除 ``some_name``：

.. literalinclude:: sessions/017.php

此方法也接受要取消设置的项键数组：

.. literalinclude:: sessions/018.php

.. _sessions-flashdata:

Flashdata
=========

CodeIgniter 支持"flashdata"，即仅在下一次请求时可用、随后自动清除的 Session 数据。

这非常有用，特别是一次性信息、错误或状态消息（例如："已删除记录 2"）。

需注意的是，flashdata 变量是常规 Session 变量，由 CodeIgniter Session 处理程序内部管理。

将现有项标记为"flashdata"：

.. literalinclude:: sessions/019.php

要将多个项标记为 flashdata，将键作为数组传入即可：

.. literalinclude:: sessions/020.php

添加 flashdata：

.. literalinclude:: sessions/021.php

或使用 ``setFlashdata()`` 方法：

.. literalinclude:: sessions/022.php

也可向 ``setFlashdata()`` 传入数组，方式与 ``set()`` 相同。

读取 flashdata 变量与通过 ``$_SESSION`` 读取常规 Session 数据相同：

.. literalinclude:: sessions/023.php

.. important:: 按键获取单个项时，``get()`` 方法 **会** 返回 flashdata 项。但获取 Session 中的所有数据时则不会。

但要确保读取的是"flashdata"（而非其他类型），可使用 ``getFlashdata()`` 方法：

.. literalinclude:: sessions/024.php

.. note:: 如果找不到项，``getFlashdata()`` 方法返回 null。

要获取所有 flashdata，省略键参数即可：

.. literalinclude:: sessions/025.php


如需在一次额外请求中保留 flashdata 变量，可使用 ``keepFlashdata()`` 方法。可传入单个项或 flashdata 项数组。

.. literalinclude:: sessions/026.php

Tempdata
========

CodeIgniter 还支持"tempdata"，即具有特定过期时间的 Session 数据。值过期、Session 过期或被删除后，该值会自动移除。

与 flashdata 类似，tempdata 变量由 CodeIgniter Session 处理程序内部管理。

将现有项标记为"tempdata"，将键和过期时间（以秒为单位！）传入 ``markAsTempdata()`` 方法即可：

.. literalinclude:: sessions/027.php

可按两种方式将多个项标记为 tempdata，取决于是否需要它们具有相同的过期时间：

.. literalinclude:: sessions/028.php

添加 tempdata：

.. literalinclude:: sessions/029.php

或使用 ``setTempdata()`` 方法：

.. literalinclude:: sessions/030.php

也可向 ``setTempdata()`` 传入数组：

.. literalinclude:: sessions/031.php

.. note:: 如省略过期时间或设为 0，将使用 300 秒（即 5 分钟）的默认生存时间。

读取 tempdata 变量，同样可通过 ``$_SESSION`` 超全局数组访问：

.. literalinclude:: sessions/032.php

.. important:: 按键获取单个项时，``get()`` 方法 **会** 返回 tempdata 项。但获取 Session 中的所有数据时则不会。

要确保读取的是"tempdata"（而非其他类型），可使用 ``getTempdata()`` 方法：

.. literalinclude:: sessions/033.php

.. note:: 如果找不到项，``getTempdata()`` 方法返回 null。

当然，要获取所有现有的 tempdata：

.. literalinclude:: sessions/034.php

如需在 tempdata 值过期前移除它，可直接从 ``$_SESSION`` 数组中 unset：

.. literalinclude:: sessions/035.php

但这不会移除使该项成为 tempdata 的标记（该标记将在下一次 HTTP 请求时失效），因此如果打算在同一请求中重用该键，应使用 ``removeTempdata()``：

.. literalinclude:: sessions/036.php

更改 Session 键类型
====================

Flashdata 和 Tempdata 等 Session 数据值仅通过内部标志区分，因此可在不重写数据的情况下更改值的类型。

.. literalinclude:: sessions/045.php

关闭 Session
=================

.. _session-close:

close()
-------

.. versionadded:: 4.4.0

不再需要当前 Session 时，使用 ``close()`` 方法手动关闭：

.. literalinclude:: sessions/044.php

无需手动关闭 Session，PHP 会在脚本终止后自动关闭。但由于 Session 数据被锁定以防止并发写入，同一时间只有一个请求可操作 Session。在完成对 Session 数据的所有修改后尽快关闭 Session，可提升站点性能。

此方法的工作方式与 PHP 的 `session_write_close() <https://www.php.net/manual/zh/function.session-write-close.php>`_ 函数完全相同。

销毁 Session
====================

.. _session-destroy:

destroy()
---------

清除当前 Session（例如登出时），使用类的 ``destroy()`` 方法即可：

.. literalinclude:: sessions/037.php

此方法的工作方式与 PHP 的 `session_destroy() <https://www.php.net/manual/zh/function.session-destroy.php>`_ 函数完全相同。

这必须是同一请求中最后一个与 Session 相关的操作。所有 Session 数据（包括 flashdata 和 tempdata）将被永久销毁。

.. note:: 常规代码中无需调用此方法。应清理 Session 数据而非销毁 Session。

访问 Session 元数据
==========================

在 CodeIgniter 2 中，Session 数据数组默认包含 4 个项：'session_id'、'ip_address'、'user_agent'、'last_activity'。

这是由于 Session 的工作方式所致，但新实现已不再需要这些项。不过，如果应用依赖这些值，以下是访问它们的替代方法：

  - session_id：``$session->session_id`` 或 ``session_id()`` （PHP 内置函数）
  - ip_address：``$_SERVER['REMOTE_ADDR']``
  - user_agent：``$_SERVER['HTTP_USER_AGENT']`` （Session 未使用）
  - last_activity：取决于存储方式，无直接方法。抱歉！

Session 偏好设置
*******************

CodeIgniter 通常会让一切开箱即用。然而，Session 是任何应用中非常敏感的组件，必须进行仔细配置。请花时间考虑所有选项及其影响。

.. note:: 自 v4.3.0 起，新增了 **app/Config/Session.php**。此前，Session 偏好设置位于 **app/Config/App.php** 文件中。

可在 **app/Config/Session.php** 中找到以下 Session 相关偏好设置：

======================= ============================================ ================================================= ============================================================================================
偏好设置                默认值                                       选项                                              描述
======================= ============================================ ================================================= ============================================================================================
**driver**              CodeIgniter\\Session\\Handlers\\FileHandler  CodeIgniter\\Session\\Handlers\\FileHandler       要使用的 Session 存储驱动程序。
                                                                     CodeIgniter\\Session\\Handlers\\DatabaseHandler
                                                                     CodeIgniter\\Session\\Handlers\\MemcachedHandler
                                                                     CodeIgniter\\Session\\Handlers\\RedisHandler
                                                                     CodeIgniter\\Session\\Handlers\\ArrayHandler
**cookieName**          ci_session                                   仅限 [A-Za-z\_-] 字符                             用于 Session Cookie 的名称。
**expiration**          7200（2 小时）                               以秒为单位的时间（整数）                          Session 持续的秒数。
                                                                                                                       如需不过期的 Session（直到浏览器关闭），将值设为零：0
**savePath**            WRITEPATH . 'session'                        无                                                指定存储位置，取决于所使用的驱动程序。
**matchIP**             false                                        true/false（布尔值）                              读取 Session Cookie 时是否验证用户 IP 地址。
                                                                                                                       注意，某些 ISP 会动态更改 IP，因此如需不过期的 Session，
                                                                                                                       可能需要将此值设为 false。
**timeToUpdate**        300                                          以秒为单位的时间（整数）                          此选项控制 Session 类重新生成自身并创建新
                                                                                                                       Session ID 的频率。设为 0 将禁用 Session ID 重新生成。
**regenerateDestroy**   false                                        true/false（布尔值）                              自动重新生成 Session ID 时，是否销毁与旧 Session ID
                                                                                                                       关联的 Session 数据。设为 false 时，数据将由垃圾回收器稍后删除。
======================= ============================================ ================================================= ============================================================================================

.. note:: 作为最后手段，如果上述任何项未配置，Session 类将尝试获取 PHP 的 Session 相关 INI 设置，以及 CodeIgniter 3 的设置（如 'sess_expire_on_close'）。但绝不应依赖此行为，因为它可能导致意外结果或将来被更改。请正确配置所有项。

.. note:: 如果 ``expiration`` 设为 ``0``，将直接使用 PHP 在 Session 管理中设置的 ``session.gc_maxlifetime`` （通常默认值为 ``1440``）。如有需要，需在 ``php.ini`` 中或通过 ``ini_set()`` 更改此设置。

除了上述值之外，Session Cookie 还使用 **app/Config/Cookie.php** 文件中的以下配置值：

============== =============== ===========================================================================
偏好设置       默认值          描述
============== =============== ===========================================================================
**domain**     ''              Session 适用的域名
**path**       /               Session 适用的路径
**secure**     false           是否仅在加密（HTTPS）连接上创建 Session Cookie
**sameSite**   Lax             Session Cookie 的 SameSite 设置
============== =============== ===========================================================================

.. note:: **app/Config/Cookie.php** 中的 ``httponly`` 设置对 Session 无效。
    出于安全原因，HttpOnly 参数始终启用。此外，``Config\Cookie::$prefix`` 设置将被完全忽略。

Session 驱动程序
****************

如前所述，Session 类提供 5 个处理程序（即存储引擎）可供使用：

  - CodeIgniter\\Session\\Handlers\\FileHandler
  - CodeIgniter\\Session\\Handlers\\DatabaseHandler
  - CodeIgniter\\Session\\Handlers\\MemcachedHandler
  - CodeIgniter\\Session\\Handlers\\RedisHandler
  - CodeIgniter\\Session\\Handlers\\ArrayHandler

默认情况下，初始化 Session 时将使用 ``FileHandler``，因为它是最安全的选择，且预计可在任何地方运行（几乎每个环境都有文件系统）。

然而，如果选择使用其他驱动程序，可通过 **app/Config/Session.php** 文件中的 ``$driver`` 设置来选择。但需注意，每个驱动程序有不同的注意事项，因此在选择之前务必熟悉它们（见下文）。

.. note:: ArrayHandler 用于测试，可将所有数据存储在 PHP 数组中，从而防止数据持久化。参见
    :doc:`Session 测试 </testing/session_testing>`。

FileHandler 驱动程序（默认）
================================

'FileHandler' 驱动程序使用文件系统存储 Session 数据。

可以肯定地说，其工作方式与 PHP 默认的 Session 实现完全一致，但若需深究细节，二者底层代码实际上并不相同，且存在一些限制（以及优势）。

更具体地说，它不支持 PHP 的 `session.save_path 中使用的目录层级和模式格式 <https://www.php.net/manual/zh/session.configuration.php#ini.session.save-path>`_，并且大多数选项出于安全考虑已硬编码。相反，``$savePath`` 设置仅支持绝对路径。

另一件需要了解的重要事项是，切勿使用公开可读或共享的目录来存储 Session 文件。必须确保 *仅限你本人* 有权访问所选 *savePath* 目录的内容。否则，任何人都可以查看和窃取 Session 数据（也称为"Session 固定"攻击）。

在类 UNIX 操作系统上，通常通过 `chmod` 命令将该目录设置为 0700 权限来实现，这仅允许目录的所有者进行读写操作。但需注意，*运行* 脚本的系统用户通常不是你，而是类似 'www-data' 的用户，因此仅设置这些权限很可能会破坏应用。

相反，应根据环境执行类似以下操作：

.. code-block:: console

    mkdir /<path to your application directory>/writable/sessions/
    chmod 0700 /<path to your application directory>/writable/sessions/
    chown www-data /<path to your application directory>/writable/sessions/

用于自动清理过期 Session 的 `内建机制 <https://www.php.net/manual/zh/session.configuration.php#ini.session.gc-probability>`_ 的运行频率可能较低，导致 *saveDir* 目录中堆积大量文件。为解决此问题，需配置 **cron** 或 **任务计划程序** 定期删除过期文件。

额外提示
---------

可能会选择其他 Session 驱动程序，因为文件存储通常较慢。这只对了一半。

非常基础的测试可能会让人相信 SQL 数据库更快，但在 99% 的情况下，这仅在当前 Session 数量较少时才成立。随着 Session 数量和服务器负载的增加——而这才是关键时候——文件系统将持续优于几乎所有关系型数据库设置。

此外，如果性能是唯一关注点，可考虑使用 `tmpfs <https://eddmann.com/posts/storing-php-sessions-file-caches-in-memory-using-tmpfs/>`_，这能让 Session 速度极快。

.. _sessions-databasehandler-driver:

DatabaseHandler 驱动程序
========================

.. important:: 由于其他平台缺乏咨询锁定机制，官方仅支持 MySQL 和 PostgreSQL 数据库。不使用锁定的 Session 可能导致各种问题，特别是大量使用 AJAX 时。如果遇到性能问题，请在处理完 Session 数据后使用 :ref:`session-close` 方法。

'DatabaseHandler' 驱动程序使用 MySQL 或 PostgreSQL 等关系型数据库存储 Session。这是许多用户的流行选择，因为它允许开发者在应用中轻松访问 Session 数据——它只是数据库中的另一张表。

但有一个限制：不能使用持久连接。

配置 DatabaseHandler
-------------------------

设置表名
^^^^^^^^^^^^^^^^^^

要使用 'DatabaseHandler' Session 驱动程序，还必须创建前述的数据库表，然后将其设置为 ``$savePath`` 值。例如，如果要使用 'ci_sessions' 作为表名：

.. literalinclude:: sessions/039.php

创建数据库表
^^^^^^^^^^^^^^^^^^^^^^^

然后当然，创建数据库表。

MySQL::

    CREATE TABLE IF NOT EXISTS `ci_sessions` (
        `id` varchar(128) NOT NULL,
        `ip_address` varchar(45) NOT NULL,
        `timestamp` timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
        `data` blob NOT NULL,
        KEY `ci_sessions_timestamp` (`timestamp`)
    );

PostgreSQL::

    CREATE TABLE "ci_sessions" (
        "id" varchar(128) NOT NULL,
        "ip_address" inet NOT NULL,
        "timestamp" timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL,
        "data" bytea DEFAULT '' NOT NULL
    );

    CREATE INDEX "ci_sessions_timestamp" ON "ci_sessions" ("timestamp");

.. note:: ``id`` 值包含 Session Cookie 名称（``Config\Session::$cookieName``）和 Session ID 以及分隔符。应视需要增加长度，例如使用较长 Session ID 时。

添加主键
^^^^^^^^^^^^^^^^^^

还需要 **根据 $matchIP 设置** 添加主键。以下示例同时适用于 MySQL 和 PostgreSQL::

    // 当 $matchIP = true 时
    ALTER TABLE ci_sessions ADD PRIMARY KEY (id, ip_address);

    // 当 $matchIP = false 时
    ALTER TABLE ci_sessions ADD PRIMARY KEY (id);

    // 删除之前创建的主键（更改设置时使用）
    ALTER TABLE ci_sessions DROP PRIMARY KEY;

.. important:: 如果未添加正确的主键，可能出现以下错误
    ::

        Uncaught mysqli_sql_exception: Duplicate entry 'ci_session:***' for key 'ci_sessions.PRIMARY'

更改数据库组
^^^^^^^^^^^^^^^^^^^^^^^

默认使用默认数据库组。要更改使用的数据库组，可在 **app/Config/Session.php** 文件中将 ``$DBGroup`` 属性更改为要使用的组名：

.. literalinclude:: sessions/040.php

使用命令设置数据库表
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果不想手动完成所有这些操作，可使用 CLI 中的 ``make:migration --session`` 命令生成迁移文件：

.. code-block:: console

  php spark make:migration --session
  php spark migrate

此命令在生成代码时会考虑 ``$savePath`` 和 ``$matchIP`` 设置。

.. _sessions-redishandler-driver:

RedisHandler 驱动程序
=====================

.. note:: 由于 Redis 没有公开的锁定机制，此驱动程序的锁定通过单独的模拟值实现，最长保留 300 秒。

.. note:: 自 v4.3.2 起，可使用 **TLS** 协议连接 Redis。

Redis 是通常用于缓存的存储引擎，因其高性能而广受欢迎，这也可能是选择 'RedisHandler' Session 驱动程序的原因。

缺点是它不如关系型数据库那样普及，且需要在系统上安装 `phpredis <https://github.com/phpredis/phpredis>`_ PHP 扩展，该扩展并未随 PHP 捆绑提供。很可能，只有在已经熟悉 Redis 且出于其他用途正在使用它时，才会使用 RedisHandler 驱动程序。

配置 RedisHandler
----------------------

与 'FileHandler' 和 'DatabaseHandler' 驱动程序一样，还必须通过 ``$savePath`` 设置配置 Session 的存储位置。这里的格式有些不同且较为复杂。最好由 *phpredis* 扩展的 README 文件来解释，因此直接提供链接：

    https://github.com/phpredis/phpredis

.. important:: CodeIgniter 的 Session 类 **不** 使用实际的 'redis' ``session.save_handler``。请 **仅** 注意上方链接中的路径格式。

但对于最常见的情况，简单的 ``host:port`` 组合即可满足：

.. literalinclude:: sessions/041.php

自 v4.5.0 起，可使用 Redis ACL（用户名和密码）::

    public string $savePath = 'tcp://localhost:6379?auth[user]=username&auth[pass]=password';

.. note:: 自 v4.5.0 起，获取锁定的间隔时间（``$lockRetryInterval``）和重试次数（``$lockMaxRetries``）可配置。

.. _sessions-memcachedhandler-driver:

MemcachedHandler 驱动程序
=========================

.. note:: 由于 Memcached 没有公开的锁定机制，此驱动程序的锁定通过单独的模拟值实现，最长保留 300 秒。

'MemcachedHandler' 驱动程序在所有属性上与 'RedisHandler' 非常相似，唯一差异可能是可用性——PHP 的 `Memcached <https://www.php.net/manual/zh/book.memcached.php>`_ 扩展通过 PECL 分发，某些 Linux 发行版将其作为易于安装的软件包提供。

除此之外，不带任何对 Redis 的偏向，关于 Memcached 没有太多可说的——它也是常用于缓存的流行产品，以速度著称。

但值得注意的是，Memcached 唯一保证的是：将值 X 设置为在 Y 秒后过期，结果是 Y 秒后它会被删除（但不一定保证不会早于该时间过期）。这种情况很少发生，但应予以考虑，因为这可能导致 Session 丢失。

配置 MemcachedHandler
--------------------------

``$savePath`` 格式相当直接，只是 ``host:port`` 组合：

.. literalinclude:: sessions/042.php

额外提示
---------

还支持多服务器配置，第三段冒号分隔的值为可选的 *weight* 参数（``:weight``），但需注意的是，我们尚未测试其可靠性。

如果想实验此功能（风险自负），只需用逗号分隔多个服务器路径即可：

.. literalinclude:: sessions/043.php
