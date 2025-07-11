###############
Session 库
###############

Session 类允许你在用户浏览你的站点时维护用户的“状态”并跟踪他们的活动。

CodeIgniter 带有几个 session 存储驱动器,你可以在目录内容的最后一节中看到:

.. contents::
    :local:
    :depth: 2

使用 Session 类
***********************

初始化 Session
======================

Session 通常会与每个页面加载一起全局运行,所以 Session 类应该自动初始化。

要访问和初始化 Session:

.. literalinclude:: sessions/001.php

``$config`` 参数是可选的 - 你的应用配置。如果没有提供,服务注册器将实例化你的默认配置。

加载后，Session 库对象将可通过以下方式访问::

    $session

另外,你可以使用辅助函数,它将使用默认配置选项。这个版本的可读性更好一些,但不接受任何配置选项。

.. literalinclude:: sessions/002.php

Session 如何工作?
=====================

当页面加载时,session 类将检查用户的浏览器是否发送了有效的 session cookie。如果 session cookie **不存在** (或与服务器上存储的不匹配或已过期),则将创建一个新 session 并保存。

如果存在有效的 session,则会更新其信息。使用每次更新,如果配置了 session ID 可能会被重新生成。

Initialized 后,Session 类会自动运行这一点非常重要。你不需要做任何事情就可以引起上述行为发生。如下所示,你可以使用 session 数据,但读取、写入和更新 session 的过程是自动的。

.. note:: 在 CLI 下,Session 库将自动停止自己,因为这是一个完全基于 HTTP 协议的概念。

关于并发的注意事项
------------------------

除非你正在开发一个使用大量 AJAX 的网站,否则可以跳过这个部分。但是,如果是这样,并且如果遇到性能问题,那么这条注意事项正是你所需要的。

CodeIgniter 2.x 中的 session 并没有实现锁定,这意味着可以完全同时运行两个使用相同 session 的 HTTP 请求。使用一个更合适的技术术语来说——请求是非阻塞的。

但是,在 session 背景下的非阻塞请求也意味着不安全,因为一个请求中的 session 数据修改(或 session ID 重新生成)可能会干扰第二个并发请求的执行。这一细节是许多问题的根源,也是 CodeIgniter 3 完全重写 Session 库的主要原因。

为什么要告诉你这些? 因为在试图找到性能问题的原因后,你可能会得出锁定是问题的结论,因此会研究如何删除锁......

不要这样做!删除锁将是 **错误** 的,并且会给你带来更多问题!

锁定不是问题,它是解决方案。你的问题在于,你仍然打开了 session,而你已经处理了它,因此不再需要它。 所以,你需要的是在不再需要它时关闭当前请求的 session。

.. literalinclude:: sessions/003.php

什么是 Session 数据?
=====================

Session 数据只是一个与特定 Session ID 相关联的数组(Cookie)。

如果你之前使用过 PHP 的 session,你应该熟悉 PHP 的 `$_SESSION 超全局变量 <https://www.php.net/manual/en/reserved.variables.session.php>`_ (如果不熟悉,请阅读该链接的内容)。

CodeIgniter 通过相同的方式提供对其 Session 数据的访问,因为它使用 PHP 提供的 Session 处理程序机制。 使用 Session 数据就像操作(读取、设置和取消设置值) ``$_SESSION`` 数组一样简单。

.. note:: 一般来说,使用全局变量是不好的实践。 所以直接使用超全局 ``$_SESSION`` 不是推荐的做法。

此外,CodeIgniter 还提供了 2 种特殊类型的 Session 数据,下面将进一步解释: `Flashdata`_ 和 `Tempdata`_。

.. note:: 出于历史原因,我们将不包括 Flashdata 和 Tempdata 的 Session 数据称为“userdata”。

检索 Session 数据
=======================

可以通过 ``$_SESSION`` 超全局变量访问 Session 数组中的任何信息:

.. literalinclude:: sessions/004.php

或者通过常规的访问器方法:

.. literalinclude:: sessions/005.php

或者通过魔术 getter:

.. literalinclude:: sessions/006.php

甚至可以通过 session 辅助函数方法:

.. literalinclude:: sessions/007.php

其中 ``item`` 是与你希望获取的项对应的数组键。例如,要将先前存储的 ``name`` 项赋值给 ``$name`` 变量,你将执行:

.. literalinclude:: sessions/008.php

.. note:: 如果尝试访问的项不存在, ``get()`` 方法将返回 null。

