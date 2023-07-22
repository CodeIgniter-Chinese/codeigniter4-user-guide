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

要访问和初始化 session:

.. literalinclude:: sessions/001.php

``$config`` 参数是可选的 - 你的应用配置。如果没有提供,服务注册表将实例化你的默认配置。

加载后,可以使用 ``$session`` 访问 Session 库对象:

.. literalinclude:: sessions/002.php

另外,你可以使用助手函数,它将使用默认配置选项。这个版本的可读性更好一些,但不接受任何配置选项。

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

不要这样做!删除锁将是**错误**的,并且会给你带来更多问题!

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

甚至可以通过 session 助手方法:

.. literalinclude:: sessions/007.php

其中 ``item`` 是与你希望获取的项对应的数组键。例如,要将先前存储的 ``name`` 项赋值给 ``$name`` 变量,你将执行:

.. literalinclude:: sessions/008.php

.. note:: 如果尝试访问的项不存在,``get()`` 方法将返回 null。

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

如果你想一次添加一个 Session 数据,``set()`` 也支持这种语法:

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

同样,正如 ``set()`` 可用于向 Session 添加信息一样,``remove()`` 可用于通过传递 session 键来删除它。例如,如果你要从 Session 数据数组中删除 ``some_name``:

.. literalinclude:: sessions/017.php

该方法还接受要取消设置的项键数组:

.. literalinclude:: sessions/018.php

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

.. note:: 如果找不到该项,``getFlashdata()`` 方法将返回 null。

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

.. note:: 如果找不到该项,``getTempdata()`` 方法将返回 null。

当然,如果你想检索所有现有的 tempdata:

.. literalinclude:: sessions/034.php

如果你需要在过期之前删除 tempdata 值,可以直接从 ``$_SESSION`` 数组中取消设置它:

.. literalinclude:: sessions/035.php

但是,这不会删除使该特定项成为 tempdata 的标记(它将在下一个 HTTP 请求上失效),所以如果你打算在同一请求中重用相同的键,你会想使用 ``removeTempdata()``:

.. literalinclude:: sessions/036.php

销毁一个 Session
====================

.. _session-destroy:

destroy()
---------

要清除当前 session(例如在退出登录时),可以使用 PHP 的 `session_destroy() <https://www.php.net/session_destroy>`_ 函数或库的 ``destroy()`` 方法。两者的作用完全相同:

.. literalinclude:: sessions/037.php

.. note:: 这必须是在同一请求期间执行的最后一个与 session 相关的操作。所有 session 数据(包括 flashdata 和 tempdata)将被永久销毁,并且在销毁 session 后,同一请求中的函数将不可用。

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
**timeToUpdate**        300                                          秒数(整数)                                        此选项控制 session 类重新生成自身和创建新的 session ID 的频率。将其设置为 0 将禁用 session ID 重新生成。
**regenerateDestroy**   false                                        true/false(布尔值)                                是否在自动重新生成 session ID 时销毁与旧 session ID 关联的数据。将其设置为 false 时,稍后数据将由垃圾收集器删除。
======================= ============================================ ================================================= ============================================================================================

.. note:: 作为最后的手段,如果上述任何内容都未配置,Session 库将尝试获取 PHP 的与 session 相关的 INI 设置,以及 CodeIgniter 3 设置,如 'sess_expire_on_close'。
    但是,你永远不应该依赖这种行为,因为它可能会导致意外结果或在未来更改。请正确配置一切。

.. note:: 如果 ``sessionExpiration`` 设置为 ``0``,则将原封不动地使用 PHP 在会话管理中设置的 ``session.gc_maxlifetime`` 设置(通常默认值为 ``1440``)。
    根据需要，这需要在 ``php.ini``或通过 ``ini_set()`` 进行更改。

此外,在你的 **app/Config/Cookie.php** 文件中使用了以下配置值用于 Session cookie:

============== =============== ===========================================================================
Preference           Default         Description
============== =============== ===========================================================================
**domain**     ''              Session 适用的域
**path**       /               Session 适用的路径
**secure**     false           是否仅在加密连接(HTTPS)上创建 session cookie
**sameSite**   Lax             Session cookie 的 SameSite 设置
============== =============== ===========================================================================

.. note:: ``httponly`` 设置不会对 session 产生影响。出于安全原因,HttpOnly 参数始终启用。另外,完全忽略了 ``Config\Cookie::$prefix`` 设置。

Session 驱动程序
*******************

如前所述,Session 库提供了 4 个处理程序或存储引擎可以使用:

  - CodeIgniter\\Session\\Handlers\\FileHandler
  - CodeIgniter\\Session\\Handlers\\DatabaseHandler
  - CodeIgniter\\Session\\Handlers\\MemcachedHandler
  - CodeIgniter\\Session\\Handlers\\RedisHandler
  - CodeIgniter\\Session\\Handlers\\ArrayHandler

初始化 session 时,如果不指定,将使用 ``FileHandler`` 驱动程序,因为这是最安全的选择,并且预期它可以在任何环境中使用(几乎每种环境都有文件系统)。

但是,如果选择这样做,可以通过 **app/Config/Session.php** 文件中的 ``public $driver`` 行来选择任何其他驱动程序。但是请记住,每个驱动程序都有不同的使用注意事项,所以在做出选择之前,请确保熟悉它们(如下所述)。

.. note:: ArrayHandler 在测试时使用,并将所有数据存储在 PHP 数组中,同时防止数据持久化。

FileHandler 驱动程序(默认)
================================

