###############
Session 类
###############

Session 类允许你维护用户的 “状态” 并跟踪他们在浏览你的网站时的活动。

CodeIgniter 有一些用于会话（session）储存的驱动程序，你可以在目录的最后部分中看到它们：

.. contents::
    :local:
    :depth: 2

.. raw:: html

  <div class="custom-index container"></div>

使用 Session 类
*********************************************************************

初始化会话
==================================================================

会话通常会在每次加载页面时在全局范围内运行，因此应该恰当地初始化 Session 类。

访问并初始化会话： ::

    $session = \Config\Services::session($config);

``$config`` 参数是可选的，它是你的应用程序配置。如果未提供，服务将会使用你的默认配置。

初始化成功后，可以用以下方式使用 Session 库对象： ::

    $session

或者，你可以使用使用默认配置的 helper 方法，这个版本阅读起来会更友好一些，但是不能配置任何配置选项

::

    $session = session();

Session 是怎样工作的？
========================

加载页面后，Session 类将检查用户的浏览器是否发送了有效的会话 cookie。如果会话 Cookie **不存在** （或者如果它不匹配一个存储在服务器上的会话ID或已过期）, 新会话将被创建和保存。

如果确实存在有效的会话，则其信息将被更新。对于每次更新，如果配置了会话 ID ，则可以对其进行重新生成。

对你来说很重要的一点是，一旦初始化，Session 类就会自动运行。你无需执行任何操作即可导致上述现象发生。如下所示，你可以使用会话数据，但是读取，写入和更新会话的过程是自动的。

.. note:: 在 CLI 下，Session 库将自动停止运行，因为它只是一个完全基于 HTTP 协议的概念。

关于异步的说明
------------------------

除非你要开发使用 AJAX 的网站，否则可以跳过本节。但是，如果你遇到了性能问题，那么本说明正是你所需要的。

早期版本的 CodeIgniter 中的会话未实现锁定，这意味着使用同一会话的两个 HTTP 请求可以完全同时运行。使用更合适的技术术语就是，请求是非阻塞的。

但是，会话上下文中的非阻塞请求也意味着不安全，因为在一个请求中对会话数据的修改（或会话 ID 再生）可能会干扰第二个并发请求的执行。这个细节是许多问题的根源，也是 CodeIgniter 4 拥有完全重写的 Session 库的主要原因。

我们为什么要告诉你这个？因为在尝试找出性能问题的原因之后，你可能会得出结论，锁定是问题所在，因此研究了如何删除锁定……

不要那样做！删除锁定是 **错误** 的，它将给你带来更多问题！

锁定不是问题，而是解决方案。你的问题是，你已经打开了会话，但已经处理了该会话，因此不再需要它。因此，你需要的是在不再需要当前请求后关闭会话。

::

    $session->destroy();

什么是会话数据？
=====================

会话数据是与特定会话 ID（cookie）关联的数组。

如果你以前在 PHP 中使用过会话，则应该熟悉 PHP 的 `$_SESSION 全局变量 <https://www.php.net/manual/en/reserved.variables.session.php>`_ （如果不熟悉，请阅读该链接上的内容）。

CodeIgniter 使用与 PHP 提供的会话处理程序机制相同的方式来访问其会话数据。使用会话数据就像操作（读取，设置和删除） ``$_SESSION``  数组一样简单。

此外，CodeIgniter 还提供 2 种特殊类型的会话数据，下面将进一步说明：闪存数据（flashdata）和临时数据（tempdata）。

检索会话数据
=======================

会话数组中的任何信息都可以通过 ``$_SESSION`` 全局变量获得： ::

    $_SESSION['item']

或通过常规访问器方法： ::

    $session->get('item');

或通过魔术方法，例如 getter ： ::

    $session->item

甚至可以通过会话辅助函数： ::

    session('item');

``item`` 就是你所要获取的项目所对应的数组的键。例如，要将先前存储的“名称”项分配给 ``$name`` 变量，你可以这样做： ::

    $name = $_SESSION['name'];

    // 或者：
    $name = $session->name

    // 或者：
    $name = $session->get('name');

.. note:: 对于 ``get()`` 方法，如果你要访问的项目不存在，返回 NULL。