如果你想检索所有现有的 session 数据,只需省略项键(魔术 getter 仅适用于单个属性值):

.. literalinclude:: sessions/009.php

.. important:: ``get()`` 方法在通过键检索单个项时,将返回 flashdata 或 tempdata 项。但是在从 session 中获取所有数据时不会返回 flashdata 或 tempdata。

添加 Session 数据
===================

假设特定用户登录你的站点。一旦认证,你可以将用户名和电子邮件地址添加到 session 中,这使得当你需要时可以全局访问它们而无需运行数据库查询。

你可以简单地像对任何其他变量一样将数据分配给 ``$_SESSION`` 数组。或者作为 ``$session`` 的属性。

你可以传递一个包含新 Session 数据的数组到 ``set()`` 方法:

.. literalinclude:: sessions/010.php

其中 ``$array`` 是一个关联数组,包含你的新数据。这里是一个例子:

.. literalinclude:: sessions/011.php

如果你想一次添加一个 Session 数据, ``set()`` 也支持这种语法:

.. literalinclude:: sessions/012.php

如果你想验证一个 Session 值是否存在,只需使用 ``isset()`` 检查:

.. literalinclude:: sessions/013.php

或者你可以调用 ``has()``:

.. literalinclude:: sessions/014.php

向 Session 数据中推送新值
=================================

``push()`` 方法用于将新值推送到一个是数组的 Session 值上。例如,如果 ``hobbies`` 键包含爱好数组,你可以像这样向数组添加一个新值:

.. literalinclude:: sessions/015.php

删除 Session 数据
=====================

与任何其他变量一样,可以通过 ``unset()`` 取消设置 ``$_SESSION`` 中的值:

.. literalinclude:: sessions/016.php

同样,正如 ``set()`` 可用于向 Session 添加信息一样, ``remove()`` 可用于通过传递 session 键来删除它。例如,如果你要从 Session 数据数组中删除 ``some_name``:

.. literalinclude:: sessions/017.php

该方法还接受要取消设置的项键数组:

.. literalinclude:: sessions/018.php

.. _sessions-flashdata:

Flashdata
=========

CodeIgniter 支持 “flashdata”,也就是只在下一次请求中可用,然后自动清除的 session 数据。

这在需要一次性信息、错误或状态消息时非常有用(例如:“记录 2 已删除”)。

需要注意的是,flashdata 变量是由 CodeIgniter session 处理程序管理的普通 session 变量。

要将现有项标记为 “flashdata”:

.. literalinclude:: sessions/019.php

如果要将多个项标记为 flashdata,只需将键作为数组传递即可:

.. literalinclude:: sessions/020.php

要添加 flashdata:

.. literalinclude:: sessions/021.php

或者可以使用 ``setFlashdata()`` 方法:

.. literalinclude:: sessions/022.php

与 ``set()`` 一样,你也可以向 ``setFlashdata()`` 传递数组。

通过 ``$_SESSION`` 读取 flashdata 变量,就像读取常规 session 数据一样:

.. literalinclude:: sessions/023.php

.. important:: ``get()`` 方法在通过键检索单个项时,将返回 flashdata 项。但是在从 session 中获取所有数据时不会返回 flashdata。

但是,如果你想确定正在读取 “flashdata”(而不是任何其他数据),也可以使用 ``getFlashdata()`` 方法:

.. literalinclude:: sessions/024.php

.. note:: 如果找不到该项, ``getFlashdata()`` 方法将返回 null。

当然,如果你想检索所有现有的 flashdata:

.. literalinclude:: sessions/025.php


如果你发现需要通过其他请求保留 flashdata 变量,可以使用 ``keepFlashdata()`` 方法。你可以保留单个项或 flashdata 项数组。

.. literalinclude:: sessions/026.php

Tempdata
========

CodeIgniter 还支持 “tempdata”,也就是在特定过期时间后自动删除的 session 数据。在值过期或 session 过期或删除后,该值将自动删除。

与 flashdata 类似,tempdata 变量由 CodeIgniter session 处理程序内部管理。

要将现有项标记为 “tempdata”,只需传递其键和过期时间(以秒为单位!)给 ``markAsTempdata()`` 方法:

.. literalinclude:: sessions/027.php

你可以通过两种方式标记多个项为 tempdata,这取决于是否希望它们都具有相同的过期时间:

.. literalinclude:: sessions/028.php

添加 tempdata:

.. literalinclude:: sessions/029.php

