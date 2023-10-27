#################
自动加载文件
#################

.. contents::
    :local:
    :depth: 2

每个应用程序由许多不同位置的大量类组成。
框架为核心功能提供类。你的应用程序将具有许多库、模型和其他实体才能正常工作。你可能会使用第三方类。跟踪每个文件的位置,并在一系列 ``require()`` 中硬编码该位置是一个巨大的头疼且极易出错。这就是自动加载器的用武之地。

CodeIgniter4 自动加载器
***********************

CodeIgniter 提供了一个非常灵活的自动加载器,可以通过非常少的配置即可使用。
它可以定位遵循 `PSR-4 <https://www.php-fig.org/psr/psr-4/>`_
自动加载目录结构的单个命名空间类。

自动加载器本身工作良好,但也可以与其他自动加载器(如 `Composer <https://getcomposer.org>`_)一起使用,如果需要的话,甚至可以与你自己的自定义自动加载器一起使用。
因为它们都通过 `spl_autoload_register <https://www.php.net/manual/en/function.spl-autoload-register.php>`_ 注册,所以它们顺序工作,不会相互干扰。

自动加载器始终处于活动状态,在框架执行开始时通过 ``spl_autoload_register()`` 注册。

.. important:: 你应该始终小心文件名的大小写。许多开发人员在 Windows 或 macOS 上使用不区分大小写的文件系统开发。
    然而,大多数服务器环境使用区分大小写的文件系统。如果文件名大小写不正确,自动加载程序无法在服务器上找到该文件。

配置
*************

初始配置在 **app/Config/Autoload.php** 中完成。该文件包含两个主要数组:一个用于类映射,一个用于 PSR-4 兼容命名空间。

命名空间
**********

组织类的推荐方法是为应用程序文件创建一个或多个命名空间。这对于任何业务逻辑相关的类、实体类等尤为重要。配置文件中的 ``$psr4`` 数组允许你将命名空间映射到可以找到这些类的目录:

.. literalinclude:: autoloader/001.php

每行的键是命名空间本身。这个不需要尾部反斜杠。
值是可以找到类的目录位置。

.. note:: 你可以使用 ``spark namespaces`` 命令检查命名空间配置:

    .. code-block:: console

        php spark namespaces

默认情况下,应用程序目录被映射到 ``App`` 命名空间。你必须为应用程序目录中的控制器、库或模型添加命名空间,它们将在 ``App`` 命名空间下被找到。

你可以通过编辑 **app/Config/Constants.php** 文件并在 ``APP_NAMESPACE`` 设置下设置新的命名空间值来更改此命名空间:

.. literalinclude:: autoloader/002.php
   :lines: 2-

你需要修改引用当前命名空间的所有现有文件。

.. important:: 配置文件使用 ``Config`` 命名空间,而不是你可能期望的 ``App\Config``。这使得核心系统文件总是能够定位它们,即使应用程序命名空间已更改。

类映射
********

CodeIgniter 通过不通过文件系统进行额外的 ``is_file()`` 调用来获取系统最后的性能,广泛使用类映射。你可以使用类映射链接到未使用命名空间的第三方库:

.. literalinclude:: autoloader/003.php

每行的键是你要定位的类的名称。值是定位它的路径。

Composer 支持
****************

默认情况下会自动初始化 Composer 支持。默认情况下,它会在 ``ROOTPATH . 'vendor/autoload.php'`` 查找 Composer 的自动加载文件。如果由于任何原因需要更改该文件的位置,可以修改 **app/Config/Constants.php** 中定义的值。

.. note:: 如果同一命名空间在 CodeIgniter 和 Composer 中都有定义,则 CodeIgniter 的自动加载器将首先获取定位该文件的机会。
