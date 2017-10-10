######################
数据库配置
######################

CodeIgniter 中有一个用来保存数据库配置（用户名，密码，数据库名等）的文件，这个配置文件位于 application/Config/Database.php。你也可以在 .env 文件中配置数据库连接参数。接下来让我们详细看下配置信息。

数据库配置信息存放在数组中::

	public $default = [
		'DSN'	=> '',
		'hostname' => 'localhost',
		'username' => 'root',
		'password' => '',
		'database' => 'database_name',
		'DBDriver' => 'MySQLi',
		'DBPrefix' => '',
		'pConnect' => TRUE,
		'DBDebug'  => TRUE,
		'cacheOn'  => FALSE,
		'cacheDir' => '',
		'charset'  => 'utf8',
		'DBCollat' => 'utf8_general_ci',
		'swapPre'  => '',
		'encrypt'  => FALSE,
		'compress' => FALSE,
		'strictOn' => FALSE,
		'failover' => array(),
	];

类属性的名称就是连接名称，并且可以使用特殊的组名连接。

有些数据库驱动（例如：PDO，PostgreSQL，Oracle，ODBC）可能需要提供完整的 DNS 信息。在这种情况下，你需要使用 DNS 配置参数，就像是使用该驱动的原生 PHP 扩展一样，例如::

	// PDO
	$default['DSN'] = 'pgsql:host=localhost;port=5432;dbname=database_name';

	// Oracle
	$default['DSN'] = '//localhost/XE';

.. 注解:: 如果你没有指定 DNS 驱动需要的参数信息，CodeIgniter 将使用你提供的其它配置信息自动构造它。

.. 注解:: 如果你提供了一个 DNS 参数，但是缺少了某些配置（例如：数据库的字符集），若该配置存在在其它的配置项中，CodeIgniter 将自动在 DNS 上附加上该配置。

当主数据库由于某些原因无法连接时，你可以配置故障转移。例如可以像下面这样为一个连接配置故障转移::

	$default['failover'] = [
			[
				'hostname' => 'localhost1',
				'username' => '',
				'password' => '',
				'database' => '',
				'DBDriver' => 'MySQLi',
				'DBPrefix' => '',
				'pConnect' => TRUE,
				'DBDebug'  => TRUE,
				'cacheOn'  => FALSE,
				'cacheDir' => '',
				'charset'  => 'utf8',
				'DBCollat' => 'utf8_general_ci',
				'swapPre'  => '',
				'encrypt'  => FALSE,
				'compress' => FALSE,
				'strictOn' => FALSE
			],
			[
				'hostname' => 'localhost2',
				'username' => '',
				'password' => '',
				'database' => '',
				'DBDriver' => 'MySQLi',
				'DBPrefix' => '',
				'pConnect' => TRUE,
				'DBDebug'  => TRUE,
				'cacheOn'  => FALSE,
				'cacheDir' => '',
				'charset'  => 'utf8',
				'DBCollat' => 'utf8_general_ci',
				'swapPre'  => '',
				'encrypt'  => FALSE,
				'compress' => FALSE,
				'strictOn' => FALSE
			]
		];

你可以指定任意多个你喜欢的故障转移配置。

你可以选择存储多组连接值的信息。例如，若你运行多个环境（开发、生产、测试等），你可以为每个环境单独建立连接组，并在组之间进行切换。举个例子：若要设置一个 'test' 环境，你可以这么做::

	public $test = [
		'DSN'	=> '',
		'hostname' => 'localhost',
		'username' => 'root',
		'password' => '',
		'database' => 'database_name',
		'DBDriver' => 'MySQLi',
		'DBPrefix' => '',
		'pConnect' => TRUE,
		'DBDebug'  => TRUE,
		'cacheOn'  => FALSE,
		'cacheDir' => '',
		'charset'  => 'utf8',
		'DBCollat' => 'utf8_general_ci',
		'swapPre'  => '',
		'compress' => FALSE,
		'encrypt'  => FALSE,
		'strictOn' => FALSE,
		'failover' => array()
	);