如果要检索所有现有的用户数据，则可以简单地省略 item 键（获取器仅适用于单个属性值）： ::

    $_SESSION

    // 或者：
    $session->get();

添加会话数据
===================

假设某个特定用户登录到你的网站。身份验证后，你可以将其用户名和电子邮件地址添加到会话中，从而使你可以全局使用该数据，而不必在需要时运行数据库查询。

你可以把 ``$_SESSION`` 看作像其他变量一样，将数据简单地分配给数组。或作为 ``$session`` 的属性。

以前的 userdata 方法已被废弃，但是你可以将包含新会话数据的数组传递给该 ``set()`` 方法： ::

    $session->set($array);

此处 ``$array`` 是一个包含新数据的关联数组，这是一个例子： ::

    $newdata = [
        'username'  => 'johndoe',
        'email'     => 'johndoe@some-site.com',
        'logged_in' => TRUE
    ];

    $session->set($newdata);

如果要一次为一个会话数据只添加一个值，则 ``set()`` 还支持以下语法： ::

    $session->set('some_name', 'some_value');

如果要验证会话值是否存在，只需使用 ``isset()`` 以下命令进行检查： ::

    // 如果'some_name'项目不存在或为 NULL，则返回 FALSE，反之则返回 TRUE
    isset($_SESSION['some_name'])

或者你可以调用 ``has()``： ::

    $session->has('some_name');

向会话数据推送新值
=================================

push 方法用于将新值推送到作为数组的会话值上。例如，如果“兴趣爱好”键包含一个兴趣爱好数组，则可以将新值添加到数组中，如下所示： ::

$session->push('hobbies', ['sport'=>'tennis']);

删除会话数据
=====================

与其他任何变量一样， ``$_SESSION`` 使用 ``unset()`` 通过以下方式取消设置的值： ::

    unset($_SESSION['some_name']);

    // 或者同时取消设置多个值

    unset(
        $_SESSION['some_name'],
        $_SESSION['another_name']
    );

同样，就像 ``set()`` 可以用来向会话添加信息一样， ``remove()`` 也可以通过传递会话数据的键来删除信息。例如，如果要从会话数据数组中删除“some_name”： ::

    $session->remove('some_name');

此方法还接受要取消设置的项目键数组： ::

    $array_items = ['username', 'email'];
    $session->remove($array_items);

闪存数据
=======================

CodeIgniter 支持“flashdata”，这是仅对下一个请求可用的会话数据，然后将其自动清除。

这可能非常有用，特别是对于一次性的信息，错误或状态消息（例如：“记录 2 已删除”）。

应当注意，flashdata 变量是常规会话变量，在 CodeIgniter 会话处理程序内部进行管理。

要将现有条目标记为“flashdata”： ::

    $session->markAsFlashdata('item');

如果要将多个项目标记为 flashdata，只需将键作为数组传递： ::

    $session->markAsFlashdata(['item', 'item2']);

要添加闪存数据： ::

    $_SESSION['item'] = 'value';
    $session->markAsFlashdata('item');

或者使用以下 ``setFlashdata()`` 方法： ::

    $session->setFlashdata('item', 'value');

你还可以通过与 ``set()`` 相同的方式，将一个数组传递给 ``setFlashdata()`` 。

读取 flashdata 变量与通过 ``$_SESSION`` 以下方式读取常规会话数据相同： ::

    $_SESSION['item']

.. important:: ``get()`` 当通过键检索单个项时，该方法将返回 flashdata 项。但是，从会话中获取所有用户数据时，它不会返回 flashdata。

但是，如果你想确定自己正在读取“flashdata”（而不是其他种类的数据），则也可以使用以下 ``getFlashdata()`` 方法： ::

    $session->getFlashdata('item');

或者，要获取包含所有 flashdata 的数组，只需省略 key 参数： ::

    $session->getFlashdata();

.. note:: getFlashdata() 如果找不到该项目，则该方法返回 NULL。

如果发现需要通过其他请求保留 flashdata 变量，则可以使用 ``keepFlashdata()`` 方法来实现。你可以传递单个项或一组 flashdata 项来保留。

