####################
生成测试数据
####################

测试应用程序的时候,你经常需要一些示例数据。``Fabricator`` 类使用 fzaninotto 的 `Faker <https://github.com/FakerPHP/Faker>`_ 将模型转化为随机数据生成器。在种子文件或测试用例中使用 fabricator 来准备假数据用于单元测试。

.. contents::
    :local:
    :depth: 2

支持的模型
================

``Fabricator`` 支持任何扩展框架核心模型 ``CodeIgniter\Model`` 的模型。你可以通过确保自己的自定义模型实现 ``CodeIgniter\Test\Interfaces\FabricatorModel`` 接口来使用它们:

.. literalinclude:: fabricator/001.php

.. note:: 除了方法之外,接口还概述了目标模型所需的一些必要属性。请参阅接口代码以获取详细信息。

加载 Fabricator
===================

最基本的 fabricator 只需要模型进行操作:

.. literalinclude:: fabricator/002.php

参数可以是指定模型名称的字符串,也可以是模型实例本身:

.. literalinclude:: fabricator/003.php

定义 Formatter
===================

Faker 通过从 formatter 请求数据来生成数据。如果没有定义 formatter, ``Fabricator`` 将尝试根据字段名称和它所表示的模型的属性来猜测最合适的匹配,如果找不到则回退到 ``$fabricator->defaultFormatter``。如果字段名称与常用 formatter 对应,或者你不太关心字段的内容,这可能就可以了,但大多数情况下你会想指定要使用的 formatter,可以将它们作为构造函数的第二个参数:

.. literalinclude:: fabricator/004.php

你也可以在初始化 fabricator 后使用 ``setFormatters()`` 方法更改 formatter。

高级格式化
-------------------

有时 formatter 的默认返回值是不够的。Faker 提供者允许大多数 formatter 使用参数来进一步限制随机数据的范围。fabricator 将检查其代表模型的 ``fake()`` 方法,在其中你可以定义伪造的数据应该是什么样的:

.. literalinclude:: fabricator/005.php

请注意,在这个例子中,前三个值等效于之前的 formatter。但是对于 ``avatar`` 我们请求了与默认不同的图像大小, ``login`` 使用基于应用配置的条件,这两者在使用 ``$formatters`` 参数时都是不可能的。
你可能希望将测试数据与生产模型分开,所以最好是在测试支持文件夹中定义一个子类:

.. literalinclude:: fabricator/006.php

本地化
============

Faker 支持许多不同的语言环境。请查看其文档以确定哪些提供程序支持你的语言环境。在初始化 fabricator 时,可以在第三个参数中指定语言环境:

.. literalinclude:: fabricator/007.php

如果未指定语言环境,它将使用在 **app/Config/App.php** 中定义为 ``defaultLocale`` 的语言环境。
你可以使用其 ``getLocale()`` 方法查看现有 fabricator 的语言环境。

伪造数据
===============

正确初始化 fabricator 后,使用 ``make()`` 命令生成测试数据很容易:

.. literalinclude:: fabricator/008.php

你可能会得到这样的返回:

.. literalinclude:: fabricator/009.php

你也可以通过提供数量来获取更多数据:

.. literalinclude:: fabricator/010.php

``make()`` 的返回类型模拟代表模型中定义的类型,但你可以使用方法直接强制类型:

.. literalinclude:: fabricator/011.php

``make()`` 的返回可在测试中使用或插入到数据库中。另一方面, ``Fabricator`` 包含 ``create()`` 命令可以帮你插入,并返回结果。由于模型回调、数据库格式化和特殊键(如主键和时间戳), ``create()`` 的返回可能与 ``make()`` 不同。你可能会得到这样的返回:

.. literalinclude:: fabricator/012.php

与 ``make()`` 类似,你可以提供数量来插入和返回对象数组:

.. literalinclude:: fabricator/013.php

最后,有时你可能希望使用完整的数据库对象进行测试,但实际上你没有使用数据库。``create()`` 的第二个参数允许模拟对象,在不实际接触数据库的情况下返回带有额外数据库字段的对象:

.. literalinclude:: fabricator/014.php

指定测试数据
====================

生成的数据很好,但有时你可能希望在不损害 formatter 配置的情况下为测试提供特定字段的值。与为每个变体创建新的 fabricator 相比,你可以使用 ``setOverrides()`` 来指定任何字段的值:

.. literalinclude:: fabricator/015.php

现在通过 ``make()`` 或 ``create()`` 生成的任何数据将始终对 ``first`` 字段使用“Bobby”:

.. literalinclude:: fabricator/016.php

``setOverrides()`` 可以带一个第二个参数来指示这是否应该是持久化的覆盖或者仅用于单个操作:

.. literalinclude:: fabricator/017.php

请注意,在第一次返回后,fabricator 停止使用覆盖:

.. literalinclude:: fabricator/018.php

如果没有提供第二个参数,则传递的值默认持久化。

测试辅助函数
=============

通常你只需要一个一次性的伪对象用于测试。测试辅助函数提供了 ``fake($model, $overrides, $persist = true)`` 来实现这一目的:

.. literalinclude:: fabricator/019.php

这相当于:

.. literalinclude:: fabricator/020.php

如果你只需要一个不保存到数据库的伪对象,可以将 persist 参数设置为 false。

表计数
============

经常地,你的伪数据将依赖于其他伪数据。``Fabricator`` 为每个表提供了已创建的伪项数的静态计数。考虑以下例子:

你的项目有用户和组。在测试用例中,你想创建具有不同组大小的各种场景,所以你使用 ``Fabricator`` 来创建一些组。
现在你想要创建伪用户,但不想分配给不存在的组 ID。
你的模型的 fake 方法可以这样:

.. literalinclude:: fabricator/021.php

现在创建新用户将确保它属于有效的组:``$user = fake(UserModel::class);``

方法
-------

``Fabricator`` 在内部处理计数,但你也可以访问这些静态方法来帮助使用它们:

getCount(string $table): int
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

返回特定表的当前值(默认值:0)。

setCount(string $table, int $count): int
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

手动设置特定表的值,例如,如果你创建了一些没有使用 fabricator 的测试项,但仍想将它们计入最终计数。

upCount(string $table): int
^^^^^^^^^^^^^^^^^^^^^^^^^^^

将特定表的值递增 1 并返回新的值。(这是在 ``Fabricator::create()`` 内部使用的)。

downCount(string $table): int
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

将特定表的值递减 1 并返回新的值,例如,如果你删除了一个伪对象,但想跟踪更改。

resetCounts()
^^^^^^^^^^^^^

重置所有计数。在测试用例之间调用这一方法是很不错的主意(虽然使用 ``CIUnitTestCase::$refresh = true`` 会自动完成此操作)。