然后，设置配置文件中的变量并告诉系统要使用该组信息::

	$defaultGroup = 'test';

.. 注解:: 组的名称为 'test' 是任意的。它可以是你想要的任意名称。默认情况下，主连接使用 'default' 这个名称，但你可以基于你的项目为它起一个更有意义的名字。

你可以修改配置文件来检测环境并且在类的构造函数中添加所需的逻辑来自动更新正确的 'defaultGroup' 值::

	class Database
	{
	    public $development = [...];
	    public $test        = [...];
	    public $production  = [...];

		public function __construct()
		{
			$this->defaultGroup = ENVIRONMENT;
		}
	}

配置文件
--------------------------

你可以将配置值保存在当前服务器数据库配置文件 ``.env`` 中。你只需要在默认组配置设置中输入你想要改变的值。该值在 ``default`` 组中的格式为::

	database.default.username = 'root';
	database.default.password = '';
	database.default.database = 'ci4';

其它信息

参数解释:
----------------------

======================  ===========================================================================================================
 配置名             描述
======================  ===========================================================================================================
**dsn**                 DNS 连接字符串 （该字符串包含了所有的数据库配置信息）
**hostname**            数据库的主机名，通常表示为本机的 'localhost'
**username**            需要连接到的数据库的用户名
**password**            登录数据库的密码
**database**            需要连接的数据库名
**DBDriver**            数据库类型。如：MySQLi、Postgre等。事例必须与程序名匹配
**DBPrefix**            当使用 :doc:`查询构造器 <query_builder>` 查询时，可以选择性的为表加个前缀，它允许在一个数据库上安装多个 CodeIgniter 程序
**pConnect**            TRUE/FALSE (boolean) - 是否使用持续连接
**DBDebug**             TRUE/FALSE (boolean) - 是否显示数据库错误信息
**cacheOn**             TRUE/FALSE (boolean) - 是否开启数据库查询缓存
**cacheDir**            数据库查询缓存目录所在的服务器绝对路径
**charset**             与数据库通信时所使用的字符集
**DBCollat**            与数据库通信时所使用的字符集规则

                        .. 注解:: 只用于 'MySQLi' 数据库驱动

**swapPre**             替换默认的 dbprefix 表前缀，该项设置对于分布式应用是非常有用的，你可以在查询中使用用户最终定于的表前缀
**schema**              默认数据库模式为 'public'，用于 PostgreSQL 和 ODBC 驱动
**encrypt**             是否是用加密连接

                        - 'sqlsrv' and 'pdo/sqlsrv' drivers accept TRUE/FALSE
                        - 'MySQLi' and 'pdo/mysql' drivers accept an array with the following options:

                        - 'ssl_key'    - Path to the private key file
                        - 'ssl_cert'   - Path to the public key certificate file
                        - 'ssl_ca'     - Path to the certificate authority file
                        - 'ssl_capath' - Path to a directory containing trusted CA certificats in PEM format
                        - 'ssl_cipher' - List of *allowed* ciphers to be used for the encryption, separated by colons (':')
                        - 'ssl_verify' - TRUE/FALSE; Whether to verify the server certificate or not ('MySQLi' only)

**compress**            是否使用客户端压缩协议（只用于 MySQL）
**strictOn**            TRUE/FALSE (boolean) - 是否强制使用 "Strict Mode" 连接。在程序开发时，使用 strict SQL 是一个好习惯
**port**                数据库端口号。 要使用这个值，你应该添加以下一行代码到数据库配置组中
                        ::

                        $default['port'] = 5432;

======================  ===========================================================================================================

.. 注解:: 根据你使用的数据库平台（MySQL、PostgreSQL等）来筛选哪些参数是必须的。例如，当你使用 SQLite 时，你无需指定用户名和密码，数据库名称是你的数据库文件路径。以上内容假设你是用的是 MySQL 数据库。