::

    $session->keepFlashdata('item');
    $session->keepFlashdata(['item1', 'item2', 'item3']);

临时数据
========

CodeIgniter 还支持“tempdata”这种具有特定到期时间的会话数据。该值过期或会话过期或被删除后，该值将自动删除。

与 flashdata 相似，tempdata 变量由 CodeIgniter 会话处理程序在内部进行管理。

要将现有项目标记为“tempdata”，只需将其密钥和有效时间（以秒为单位）传递给该 ``mark_as_temp()`` 方法： ::

    // 'item' will be erased after 300 seconds
    $session->markAsTempdata('item', 300);

你可以通过两种方式将多个项目标记为临时数据，具体取决于你是否希望它们都具有相同的到期时间： ::

    // “item”和“item2”都将在 300 秒后过期
    $session->markAsTempdata(['item', 'item2'], 300);

    // 'item'将在 300 秒后删除，而'item2'将在 240 秒后删除
    $session->markAsTempdata([
        'item'  => 300,
        'item2' => 240
    ]);

添加临时数据： ::

    $_SESSION['item'] = 'value';
    $session->markAsTempdata('item', 300); // Expire in 5 minutes

或者使用以下 ``setTempdata()`` 方法： ::

    $session->setTempdata('item', 'value', 300);

你还可以将数组传递给 ``set_tempdata()`` ： ::

    $tempdata = ['newuser' => TRUE, 'message' => 'Thanks for joining!'];
    $session->setTempdata($tempdata, NULL, $expire);

.. note:: 如果省略了到期时间或将其设置为 0，则将使用默认的生存时间值为 300 秒（或 5 分钟）。


要读取 tempdata 变量，同样可以通过 ``$_SESSION`` 超全局数组访问它 ： ::

    $_SESSION['item']

.. important:: ``get()`` 当通过键检索单个项目时，该方法将返回 tempdata 项目。但是，从会话中获取所有用户数据时，它不会返回 tempdata。

或者，如果你想确保自己正在读取“tempdata”（而不是其他种类的数据），则也可以使用以下 ``getTempdata()`` 方法： ::

    $session->getTempdata('item');

当然，如果要检索所有现有的临时数据： ::

    $session->getTempdata();

.. note:: ``getTempdata()`` 如果找不到该项目，则该方法返回 NULL。

如果你需要在一个临时数据过期之前删除它，你可以在 ``$_SESSION`` 数组里面做到 ::

    unset($_SESSION['item']);

但是，这不会删除使该特定项成为 tempdata 的标记（它将在下一个 HTTP 请求中失效），因此，如果你打算在同一请求中重用同一键，则需要使用 ``removeTempdata()``： ::

    $session->removeTempdata('item');

销毁会话
====================

要清除当前会话（例如，在注销过程中），你可以简单地使用 PHP 的 `session_destroy() <https://www.php.net/session_destroy>`_ 函数或库的 ``destroy()`` 方法。两者将以完全相同的方式工作： ::

    session_destroy();

    // 或者

    $session->destroy();

.. note:: 这必须是你在同一请求期间执行的与会话有关的最后一个操作。销毁会话后，所有会话数据（包括 flashdata 和 tempdata）将被永久销毁，并且在同一请求期间功能将无法使用。


你还可以 ``stop()`` 通过删除旧的 session_id，销毁所有数据并销毁包含会话 ID 的 cookie，使用该方法完全终止会话： ::

    $session->stop();

访问会话元数据
==========================

在以前的 CodeIgniter 版本中，默认情况下，会话数据数组包括 4 个项目：“session_id”，“ip_address”，“user_agent”，“last_activity”。


这是由于会话如何工作的细节所致，但现在在我们的新实现中不再需要。但是，你的应用程序可能会依赖这些值，因此下面是访问它们的替代方法：

  - session_id: ``session_id()``
  - ip_address: ``$_SERVER['REMOTE_ADDR']``
  - user_agent: ``$_SERVER['HTTP_USER_AGENT']`` (unused by sessions)
  - last_activity: Depends on the storage, no straightforward way. Sorry!

会话首选项
************************************

