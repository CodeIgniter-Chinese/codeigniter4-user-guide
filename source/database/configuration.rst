######################
数据库配置
######################

.. contents::
    :local:
    :depth: 2

CodeIgniter 有一个用来保存数据库配置的文件（用户名，密码，数据库名等），这个配置文件位于 application/Config/Database.php。你也可以在 .env 文件里配置数据库连接参数。下面来看看详细配置信息。

配置信息是一个数组，存储在类的属性里面，原型如下::

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

类的属性名称就是连接名称，并且在连接时可以作为指定配置组名称使用。

有些数据库驱动（例如：PDO，PostgreSQL，Oracle，ODBC）可能需要提供完整的 DNS 信息。在这种情况下，你需要使用 DNS 配置参数，就像使用该驱动的原生 PHP 扩展一样，例如::

	// PDO
	$default['DSN'] = 'pgsql:host=localhost;port=5432;dbname=database_name';

	// Oracle
	$default['DSN'] = '//localhost/XE';

.. 注解:: 如果你没有指定 DNS 驱动需要的参数信息，CodeIgniter 将使用你提供的其它配置信息自动构造它。

.. 注解:: 如果你提供了一个 DNS 参数，但是缺少了某些配置（例如：数据库的字符集），若该配置存在在其它的配置项中，CodeIgniter 将自动在 DNS 上附加上该配置。

当主数据库由于某些原因无法连接时，你可以配置多个灾备数据库。例如可以像下面这样为一个连接配置灾备数据库::

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

你可以指定任意多个灾备数据库配置。

你可以选择性地存储多组连接信息。例如，在一个安装实例里面运行多个环境（开发、生产、测试等），你可以为每个环境配置连接组，然后在组之间进行切换。举个例子：若要设置一个 'test' 环境，你可以这么做::

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

然后，修改该配置文件中的属性值，告知系统使用该组信息::

	$defaultGroup = 'test';

.. 注解:: 组名称 'test' 是任意的。它可以是你想要的任意名称。默认情况下，主连接使用 'default' 这个名称，但你也可以起一个与你项目更加相关的名称。

你可以修改配置文件里面类的构造函数，让它自动检测运行环境并将 'defaultGroup' 更新为正确的值::

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

配置 .env 文件
--------------------------

你也可以将当前服务器的数据库配置保存到 ``.env`` 文件 中。你只需要在默认配置组中输入你想要变更的值。该值在 ``default`` 组中的格式为::

	database.default.username = 'root';
	database.default.password = '';
	database.default.database = 'ci4';

其它信息

参数解释:
----------------------

======================  ===========================================================================================================
 配置名                   描述
======================  ===========================================================================================================
**dsn**                 DNS 连接字符串 （该字符串包含了连接数据库的全部配置信息）
**hostname**            数据库的主机名，通常为本机的 'localhost'
**username**            连接数据库的用户名
**password**            连接数据库的密码
**database**            需要连接的数据库名
**DBDriver**            数据库类型，如：MySQLi、Postgre等。大小写必须与驱动名匹配
**DBPrefix**            当使用 :doc:`查询构造器 <query_builder>` 查询时，可以选择性的为表加个前缀，它允许多个 CodeIgniter 程序共用一个数据库
**pConnect**            TRUE/FALSE (boolean) - 是否使用持续连接
**DBDebug**             TRUE/FALSE (boolean) - 是否显示数据库错误信息
**cacheOn**             TRUE/FALSE (boolean) - 是否开启数据库查询缓存
**cacheDir**            数据库查询缓存目录，服务器绝对路径
**charset**             与数据库通信时所使用的字符集
**DBCollat**            与数据库通信时所使用的字符集规则

                        .. 注解:: 只用于 'MySQLi' 数据库驱动

**swapPre**             替换默认的 dbprefix 表前缀，该项设置对于分布式应用是非常有用的， 你可以在查询中使用由最终用户定制的表前缀。
**schema**              默认数据库模式为 'public'，用于 PostgreSQL 和 ODBC 驱动
**encrypt**             是否是用加密连接

                        - 'sqlsrv' 和 'pdo/sqlsrv' 驱动接受 TRUE/FALSE
                        - 'MySQLi' 和 'pdo/mysql' 驱动接受一个数组，选项如下:

                        - 'ssl_key'    - 私钥文件存放路径
                        - 'ssl_cert'   - 公钥证书文件存放路径
                        - 'ssl_ca'     - CA证书授权文件路径
                        - 'ssl_capath' - PEM格式的受信任CA证书存放目录
                        - 'ssl_cipher' -  *允许* 使用的加密算法列表，多项用 (':') 分割
                        - 'ssl_verify' - TRUE/FALSE; 是否验证服务器的证书 (仅限 MySQLi)

**compress**            是否使用客户端压缩协议（只用于 MySQL）
**strictOn**            TRUE/FALSE (boolean) - 是否强制使用 "Strict Mode" 连接。在程序开发时，使用 strict SQL 是一个好习惯
**port**                数据库端口号。 要使用这个值，你应该添加以下一行代码到数据库配置组中
                        ::

                        $default['port'] = 5432;

======================  ===========================================================================================================

.. 注解:: 根据你使用的数据库平台（MySQL、PostgreSQL等）不是所有参数都要配置。例如，当你使用 SQLite 时，你无需指定用户名和密码，数据库名称是你的数据库文件路径。以上内容假设你使用的是 MySQL 数据库。
