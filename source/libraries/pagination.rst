##########
分页
##########

CodeIgniter 提供了一个简洁但灵活的分页类，易于定制主题，支持与模型配合使用，
并能在单个页面上支持多个分页器。

.. contents::
    :local:
    :depth: 2

*******************
加载类
*******************

与 CodeIgniter 中的所有服务一样，可通过 ``Config\Services`` 加载，但通常不需要手动加载：

.. literalinclude:: pagination/001.php

.. _paginating-with-models:

**********************
使用模型进行分页
**********************

大多数情况下，分页库用于对从数据库检索的结果进行分页。
使用 :doc:`模型 </models/model>` 类时，可利用其内置的 ``paginate()`` 方法自动
获取当前批次的结果，并设置好 Pager 库以便在控制器中使用。
该方法还会从当前 URL 的 ``page=X`` 查询变量中自动读取应显示的页码。

要在应用中提供分页的用户列表，控制器方法大致如下：

.. literalinclude:: pagination/002.php

在此示例中，首先创建 ``UserModel`` 的新实例，然后准备发送到视图的数据。
第一个元素是数据库查询结果 **users**，按正确页码返回，每页
10 条用户记录。第二个必须发送到视图的元素是 Pager 实例。为方便起见，
模型会保留所使用的实例并将其存储在公共属性 ``$pager`` 中。因此，直接
将其赋值给视图中的 ``$pager`` 变量即可。

自定义分页查询
================

要在模型中自定义分页查询，可在 ``paginate()``
方法前添加 :doc:`查询构建器 <../database/query_builder>` 方法。

添加 WHERE 条件
---------------

如需添加 WHERE 条件，可直接指定：

.. literalinclude:: pagination/003.php
    :lines: 2-

也可将条件移至独立方法中：

.. literalinclude:: pagination/017.php

.. literalinclude:: pagination/018.php
    :lines: 2-

添加 JOIN
---------

可连接其他表：

.. literalinclude:: pagination/016.php

.. important:: 需要理解的是，``Model::paginate()`` 方法
    使用的是模型内部的 **模型** 和 **查询构建器** 实例。
    因此，尝试将 ``Model::paginate()`` 与 :ref:`db-query` 一起使用
    **无法正常工作**，因为 ``$db->query()`` 会立即执行查询，
    与查询构建器无关。

如需执行无法用查询构建器编写的复杂 SQL 查询，
请尝试使用 :ref:`db-query` 和 `手动分页`_。

显示分页链接
======================

在视图中，需要指定分页链接的显示位置::

    <?= $pager->links() ?>

仅此而已。Pager 类会渲染首页和末页链接，以及当前页两侧超过两页时的
"上一页"和"下一页"链接。

需要注意的是，库中"上一页"和"下一页"的链接模式与传统分页方式不同。

此处的"下一页"和"上一页"链接到分页结构中要显示的链接组，而不是记录的下一页或上一页。

如需更简化的输出，可使用 ``simpleLinks()`` 方法，该方法仅使用"Older"和"Newer"链接，
而不显示详细的分页链接::

    <?= $pager->simpleLinks() ?>

在幕后，库会加载一个视图文件来确定链接的格式，便于根据需要修改。
详见下文关于完全自定义输出的说明。

分页多组结果
===========================

如需为两组不同的结果集提供链接，可向大多数分页
方法传入分组名称，以保持数据独立：

.. literalinclude:: pagination/004.php

手动设置页码
=====================

如需指定返回哪一页结果，可将页码作为第 3 个参数传入。
当使用不同于默认 ``$_GET`` 变量来控制页码时，此功能非常实用。

.. literalinclude:: pagination/005.php

指定页码的 URI 段
===================================

也可使用 URI 段作为页码，而非 page 查询参数。只需将
要使用的段号作为第 4 个参数传入即可。此时分页器生成的 URI 形如
**https://domain.tld/foo/bar/[pageNumber]**，而非 **https://domain.tld/foo/bar?page=[pageNumber]**。

.. literalinclude:: pagination/006.php

请注意：``$segment`` 的值不能大于 URI 段数加 1。

*****************
手动分页
*****************