通常，CodeIgniter 可以使所有工作立即可用。但是，会话是任何应用程序中非常敏感的组件，因此必须进行一些仔细的配置。请花点时间考虑所有选项及其效果。

你将在 **app/Config/App.php** 文件中找到以下与会话相关的首选项：

============================= =========================================== =============================================== ==========================================================
           配置项                                  默认                                         选项                                                 描述
============================= =========================================== =============================================== ==========================================================
**sessionDriver**              CodeIgniter\Session\Handlers\FileHandler    CodeIgniter\Session\Handlers\FileHandler         使用的会话驱动程序
                                                                           CodeIgniter\Session\Handlers\DatabaseHandler
                                                                           CodeIgniter\Session\Handlers\MemcachedHandler
                                                                           CodeIgniter\Session\Handlers\RedisHandler
                                                                           CodeIgniter\Session\Handlers\ArrayHandler
**sessionCookieName**          ci_session                                  [A-Za-z\_-] characters only                      会话 cookie 的名字
**sessionExpiration**          7200 (2 hours)                              Time in seconds (integer)                        您希望会话持续的秒数。如果您希望会话不过期（直到浏览器关闭），请将值设置为零：0
**sessionSavePath**            NULL                                        None                                             指定存储位置，取决于所使用的驱动程序。
**sessionMatchIP**             FALSE                                       TRUE/FALSE (boolean)                             读取会话 cookie 时是否验证用户的 IP 地址。
                                                                                                                            请注意，某些 ISP 会动态更改 IP，因此，如果您希望会话不过期，可能会将其设置为 FALSE。
**sessionTimeToUpdate**        300                                         Time in seconds (integer)                        此选项控制会话类重新生成自身并创建新的频率。会话 ID。将其设置为 0 将禁用会话 ID 再生。
**sessionRegenerateDestroy**   FALSE                                       TRUE/FALSE (boolean)                             自动重新生成时是否销毁与旧会话 ID 相关联的会话 ID。
                                                                                                                            设置为 FALSE 时，垃圾收集器稍后将删除数据。
============================= =========================================== =============================================== ==========================================================

.. note:: 作为最后的选择，如果未配置上述任何项，则会话库将尝试获取 PHP 的与会话相关的 INI 设置以及旧式 CI 设置，例如“sess_expire_on_close”。但是，你永远不要依赖此行为，因为它可能导致意外的结果或将来被更改。请正确配置所有内容。

除了上述值之外，cookie 和本机驱动程序还应用了 :doc:`IncomingRequest </incoming/incomingrequest>` 和 :doc:`Security <security>` 类共享的以下配置值：

================== =============== ===========================================================================
配置项                  默认                  描述
================== =============== ===========================================================================
**cookieDomain**   ''              会话适用的域
**cookiePath**     /               会话适用的路径
**cookieSecure**   FALSE           是否仅在加密（HTTPS）连接上创建会话 cookie
================== =============== ===========================================================================

.. note:: “cookieHTTPOnly”设置对会话没有影响。出于安全原因，始终启用 HttpOnly 参数。此外，“cookiePrefix”设置被完全忽略。

Session 驱动程序
*********************************************************************

如前所述，Session 库带有 4 个处理程序或存储引擎，你可以使用它们：

  - CodeIgniter\Session\Handlers\FileHandler
  - CodeIgniter\Session\Handlers\DatabaseHandler
  - CodeIgniter\Session\Handlers\MemcachedHandler
  - CodeIgniter\Session\Handlers\RedisHandler
  - CodeIgniter\Session\Handlers\ArrayHandler

默认情况下，在 ``FileHandler`` 初始化会话时将使用驱动程序，因为它是最安全的选择，并且有望在任何地方都可以使用（实际上每个环境都有一个文件系统）。

但是，可以选择通过 **app/Config/App.php** 文件中的 ``public $sessionDriver`` 行选择任何其他驱动程序。请记住，每个驾驶员都有不同的警告，因此在做出选择之前，一定要使自己熟悉（如下）。

.. note:: 在测试期间使用 ArrayHandler 并将其存储在 PHP 数组中，同时防止数据被持久保存。


FileHandler 驱动程序（默认）
==================================================================

“FileHandler”驱动程序使用你的文件系统来存储会话数据。