或者也可以使用 ``setTempdata()`` 方法:

.. literalinclude:: sessions/030.php

你也可以向 ``setTempdata()`` 传递数组:

.. literalinclude:: sessions/031.php

.. note:: 如果省略过期时间或设置为 0,将使用默认的 300 秒(5 分钟)的生存时间。

要读取 tempdata 变量,再次只需通过 ``$_SESSION`` 超全局数组访问它:

.. literalinclude:: sessions/032.php

.. important:: ``get()`` 方法在通过键检索单个项时,将返回 tempdata 项。但是在从 session 中获取所有数据时不会返回 tempdata。

或者如果你想确定正在读取 “tempdata”(而不是任何其他数据),也可以使用 ``getTempdata()`` 方法:

.. literalinclude:: sessions/033.php

.. note:: 如果找不到该项, ``getTempdata()`` 方法将返回 null。

当然,如果你想检索所有现有的 tempdata:

.. literalinclude:: sessions/034.php

如果你需要在过期之前删除 tempdata 值,可以直接从 ``$_SESSION`` 数组中取消设置它:

.. literalinclude:: sessions/035.php

但是,这不会删除使该特定项成为 tempdata 的标记(它将在下一个 HTTP 请求上失效),所以如果你打算在同一请求中重用相同的键,你会想使用 ``removeTempdata()``:

.. literalinclude:: sessions/036.php

更改 Session 键类型
====================

由于 Flashdata 和 Tempdata 等 session 数据值仅通过内部标志区分，因此你可以在不重写数据的情况下更改值的类型。

.. literalinclude:: sessions/045.php

关闭一个 Session
=================

.. _session-close:

close()
-------

.. versionadded:: 4.4.0

在不再需要当前 Session 时，可以使用 ``close()`` 方法手动关闭 Session：

.. literalinclude:: sessions/044.php

你不必手动关闭 Session，PHP 会在脚本终止后自动关闭它。但是，由于 Session 数据被锁定以防止并发写入，因此一次只能有一个请求操作 Session。通过在所有对 Session 数据的更改完成后立即关闭 Session，可以提高网站性能。

此方法的工作方式与 PHP 的 `session_write_close() <https://www.php.net/session_write_close>`_ 函数完全相同。

销毁一个 Session
====================

.. _session-destroy:

destroy()
---------

要清除当前 session(例如在退出登录时),可以使用类库的 ``destroy()`` 方法:

.. literalinclude:: sessions/037.php

此方法的工作方式与 PHP 的 `session_destroy() <https://www.php.net/session_destroy>`_ 函数完全相同。

这必须是在同一请求中进行的最后一个与 Session 相关的操作。
所有 Session 数据（包括 flashdata 和 tempdata）将被永久销毁。

.. note:: 你不必在常规代码中调用此方法。清理 Session 数据而不是销毁会话。

.. _session-stop:

stop()
------

.. deprecated:: 4.3.5

Session 类还有 ``stop()`` 方法。

.. warning:: 在 v4.3.5 之前,由于一个错误,此方法不会销毁 session。

从 v4.3.5 开始,此方法已被修改为销毁 session。但是,由于它与 ``destroy()`` 方法完全相同,已被弃用。请使用 ``destroy()`` 方法。

访问 Session 元数据
==========================

在 CodeIgniter 2 中,默认情况下 session 数据数组包含 4 个项:
'session_id'、'ip_address'、'user_agent'、'last_activity'。

这是由于 session 工作方式的特殊性,但现在在我们的新实现中不再是必需的。
但是,你的应用程序可能依赖于这些值,所以这里提供了访问它们的替代方法:

  - session_id: ``$session->session_id`` 或 ``session_id()`` (PHP 的内置函数)
  - ip_address: ``$_SERVER['REMOTE_ADDR']``
  - user_agent: ``$_SERVER['HTTP_USER_AGENT']`` (session 不使用它)
  - last_activity: 取决于存储,没有直接的方法。抱歉!

Session 首选项
*******************

CodeIgniter 通常会使一切正常工作。但是,Session 是任何应用程序中一个非常敏感的组件,因此必须谨慎配置。请花时间考虑所有选项及其影响。

.. note:: 自 v4.3.0 起,添加了新的 **app/Config/Session.php** 文件。之前,Session 首选项在你的 **app/Config/App.php** 文件中。

你会在 **app/Config/Session.php** 文件中找到以下与 Session 相关的首选项:

======================= ============================================ ================================================= ============================================================================================
首选项                  默认值                                       选项                                              描述
======================= ============================================ ================================================= ============================================================================================
**driver**              CodeIgniter\\Session\\Handlers\\FileHandler  CodeIgniter\\Session\\Handlers\\FileHandler       要使用的 session 存储驱动程序。
                                                                     CodeIgniter\\Session\\Handlers\\DatabaseHandler
                                                                     CodeIgniter\\Session\\Handlers\\MemcachedHandler
                                                                     CodeIgniter\\Session\\Handlers\\RedisHandler
                                                                     CodeIgniter\\Session\\Handlers\\ArrayHandler
**cookieName**          ci_session                                   [A-Za-z\_-] 字符                                  用于 session cookie 的名称。
**expiration**          7200 (2 小时)                                秒数(整数)                                        你希望 session 持续的秒数。
                                                                                                                       如果你希望一个不过期的 session(直到浏览器关闭),请将值设置为零:0
**savePath**            null                                         无                                                根据所使用的驱动程序指定存储位置。
**matchIP**             false                                        true/false(布尔值)                                从 session cookie 读取时是否验证用户的 IP 地址。
                                                                                                                       请注意,某些 ISP 会动态更改 IP,因此如果你需要一个不过期的 session,你可能会将此设置为 false。
**timeToUpdate**        300                                          秒数(整数)                                        此选项控制 session 类重新生成自身和创建新的 session ID 的频率。
                                                                                                                       将其设置为 0 将禁用 session ID 重新生成。
**regenerateDestroy**   false                                        true/false(布尔值)                                是否在自动重新生成 session ID 时销毁与旧 session ID 关联的数据。
                                                                                                                       将其设置为 false 时,稍后数据将由垃圾收集器删除。
======================= ============================================ ================================================= ============================================================================================

.. note:: 作为最后的手段,如果上述任何内容都未配置,Session 库将尝试获取 PHP 的与 session 相关的 INI 设置,以及 CodeIgniter 3 设置,如 'sess_expire_on_close'。
    但是,你永远不应该依赖这种行为,因为它可能会导致意外结果或在未来更改。请正确配置一切。

.. note:: 如果 ``expiration`` 设置为 ``0``,则将原封不动地使用 PHP 在会话管理中设置的 ``session.gc_maxlifetime`` 设置(通常默认值为 ``1440``)。
    根据需要，这需要在 ``php.ini`` 或通过 ``ini_set()`` 进行更改。

此外,在你的 **app/Config/Cookie.php** 文件中使用了以下配置值用于 Session cookie:

============== =============== ===========================================================================
Preference           Default         Description
============== =============== ===========================================================================
**domain**     ''              Session 适用的域
**path**       /               Session 适用的路径
**secure**     false           是否仅在加密连接(HTTPS)上创建 session cookie
**sameSite**   Lax             Session cookie 的 SameSite 设置
============== =============== ===========================================================================

.. note:: ``httponly`` 设置（在 **app/Config/Cookie.php** 中）不会对 session 产生影响。出于安全原因，HttpOnly 参数始终启用。另外，完全忽略了 ``Config\Cookie::$prefix`` 设置。

Session 驱动程序
*******************

如前所述，Session 库提供了 5 个处理程序或存储引擎可以使用:

  - CodeIgniter\\Session\\Handlers\\FileHandler
  - CodeIgniter\\Session\\Handlers\\DatabaseHandler
  - CodeIgniter\\Session\\Handlers\\MemcachedHandler
  - CodeIgniter\\Session\\Handlers\\RedisHandler
  - CodeIgniter\\Session\\Handlers\\ArrayHandler

初始化 session 时，如果不指定，将使用 ``FileHandler``，因为这是最安全的选择，并且预期它可以在任何环境中使用(几乎每种环境都有文件系统)。

然而，如果你愿意，可以通过 **app/Config/Session.php** 文件中的 ``$driver`` 设置来选择任何其他驱动。但请记住，每个驱动都有不同的注意事项，所以在你做出选择之前，确保你熟悉它们（如下所示）。

.. note:: ArrayHandler 在测试时使用,并将所有数据存储在 PHP 数组中,同时防止数据持久化。

FileHandler 驱动程序(默认)
================================

'FileHandler' 驱动程序使用你的文件系统来存储 session 数据。

可以肯定地说，它的工作方式与 PHP 自带的默认 Session 实现完全一样。但如果你认为这是一个重要的细节，实际上，它并不是相同的代码，并且有一些限制（以及优势）。

