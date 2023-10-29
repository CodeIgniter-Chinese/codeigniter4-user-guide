##############
数组辅助函数
##############

数组辅助函数提供了几个函数来简化数组的更复杂用法。它不打算重复 PHP 提供的任何现有功能 - 除非是为了极大地简化它们的用法。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
===================

使用以下代码加载此辅助函数:

.. literalinclude:: array_helper/001.php

可用函数
===================

以下函数可用:

.. php:function:: dot_array_search(string $search, array $values)

    :param string $search: 用点表示法描述如何在数组中搜索的字符串
    :param array $values: 要搜索的数组
    :returns: 在数组中找到的值,如果没有找到则为 null
    :rtype: mixed

    该方法允许你使用点表示法在数组中搜索特定键,并允许使用通配符 '*'。给定以下数组:

    .. literalinclude:: array_helper/002.php

    我们可以使用搜索字符串“foo.buzz.fizz”定位 'fizz' 的值。类似地,可以使用“foo.bar.baz”找到 baz 的值:

    .. literalinclude:: array_helper/003.php

    你可以使用星号作为通配符来替换任何段。找到时,它将搜索所有子节点直到找到它。如果你不知道值,或如果你的值具有数值索引,这很方便:

    .. literalinclude:: array_helper/004.php

    如果数组键包含点,则可以用反斜杠转义键:

    .. literalinclude:: array_helper/005.php

.. note:: 在 v4.2.0 之前,由于一个 bug, ``dot_array_search('foo.bar.baz', ['foo' => ['bar' => 23]])`` 返回的是 ``23``。v4.2.0 及更高版本返回 ``null``。

.. php:function:: array_deep_search($key, array $array)

    :param mixed $key: 目标键
    :param array $array: 要搜索的数组
    :returns: 在数组中找到的值,如果没有找到则为 null
    :rtype: mixed

    从一个深度不确定的数组返回具有键值的元素的值

.. php:function:: array_sort_by_multiple_keys(array &$array, array $sortColumns)

    :param array $array: 要排序的数组(通过引用传递)。
    :param array $sortColumns: 要排序的数组键及各自的 PHP 排序标志的关联数组
    :returns: 排序是否成功
    :rtype: bool

    此方法以分层方式根据一个或多个键的值对多维数组的元素进行排序。例如,从某个模型的 ``find()`` 函数返回以下数组:

    .. literalinclude:: array_helper/006.php

    现在按两个键对该数组进行排序。请注意,该方法支持使用点表示法访问更深层数组级别中的值,但不支持通配符:

    .. literalinclude:: array_helper/007.php

    现在 ``$players`` 数组已根据每个球员 'team' 子数组中的 'order' 值排序。如果对几个球员此值相等,则这些球员将根据其 'position' 进行排序。结果数组为:

    .. literalinclude:: array_helper/008.php

    同样,该方法也可以处理对象数组。在上面的示例中,每个 'player' 都可能由一个数组表示,而 'teams' 是对象。该方法将检测每个嵌套级别中的元素类型并相应处理。

.. php:function:: array_flatten_with_dots(iterable $array[, string $id = '']): array

    :param iterable $array: 要打平的多维数组
    :param string $id: 可选的 ID 以添加到外部键前面。内部使用以展平键。
    :rtype: array
    :returns: 打平的数组

    此函数使用点作为键的分隔符,将多维数组展平为单个键值对数组。

    .. literalinclude:: array_helper/009.php

    检查后, ``$flattened`` 等于:

    .. literalinclude:: array_helper/010.php

    用户可以自己使用 ``$id`` 参数,但不需要这样做。该函数在内部使用此参数来跟踪展平后的键。如果用户将提供初始 ``$id``,它将添加到所有键前面。

    .. literalinclude:: array_helper/011.php

.. php:function:: array_group_by(array $array, array $indexes[, bool $includeEmpty = false]): array

    :param array $array:        数据行（很可能来自查询结果）
    :param array $indexes:      要按索引值分组的索引。遵循点语法
    :param bool  $includeEmpty: 如果为 true，则不过滤掉 ``null`` 和 ``''`` 值
    :rtype: array
    :returns: 按索引值分组的数组

    该函数允许你按索引值将数据行分组在一起。返回的数组的深度等于作为参数传递的索引数。

    以下示例显示了一些数据（例如从 API 加载的数据）和嵌套数组。

    .. literalinclude:: array_helper/012.php

    我们首先想要按 "gender" 分组，然后按 "hr.department" 分组（最大深度为 2）。首先排除空值的结果如下：

    .. literalinclude:: array_helper/013.php

    这里是相同的代码，但这次我们想要包括空值：

    .. literalinclude:: array_helper/014.php