可以肯定地说，它的工作原理与 PHP 自己的默认会话实现完全相同，但是如果这对你来说是一个重要的细节，请记住，它实际上不是相同的代码，并且有一些限制（和优点）。


更具体地说，它不支持 `directory level and mode
formats used in session.save_path
<https://www.php.net/manual/en/session.configuration.php#ini.session.save-path>`_ ，并且为了安全起见，大多数选项都经过硬编码。相反， ``public $sessionSavePath`` 仅支持绝对路径。


你还应该知道的另一件事是，确保不要使用公共可读或共享目录来存储会话文件。确保 *只有你* 有权查看所选 *sessionSavePath* 目录的内容。否则，任何能够做到这一点的人都可以窃取当前的任何会话（也称为“会话固定”攻击）。


在类似 UNIX 的操作系统上，这通常是通过使用 *chmod* 命令在该目录上设置 0700 模式权限来实现的，该命令仅允许目录所有者对目录执行读取和写入操作。但是要小心，因为 *运行* 脚本的系统用户通常不是你自己的，而是“www-data”之类的东西，因此仅设置这些权限可能会破坏你的应用程序。


Instead, you should do something like this, depending on your environment
取而代之的是，你应该根据自己的环境执行类似的操作

::

    mkdir /<path to your application directory>/Writable/sessions/
    chmod 0700 /<path to your application directory>/Writable/sessions/
    chown www-data /<path to your application directory>/Writable/sessions/

Bonus Tip
--------------------------------------------------------

某些人可能会选择其他会话驱动程序，因为文件存储通常较慢。这只有一半是正确的。


一个非常基本的测试可能会让你相信 SQL 数据库更快，但是在 99％的情况下，只有当你只有几个当前会话时，这才是正确的。随着会话数的增加和服务器负载的增加（这很重要），文件系统将始终胜过几乎所有的关系数据库设置。

此外，如果只考虑性能，则可能需要研究使用 `tmpfs <https://eddmann.com/posts/storing-php-sessions-file-caches-in-memory-using-tmpfs/>`_ ，（警告：外部资源），它可以使会话快速发展。


DatabaseHandler 驱动程序
==================================================================

“DatabaseHandler”驱动程序使用关系数据库（例如 MySQL 或 PostgreSQL）来存储会话。这是许多用户中的一个流行选择，因为它使开发人员可以轻松访问应用程序中的会话数据 - 它只是数据库中的另一个表。

但是，必须满足一些条件：

  - 你不能使用持久连接。
  - 你不能在启用 *cacheOn* 设置的情况下使用连接。

为了使用“DatabaseHandler”会话驱动程序，你还必须创建我们已经提到的该表，然后将其设置为你的 ``$sessionSavePath`` 值。例如，如果你想使用“ci_sessions”作为表名，则可以这样做： ::

    public $sessionDriver   = 'CodeIgniter\Session\Handlers\DatabaseHandler';
    public $sessionSavePath = 'ci_sessions';

然后，当然要创建数据库表…

对于 MySQL： ::

    CREATE TABLE IF NOT EXISTS `ci_sessions` (
        `id` varchar(128) NOT NULL,
        `ip_address` varchar(45) NOT NULL,
        `timestamp` int(10) unsigned DEFAULT 0 NOT NULL,
        `data` blob NOT NULL,
        KEY `ci_sessions_timestamp` (`timestamp`)
    );

对于 PostgreSQL： ::

    CREATE TABLE "ci_sessions" (
        "id" varchar(128) NOT NULL,
        "ip_address" varchar(45) NOT NULL,
        "timestamp" bigint DEFAULT 0 NOT NULL,
        "data" text DEFAULT '' NOT NULL
    );

    CREATE INDEX "ci_sessions_timestamp" ON "ci_sessions" ("timestamp");

你还需要 **根据你的“sessionMatchIP”设置** 添加主键。以下示例在 MySQL 和 PostgreSQL 上均可使用： ::

    // 当 sessionMatchIP = TRUE 时
    ALTER TABLE ci_sessions ADD PRIMARY KEY (id, ip_address);

    // 当 sessionMatchIP = FALSE 时
    ALTER TABLE ci_sessions ADD PRIMARY KEY (id);

    // 删除先前创建的主键（在更改设置时使用）
    ALTER TABLE ci_sessions DROP PRIMARY KEY;