'FileHandler' 驱动程序使用你的文件系统来存储 session 数据。

可以安全地说,它的工作方式与 PHP 自己的默认 session 实现完全相同,但如果这对你很重要,请记住这实际上不是相同的代码,并且它有一些限制(和优点)。

更具体地说,它不支持 PHP 的 `session.save_path 中使用的目录级别和模式格式 <https://www.php.net/manual/en/session.configuration.php#ini.session.save-path>`_,大多数选项出于安全考虑都是硬编码的。相反,它只支持绝对路径作为 ``public string $savePath``。

另一件重要的事情是,你应该知道,不要使用公开可读或共享的目录来存储 session 文件。请确保*只有你*可以查看选择的 *savePath* 目录的内容。否则,任何能够执行此操作的人都可以偷取当前的任何 session(也称为“会话固定”攻击)。

在类 UNIX 操作系统上,这通常通过使用 `chmod` 命令对该目录设置 0700 模式权限来实现,它仅允许目录所有者在其上执行读写操作。但是要小心,因为*运行*脚本的系统用户通常不是你自己,而是类似 'www-data' 的用户,所以只设置这些权限可能会中断你的应用程序。

相反,你应该执行类似以下操作,这取决于你的环境::

    > mkdir /<path to your application directory>/writable/sessions/
    > chmod 0700 /<path to your application directory>/writable/sessions/
    > chown www-data /<path to your application directory>/writable/sessions/

奖励提示
---------

你们中一些人可能会选择另一个 session 驱动程序,因为文件存储通常较慢。这只有一半是真的。

一个非常基本的测试可能会误导你相信 SQL 数据库更快,但在 99% 的情况下,这仅当你只有少量当前 session 时才是真的。随着 session 计数和服务器负载的增加——这是至关重要的时候——文件系统将始终优于几乎所有关系数据库设置。

另外,如果性能是你唯一的关注点,你可能需要研究使用 `tmpfs <https://eddmann.com/posts/storing-php-sessions-file-caches-in-memory-using-tmpfs/>`_,(警告:外部资源),它可以使你的 session 飞快。

.. _sessions-databasehandler-driver:

DatabaseHandler 驱动程序
==========================

.. important:: 由于其他平台缺乏顾问锁定机制,因此仅正式支持 MySQL 和 PostgreSQL 数据库。在其他平台上使用不带锁定的会话可能会导致各种问题,特别是在大量使用 AJAX 的情况下,我们不会支持此类情况。如果遇到性能问题,请在处理完 session 数据后使用 ``session_write_close()``。

'DatabaseHandler' 驱动程序使用 MySQL 或 PostgreSQL 等关系数据库来存储会话。这对许多用户来说是一个流行的选择,因为它允许开发人员轻松访问应用程序中的 session 数据——它只是数据库中的另一个表。

但是,必须满足一些条件:

  - 你不能使用持久连接。

配置 DatabaseHandler
-------------------------

为了使用 'DatabaseHandler' session 驱动程序,还必须创建我们已经提到的表,然后将其设置为你的 ``$savePath`` 值。例如,如果你想使用 'ci_sessions' 作为表名,你将执行以下操作:

.. literalinclude:: sessions/039.php

然后当然,创建数据库表......

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

你还需要根据你的 $matchIP 设置添加主键::

    // 当 sessionMatchIP = true 时
    ALTER TABLE ci_sessions ADD PRIMARY KEY (id, ip_address);

    // 当 sessionMatchIP = false 时
    ALTER TABLE ci_sessions ADD PRIMARY KEY (id);

    // 删除先前创建的主键(更改设置时使用)
    ALTER TABLE ci_sessions DROP PRIMARY KEY;

你可以通过向 **app/Config/Session.php** 添加带有要使用的组名称的新行来选择要使用的数据库组:

.. literalinclude:: sessions/040.php

当然,如果你不想手动执行所有这些操作,可以使用 cli 中的 ``php spark make:migration --session`` 命令为你生成迁移文件::

  > php spark make:migration --session
  > php spark migrate

此命令将考虑 ``$savePath`` 和 ``$matchIP`` 设置并生成代码。

.. _sessions-redishandler-driver:

RedisHandler 驱动程序
=======================

.. note:: 由于 Redis 没有公开锁定机制,因此通过单独保留 300 秒的额外值来模拟此驱动程序的锁。在 ``v4.3.2`` 或更高版本中,你可以使用 **TLS** 协议连接 ``Redis``。

Redis 是一个通常用于缓存且以高性能而著称的存储引擎,这也可能是你使用 'RedisHandler' session 驱动程序的原因。

缺点是它不像关系数据库那么无所不在,并且需要系统上安装 `phpredis <https://github.com/phpredis/phpredis>`_ PHP 扩展,而该扩展不与 PHP 一起打包。
除非你已经熟悉并出于其他目的使用 Redis,否则只会考虑使用 RedisHandler 驱动程序。

配置 RedisHandler
----------------------

与 'FileHandler' 和 'DatabaseHandler' 驱动程序一样,你还必须通过 ``$savePath`` 设置配置你的 session 的存储位置。
这里的格式有点不同,同时也比较复杂。最好通过 *phpredis* 扩展的 README 文件进行解释,所以我们简单地链接到它:

    https://github.com/phpredis/phpredis

.. important:: CodeIgniter 的 Session 库不使用实际的 'redis' ``session.save_handler``。在上面的链接中**仅**注意路径格式。

但是,对于最常见的情况,一个简单的 ``host:port`` 对应关系应该就足够了:

.. literalinclude:: sessions/041.php

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