有时可能只需基于已知数据创建分页。可使用
``makeLinks()`` 方法手动创建链接，该方法依次接受当前页码、每页结果数和
总条目数作为第 1、第 2 和第 3 个参数：

.. literalinclude:: pagination/015.php

默认情况下，这会以常规方式将链接显示为一系列链接，但也可通过在第 4 个参数中传入
模板名称来更改所使用的显示模板。详见下文各节::

    $pager->makeLinks($page, $perPage, $total, 'template_name');

如前一节所述，也可使用 URI 段作为页码，而非 page 查询参数。将
段号作为第 5 个参数传入 ``makeLinks()`` 即可::

    $pager->makeLinks($page, $perPage, $total, 'template_name', $segment);

请注意：``$segment`` 的值不能大于 URI 段数加 1。

如需在同一页面显示多个分页器，则额外的分组参数会很有帮助：

.. literalinclude:: pagination/007.php

默认情况下，分页库使用 **page** 查询参数（未指定分组或使用 ``default`` 分组名时），
或使用 ``page_[groupName]`` 作为自定义组名。

*************************************
仅使用预期查询进行分页
*************************************

默认情况下，分页链接会显示所有 GET 查询参数。

例如，访问 URL **https://domain.tld?search=foo&order=asc&hello=i+am+here&page=2** 时，第 3 页的链接及其他链接将按如下方式生成：

.. literalinclude:: pagination/008.php

``only()`` 方法可将链接中的查询参数限制为仅预期的参数：

.. literalinclude:: pagination/009.php

*page* 查询参数默认启用。``only()`` 对所有分页链接生效。

*********************
自定义链接
*********************

视图配置
==================

渲染分页链接时，使用视图文件来描述 HTML 结构。可通过编辑 **app/Config/Pager.php** 轻松
更改所使用的视图：

.. literalinclude:: pagination/010.php

此设置存储视图的别名和 :doc:`命名空间视图路径 </outgoing/views>`。
``default_full`` 和 ``default_simple`` 视图分别用于 ``links()`` 和 ``simpleLinks()``
方法。要更改应用范围内的显示方式，可在此处分配新视图。

例如，假设创建了一个适配 Foundation CSS 框架的新视图文件，
并将其放置在 **app/Views/Pagers/foundation_full.php**。由于 **application** 目录
的命名空间为 ``App``，其下的所有目录直接映射到命名空间的对应段，因此可通过命名空间定位
视图文件::

    'default_full' => 'App\Views\Pagers\foundation_full'

由于该文件位于标准的 **app/Views** 目录下，无需使用命名空间，
因为 ``view()`` 方法可通过文件名定位。此时，只需指定子目录和文件名即可::

    'default_full' => 'Pagers/foundation_full'

创建视图并在配置中设置后，系统会自动使用它。无需替换现有模板。
可根据需要在配置文件中创建任意数量的额外模板。
常见场景是应用的前台和后台需要不同样式的分页器。

.. literalinclude:: pagination/011.php

配置完成后，可在 ``links()``、``simpleLinks()`` 和 ``makeLinks()``
方法的最后一个参数中指定::

    <?= $pager->links('group1', 'front_full') ?>
    <?= $pager->simpleLinks('group2', 'front_full') ?>
    <?= $pager->makeLinks($page, $perPage, $total, 'front_full') ?>

创建视图
=================

创建新视图时，只需编写生成分页链接所需的代码。
不应创建多余的外层 div，因为视图可能在多处使用，多余结构会降低其适用性。
以下通过展示现有的 ``default_full`` 模板来说明如何创建新视图：

.. literalinclude:: pagination/012.php

setSurroundCount()
------------------

在第一行中，``setSurroundCount()`` 方法指定在当前页链接两侧各显示两个链接。
它唯一接受的参数是要显示的链接数量。

.. note:: 必须首先调用此方法才能生成正确的分页链接。

hasPrevious() 和 hasNext()
--------------------------

根据传递给 `setSurroundCount()`_ 的值，如果当前页两侧还有可显示的链接，
这些方法分别返回布尔值 ``true``。

例如，假设有 20 页数据。当前
页是第 3 页。如果 surroundCount 为 2，则显示的链接如下::

    1  |  2  |  3  |  4  |  5

