###################
记录日志信息
###################

.. contents::
    :local:
    :depth: 2

你可以通过 ``log_message()`` 方法将信息记录在本地日志文件中，并且必须在第一个参数中指定错误的"级别"，来表明这个信息的类型（debug，error等）。
第二个参数就是信息本身::

	if ($some_var == '')
	{
		log_message('error', 'Some variable did not contain a value.');
	}

总共有八种不同的事件报错级别，与 `RFC 5424 <http://tools.ietf.org/html/rfc5424>`_ 中所定义的错误级别一一对应，它们是::

* **debug** - 详细的debug信息。
* **info** - 你的应用中的一些有意义的事件，例如用户登录，记录SQL语句等。
* **notice** - 你的应用中的一些正常但明显有价值的事件。
* **warning** - 出现了异常，但不是错误，例如使用了被废弃的API，某个API的调用异常，或其他不期望出现的，但不是错误的情况。
* **error** - 运行时错误，不需要立即被处理但通常需要被记录或者监控。
* **critical** - 危险情况，例如某个程序组件不可用，或出现未被捕获的异常等。
* **alert** - 告警，必须采取行动来修复，例如整个网站宕机或数据库无法访问等。
* **emergency** - 系统不可用。

日志系统不提供警告系统管理员或网站管理者的方法，只是单纯的记录信息。对于诸多更为危险的错误级别，日志就会被异常调度器自动抛出，如上所述。

配置
=============

你可以修改 ``/app/Config/Logger.php` 配置文件来修改哪些级别的事件会被实际记录，以及为不同的事件等级分配不同的日志记录器等。

配置文件中的 ``threshold`` （报错阈值）决定了从哪个级别开始的事件将会在整个应用中记录下来。如果应用中有任何低于报错阈值的事件记录被记录时，这些请求将会被忽略。
最为简单的使用阈值的方法就是将其设为你希望记录的报错等级的最低值。举例来说，如果你想记录warning信息，而不是information信息，就需要将报错阈值设为 ``5`` 。所有报错等级低于5的日志记录请求
（包括运行时错误，系统错误等）将会被记录，而info, notice和debug级别的错误就会被忽略::

	public $threshold = 5;

关于报错级别和对应的阈值的列表列举在配置文件中以供参阅。

你可以通过给报错阈值赋值一个包含报错等级数字的数组，来选择特定的报错级别::

	// 只记录debug和info类型的报错
	public $threshold = [5, 8];

使用多个日志调度器
---------------------------

日志系统支持同时使用多种方法来处理日志记录。每一种调度器可以独立地设置用于特定的错误等级，并忽略其他的。现状而言，我们默认安装了两种调度器以供使用:

- **File Handler** is the default handler and will create a single file for every day locally. This is the
  recommended method of logging.
- **ChromeLogger Handler** If you have the `ChromeLogger extension <https://craig.is/writing/chrome-logger>`_
  installed in the Chrome web browser, you can use this handler to display the log information in
  Chrome's console window.

The handlers are configured in the main configuration file, in the ``$handlers`` property, which is simply
an array of handlers and their configuration. Each handler is specified with the key being the fully
name-spaced class name. The value will be an array of varying properties, specific to each handler.
Each handler's section will have one property in common: ``handles``, which is an array of log level
*names* that the handler will log information for.
::

	public $handlers = [

		//--------------------------------------------------------------------
		// File Handler
		//--------------------------------------------------------------------

		'CodeIgniter\Log\Handlers\FileHandler' => [

			'handles' => ['critical', 'alert', 'emergency', 'debug', 'error', 'info', 'notice', 'warning'],
		]
	];

Modifying the Message With Context
==================================

You will often want to modify the details of your message based on the context of the event being logged.
You might need to log a user id, an IP address, the current POST variables, etc. You can do this by use
placeholders in your message. Each placeholder must be wrapped in curly braces. In the third parameter,
you must provide an array of placeholder names (without the braces) and their values. These will be inserted
into the message string::

	// Generates a message like: User 123 logged into the system from 127.0.0.1
	$info = [
		'id' => $user->id,
		'ip_address' => $this->request->ip_address()
	];

	log_message('info', 'User {id} logged into the system from {ip_address}', $info);

If you want to log an Exception or an Error, you can use the key of 'exception', and the value being the
Exception or Error itself. A string will be generated from that object containing the error message, the
file name and line number. You must still provide the exception placeholder in the message::

	try
	{
		... Something throws error here
	}
	catch (\Exception $e)
	{
		log_message('error', '[ERROR] {exception}', ['exception' => $e]);
	}

Several core placeholders exist that will be automatically expanded for you based on the current page request:

+----------------+---------------------------------------------------+
| Placeholder    | Inserted value                                    |
+================+===================================================+
| {post_vars}    | $_POST variables                                  |
+----------------+---------------------------------------------------+
| {get_vars}     | $_GET variables                                   |
+----------------+---------------------------------------------------+
| {session_vars} | $_SESSION variables                               |
+----------------+---------------------------------------------------+
| {env}          | Current environment name, i.e. development        |
+----------------+---------------------------------------------------+
| {file}         | The name of file calling the logger               |
+----------------+---------------------------------------------------+
| {line}         | The line in {file} where the logger was called    |
+----------------+---------------------------------------------------+
| {env:foo}      | The value of 'foo' in $_ENV                       |
+----------------+---------------------------------------------------+

Using Third-Party Loggers
=========================

You can use any other logger that you might like as long as it extends from either
``Psr\Log\LoggerInterface`` and is `PSR3 <http://www.php-fig.org/psr/psr-3/>`_ compatible. This means
that you can easily drop in use for any PSR3-compatible logger, or create your own.

You must ensure that the third-party logger can be found by the system, by adding it to either
the ``/app/Config/Autoload.php`` configuration file, or through another autoloader,
like Composer. Next, you should modify ``/app/Config/Services.php`` to point the ``logger``
alias to your new class name.

Now, any call that is done through the ``log_message()`` function will use your library instead.

LoggerAware Trait
=================

If you would like to implement your libraries in a framework-agnostic method, you can use
the ``CodeIgniter\Log\LoggerAwareTrait`` which implements the ``setLogger()`` method for you.
Then, when you use your library under different environments for frameworks, your library should
still be able to log as it would expect, as long as it can find a PSR3 compatible logger.
