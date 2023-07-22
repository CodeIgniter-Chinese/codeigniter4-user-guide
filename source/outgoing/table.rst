################
HTML 表格类
################

Table 类提供了使你能够从数组或数据库结果集自动生成 HTML 表格的方法。

.. contents::
    :local:
    :depth: 2

*********************
使用 Table 类
*********************

初始化类
======================

Table 类没有作为服务提供,应该进行“正常”实例化,例如:

.. literalinclude:: table/001.php

例子
========

下面是一个示例,展示了如何从多维数组创建表格。请注意,第一个数组索引将成为表格标题(或者你可以使用下面函数参考中描述的 ``setHeading()`` 方法设置自己的标题)。

.. literalinclude:: table/002.php

下面是从数据库查询结果创建的表格示例。表类将自动基于表名生成标题(或者你可以使用下面类参考中描述的 ``setHeading()`` 方法设置自己的标题)。

.. literalinclude:: table/003.php

下面是一个使用离散参数创建表格的示例:

.. literalinclude:: table/004.php

下面是相同的示例,只是使用数组代替各个参数:

.. literalinclude:: table/005.php

更改表格外观
===============================

Table 类允许你设置一个表格模板来指定布局设计。下面是模板原型:

.. literalinclude:: table/006.php

.. note:: 你会注意到模板中有两组 "row" 块。这允许你创建交替的行颜色或与每次迭代行数据交替的设计元素。

你不需要提交完整的模板。如果你只需要更改布局的一部分,只需提交这些元素即可。在此示例中,仅更改表格打开标签:

.. literalinclude:: table/007.php

你还可以通过向 Table 构造函数传递模板设置数组来为这些设置默认值:

.. literalinclude:: table/008.php

***************
类参考
***************

.. php:namespace:: CodeIgniter\View

.. php:class:: Table

    .. attribute:: $function = null

        允许你指定 native PHP 函数或一个有效的函数数组对象应用于所有单元格数据。

        .. literalinclude:: table/009.php

        在上面的例子中,所有单元格数据都将通过 PHP 的 :php:func:`htmlspecialchars()` 函数运行,结果是::

            <td>Fred</td><td>&lt;strong&gt;Blue&lt;/strong&gt;</td><td>Small</td>

    .. php:method:: generate([$tableData = null])

        :param    mixed    $tableData: 用来填充表格行的数据
        :returns:    HTML表格
        :rtype:    string

        返回包含生成表格的字符串。接受一个可选参数,可以是数组或数据库结果对象。

    .. php:method:: setCaption($caption)

        :param    string    $caption: 表格标题
        :returns:    Table 实例(方法链)
        :rtype:    Table

        允许你为表格添加标题。

        .. literalinclude:: table/010.php

    .. php:method:: setHeading([$args = [] [, ...]])

        :param    mixed    $args: 包含表格列标题的数组或多个字符串
        :returns:    Table 实例(方法链)
        :rtype:    Table

        允许你设置表格标题。你可以提交数组或离散参数:

        .. literalinclude:: table/011.php

    .. php:method:: setFooting([$args = [] [, ...]])

        :param    mixed    $args: 包含表格页脚值的数组或多个字符串
        :returns:    Table 实例(方法链)
        :rtype:    Table

        允许你设置表格页脚。你可以提交数组或离散参数:

        .. literalinclude:: table/012.php

    .. php:method:: addRow([$args = [] [, ...]])

        :param    mixed    $args: 包含行值的数组或多个字符串
        :returns:    Table 实例(方法链)
        :rtype:    Table

        允许你向表格添加行。你可以提交数组或离散参数:

        .. literalinclude:: table/013.php

        如果你想为单个单元格的标签属性设置值,可以为该单元格使用关联数组。
        关联键 **data** 定义单元格的数据。任何其他的 key => val 对会作为 key='val' 属性添加到标签中:

        .. literalinclude:: table/014.php

    .. php:method:: makeColumns([$array = [] [, $columnLimit = 0]])

        :param    array    $array: 包含多个行数据的数组
        :param    int    $columnLimit: 表格中的列数
        :returns:    HTML表格列的多维数组
        :rtype:    array

        此方法接受一维数组作为输入,并创建深度等于所需列数的多维数组。
        这允许具有大量元素的单个数组以固定列数显示在表格中。考虑这个例子:

        .. literalinclude:: table/015.php

    .. php:method:: setTemplate($template)

        :param    array    $template: 包含模板值的关联数组
        :returns:    成功为 true,失败为 false
        :rtype:    bool

        允许你设置模板。你可以提交完整或部分模板。

        .. literalinclude:: table/016.php

    .. php:method:: setEmpty($value)

        :param    mixed    $value: 放入空单元格中的值
        :returns:    Table 实例(方法链)
        :rtype:    Table

        允许你为使用在任何空表格单元格中的默认值设置值。
        例如,你可以设置一个不间断的空格:

        .. literalinclude:: table/017.php

    .. php:method:: clear()

        :returns:    Table 实例(方法链)
        :rtype:    Table

        允许你清除表格标题、行数据和标题。
        如果你需要显示具有不同数据的多个表格,应在每个表格生成后调用此方法以清除先前的表格信息。

        例子

        .. literalinclude:: table/018.php
