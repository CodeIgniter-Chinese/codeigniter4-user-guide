################################
配置文件
################################

每一个项目，都需要一种方法来定义不同的全局配置项，而这通常是借助配置文件来实现的。
而配置文件，一般来说，是通过声明一个将所有的配置项作为公开属性的类，来实现这一配置过程的。

Unlike many other frameworks, CodeIgniter configurable items aren't contained in
a single file. Instead, each class that needs configurable items will have a
configuration file with the same name as the class that uses it. You will find
the application configuration files in the **/app/Config** folder.

.. contents::
    :local:
    :depth: 2

访问配置文件
======================

You can access configuration files for your classes in several different ways.

- By using the ``new`` keyword to create an instance::

	// Creating new configuration object by hand
	$config = new \Config\Pager();

- By using the ``config()`` function::

	// Get shared instance with config function
	$config = config('Pager');

	// Access config class with namespace
	$config = config( 'Config\\Pager' );

	// Creating a new object with config function
	$config = config('Pager', false);

All configuration object properties are public, so you access the settings like any other property::

        $config = config('Pager');
	// Access settings as object properties
	$pageSize = $config->perPage;


若没有给定namespace(命名空间），框架会在所有可用的、已被定义的命名空间中搜寻所需的文件，就如同 **/app/Config/** 一样。

All of the configuration files that ship with CodeIgniter are namespaced with
``Config``. Using this namespace in your application will provide the best
performance since it knows exactly where to find the files.

我们也可以通过使用一个不同的命名空间，从而在服务器的任意位置上部署所需的配置文件。
这一举措可以让我们将生产环境的服务器中的配置文件移动到一个不能通过Web访问的位置；而在开发环境中，将其放置在 **/app** 目录下以便访问。

创建配置文件
============================

When you need a new configuration, first you create a new file at your desired location.
The default file location (recommended for most cases) is **/app/Config**.
The class should use the appropriate namespace, and it should extend
``CodeIgniter\Config\BaseConfig`` to ensure that it can receive environment-specific settings.

Define the class and fill it with public properties that represent your settings.::

    <?php namespace Config;

    use CodeIgniter\Config\BaseConfig;

    class CustomClass extends BaseConfig
    {
    	public $siteName  = 'My Great Site';
    	public $siteEmail = 'webmaster@example.com';

    }

环境变量
=====================

One of today’s best practices for application setup is to use Environment Variables. One reason for this is that Environment Variables are easy to change between deploys without changing any code. Configuration can change a lot across deploys, but code does not. For instance, multiple environments, such as the developer’s local machine and the production server, usually need different configuration values for each particular setup.

Environment Variables should also be used for anything private such as passwords, API keys, or other sensitive data.

Environment Variables and CodeIgniter
=====================================

CodeIgniter makes it simple and painless to set Environment Variables by using a “dotenv” file. The term comes from the file name, which starts with a dot before the text “env”.

CodeIgniter expects **.env** to be at the root of your project alongside the ``system``
and ``app`` directories. There is a template file distributed with CodeIgniter that’s
located at the project root named **env** (Notice there’s no dot (**.**) at the start?).
It has a large collection of variables your project might use that have been assigned
empty, dummy, or default values. You can use this file as a starting place for your
application by either renaming the template to **.env**, or by making a copy of it named **.env**.

.. important:: Make sure the **.env** file is NOT tracked by your version control system. For *git* that means adding it to **.gitignore**. Failure to do so could result in sensitive credentials being exposed to the public.

Settings are stored in **.env** files as a simple a collection of name/value pairs separated by an equal sign.
::

	S3_BUCKET = dotenv
	SECRET_KEY = super_secret_key
        CI_ENVIRONMENT = development

When your application runs, **.env** will be loaded automatically, and the variables put
into the environment. If a variable already exists in the environment, it will NOT be
overwritten. The loaded Environment variables are accessed using any of the following:
``getenv()``, ``$_SERVER``, or ``$_ENV``.
::

	$s3_bucket = getenv('S3_BUCKET');
	$s3_bucket = $_ENV['S3_BUCKET'];
	$s3_bucket = $_SERVER['S3_BUCKET'];

嵌套变量
=================

为了减少输入，我们也可以用将变量名包裹在 ``${...}`` 的形式，来重用先前定义过的变量::

	BASE_DIR="/var/webroot/project-root"
	CACHE_DIR="${BASE_DIR}/cache"
	TMP_DIR="${BASE_DIR}/tmp"

命名空间中的变量
====================

有时候，我们会遇到多个变量具有相同名字的情况。当这种情况发生时，系统将没有办法获知这个变量所对应的确切的值。
我们可以通过将这些变量放入”命名空间“中，来放置这一情况的出现。

在配置文件中，点号(.)通常被用来表示一个变量是命名空间变量。这种变量通常是由一个独立前缀，后接一个点号(.)然后才是变量名称本身所组成的::

    // 非命名空间变量
    name = "George"
    db=my_db

    // 命名空间变量
    address.city = "Berlin"
    address.country = "Germany"
    frontend.db = sales
    backend.db = admin
    BackEnd.db = admin

Configuration Classes and Environment Variables
===============================================

When you instantiate a configuration class, any *namespaced* environment variables
are considered for merging into the configuration object's properties.

If the prefix of a namespaced variable exactly matches the namespace of the configuration
class, then the trailing part of the setting (after the dot) is treated as a configuration
property. If it matches an existing configuration property, the environment variable's
value will replace the corresponding value from the configuration file. If there is no match,
the configuration class properties are left unchanged. In this usage, the prefix must be
the full (case-sensitive) namespace of the class.
::

    Config\App.CSRFProtection  = true
    Config\App.CSRFCookieName = csrf_cookie
    Config\App.CSPEnabled = true


.. note:: Both the namespace prefix and the property name are case-sensitive. They must exactly match the full namespace and property names as defined in the configuration class file.

The same holds for a *short prefix*, which is a namespace using only the lowercase version of
the configuration class name. If the short prefix matches the class name,
the value from **.env** replaces the configuration file value.
::

    app.CSRFProtection  = true
    app.CSRFCookieName = csrf_cookie
    app.CSPEnabled = true

.. note:: When using the *short prefix* the property names must still exactly match the class defined name.

以数组的方式调用环境变量
========================================

从更长远的角度来看，一个命名空间环境变量也可以以数组的方式被调用。
如果一个命名空间环境变量的前缀与某个配置类所匹配，那么这个变量的剩余部分，若同样包含点号，则将会被当做一个数组的引用来调用::

    // 常规的命名空间变量
    Config\SimpleConfig.name = George

    // 数组化的命名空间变量
    Config\SimpleConfig.address.city = "Berlin"
    Config\SimpleConfig.address.country = "Germany"


如果这个变量是对SimpleConfig配置类的成员的引用，上述例子将会如下图所示::

    $address['city'] = "Berlin";
    $address['country'] = "Germany";

而 ``$address`` 属性的其他部分将不会被改动。

我们同样可以将数组属性名作为前缀来使用，当配置文件如下所示时::

    // array namespaced variables
    Config\SimpleConfig.address.city = "Berlin"
    address.country = "Germany"

Handling Different Environments
===============================

Configuring multiple environments is easily accomplished by using a separate **.env** file with values modified to meet that environment's needs.

The file should not contain every possible setting for every configuration class used by the application. In truth, it should include only those items that are specific to the environment or are sensitive details like passwords and API keys and other information that should not be exposed. But anything that changes between deployments is fair-game.

In each environment, place the **.env** file in the project's root folder. For most setups, this will be the same level as the ``system`` and ``app`` directories.

Do not track **.env** files with your version control system. If you do, and the repository is made public, you will have put sensitive information where everybody can find it.

.. _registrars:

注册器
==========

一个配置文件可以指定任意数量的”注册器“；这里所指的注册器为其他类可能提供的额外的配置属性。
这一行为通常通过在配置文件中增加一个 ``registrars`` 属性来实现，这一属性存有一个可选的注册器数组。::

    protected $registrars = [
        SupportingPackageRegistrar::class
    ];

为了实现“注册器”的功能，这些类中必须声明一个与配置类同名的静态方法，而这一方法应当返回一个包含有属性配置项的关联数组。

当我们实例化了一个配置类的对象后，系统将自动循环搜索在 ``$registrars`` 中指定的类。
对于这些类而言，当其中包含有与该配置类同名的方法时，框架将调用这一方法，并将其返回的所有属性，如同上节所述的命名空间变量一样，并入到配置项中。

配置类举例如下::

    <?php namespace App\Config;
    
    use CodeIgniter\Config\BaseConfig;
    
    class MySalesConfig extends BaseConfig
    {
        public $target        = 100;
        public $campaign      = "Winter Wonderland";
        protected $registrars = [
            '\App\Models\RegionalSales';
        ];
    }

... 所关联的地区销售模型将如下所示::

    <?php namespace App\Models;
    
    class RegionalSales
    {
        public static function MySalesConfig()
        {
            return ['target' => 45, 'actual' => 72];
        }
    }

如上所示，当 `MySalesConfig` 被实例化后，它将以两个属性的被声明而结束，然而 `$target` 属性将会被 `RegionalSalesModel` 的注册器所覆盖，故而最终的配置属性为::


    $target = 45;
    $campaign = "Winter Wonderland";