更具体地说，它不支持 PHP 的 `session.save_path 中使用的目录级别和模式格式 <https://www.php.net/manual/zh/session.configuration.php#ini.session.save-path>`_。并且，出于安全考虑，大部分选项都是硬编码的。相反，只支持使用 ``$savePath`` 设置的绝对路径。

另一件你需要知道的重要事情是，确保你不要使用公开可读或共享的目录来存储你的 session 文件。*只有你* 可以访问你选择的 *savePath* 目录的内容。否则，任何人都可以查看并窃取 Session 数据（这也被称为 "会话固定" 攻击）。

在类 UNIX 操作系统上,这通常通过使用 `chmod` 命令对该目录设置 0700 模式权限来实现,它仅允许目录所有者在其上执行读写操作。但是要小心,因为 *运行* 脚本的系统用户通常不是你自己,而是类似 'www-data' 的用户,所以只设置这些权限可能会中断你的应用程序。

相反,你应该执行类似以下操作,这取决于你的环境:

.. code-block:: console

    mkdir /<path to your application directory>/writable/sessions/
    chmod 0700 /<path to your application directory>/writable/sessions/
    chown www-data /<path to your application directory>/writable/sessions/

奖励提示
---------

你们中一些人可能会选择另一个 session 驱动程序,因为文件存储通常较慢。这只有一半是真的。

一个非常基本的测试可能会让你误以为 SQL 数据库更快，但在 99% 的情况下，这种观点只有在你的当前 Session 数量很少时才成立。随着 Session 数量的增加和服务器负载的提升——这才是真正重要的时刻——文件系统将始终优于几乎所有的关系型数据库设置。

另外，如果性能是你唯一的关注点，你可能需要研究使用 `tmpfs <https://eddmann.com/posts/storing-php-sessions-file-caches-in-memory-using-tmpfs/>`_，它可以使你的 session 飞快。

.. _sessions-databasehandler-driver:

DatabaseHandler 驱动程序
==========================

.. important:: 由于其他平台缺乏咨询锁机制，因此官方仅支持 MySQL 和 PostgreSQL 数据库。在不使用锁的情况下使用 Session 可能会导致各种问题，特别是在大量使用 AJAX 的情况下。如果你遇到性能问题，在处理完 Session 数据后，请使用 :ref:`session-close` 方法。

'DatabaseHandler' 驱动程序使用 MySQL 或 PostgreSQL 等关系数据库来存储会话。这对许多用户来说是一个流行的选择,因为它允许开发人员轻松访问应用程序中的 session 数据——它只是数据库中的另一个表。

然而，有一个限制：你不能使用持久连接。

配置 DatabaseHandler
-------------------------

设置表名
^^^^^^^^^^^^^^^^^^

为了使用 'DatabaseHandler' session 驱动程序,还必须创建我们已经提到的表,然后将其设置为你的 ``$savePath`` 值。例如,如果你想使用 'ci_sessions' 作为表名,你将执行以下操作:

.. literalinclude:: sessions/039.php

创建数据库表
^^^^^^^^^^^^^^^^^^^^^^^

然后当然，创建数据库表。

对于 MySQL::

    CREATE TABLE IF NOT EXISTS `ci_sessions` (
        `id` varchar(128) NOT null,
        `ip_address` varchar(45) NOT null,
        `timestamp` int(10) unsigned DEFAULT 0 NOT null,
        `data` blob NOT null,
        KEY `ci_sessions_timestamp` (`timestamp`)
    );

对于 PostgreSQL::

    CREATE TABLE "ci_sessions" (
        "id" varchar(128) NOT NULL,
        "ip_address" inet NOT NULL,
        "timestamp" bigint DEFAULT 0 NOT NULL,
        "data" text DEFAULT '' NOT NULL
    );

    CREATE INDEX "ci_sessions_timestamp" ON "ci_sessions" ("timestamp");

.. note:: ``id`` 值包含 session cookie 名称(``Config\Session::$cookieName``)和 session ID 以及一个分隔符。根据需要应增加它,例如在使用长 session ID 时。

添加主键
^^^^^^^^^^^^^^^^^^

**根据你的 $matchIP 设置**，你还需要添加一个主键。以下示例适用于 MySQL 和 PostgreSQL::

    // 当 $matchIP = true 时
    ALTER TABLE ci_sessions ADD PRIMARY KEY (id, ip_address);

    // 当 $matchIP = false 时
    ALTER TABLE ci_sessions ADD PRIMARY KEY (id);

    // 删除先前创建的主键(更改设置时使用)
    ALTER TABLE ci_sessions DROP PRIMARY KEY;

