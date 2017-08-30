################################
利用配置文件开始工作
################################

每一个项目，都需要一种方法来定义不同的全局配置项，而这通常是借助配置文件来实现的。
而配置文件，一般来说，是通过声明一个将所有的配置项作为公开属性的类，来实现这一配置过程的。
不同于许多其他的框架，在CI4中，不需要访问某个具体的类来修改我们的配置项信息。
取而代之的是，我们仅仅需要创建一个配置类的实例，从而轻而易举的实现配置流程。 

访问配置文件
======================

我们可以通过创建一个新的配置类实例，来访问类中的配置项。
配置类中所有的这些属性都是公开的，故而可以如调用其他属性一样调用相应的配置项::

	$config = new \Config\EmailConfig();
	
	// 如类属性一样调用配置项
	$protocol = $config->protocol;
	$mailpath = $config->mailpath;


若没有给定namespace(命名空间），框架会在所有可用的、已被定义的命名空间中搜寻所需的文件，就如同 **/application/Config/** 一样。
所以Codeigniter里所有的配置文件都应当被放置在 ``Config`` 这一命名空间下。
由于框架可以确切地了解配置文件所在目录的的位置，从而不必扫描文件系统中的不同区域；故而在我们的项目中，使用命名空间将会有效地提升性能。

我们也可以通过使用一个不同的命名空间，从而在服务器的任意位置上部署所需的配置文件。
这一举措可以让我们将生产环境的服务器中的配置文件移动到一个不能通过Web访问的位置；而在开发环境中，将其放置在 **/application** 目录下以便访问。

创建配置文件
============================


当我们需要创建一个新的配置文件时，需要在指定位置创建一个新的文件，例如在默认的 **/aplication/Config** 目录下。然后创建一个带有公开属性的类，从而放置相应的配置信息::


	<?php namespace Config;
	
	class App extends \CodeIgniter\Config\BaseConfig {
	
		public $siteName = 'My Great Site';
		public $siteEmail = 'webmaster@example.com';
		
	}



这个类应当继承 ``\CodeIgniter\Config\BaseConfig`` 从而保证框架可以得到具体环境下的配置信息。

针对不同的环境
===============================

由于我们的站点将会在不同的环境中运行，例如开发者的本地机器上，或是用于部署的远端服务器上，我们可以基于环境来修改配置信息。
在这基础上，我们将能够根据站点所运行的服务器，来使用不同的配置信息。这些包括并不限于数据库配置信息，API认证信息，以及其他的根据部署环境而改变的配置信息。

我们可以将这些值保存在根目录下的一个 **.env** 文件中，就如system和application目录一样。这个文件就如一个.ini配置文件一样，由许多对被等号分割的键/值对所组成::

	S3_BUCKET="dotenv"
	SECRET_KEY="super_secret_key"


当这些变量已经在环境中被定义时，它们将不会被重复定义。

.. important:: 确保 **.env** 类型的文件已经添加到 **.gitignore** （或是相同类型的其他版本控制系统）中，从而保证在代码中不会被上传。
    若这一举措未能成功，则可能会导致该目录中的相关敏感认证信息能够被任何人随意访问。

创建一个类似于 **.env.example** 的，其中包含了所有我们的项目所需的，仅设置了配置项的空值或默认值的模板文件，是一个不错的方法。
在不同的环境里，我们可以把这个文件复制到 **.env** 目录下并填充这个环境相对应的配置项的值。

当应用开始运行时，这个文件将会被自动加载，同时这些变量也会被运行环境所调用——这一过程适用于除生产环境外的其他环境的部署：在这些环境中变量应当被通过类似于.htaceess一样的文件所设置的getServer方法所支持。
在这之后，这些变量将通过 ``getenv()``, ``$_SERVER``, and ``$_ENV`` 的方式被调用。在这三者中， ``getenv()`` 方法由于其大小写不敏感而被推荐使用::

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


将环境变量并入配置中
========================================================
当实例化一个配置文件时，所有的命名空间中的环境变量都将会被并入到这个实例对象的属性中。

如果一个命名空间变量的前缀（以大小写敏感的方式）可以正确匹配到配置类的名称，那么这个变量名的剩余部分（点号后面的部分）将会被当做一个配置项属性。
如果这个变量能够匹配到一个已经存在的配置项属性，那么相对应的配置项属性值将会被覆盖。当没有匹配到时，配置项属性值将不会被更改。

对于”短前缀“而言也是如此，当环境变量的前缀匹配到一个被转换到小写的配置类名时，首字母也将被替换成相对应的大小写情况。


以数组的方式调用环境变量
========================================

从更长远的角度来看，一个命名空间环境变量也可以以数组的方式被调用。
如果一个命名空间环境变量的前缀与某个配置类所匹配，那么这个变量的剩余部分，若同样包含点号，则将会被当做一个数组的引用来调用::

    // 常规的命名空间变量
    SimpleConfig.name = George

    // 数组化的命名空间变量
    SimpleConfig.address.city = "Berlin"
    SimpleConfig.address.country = "Germany"


如果这个变量是对SimpleConfig配置类的成员的引用，上述例子将会如下图所示::

    $address['city'] = "Berlin";
    $address['country'] = "Germany";

而 ``$address`` 属性的其他部分将不会被改动。

我们同样可以将数组属性名作为前缀来使用，当配置文件如下所示时::

    // array namespaced variables
    SimpleConfig.address.city = "Berlin"
    address.country = "Germany"

结果与原来的相同

注册器
==========

一个配置文件可以指定任意数量的”注册器“；这里所指的注册器为其他类可能提供的额外的配置属性。
这一行为通常通过在配置文件中增加一个 ``registrars`` 属性来实现，这一属性存有一个可选的注册器数组。::

    protected $registrars = [
        SupportingPackageRegistrar::class
    ];

为了实现”注册器“的功能，这些类中必须声明一个与配置类同名的静态方法，而这一方法应当返回一个包含有属性配置项的关联数组。

当我们实例化了一个配置类的对象后，系统将自动循环搜索在 ``$registrars`` 中指定的类。
对于这些类而言，当其中包含有与该配置类同名的方法时，框架将调用这一方法，并将其返回的所有属性，如同上节所述的命名空间变量一样，并入到配置项中。

配置类举例如下::

    namespace App\Config;
    class MySalesConfig extends \CodeIgniter\Config\BaseConfig {
        public $target = 100;
        public $campaign = "Winter Wonderland";
        protected $registrars = [
            '\App\Models\RegionalSales';
        ];
    }

... 所关联的地区销售模型将如下所示::

    namespace App\Models;
    class RegionalSales {   
        public static function MySalesConfig() {
            return ['target' => 45, 'actual' => 72];
        }
    }

如上所示，当 `MySalesConfig` 被实例化后，它将以两个属性的被声明而结束，然而 `$target` 属性将会被 `RegionalSalesModel` 的注册器所覆盖，故而最终的配置属性为::


    $target = 45;
    $campaign = "Winter Wonderland";

