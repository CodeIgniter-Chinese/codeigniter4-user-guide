#################
自动加载文件
#################

每个应用都在不同的位置包含有大量的类文件。框架提供了实现核心功能的类，而你的应用将会由大量的库，模型，以及其他实体文件以运行。
你也可能需要第三方的类库以供项目使用。记录每个单独的文件的位置，并硬编码一系列的 ``requires()`` 在文件中，这是一个非常头疼且容易出错的事情。
这就是自动加载器的用武之地。

CodeIgniter提供了一个非常灵活且需要极少配置的自动加载器。它可以定位单个的非命名空间标注的类，符合命名空间规范 `PSR4 <http://www.php-fig.org/psr/psr-4/>`_ 目录加载结构的类，
甚至可以在常规目录下定位类文件（例如控制器，模型等）。

为了提升性能，CodeIgniter的核心组件已被添加到类映射文件中。

自动加载器可以单独运行，如果你需要的话，可以和其他自动加载器协同运行，例如 `Composer <https://getcomposer.org>`_ 或者是你自己的自定义加载器。
因为它们都是通过 `spl_autoload_register <http://php.net/manual/en/function.spl-autoload-register.php>`_ 来注册运行的，所以可以依次运行，互不打扰。

The autoloader is always active, being registered with ``spl_autoload_register()`` at the
beginning of the framework's execution.

Configuration
=============

Initial configuration is done in **/application/Config/Autoload.php**. This file contains two primary
arrays: one for the classmap, and one for PSR4-compatible namespaces.

Namespaces
==========

The recommended method for organizing your classes is to create one or more namespaces for your
application's files. This is most important for any business-logic related classes, entity classes,
etc. The ``psr4`` array in the configuration file allows you to map the namespace to the directory
those classes can be found in::

	$psr4 = [
		'App'         => APPPATH,
		'CodeIgniter' => BASEPATH,
	];

The key of each row is the namespace itself. This does not need a trailing slash. If you use double-quotes
to define the array, be sure to escape the backwards slash. That means that it would be ``My\\App``,
not ``My\App``. The value is the location to the directory the classes can be found in. They should
have a trailing slash.

By default, the application folder is namespace to the ``App`` namespace. While you are not forced to namespace the controllers,
libraries, or models in the application directory, if you do, they will be found under the ``App`` namespace.
You may change this namespace by editing the **/application/Config/Constants.php** file and setting the
new namespace value under the ``APP_NAMESPACE`` setting::

	define('APP_NAMESPACE', 'App');

You will need to modify any existing files that are referencing the current namespace.

.. important:: Config files are namespaced in the ``Config`` namespace, not in ``App\Config`` as you might
	expect. This allows the core system files to always be able to locate them, even when the application
	namespace has changed.

Classmap
========

The classmap is used extensively by CodeIgniter to eke the last ounces of performance out of the system
by not hitting the file-system with extra ``file_exists()`` calls. You can use the classmap to link to
third-party libraries that are not namespaced::

	$classmap = [
		'Markdown' => APPPATH .'third_party/markdown.php'
	];

The key of each row is the name of the class that you want to locate. The value is the path to locate it at.

Legacy Support
==============

If neither of the above methods find the class, and the class is not namespaced, the autoloader will look in the
**/application/Libraries** and **/application/Models** directories to attempt to locate the files. This provides
a measure to help ease the transition from previous versions.

There are no configuration options for legacy support.
