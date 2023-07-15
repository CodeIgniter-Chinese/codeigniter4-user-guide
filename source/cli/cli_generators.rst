##############
CLI 生成器
##############

CodeIgniter4 现在配备了生成器,以简化常规控制器、模型、实体等的创建。您还可以使用一个命令搭建一整套完整的文件。

.. contents::
    :local:
    :depth: 2

************
简介
************

所有内置生成器在使用 ``php spark list`` 列出时都位于 ``Generators`` 组下。
要查看特定生成器的完整描述和使用信息,请使用命令::

    > php spark help <生成器命令>

其中 ``<生成器命令>`` 将替换为要检查的命令。

.. note:: 您需要在子文件夹中生成代码吗?例如,如果您想在主 ``Controllers`` 文件夹的 ``Admin`` 子文件夹中创建一个控制器类,您只需要在类名前加上子文件夹,像这样:``php spark make:controller admin/login``。这个命令将在 ``Controllers/Admin`` 子文件夹中创建 ``Login`` 控制器,命名空间为 ``App\Controllers\Admin``。

.. note:: 在模块上工作?代码生成将根命名空间默认设置为 ``APP_NAMESPACE``。如果需要在模块命名空间的其他位置生成代码,请确保在命令中设置 ``--namespace`` 选项,例如 ``php spark make:model blog --namespace Acme\\Blog``。

.. warning:: 设置 ``--namespace`` 选项时,请确保提供的命名空间是在 ``Config\Autoload`` 中的 ``$psr4`` 数组或您的 composer 自动加载文件中定义的有效命名空间。否则,代码生成将中断。

.. important:: 从 v4.0.5 开始,使用 ``migrate:create`` 创建迁移文件已被弃用。它将在未来版本中删除。请使用 ``make:migration`` 作为替代。另外,请使用 ``make:migration --session`` 来代替已弃用的 ``session:migration``。

*******************
内置生成器
*******************

CodeIgniter4 默认附带以下生成器。

make:cell
---------

.. versionadded:: 4.3.0

创建一个新的 Cell 文件及其视图。

用法:
======
::

    make:cell <名称> [选项]

参数:
=========
* ``名称``:单元类的名称。应为 PascalCase。**[必需]**

选项:
========
* ``--namespace``:设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--force``:设置此标志以覆盖目标上的现有文件。

make:command
------------

创建一个新的 spark 命令。

用法:
======
::

    make:command <名称> [选项]

参数:
=========
* ``名称``:命令类的名称。**[必需]**

选项:
========
* ``--command``:在 spark 中运行的命令名称。默认为 ``command:name``。
* ``--group``:命令的组/命名空间。对于基本命令默认为 ``CodeIgniter``,对于生成器命令默认为 ``Generators``。
* ``--type``:命令类型,可以是 ``basic`` 基本命令或 ``generator`` 生成器命令。默认为 ``basic``。
* ``--namespace``:设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``:在生成的类名后附加组件后缀。
* ``--force``:设置此标志以覆盖目标上的现有文件。

make:config
-----------

创建一个新的配置文件。

用法:
======
::

    make:config <名称> [选项]

参数:
=========
* ``名称``:配置类的名称。**[必需]**

选项:
========
* ``--namespace``:设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``:在生成的类名后附加组件后缀。
* ``--force``:设置此标志以覆盖目标上的现有文件。

make:controller
---------------

创建一个新的控制器文件。

用法:
======
::

    make:controller <名称> [选项]

参数:
=========
* ``名称``:控制器类的名称。**[必需]**

选项:
========
* ``--bare``:扩展自 ``CodeIgniter\Controller`` 而不是 ``BaseController``。
* ``--restful``:扩展自一个 RESTful 资源。可选 ``controller`` 和 ``presenter``。默认为 ``controller``。
* ``--namespace``:设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``:在生成的类名后附加组件后缀。
* ``--force``:设置此标志以覆盖目标上的现有文件。

.. note:: 如果使用 ``--suffix``,生成的控制器名称将类似于 ``ProductController``。这与使用 :ref:`自动路由 <controller-auto-routing-improved>` 的控制器命名约定相违背(控制器类名必须以大写字母开头,且只能大写第一个字符)。所以 ``--suffix`` 可与 :ref:`定义路由 <defined-route-routing>` 一起使用。

make:entity
-----------

