############
数组辅助函数
############

数组辅助函数提供了若干函数，旨在简化较为复杂的数组操作。它无意重复 PHP 现有的任何功能——除非这样做能大幅简化这些功能的使用。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
===================

使用以下代码加载此辅助函数：

.. literalinclude:: array_helper/001.php
        :lines: 2-

可用函数
===================

提供以下函数：

.. php:function:: dot_array_search(string $search, array $values)

    :param  string  $search: 描述如何搜索数组的点号表示法字符串
    :param  array   $values: 要搜索的数组
    :returns: 在数组中找到的值，如果没有找到则为 null
    :rtype: mixed

    此方法允许你使用点号表示法在数组中搜索特定键，并允许使用 ``*`` 通配符。给定以下数组：

    .. literalinclude:: array_helper/002.php
        :lines: 2-

    我们可以使用搜索字符串 ``foo.buzz.fizz`` 来定位 ``fizz`` 的值。同样，``baz`` 的值可以通过 ``foo.bar.baz`` 找到：

    .. literalinclude:: array_helper/003.php
        :lines: 2-

    你可以使用星号 (``*``) 作为通配符来替换任何段。当找到时，它将搜索所有子节点直到找到它。当你不知道值，或者值有数字索引时，这很方便：

    .. literalinclude:: array_helper/004.php
        :lines: 2-

    如果数组键包含点号 (``.``)，则该键可以用反斜杠 (``\``) 转义：

    .. literalinclude:: array_helper/005.php
        :lines: 2-

.. note:: 在 v4.2.0 之前，``dot_array_search('foo.bar.baz', ['foo' => ['bar' => 23]])`` 由于一个错误返回 ``23``。
          v4.2.0 及更高版本返回 ``null``。

.. php:function:: array_deep_search($key, array $array)

    :param  mixed  $key: 目标键
    :param  array  $array: 要搜索的数组
    :returns: 在数组中找到的值，如果没有找到则为 null
    :rtype: mixed

    返回具有键值的元素在不确定深度数组中的值

.. php:function:: array_sort_by_multiple_keys(array &$array, array $sortColumns)

    :param  array  $array:       要排序的数组（按引用传递）。
    :param  array  $sortColumns: 要排序的数组键和相应的 PHP 排序标志作为关联数组。
    :returns: 排序是否成功。
    :rtype: bool

    此方法通过一个或多个键的值以分层方式对多维数组的元素进行排序。采用以下数组，可能从模型的 ``find()`` 函数返回：

    .. literalinclude:: array_helper/006.php
        :lines: 2-

    现在通过两个键对此数组进行排序。注意，该方法支持点号表示法来访问更深层级的数组值，但不支持通配符：

    .. literalinclude:: array_helper/007.php
        :lines: 2-

    ``$players`` 数组现在按每个玩家的 ``team`` 子数组中的 ``order`` 值排序。如果多个玩家的此值相等，这些玩家将按他们的 ``position`` 排序。结果数组为：

    .. literalinclude:: array_helper/008.php
        :lines: 2-

    同样，该方法也可以处理对象数组。在上面的示例中，每个 ``player`` 可能是数组，而 ``teams`` 是对象。该方法将检测每个嵌套级别中元素的类型并相应地处理它。

.. php:function:: array_flatten_with_dots(iterable $array[, string $id = '']): array

    :param iterable $array: 要扁平化的多维数组
    :param string $id: 可选 ID，用于添加到外部键前。内部用于扁平化键。
    :rtype: array
    :returns: 扁平化的数组

    此函数通过使用点号作为键的分隔符，将多维数组扁平化为单键值数组。

    .. literalinclude:: array_helper/009.php
        :lines: 2-

    检查后，``$flattened`` 等于：

    .. literalinclude:: array_helper/010.php
        :lines: 2-

    用户可以自行使用 ``$id`` 参数，但这不是必需的。该函数在内部使用此参数来跟踪扁平化的键。如果用户提供初始 ``$id``，它将添加到所有键前。

    .. literalinclude:: array_helper/011.php
        :lines: 2-

.. php:function:: array_group_by(array $array, array $indexes[, bool $includeEmpty = false]): array

    :param array $array:        数据行（很可能来自查询结果）
    :param array $indexes:      用于分组值的索引。遵循点号语法
    :param bool  $includeEmpty: 如果为 true，``null`` 和 ``''`` 值不会被过滤掉
    :rtype: array
    :returns: 按索引值分组的数组

    此函数允许你按索引值将数据行分组在一起。返回数组的深度等于作为参数传递的索引数量。

    示例显示了一些数据（即从 API 加载的）具有嵌套数组。

    .. literalinclude:: array_helper/012.php
        :lines: 2-

    我们想首先按 ``gender`` 分组，然后按 ``hr.department`` 分组（最大深度 = 2）。
    首先是排除空值时的结果：

    .. literalinclude:: array_helper/013.php
        :lines: 2-

    这里是相同的代码，但这次我们想包含空值：

    .. literalinclude:: array_helper/014.php
        :lines: 2-
