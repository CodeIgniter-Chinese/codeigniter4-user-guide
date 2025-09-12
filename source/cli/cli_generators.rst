##############
CLI 生成器
##############

CodeIgniter4 现在配备了生成器，可以简化创建标准控制器、模型、实体等文件的过程。你也可以通过一条命令搭建一整套文件。

.. contents::
    :local:
    :depth: 2

************
简介
************

当使用 ``php spark list`` 命令列出时，所有内置的生成器都位于 ``Generators`` 组下。要查看特定生成器的完整描述和用法信息，请使用以下命令：

.. code-block:: console

    php spark help <generator_command>

其中 ``<generator_command>`` 将替换为要检查的命令。

.. note:: 你需要将生成的代码放在子文件夹中吗？例如，如果你想创建一个位于主 ``Controllers`` 文件夹的 ``Admin`` 子文件夹中的控制器类，你只需在类名前加上子文件夹名称，如下所示：``php spark make:controller admin/login``。此命令将在 ``Controllers/Admin`` 子文件夹中创建 ``Login`` 控制器，并且命名空间为 ``App\Controllers\Admin``。

.. note:: 正在开发模块吗？代码生成会将根命名空间设置为默认的 ``APP_NAMESPACE``。如果你需要将生成的代码放在模块命名空间的其他位置，请确保在命令中设置 ``--namespace`` 选项，例如：``php spark make:model blog --namespace Acme\\Blog``。

.. warning:: 设置 ``--namespace`` 选项时，请确保提供的命名空间是在 ``Config\Autoload`` 的 ``$psr4`` 数组中定义的，或者在 Composer 的自动加载文件中定义的有效命名空间。否则，代码生成将被中断。

*******************
内置生成器
*******************

CodeIgniter4 默认附带以下生成器。

make:cell
---------

.. versionadded:: 4.3.0

创建一个新的 Cell 文件及其视图。

用法：
======
::

    make:cell <name> [options]

参数：
=========
* ``name``：Cell 类的名称。应该使用 PascalCase。 **[必需] **

选项：
========
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--force``：设置此标志以覆盖目标位置的现有文件。

make:command
------------

创建一个新的 spark 命令。

用法：
======
::

    make:command <name> [options]

参数：
=========
* ``name``：命令类的名称。 **[必需] **

选项：
========
* ``--command``：在 spark 中运行的命令名称。默认为 ``command:name``。
* ``--group``：命令的组/命名空间。基本命令默认为 ``App``，生成器命令默认为 ``Generators``。
* ``--type``：命令的类型，可以是 ``basic``（基本）命令或 ``generator``（生成器）命令。默认为 ``basic``。
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：将组件后缀附加到生成的类名上。
* ``--force``：设置此标志以覆盖目标位置的现有文件。

make:config
-----------

创建一个新的配置文件。

用法：
======
::

    make:config <name> [options]

参数：
=========
* ``name``：配置类的名称。 **[必需] **

选项：
========
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：将组件后缀附加到生成的类名上。
* ``--force``：设置此标志以覆盖目标位置的现有文件。

make:controller
---------------

创建一个新的控制器文件。

用法：
======
::

    make:controller <name> [options]

参数：
=========
* ``name``：控制器类的名称。 **[必需] **

选项：
========
* ``--bare``：从 ``CodeIgniter\Controller`` 而不是 ``BaseController`` 继承。
* ``--restful``：从 RESTful 资源继承。选项有 ``controller`` 和 ``presenter``。默认为 ``controller``。
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：将组件后缀附加到生成的类名上。
* ``--force``：设置此标志以覆盖目标位置的现有文件。

.. note:: 如果你使用 ``--suffix``，生成的控制器名称将类似于 ``ProductController``。这违反了使用 :ref:`自动路由 <controller-auto-routing-improved>` 时的控制器命名约定（控制器类名必须以大写字母开头，并且只有第一个字符可以是大写）。因此，当使用 :ref:`定义路由 <defined-route-routing>` 时，可以使用 ``--suffix``。

make:entity
-----------

创建一个新的实体文件。

用法：
======
::

    make:entity <name> [options]

参数：
=========
* ``name``：实体类的名称。 **[必需] **

选项：
========
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：将组件后缀附加到生成的类名上。
* ``--force``：设置此标志以覆盖目标位置的现有文件。

make:filter
-----------

