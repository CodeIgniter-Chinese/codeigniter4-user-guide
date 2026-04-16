################
HTML Table 类
################

Table 类提供了用于从数组或数据库结果集自动生成 HTML 表格的方法。

.. contents::
    :local:
    :depth: 2

*********************
使用 Table 类
*********************

初始化类
======================

Table 类不作为服务提供，应"常规"实例化，例如：

.. literalinclude:: table/001.php

示例
========

以下示例展示如何从多维数组创建表格。注意第一个数组索引将成为表头（也可以使用下方函数参考中介绍的 ``setHeading()`` 方法设置自定义标题）。

.. literalinclude:: table/002.php

以下示例展示从数据库查询结果创建表格。Table 类会根据表名自动生成标题（也可以使用下方类参考中介绍的 ``setHeading()`` 方法设置自定义标题）。

.. literalinclude:: table/003.php

以下示例展示如何使用独立参数创建表格：

.. literalinclude:: table/004.php

以下示例与上例相同，但使用数组而非单独的参数：

.. literalinclude:: table/005.php

改变表格外观
===============================

Table 类允许设置表格模板来指定期望的布局设计。以下是模板原型：

.. literalinclude:: table/006.php

.. note:: 模板中提供两组 "row" 块，用于创建交替的行颜色，或使设计元素随数据行的每次迭代交替呈现。

无需提交完整模板。如果只需更改布局的某些部分，只需提交相应元素即可。以下示例仅更改表格起始标签：

.. literalinclude:: table/007.php

还可以通过将模板设置数组传递给 Table 构造函数来设置默认值：

.. literalinclude:: table/008.php

.. _table-sync-rows-with-headings:

将行与标题同步
================================

.. versionadded:: 4.4.0

如果使用关联数组作为参数，``setSyncRowsWithHeading(true)`` 方法可使每个数据值放置在 ``setHeading()`` 所定义的对应列中。这在通过 REST API 加载数据时尤其有用——API 返回的数据顺序可能不符合需求，或者返回了过多数据。

如果数据行包含标题中不存在的键，其值会被过滤。反之，如果数据行缺少标题中列出的键，会在对应位置放置空单元格。

.. literalinclude:: table/019.php

.. important:: 在通过 ``addRow([...])`` 添加任何行之前，必须先调用 ``setSyncRowsWithHeading(true)`` 和 ``setHeading([...])``，才能进行列的重排。

使用数组作为 ``generate()`` 的输入会产生相同结果：

.. literalinclude:: table/020.php


***************
类参考
***************

.. php:namespace:: CodeIgniter\View

.. php:class:: Table

    .. attribute:: $function = null

        用于指定一个 PHP 原生函数或有效的函数数组对象，应用于所有单元格数据。

        .. literalinclude:: table/009.php

        上例中，所有单元格数据都会经过 PHP 的 :php:func:`htmlspecialchars()` 函数处理，结果为::

            <td>Fred</td><td>&lt;strong&gt;Blue&lt;/strong&gt;</td><td>Small</td>

    .. php:method:: generate([$tableData = null])

        :param    mixed    $tableData: 用于填充表格行的数据
        :returns:    HTML 表格
        :rtype:    string

        返回包含已生成表格的字符串。接受可选参数，可以是数组或数据库结果对象。

    .. php:method:: setCaption($caption)

        :param    string    $caption: 表格标题
        :returns:    Table 实例（方法链式调用）
        :rtype:    Table

        用于为表格添加标题。

        .. literalinclude:: table/010.php

    .. php:method:: setHeading([$args = [] [, ...]])

        :param    mixed    $args: 包含表格列标题的数组或多个字符串
        :returns:    Table 实例（方法链式调用）
        :rtype:    Table

        用于设置表格标题。可提交数组或独立参数：

        .. literalinclude:: table/011.php

    .. php:method:: setFooting([$args = [] [, ...]])

        :param    mixed    $args: 包含表格脚注值的数组或多个字符串
        :returns:    Table 实例（方法链式调用）
        :rtype:    Table

        用于设置表格脚注。可提交数组或独立参数：

        .. literalinclude:: table/012.php

    .. php:method:: addRow([$args = [] [, ...]])

        :param    mixed    $args: 包含行值的数组或多个字符串
        :returns:    Table 实例（方法链式调用）
        :rtype:    Table

        用于为表格添加行。可提交数组或独立参数：

        .. literalinclude:: table/013.php

        如需设置单个单元格的标签属性，可为该单元格使用关联数组。
        关联键 **data** 定义单元格的数据。任何其他 key => val 键值对会作为 key='val' 属性添加到标签上：

        .. literalinclude:: table/014.php

    .. php:method:: makeColumns([$array = [] [, $columnLimit = 0]])

        :param    array    $array: 包含多行数据的数组
        :param    int    $columnLimit: 表格的列数
        :returns:    HTML 表格列数组
        :rtype:    array

        此方法接受一维数组作为输入，并创建一个深度等于所需列数的多维数组。
        这样就能将包含多个元素的单维数组以固定列数的表格显示。参考以下示例：

        .. literalinclude:: table/015.php

    .. php:method:: setTemplate($template)

        :param    array    $template: 包含模板值的关联数组
        :returns:    成功返回 true，失败返回 false
        :rtype:    bool

        用于设置模板。可提交完整或部分模板。

        .. literalinclude:: table/016.php

    .. php:method:: setEmpty($value)

        :param    mixed    $value: 放入空单元格的值
        :returns:    Table 实例（方法链式调用）
        :rtype:    Table

        用于为所有空单元格设置默认值。例如，可将其设置为不换行空格：

        .. literalinclude:: table/017.php

    .. php:method:: clear()

        :returns:    Table 实例（方法链式调用）
        :rtype:    Table

        清除表格标题、行数据和标题。如果需要用不同数据展示多个表格，
        应在每个表格生成后调用此方法，清除上一个表格的信息。

        示例

        .. literalinclude:: table/018.php

    .. php:method:: setSyncRowsWithHeading(bool $orderByKey)

        :returns:   Table 实例（方法链式调用）
        :rtype:     Table

        使每行数据的键按标题键的顺序排列。由此可更好地控制数据放在正确的列中。
        确保在首次调用 ``addRow()`` 方法之前设置此值。