由于第一个显示的链接是第 1 页，``hasPrevious()`` 会返回 ``false``，因为不存在第 0 页。
而 ``hasNext()`` 会返回 ``true``，因为第 5 页之后还有 15 页。

getPrevious() 和 getNext()
--------------------------

这些方法返回编号链接两侧上一页或下一页的 **URL**。

例如，当前页设为 5，前后两侧（surroundCount）各设为 2，结果如下::

    3  |  4  |  5  |  6  |  7

``getPrevious()`` 返回第 2 页的 URL。``getNext()`` 返回第 8 页的 URL。

如需获取第 4 页和第 6 页，请改用 `getPreviousPage() 和 getNextPage()`_。

getFirst() 和 getLast()
-----------------------

与 `getPrevious() 和 getNext()`_ 类似，这些方法返回结果集中首页和末页的
**URL**。

links()
-------

返回所有编号链接的数据数组。每个链接的数组包含链接的 URI、
标题（即数字），以及指示是否为当前活动链接的布尔值：

.. literalinclude:: pagination/013.php

在上述标准分页结构的代码中，使用 `getPrevious() 和 getNext()`_ 方法分别获取上一页和下一页的链接。

如果希望使用基于当前页的上一页和下一页链接的分页结构，
只需将 `getPrevious() 和 getNext()`_ 方法替换为 `getPreviousPage() 和 getNextPage()`_，
并将 `hasPrevious() 和 hasNext()`_ 方法替换为 `hasPreviousPage() 和 hasNextPage()`_ 即可。

请参阅以下使用这些改动的示例：

.. literalinclude:: pagination/014.php

hasPreviousPage() 和 hasNextPage()
----------------------------------

如果当前显示页的前后分别有可跳转的页面，此方法返回布尔值 ``true``。

例如，假设有 20 页数据。当前
页是第 3 页。如果 surroundCount 为 2，则显示的链接如下::

    1  |  2  |  3  |  4  |  5

``hasPreviousPage()`` 会返回 ``true``，因为存在第 2 页。
``hasNextPage()`` 会返回 ``true``，因为存在第 4 页。

.. note:: 与 `hasPrevious() 和 hasNext()`_ 的区别在于，此方法基于
    当前页判断，而 `hasPrevious() 和 hasNext()`_ 基于传递给
    `setSurroundCount()`_ 的值所确定的链接集合。

getPreviousPage() 和 getNextPage()
----------------------------------

这些方法返回相对于当前显示页的上一页和下一页的 **URL**。

例如，当前页设为 5，前后两侧（surroundCount）各设为 2，结果如下::

    3  |  4  |  5  |  6  |  7

``getPreviousPage()`` 返回第 4 页的 URL。``getNextPage()`` 返回第 6 页的 URL。

.. note:: `getPrevious() 和 getNext()`_ 返回编号链接两侧上一页或下一页的 URL。

如需使用页码而非 URL，可使用以下方法：

getPreviousPageNumber() 和 getNextPageNumber()
----------------------------------------------

这些方法返回相对于当前显示页的上一页和下一页的页码。

getFirstPageNumber() 和 getLastPageNumber()
-------------------------------------------

这些方法返回要显示的链接集合中首页和末页的页码。
例如，如果要显示的链接集合如下::

    3  |  4  |  5  |  6  |  7

``getFirstPageNumber()`` 返回 3，``getLastPageNumber()`` 返回 7。

.. note:: 如需获取整个结果集中首页和末页的页码，
    可使用以下方法：首页页码始终为 1，末页页码可通过 `getPageCount()`_ 获取。

getCurrentPageNumber()
----------------------

此方法返回当前页的页码。

getPageCount()
--------------

此方法返回总页数。

.. _displaying-the-number-of-items-on-the-page:

显示当前页的条目数量
==========================

.. versionadded:: 4.6.0

对条目进行分页时，显示总条目数和当前页展示的条目范围通常很有帮助。为简化此任务，新增了以下方法。
这些方法让管理和展示分页信息更加便捷。示例如下：

.. literalinclude:: pagination/019.php

getTotal()
----------
返回页面的总条目数。

getPerPage()
------------
返回每页应显示的条目数。

getPerPageStart()
-----------------
返回当前页起始条目的序号。

getPerPageEnd()
---------------
返回当前页结束条目的序号。
