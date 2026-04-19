##############
CLI 生成器
##############

CodeIgniter4 现已配备生成器，可简化控制器、模型、实体等常用组件的创建工作。此外，仅需一条命令即可搭建全套关联文件。

.. contents::
    :local:
    :depth: 2

************
简介
************

使用 ``php spark list`` 列出命令时，所有内置生成器均归属于 ``Generators`` 组。若要查看特定生成器的完整说明和用法，请运行以下命令：

.. code-block:: console

    php spark help <generator_command>

其中 ``<generator_command>`` 需替换为待查询的命令。

.. note:: 需要将生成的代码存放在子目录中？例如，若要将控制器类放在主 ``Controllers`` 目录下的 ``Admin`` 子目录中，只需在类名前加上子目录名，例如：``php spark make:controller admin/login``。该命令将在 ``Controllers/Admin`` 子目录中创建 ``Login`` 控制器，其命名空间为 ``App\Controllers\Admin``。

.. note:: 正在开发模块？代码生成会将根命名空间默认设为 ``APP_NAMESPACE``。若需在模块命名空间的其他位置生成代码，请确保在命令中设置 ``--namespace`` 选项，例如：``php spark make:model blog --namespace Acme\\Blog``。

.. warning:: 设置 ``--namespace`` 选项时，请确保提供的命名空间已在 ``Config\Autoload`` 的 ``$psr4`` 数组或 Composer 自动加载文件中定义，否则代码生成过程将中断。

*******************
内置生成器
*******************

CodeIgniter4 默认包含以下生成器。

make:cell
---------

.. versionadded:: 4.3.0

创建新的 Cell 文件及其视图。

用法：
======
::

    make:cell <name> [options]

参数：
=========
* ``name``：Cell 类的名称。应使用 PascalCase 格式。**[必填]**

选项：
========
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--force``：设置此标志将覆盖目标位置的现有文件。

make:command
------------

创建新的 spark 命令。

用法：
======
::

    make:command <name> [options]

参数：
=========
* ``name``：命令类的名称。**[必填]**

选项：
========
* ``--command``：在 spark 中运行的命令名。默认为 ``command:name``。
* ``--group``：命令的分组/命名空间。基本命令默认为 ``App``，生成器命令默认为 ``Generators``。
* ``--type``：命令类型，可选值为 ``basic`` （基本）或 ``generator`` （生成器）。默认为 ``basic``。
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：在生成的类名后追加组件后缀。
* ``--force``：设置此标志将覆盖目标位置的现有文件。

make:config
-----------

创建新的配置文件。

用法：
======
::

    make:config <name> [options]

参数：
=========
* ``name``：配置类的名称。**[必填]**

选项：
========
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：在生成的类名后追加组件后缀。
* ``--force``：设置此标志将覆盖目标位置的现有文件。

make:controller
---------------

创建新的控制器文件。

用法：
======
::

    make:controller <name> [options]

参数：
=========
* ``name``：控制器类的名称。**[必填]**

选项：
========
* ``--bare``：继承自 ``CodeIgniter\Controller`` 而非 ``BaseController``。
* ``--restful``：继承自 RESTful 资源。可选值为 ``controller`` 和 ``presenter``。默认为 ``controller``。
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：在生成的类名后追加组件后缀。
* ``--force``：设置此标志将覆盖目标位置的现有文件。

.. note:: 使用 ``--suffix`` 选项后，生成的控制器名称如 ``ProductController``。这在使用 :ref:`自动路由 <controller-auto-routing-improved>` 时会违反控制器命名规范（控制器类名必须以大写字母开头，且 **仅有** 首字母可以大写）。因此，只有在使用 :ref:`定义路由 <defined-route-routing>` 时才建议使用 ``--suffix``。

make:entity
-----------

创建新的实体文件。

用法：
======
::

    make:entity <name> [options]

参数：
=========
* ``name``：实体类的名称。**[必填]**

选项：
========
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：在生成的类名后追加组件后缀。
* ``--force``：设置此标志将覆盖目标位置的现有文件。

make:filter
-----------

创建新的过滤器文件。

用法：
======
::

    make:filter <name> [options]

参数：
=========
* ``name``：过滤器类的名称。**[必填]**

选项：
========
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：在生成的类名后追加组件后缀。
* ``--force``：设置此标志将覆盖目标位置的现有文件。

make:model
----------

创建新的模型文件。