你可以通过在 **application\Config\App.php** 文件中添加新行并使用要使用的组名来选择要使用的数据库组 ： ::

  public $sessionDBGroup = 'groupName';

如果你不想手工完成所有这些操作，则可以使用 **session:migrationcli** 中的命令为你生成一个迁移文件： ::

  > php spark session:migration
  > php spark migrate

该命令在生成代码时将考虑 **sessionSavePath** 和 **sessionMatchIP** 设置。

.. important:: 由于缺少其他平台上的建议性锁定机制，因此仅正式支持 MySQL 和 PostgreSQL 数据库。使用不带锁的会话会导致各种问题，尤其是在大量使用 AJAX 的情况下，我们不支持这种情况。 ``session_write_close()`` 如果遇到性能问题，请在处理完会话数据后使用。


RedisHandler 驱动程序
==================================================================

.. note:: 由于 Redis 没有公开锁定机制，因此该驱动程序的锁定由一个单独的值模拟，该值最多可保留 300 秒。

Redis 是一种存储引擎，由于其高性能而通常用于缓存并广受欢迎，这可能也是你使用'RedisHandler'会话驱动程序的原因。

缺点是它不像关系数据库那样普遍存在，并且需要在系统上安装 `phpredis <https://github.com/phpredis/phpredis>`_  PHP 扩展，并且没有与 PHP 捆绑在一起。很有可能，仅当你已经熟悉 Redis 并将其用于其他目的时，才使用 RedisHandler 驱动程序。

与“FileHandler”和“DatabaseHandler”驱动程序一样，你还必须通过该 ``$sessionSavePath`` 设置配置会话的存储位置 。此处的格式有些不同，同时又很复杂。最好用 *phpredis* 扩展的 README 文件来解释，所以我们将简单地链接到它： ::

    https://github.com/phpredis/phpredis

.. warning:: CodeIgniter 的会话库不使用实际的'redis' session.save_handler。 ``仅`` 注意上面链接中的路径格式。

但是，对于最常见的情况，一个简单的 ``host:port`` 配对就足够了： ::

    public $sessionDiver    = 'CodeIgniter\Session\Handlers\RedisHandler';
    public $sessionSavePath = 'tcp://localhost:6379';

MemcachedHandler 驱动程序
==================================================================

.. note:: 由于 Memcached 没有公开锁定机制，因此该驱动程序的锁定由一个单独的值模拟，该值最多保留 300 秒。

除了可能的可用性外，“`Memcached
<https://www.php.net/memcached>`_ ”驱动程序的所有属性都与“RedisHandler”驱动程序非常相似，因为 PHP 的 Memcached 扩展是通过 PECL 分发的，并且某些 Linux 发行版使其可以作为易于安装的软件包使用。

除此之外，对于 Redis 并没有任何故意的偏见，关于 Memcached 的说法没有多大不同 - 它也是一种流行的产品，通常用于缓存并以其速度着称。

但是，值得注意的是，Memcached 给出的唯一保证是将值 X 设置为在 Y 秒后过期将导致在 Y 秒过去之后将其删除（但不一定要在该时间之前过期）。这种情况很少发生，但是应该考虑，因为这可能会导致会话丢失。

该 ``$sessionSavePath`` 格式相当这里简单，仅仅是一对 ``host:port`` ： ::

    public $sessionDriver   = 'CodeIgniter\Session\Handlers\MemcachedHandler';
    public $sessionSavePath = 'localhost:11211';

Bonus Tip
--------------------------------------------------------

还支持使用可选的 *weight* 参数作为第三个冒号 ( ``:weight`` ) 值的多服务器配置，但是我们必须注意，我们尚未测试这是否可靠。

如果要尝试使用此功能（后果自负），只需用逗号分隔多个服务器路径： ::

    // 相比于 192.0.2.1 权重为 1，本地主机将获得更高的优先级（5）。
    public $sessionSavePath = 'localhost:11211:5,192.0.2.1:11211:1';
