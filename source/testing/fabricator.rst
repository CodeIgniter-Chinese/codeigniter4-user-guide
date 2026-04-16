####################
生成测试数据
####################

开发应用时，经常需要样本数据来运行测试。``Fabricator`` 类
借助 `Faker <https://github.com/FakerPHP/Faker>`_ 将模型转化为随机数据生成器。
可在 Seed 文件或测试用例中使用 Fabricator 来生成模拟数据，用于单元测试。

.. contents::
    :local:
    :depth: 2

支持的模型
================

``Fabricator`` 支持任何继承自框架核心模型 ``CodeIgniter\Model`` 的模型。
如需使用自定义模型，确保其实现了 ``CodeIgniter\Test\Interfaces\FabricatorModel`` 接口即可：

.. literalinclude:: fabricator/001.php

.. note:: 除方法外，该接口还定义了一些目标模型所需的属性。详见接口源码。

加载 Fabricator
===================

最基本的用法是传入要操作的模型：

.. literalinclude:: fabricator/002.php

参数可以是指定模型名称的字符串，也可以是模型实例：

.. literalinclude:: fabricator/003.php

定义格式化器
===================

Faker 通过格式化器来生成数据。未指定格式化器时，``Fabricator`` 会
根据字段名和模型属性自动推测最合适的格式化器，
若推测失败则回退到 ``$fabricator->defaultFormatter``。
如果字段名恰好对应常见格式化器，或者不关心字段内容，自动推测可能够用，
但多数情况下需要通过构造函数的第二个参数明确指定：

.. literalinclude:: fabricator/004.php

也可以在 Fabricator 初始化后通过 ``setFormatters()`` 方法更改格式化器。

高级格式化
-------------------

有时格式化器的默认返回值并不够用。Faker Provider 的大多数格式化器都支持接收参数，从而进一步缩小随机数据的生成范围。Fabricator 会检查关联模型中是否定义了 ``fake()`` 方法，以便在该方法中精确定义模拟数据的格式：

.. literalinclude:: fabricator/005.php

在此示例中，前三个值与先前的格式化器完全等效。但 ``avatar`` 请求了非默认的图像尺寸，``login`` 则根据应用配置使用了条件逻辑，这两项需求均无法通过 ``$formatters`` 参数实现。

为了将测试数据与生产模型分离，最佳实践是在测试支持目录中定义一个子类：

.. literalinclude:: fabricator/006.php

设置修饰器
=================

.. versionadded:: 4.5.0

Faker 提供三个特殊 Provider ``unique()``、``optional()`` 和 ``valid()``，
可在任何 Provider 之前调用。Fabricator 通过专用方法完全支持这些修饰器。

.. literalinclude:: fabricator/022.php

字段名之后的参数会原样传递给修饰器。详见 `Faker 修饰器文档`_。

.. _Faker 修饰器文档: https://fakerphp.github.io/#modifiers

除了调用 Fabricator 的方法外，如果模型使用了 ``fake()`` 方法，
也可以直接使用 Faker 的修饰器。

.. literalinclude:: fabricator/023.php

本地化
============

Faker 支持多种语言环境。查阅 Faker 文档了解哪些 Provider 支持所需语言环境。
初始化 Fabricator 时，通过第三个参数指定语言环境：

.. literalinclude:: fabricator/007.php

未指定语言环境时，将使用 **app/Config/App.php** 中 ``defaultLocale`` 定义的值。
可通过现有 Fabricator 的 ``getLocale()`` 方法检查其语言环境。

生成模拟数据
===============

正确初始化 Fabricator 后，使用 ``make()`` 命令即可轻松生成测试数据：

.. literalinclude:: fabricator/008.php

返回值可能如下：

.. literalinclude:: fabricator/009.php

传入数量参数可批量生成：

.. literalinclude:: fabricator/010.php

``make()`` 的返回类型与模型定义的保持一致，也可以通过对应方法强制指定类型：

.. literalinclude:: fabricator/011.php

``make()`` 的返回值可直接用于测试或手动插入数据库。此外，``Fabricator`` 提供的 ``create()`` 方法可自动执行插入操作并返回结果。由于受模型回调、数据库格式化以及主键、时间戳等特殊字段的影响，``create()`` 的返回值可能与 ``make()`` 有所不同。返回结果示例如下：

.. literalinclude:: fabricator/012.php

与 ``make()`` 类似，可传入数量参数来批量执行插入并返回对象数组：

.. literalinclude:: fabricator/013.php

最后，若需在不实际使用数据库的情况下，使用完整的数据库对象进行测试，可为 ``create()`` 传入第二个参数来 Mock 对象。该操作无需访问数据库，即可返回包含上述额外数据库字段的对象：

.. literalinclude:: fabricator/014.php

指定测试数据
====================

自动生成的数据固然方便，但有时需要在测试中为特定字段指定数值，同时又不希望改动原有的格式化器配置。无需为每种变体重复创建 Fabricator，通过 ``setOverrides()`` 方法即可为任意字段指定覆盖值：

.. literalinclude:: fabricator/015.php

现在使用 ``make()`` 或 ``create()`` 生成的任何数据，``first`` 字段始终为 "Bobby"：

.. literalinclude:: fabricator/016.php

``setOverrides()`` 接受第二个参数，用于指定该覆盖是持久的还是仅单次生效：

.. literalinclude:: fabricator/017.php

注意第一次返回后 Fabricator 就不再使用覆盖值：

.. literalinclude:: fabricator/018.php

未传入第二个参数时，默认覆盖值会持续生效。

测试辅助函数
============

很多时候测试只需要一个一次性的模拟对象。测试辅助函数提供
``fake($model, $overrides, $persist = true)`` 函数来实现此功能：

.. literalinclude:: fabricator/019.php

等价于：

.. literalinclude:: fabricator/020.php

如果只需要模拟对象而不想保存到数据库，可将 ``persist`` 参数设为 false。

表计数
============

模拟数据之间往往存在依赖关系。``Fabricator`` 针对每张表维护了已生成模拟数据总数的静态计数。

以“用户与组”的关系为例：若测试场景中需要创建不同规模的分组，可先利用 ``Fabricator`` 生成一批分组。随后在创建模拟用户时，为确保关联到有效的组 ID，可在模型的 ``fake()`` 方法中按如下方式编写：

.. literalinclude:: fabricator/021.php

此时创建新用户即可确保其属于有效分组：``$user = fake(UserModel::class);``

方法
-------

``Fabricator`` 内部管理计数，同时提供以下静态方法
方便使用：

getCount(string $table): int
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

返回指定表的当前计数值（默认：0）。

setCount(string $table, int $count): int
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

手动设置指定表的计数值，例如创建了一些未通过 Fabricator 生成的
测试条目，但仍想将其计入总数。

upCount(string $table): int
^^^^^^^^^^^^^^^^^^^^^^^^^^^

将指定表的计数加一并返回新值。（``Fabricator::create()`` 内部使用此方法）。

downCount(string $table): int
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

将指定表的计数减一并返回新值，例如删除了某个模拟条目
但又想追踪此变更。

resetCounts()
^^^^^^^^^^^^^

重置所有计数。建议在测试用例之间调用（如果设置了
``CIUnitTestCase::$refresh = true`` 则会自动调用）。