用法：
======
::

    make:model <name> [options]

参数：
=========
* ``name``：模型类的名称。**[必填]**

选项：
========
* ``--dbgroup``：要使用的数据库分组。默认为 ``default``。
* ``--return``：设置返回类型，可选值为 ``array``、``object`` 或 ``entity``。默认为 ``array``。
* ``--table``：指定不同的表名。默认为类名的复数形式。
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：在生成的类名后追加组件后缀。
* ``--force``：设置此标志将覆盖目标位置的现有文件。

make:seeder
-----------

创建新的数据填充文件。

用法：
======
::

    make:seeder <name> [options]

参数：
=========
* ``name``：数据填充类的名称。**[必填]**

选项：
========
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：在生成的类名后追加组件后缀。
* ``--force``：设置此标志将覆盖目标位置的现有文件。


.. _cli-generators-make-test:

make:test
-----------

.. versionadded:: 4.5.0

创建新的测试文件。

用法：
======
::

    make:test <name> [options]

参数：
=========
* ``name``：测试类的名称。**[必填]**

选项：
========
* ``--namespace``：设置根命名空间。默认为 ``Tests``。
* ``--force``：设置此标志将覆盖目标位置的现有文件。

make:transformer
----------------

创建新的 API Transformer 文件。

用法：
======
::

    make:transformer <name> [options]

参数：
=========
* ``name``：Transformer 类的名称。**[必填]**

选项：
========
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：在生成的类名后追加组件后缀。
* ``--force``：设置此标志将覆盖目标位置的现有文件。

make:migration
--------------

创建新的迁移文件。

用法：
======
::

    make:migration <name> [options]

参数：
=========
* ``name``：迁移类的名称。**[必填]**

选项：
========
* ``--session``：为数据库 Session 生成迁移文件。
* ``--table``：设置用于数据库 Session 的表名。默认为 ``ci_sessions``。
* ``--dbgroup``：设置数据库 Session 使用的数据库分组。默认为 ``default``。
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：在生成的类名后追加组件后缀。
* ``--force``：设置此标志将覆盖目标位置的现有文件。

make:validation
---------------

创建新的验证文件。

用法：
======
::

    make:validation <name> [options]

参数：
=========
* ``name``：验证类的名称。**[必填]**

选项：
========
* ``--namespace``：设置根命名空间。默认为 ``APP_NAMESPACE`` 的值。
* ``--suffix``：在生成的类名后追加组件后缀。
* ``--force``：设置此标志将覆盖目标位置的现有文件。

****************************************
搭建全套标准代码
****************************************

在开发阶段，有时会按组（例如 *Admin* 组）创建功能。此类功能通常包含专属的控制器、模型、迁移文件甚至实体。如果觉得逐一运行生成器命令太繁琐，希望能有一条命令搞定一切。

现在可以如愿以偿了！CodeIgniter4 提供了专属的 ``make:scaffold`` 命令，该命令实质上是控制器、模型、实体、迁移和数据填充生成器命令的封装。只需提供一个类名，即可据此命名所有生成的类。此外，scaffold 命令也支持各生成器命令所拥有的 **所有独立选项**。

在终端中运行以下命令：

.. code-block:: console

    php spark make:scaffold user

将创建以下文件：

(1) **app/Controllers/User.php**
(2) **app/Models/User.php**
(3) **app/Database/Migrations/<日期>_User.php** 以及
(4) **app/Database/Seeds/User.php**

若要在搭建的文件中包含 ``Entity`` 类，只需在命令中添加 ``--return entity``，该选项会透传给模型生成器。

**************
GeneratorTrait
**************

所有生成器命令必须使用 ``GeneratorTrait``，以便充分利用代码生成相关的各种方法。

*************************************************************
声明自定义生成器命令模板的位置
*************************************************************

生成器模板的默认查找顺序如下：(1) **app/Config/Generators.php** 文件中定义的模板；(2) 若未找到，则在 ``CodeIgniter\Commands\Generators\Views`` 命名空间下查找。

若要为自定义生成器命令声明模板位置，需将其添加到 **app/Config/Generators.php** 文件中。例如，若有一个 ``make:awesome-command`` 命令，且生成器模板位于 *app* 目录下的 **app/Commands/Generators/Views/awesomecommand.tpl.php**，则需按如下方式更新配置文件：

.. literalinclude:: cli_generators/001.php