创建一个新的过滤器文件。

用法：
======
::

    make:filter <name> [options]

参数：
=========
* ``name``：过滤器类的名称。 **[必需] **

选项：
========
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：将组件后缀附加到生成的类名上。
* ``--force``：设置此标志以覆盖目标位置的现有文件。

make:model
----------

创建一个新的模型文件。

用法：
======
::

    make:model <name> [options]

参数：
=========
* ``name``：模型类的名称。 **[必需] **

选项：
========
* ``--dbgroup``：要使用的数据库组。默认为 ``default``。
* ``--return``：设置返回类型，可选 ``array``、``object`` 或 ``entity``。默认为 ``array``。
* ``--table``：提供不同的表名。默认为类名的复数形式。
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：将组件后缀附加到生成的类名上。
* ``--force``：设置此标志以覆盖目标位置的现有文件。

make:seeder
-----------

创建一个新的数据填充文件。

用法：
======
::

    make:seeder <name> [options]

参数：
=========
* ``name``：数据填充类的名称。 **[必需] **

选项：
========
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：将组件后缀附加到生成的类名上。
* ``--force``：设置此标志以覆盖目标位置的现有文件。

.. _cli-generators-make-test:

make:test
-----------

.. versionadded:: 4.5.0

创建一个新的测试文件。

用法：
======
::

    make:test <name> [options]

参数：
=========
* ``name``：测试类的名称。 **[必需] **

选项：
========
* ``--namespace``：设置根命名空间。默认为 ``Tests`` 的值。
* ``--force``：设置此标志以覆盖目标位置的现有文件。

make:migration
--------------

创建一个新的迁移文件。

用法：
======
::

    make:migration <name> [options]

参数：
=========
* ``name``：迁移类的名称。 **[必需] **

选项：
========
* ``--session``：为数据库会话生成一个迁移文件。
* ``--table``：为数据库会话设置表名。默认为 ``ci_sessions``。
* ``--dbgroup``：为数据库会话设置数据库组。默认为 ``default`` 组。
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：将组件后缀附加到生成的类名上。
* ``--force``：设置此标志以覆盖目标位置的现有文件。

make:validation
---------------

创建一个新的验证文件。

用法：
======
::

    make:validation <name> [options]

参数：
=========
* ``name``：验证类的名称。 **[必需] **

选项：
========
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：将组件后缀附加到生成的类名上。
* ``--force``：设置此标志以覆盖目标位置的现有文件。

****************************************
搭建一整套标准代码
****************************************

有时在开发阶段，我们会按组创建功能，例如创建一个 *Admin* 组。这个组将包含它自己的控制器、模型、迁移文件，甚至实体。你可能会想在终端中逐个输入每个生成器命令，并希望有一个单一的生成器命令可以搞定一切。

不必再担心了！CodeIgniter4 还附带了一个专门的 ``make:scaffold`` 命令，它基本上是控制器、模型、实体、迁移和数据填充生成器命令的包装器。你只需要提供将用于命名所有生成类的类名。此外，每个生成器命令支持的 **独立选项** 也会被脚手架命令识别。

在终端中运行以下命令：

.. code-block:: console

    php spark make:scaffold user

将创建以下文件：

(1) **app/Controllers/User.php**
(2) **app/Models/User.php**
(3) **app/Database/Migrations/<日期>_User.php** 以及
(4) **app/Database/Seeds/User.php**

要将 ``Entity`` 类包含在搭建的文件中，只需在命令中包含 ``--return entity``，它将被传递给模型生成器。

**************
GeneratorTrait
**************

所有生成器命令都必须使用 ``GeneratorTrait`` 以充分利用其在代码生成中使用的方法。

*************************************************************
声明自定义生成器命令模板的位置
*************************************************************

查找生成器模板的默认顺序是：(1) 在 **app/Config/Generators.php** 文件中定义的模板，以及 (2) 如果未找到，则在 ``CodeIgniter\Commands\Generators\Views`` 命名空间中找到的模板。

要为你的自定义生成器命令声明模板位置，你需要将其添加到 **app/Config/Generators.php** 文件中。例如，如果你有一个 ``make:awesome-command`` 命令，并且你的生成器模板位于 *app* 目录内的 **app/Commands/Generators/Views/awesomecommand.tpl.php**，你应该像这样更新配置文件：

.. literalinclude:: cli_generators/001.php