创建一个新的实体文件。

用法:
======
::

    make:entity <名称> [选项]

参数:
=========
* ``名称``:实体类的名称。**[必需]**

选项:
========
* ``--namespace``:设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``:在生成的类名后附加组件后缀。
* ``--force``:设置此标志以覆盖目标上的现有文件。

make:filter
-----------

创建一个新的过滤器文件。

用法:
======
::

    make:filter <名称> [选项]

参数:
=========
* ``名称``:过滤器类的名称。**[必需]**

选项:
========
* ``--namespace``:设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``:在生成的类名后附加组件后缀。
* ``--force``:设置此标志以覆盖目标上的现有文件。

make:model
----------

创建一个新的模型文件。

用法:
======
::

    make:model <名称> [选项]

参数:
=========
* ``名称``:模型类的名称。**[必需]**

选项:
========
* ``--dbgroup``:要使用的数据库组。默认为 ``default``。
* ``--return``:设置返回类型,可以是 ``array``、``object`` 或 ``entity``。默认为 ``array``。
* ``--table``:提供不同的表名。默认为将类名复数化。
* ``--namespace``:设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``:在生成的类名后附加组件后缀。
* ``--force``:设置此标志以覆盖目标上的现有文件。

make:seeder
-----------

创建一个新的种子文件。

用法:
======
::

    make:seeder <名称> [选项]

参数:
=========
* ``名称``:种子类的名称。**[必需]**

选项:
========
* ``--namespace``:设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``:在生成的类名后附加组件后缀。
* ``--force``:设置此标志以覆盖目标上的现有文件。

make:migration
--------------

创建一个新的迁移文件。

用法:
======
::

    make:migration <名称> [选项]

参数:
=========
* ``名称``:迁移类的名称。**[必需]**

选项:
========
* ``--session``:为数据库会话生成迁移文件。
* ``--table``:设置数据库会话的表名。默认为 ``ci_sessions``。
* ``--dbgroup``:设置数据库会话的数据库组。默认为 ``default`` 组。
* ``--namespace``:设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``:在生成的类名后附加组件后缀。
* ``--force``:设置此标志以覆盖目标上的现有文件。

make:validation
---------------

创建一个新的验证文件。

用法:
======
::

    make:validation <名称> [选项]

参数:
=========
* ``名称``:验证类的名称。**[必需]**

选项:
========
* ``--namespace``:设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``:在生成的类名后附加组件后缀。
* ``--force``:设置此标志以覆盖目标上的现有文件。

****************************************
搭建一整套完整的代码
****************************************

在开发阶段,我们有时会分组创建功能,比如创建一个 *Admin* 组。该组将包含自己的控制器、模型、迁移文件,甚至实体。您可能会想一一在终端中输入每个生成器命令,并希望有一个单一的生成器命令可以统治一切。

不要担心!CodeIgniter4 还配备了专用的 ``make:scaffold`` 命令,它基本上是控制器、模型、实体、迁移和种子生成器命令的包装器。您只需要输入用于命名所有生成类的类名。另外,**每个生成器命令支持的单独选项** 也会被脚手架命令识别。

在终端中运行此命令::

    > php spark make:scaffold user

将创建以下文件:

(1) **app/Controllers/User.php**
(2) **app/Models/User.php**
(3) **app/Database/Migrations/<某日期>_User.php** 和
(4) **app/Database/Seeds/User.php**

要在生成的文件中包含 ``Entity`` 类,只需在命令中包含 ``--return entity`` 选项即可将其传递给模型生成器。

**************
GeneratorTrait
**************

所有生成器命令必须使用 ``GeneratorTrait`` 以充分利用其在代码生成中使用的方法。

*************************************************************
声明自定义生成器命令模板的位置
*************************************************************

生成器模板的默认查找顺序是 (1) **app/Config/Generators.php** 文件中定义的模板,如果未找到,则是 (2) 在 ``CodeIgniter\Commands\Generators\Views`` 命名空间下找到的模板。

要为自定义生成器命令声明模板位置,需要将其添加到 **app/Config/Generators.php** 文件中。例如,如果您有一个命令 ``make:awesome-command``,并且生成器模板位于 *app* 目录 **app/Commands/Generators/Views/awesomecommand.tpl.php** 中,则需要按如下方式更新配置文件:

.. literalinclude:: cli_generators/001.php
