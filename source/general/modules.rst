############
代码模块
############

CodeIgniter 支持代码模块化组合，以便于你构建可重用的代码。模块通常来说是以一个特定主题为中心而构建的，并可被认为是在大型的程序中的一系列微型程序。
我们支持框架中所有标准的文件类型，例如控制器，模型，视图，配置文件，辅助函数，语言文件等。模块可能包含着或多或少的你所需要的以上这些类型中。

.. contents::
    :local:
    :depth: 2

==========
命名空间
==========

CodeIgniter所使用的模块功能的核心组件来自于 :doc:`与PSR4相适应的自动加载 </concepts/autoloader>` 。
虽然所有的代码都可以使用PSR4的自动加载和命名空间，最主要的充分使用模块优势的方式还是为你的代码加上命名空间，并将其添加到 **app/Config/Autoload.php** 中，在 ``psr4`` 这节中。

举例而言，比如我们需要维护一个在应用间复用的简单的博客模块。我们可能会创建一个带有公司名（比如acme）的文件夹来保存所有的模块。
我们可能会将其置于我们的 **application** 目录旁边，在主项目目录下::

    /acme        // 新的模块目录
    /application
    /public
    /system
    /tests
    /writable

打开 **app/Config/Autoload.php** 并将 **Acme** 命名空间加入到 ``psr4`` 数组成员中::

    $psr4 = [
        'Config'        => APPPATH . 'Config',
        APP_NAMESPACE   => APPPATH,                // 自定义命名空间
        'App'           => APPPATH,                // 确保筛选器等组件可找到,
        'Acme'          => ROOTPATH.'acme'
    ];

当我们设置完以上流程后，就可以通过 ``Acme`` 命名空间来访问 **acme** 目录下的文件夹内容。这已经完成了80%的模块工作所需要的内容，
所以你可以通过熟悉命名空间来适应这种使用方式。这样多种文件类型将会被自动扫描并在整个定义的命名空间中使用——这也是使用模块的关键。

在模块中的常见目录结构和主程序目录类似::

    /acme
        /Blog
            /Config
            /Controllers
            /Database
                /Migrations
                /Seeds
            /Helpers
            /Language
                /en
            /Libraries
            /Models
            /Views

当然了，不强制使用这样的目录结构，你也可以自定义目录结构来更好地符合你的模块要求，去掉那些你不需要的目录并增加一些新的目录，例如实体（Entites），接口（Interfaces），仓库（Repository）等。

==============
自动发现
==============

很多情况下，你需要指名你所需要包含进来的文件的命名空间全称，但是CodeIgniter可以通过配置自动发现的文件类型，来将模块更方便地整合进你的项目中:

- :doc:`Events </extending/events>`
- :doc:`Registrars </general/configuration>`
- :doc:`Route files </incoming/routing>`
- :doc:`Services </concepts/services>`

这些是在 **app/Config/Modules.php** 文件中配置的。

自动发现系统通过扫描所有在 **Config/Autoload.php** 中定义的PSR4类型的命名空间来实现对于目录/文件的识别。

To make auto-discovery work for our **Blog** namespace, we need to make one small adjustment.
**Acme** needs to be changed to **Acme\\Blog** because each "module" within the namespace needs to be fully defined. Once your module folder path is defined, the discovery process would look for discoverable items on that path and should, for example, find the routes file at **/acme/Blog/Config/Routes.php**.

开启/关闭自动发现
=======================

你可以开启或关闭所有的系统中的自动发现，通过 **$enabled** 类变量。False的话就会关闭所有的自动发现，优化性能，但却会让你的模块可用性相对下降。

明确目录项目
=======================

通过 **$activeExplorers** 选项，你可以明确哪些项目是自动发现的。如果这个项目不存在，就不会对它进行自动发现流程，而数组中的其他成员仍旧会被自动发现。

自动发现与Composer
======================

通过Composer安装的包将会默认被自动发现。这只需要Composer识别所需要加载的命名空间是符合PSR4规范的命名空间，PSR0类型的命名空间将不会被发现。

如果在定位文件时，你不想扫描所有Composer已识别的的目录，可以通过编辑 ``Config\Modules.php`` 中的 ``$discoverInComposer`` 变量来关闭这一功能::

    public $discoverInComposer = false;

==================
处理文件
==================

这节将会详细介绍每种文件类型（控制器，视图，语言文件等）以及在模块中如果使用它们。其中的某些信息在用户手册中将会更为详细地描述，不过在这里重新介绍一下以便了解全局的情况。

路由
======

默认情况下， :doc:`路由 </incoming/routing>` 将会在模块内部自动扫描，而这一特性可在 **Modules** 配置文件中被关闭，如上所述。

.. note:: 由于在当前域内包含了路由文件， ``$routes`` 实例已经被定义了，所以当你尝试重新定义类的时候可能会引起错误。

控制器
===========

在主 **app/Controller** 目录下定义的控制器不会自动被URI路由自动调用，所以需要在路由文件内部手动声明::

    // Routes.php
    $routes->get('blog', 'Acme\Blog\Controllers\Blog::index');

为了减少不必要的输入， **group** 路由特性（译者注： `分组路由 </incoming/routing#分组路由>` ）是一个不错的选择::

    $routes->group('blog', ['namespace' => 'Acme\Blog\Controllers'], function($routes)
    {
        $routes->get('/', 'Blog::index');
    });

配置文件
============

No special change is needed when working with configuration files. These are still namespaced classes and loaded
with the ``new`` command::

    $config = new \Acme\Blog\Config\Blog();

Config files are automatically discovered whenever using the **config()** function that is always available.

迁移
==========

迁移文件将通过定义的命名空间自动发现。所有命名空间里找到的迁移每次都会被自动运行。

种子
=====

种子文件可在CLI或其他种子文件里使用，只要提供了完整的命名空间名。如果通过CLI调用，就需要提供双反斜杠定义的类名格式(\\)::

    > php public/index.php migrations seed Acme\\Blog\\Database\\Seeds\\TestPostSeeder

辅助函数
==========

当使用 ``helper()`` 方法时，辅助函数将会通过定义的命名空间自动定位。只要它存在于 **Helpers** 命名空间目录下::

    helper('blog');

语言文件
==============

当使用 ``lang()`` 方法时，语言文件是通过定义的命名空间来自动定位的。只要这个文件是遵循主程序目录一样的目录结构来放置的。

库
=========

库总是通过完全命名空间化的类名进行实例化，所以不需要额外的操作::

    $lib = new \Acme\Blog\Libraries\BlogLib();

模型
======

模型总是通过完全命名空间化的类名进行实例化，所以不需要额外的操作::

    $model = new \Acme\Blog\Models\PostModel();

视图
=====

视图文件可通过 :doc:`视图 </outgoing/views>` 文档中所述的类命名空间进行加载::

    echo view('Acme\Blog\Views\index');
