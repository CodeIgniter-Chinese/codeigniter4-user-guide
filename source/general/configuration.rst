################################
利用配置文件开始你的工作
################################

每一个项目，都需要一种方法来定义不同的全局配置项，而这一过程是通常通过配置文件来实现的。
而配置文件一般来说是通过声明一个类，而这个类将所有的配置项作为公开属性，从而实现这一配置过程。
不同于许多其他的框架，在CI4中，不需要访问某个类来修改你的配置项信息。
取而代之的是，你仅仅需要创建一个配置类的实例，从而轻而易举的实现配置流程。

访问配置文件
======================


你可以通过创建一个新的实例，来访问你的类中的配置文件。
所有的这些属性都是公开的，故而你可以像其他属性一样调用你的配置项::

	$config = new \Config\EmailConfig();
	
	// 像类属性一样调用配置项
	$protocol = $config->protocol;
	$mailpath = $config->mailpath;



若没有给出namespace(命名空间），框架会在所有可用的、已被定义的命名空间中搜寻所需的文件，就如同 **/application/Config/** 一样。
所以Codeigniter里所有的配置文件都应当在 ``Config`` 这一命名空间下。
由于框架可以确切地了解配置文件的目录位置，从而不必扫描文件系统中的不同区域。
故而在你的项目中，使用这一命名空间将会有效地提升性能。


你也可以通过使用一个不同的命名空间，从而在你的服务器的任意位置上部署所需的配置文件。
这一举措可以允许你将生产环境的服务器中的配置文件移动到一个不能通过Web访问的位置；而在开发环境中，将其放置在 **/application** 目录下以便访问。


创建配置文件
============================


当你需要创建一个新的配置文件时，你需要在指定位置创建一个新的文件，例如在默认的 **/aplication/Config** 目录下。然后创建一个带有公开属性的类，从而放置你的配置信息::


	<?php namespace Config;
	
	class App extends \CodeIgniter\Config\BaseConfig {
	
		public $siteName = 'My Great Site';
		public $siteEmail = 'webmaster@example.com';
		
	}

The class should extend ``\CodeIgniter\Config\BaseConfig`` to ensure that it can receive environment-specific
settings.
这个类应当继承 ``\CodeIgniter\Config\BaseConfig`` 从而保证框架可以得到具体环境中的配置信息。

面对不同的环境情况
===============================

Because your site can operate within multiple environments, such as the developer's local machine or
the server used for the production site, you can modify your values based on the environment.  Within these
you will have settings that might change depending on the server it's running on.This can include
database settings, API credentials, and other settings that will vary between deploys.

You can store values in a **.env** file in the root directory, alongside the system and application directories.
It is simply a collection of name/value pairs separated by an equal sign, much like a .ini file::

	S3_BUCKET="dotenv"
	SECRET_KEY="super_secret_key"

If the variable exists in the environment already, it will NOT be overwritten. 

.. important:: Make sure the **.env** file is added to **.gitignore** (or your version control system's equivalent)
	so it is not checked in the code. Failure to do so could result in sensitive credentials being stored in the
	repository for anyone to find.

You are encouraged to create a template file, like **env.example**, that has all of the variables your project
needs with empty or dummy data. In each environment, you can then copy the file to **.env** and fill in the
appropriate data.

When your application runs, this file will be automatically loaded and the variables will be put into
the environment. This will work in any environment except for production, where the variables should be
set in the environment through whatever means your getServer supports, such as .htaccess files, etc. These
variables are then available through ``getenv()``, ``$_SERVER``, and ``$_ENV``. Of the three, ``getenv()`` function
is recommended since it is not case-sensitive::

	$s3_bucket = getenv('S3_BUCKET');
	$s3_bucket = $_ENV['S3_BUCKET'];
	$s3_bucket = $_SERVER['S3_BUCKET'];

Nesting Variables
=================

To save on typing, you can reuse variables that you've already specified in the file by wrapping the
variable name within ``${...}``::

	BASE_DIR="/var/webroot/project-root"
	CACHE_DIR="${BASE_DIR}/cache"
	TMP_DIR="${BASE_DIR}/tmp" 


Namespaced Variables
====================

There will be times when you will have several variables of the same name. When this happens, the
system has no way of knowing what the correct value should be. You can protect against this by
"namespacing" the variables.

Namespaced variables use a dot notation to qualify variable names when those variables
get incorporated into configuration files. This is done by including a distinguishing
prefix, followed by a dot (.), and then the variable name itself::

    // not namespaced variables
    name = "George"
    db=my_db

    // namespaced variables
    address.city = "Berlin"
    address.country = "Germany"
    frontend.db = sales
    backend.db = admin
    BackEnd.db = admin

Incorporating Environment Variables Into a Configuration
========================================================

When you instantiate a configuration file, any namespaced environment variables
are considered for merging into the a configuration objects' properties.

If the prefix of a namespaced variable matches the configuration class name exactly,
case-sensitive, then the trailing part of the variable name (after the dot) is
treated as a configuration property name. If it matches an existing configuration
property, the environment variable's value will override the corresponding one
in the configuration file. If there is no match, the configuration properties are left unchanged.

The same holds for a "short prefix", which is the name given to the case when the
environment variable prefix matches the configuration class name converted to lower case.

Treating Environment Variables as Arrays
========================================

A namespaced environment variable can be further treated as an array.
If the prefix matches the configuration class, then the remainder of the 
environment variable name is treated as an array reference if it also
contains a dot::

    // regular namespaced variable
    SimpleConfig.name = George

    // array namespaced variables
    SimpleConfig.address.city = "Berlin"
    SimpleConfig.address.country = "Germany"

If this was referring to a SimpleConfig configuration object, the above example would be treated as:: 

    $address['city'] = "Berlin";
    $address['country'] = "Germany";

Any other elements of the ``$address`` property would be unchanged.

You can also use the array property name as a prefix. If the environment file
held instead::

    // array namespaced variables
    SimpleConfig.address.city = "Berlin"
    address.country = "Germany"

then the result would be the same as above.

Registrars
==========

A configuration file can also specify any number of "registrars", which are any 
other clases which might provide additional configuration properties.
This is done by adding a ``registrars`` property to your configuration file,
holding an array of the names of candidate registrars.::

    protected $registrars = [
        SupportingPackageRegistrar::class
    ];

In order to act as a "registrar" the classes so identified must have a
static function named the same as the configuration class, and it should return an associative
array of property settings.

When your configuration object is instantiated, it will loop over the 
designated classes in ``$registrars``. For each of these classes, which contains a method name matching
the configuration class, it will invoke that method, and incorporate any returned properties
the same way as described for namespaced variables.

A sample configuration class setup for this::

    namespace App\Config;
    class MySalesConfig extends \CodeIgniter\Config\BaseConfig {
        public $target = 100;
        public $campaign = "Winter Wonderland";
        protected $registrars = [
            '\App\Models\RegionalSales';
        ];
    }

... and the associated regional sales model might look like::

    namespace App\Models;
    class RegionalSales {   
        public static function MySalesConfig() {
            return ['target' => 45, 'actual' => 72];
        }
    }

With the above example, when `MySalesConfig` is instantiated, it will end up with
the two properties declared, but the value of the `$target` property will be over-ridden
by treating `RegionalSalesModel` as a "registrar". The resulting configuration properties::

    $target = 45;
    $campaign = "Winter Wonderland";