.. important:: 如果你没有添加正确的主键，
    可能会出现以下错误::

        Uncaught mysqli_sql_exception: Duplicate entry 'ci_session:***' for key 'ci_sessions.PRIMARY'

更改数据库组
^^^^^^^^^^^^^^^^^^^^^^^

默认情况下使用默认数据库组。
你可以通过更改 **app/Config/Session.php** 文件中的 ``$DBGroup`` 属性为要使用的组的名称来更改数据库组：

.. literalinclude:: sessions/040.php

使用命令设置数据库表
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

当然,如果你不想手动执行所有这些操作,可以使用 cli 中的 ``php spark make:migration --session`` 命令为你生成迁移文件:

.. code-block:: console

  php spark make:migration --session
  php spark migrate

此命令将考虑 ``$savePath`` 和 ``$matchIP`` 设置并生成代码。

.. _sessions-redishandler-driver:

RedisHandler 驱动程序
=======================

.. note:: 由于 Redis 没有暴露锁机制，因此该驱动的锁是通过一个单独的值来模拟的，该值最多保留 300 秒。

.. note:: 从 v4.3.2 开始，你可以使用 **TLS** 协议连接 Redis。

Redis 是一个通常用于缓存且以高性能而著称的存储引擎,这也可能是你使用 'RedisHandler' session 驱动程序的原因。

缺点是它不像关系型数据库那样普遍，并且需要安装 `phpredis <https://github.com/phpredis/phpredis>`_ PHP 扩展在你的系统上，而这个扩展并不随 PHP 一起捆绑提供。
很可能，你只有在已经熟悉 Redis 并且还出于其他目的使用它的情况下，才会使用 RedisHandler 驱动。

配置 RedisHandler
----------------------

就像 'FileHandler' 和 'DatabaseHandler' 驱动一样，你也必须通过 ``$savePath`` 设置来配置你的 Session 存储位置。
这里的格式有点不同且复杂。最好是通过 *phpredis* 扩展的 README 文件来解释，因此我们将直接提供一个链接：

    https://github.com/phpredis/phpredis

.. important:: CodeIgniter 的 Session 库不使用实际的 'redis' ``session.save_handler``。在上面的链接中 **仅** 注意路径格式。

但是,对于最常见的情况,一个简单的 ``host:port`` 对应关系应该就足够了:

.. literalinclude:: sessions/041.php

从 v4.5.0 开始，你可以使用 Redis ACL（用户名和密码）::

    public string $savePath = 'tcp://localhost:6379?auth[user]=username&auth[pass]=password';

.. note:: 从 v4.5.0 开始，获取锁的间隔时间（``$lockRetryInterval``）和重试次数（``$lockMaxRetries``）是可配置的。

.. _sessions-memcachedhandler-driver:

MemcachedHandler 驱动程序
===========================

.. note:: 由于 Memcached 没有公开锁定机制,因此通过单独保留 300 秒的额外值来模拟此驱动程序的锁。

'MemcachedHandler' 驱动程序几乎与 'RedisHandler' 驱动程序的所有属性相同,可能仅在可用性方面有所不同,因为 PHP 的 `Memcached <https://www.php.net/memcached>`_ 扩展通过 PECL 分发,一些 Linux 发行版将其作为易于安装的包。

除此之外,如果没有任何故意的偏见针对 Redis,关于 Memcached 就没有太多不同的可说的 —— 它也是一个流行的产品,以其速度而闻名。

但是,值得注意的是,Memcached 所做的唯一保证是,设置值 X 在 Y 秒后过期将导致在 Y 秒过去后删除该值(但不一定保证不会比该时间过期更早)。这种情况非常罕见,但应该考虑到它可能导致 session 丢失。

配置 MemcachedHandler
--------------------------

这里的 ``$savePath`` 格式相当简单,只是一个 ``host:port`` 对:

.. literalinclude:: sessions/042.php

奖励提示
---------

也支持多服务器配置,以可选的 *weight* 参数作为第三个冒号分隔(``:weight``)值,但我们必须注意,我们还没有测试这一特性的可靠性。

如果你想要实验此功能(自负风险),只需用逗号分隔多个服务器路径:

.. literalinclude:: sessions/043.php
