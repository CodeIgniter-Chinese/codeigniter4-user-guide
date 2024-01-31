##########
分页
##########

CodeIgniter 提供了一个非常简单但灵活的分页库,它易于主题化,可与模型一起使用,并且能够在单个页面上支持多个分页器。

.. contents::
    :local:
    :depth: 2

*******************
加载库
*******************

与 CodeIgniter 中的所有服务一样,它可以通过 ``Config\Services`` 加载,尽管你通常不需要手动加载它:

.. literalinclude:: pagination/001.php

.. _paginating-with-models:

**********************
对模型进行分页
**********************

在大多数情况下,你将使用 Pager 库对从数据库检索的结果进行分页。当使用 :doc:`Model </models/model>` 类时,你可以使用其内置的 ``paginate()`` 方法自动检索当前批次的结果,以及设置 Pager 库使其准备在控制器中使用。它甚至会通过当前 URL 中的 ``page=X`` 查询变量读取它应该显示的当前页面。

要在应用程序中提供用户的分页列表,你的控制器方法类似于:

.. literalinclude:: pagination/002.php

在这个示例中,我们首先创建 ``UserModel`` 的新实例。然后我们填充要发送到视图的数据。第一个元素是来自数据库的结果, **users**,它为正确的页面检索出 10 个用户每页。必须发送到视图的第二个项目是 Pager 实例本身。为方便起见,Model 将保存它使用的实例,并将其存储在公共属性 ``$pager`` 中。所以,我们获取它并将其赋值给视图中的 ``$pager`` 变量。

自定义分页查询
================

要在模型中自定义分页查询，你可以在 ``paginate()`` 方法之前添加 :doc:`查询构建器 <../database/query_builder>` 方法。

添加 WHERE
------------

如果你想添加 WHERE 条件，可以直接指定条件：

.. literalinclude:: pagination/003.php
    :lines: 2-

你还可以将条件移动到单独的方法中：

.. literalinclude:: pagination/017.php

.. literalinclude:: pagination/018.php
    :lines: 2-

添加 JOIN
---------

你可以连接另一个表：

.. literalinclude:: pagination/016.php

.. important:: 需要理解的重要一点是，``Model::paginate()`` 方法使用了 **模型** 和模型中的 **查询构建器** 实例。因此，尝试使用 ``Model::paginate()`` 与 :ref:`db-query` **不起作用**，因为 ``$db->query()`` 会立即执行查询，并且与查询构建器没有关联。

如果你需要一个无法使用查询构建器编写的复杂 SQL 查询，请尝试使用 :ref:`db-query` 和 `手动分页`_。

显示分页链接
======================

在视图内,我们然后需要告诉它在何处显示生成的链接::

    <?= $pager->links() ?>

就这么简单。Pager 类将渲染第一页和最后一页链接,以及当前页面两侧超过两个页面的下一页和上一页链接。

重要的是要意识到下一页和上一页的库模式与用于传统分页结果的模式不同。

这里的下一页和上一页链接到要在分页结构中显示的链接组,而不是记录的下一页或上一页。

如果你更喜欢更简单的输出,可以使用 ``simpleLinks()`` 方法,它只使用“较旧”和“较新”链接,而不是详细的分页链接::

    <?= $pager->simpleLinks() ?>

在幕后,库加载一个视图文件来确定如何格式化链接,使其可以简单修改以满足需求。有关如何完全自定义输出的详细信息,请参阅下面。

分页多个结果
===========================

如果你需要从两个不同的结果集提供链接,你可以将组名称传递给大多数分页方法以保持数据分开:

.. literalinclude:: pagination/004.php

手动设置页面
=====================

如果需要指定要返回哪个页面的结果,可以将页面指定为第 3 个参数。当你有一种不同于默认 ``$_GET`` 变量控制要显示哪个页面的方式时,这很方便。

.. literalinclude:: pagination/005.php

指定页面的 URI 段
===================================

也可以使用 URI 段作为页面编号,而不是页面查询参数。简单地将要使用的段编号指定为第四个参数。然后 Pager 生成的 URI 看起来像是 **https://domain.tld/foo/bar/[pageNumber]** 而不是 **https://domain.tld/foo/bar?page=[pageNumber]**。

.. literalinclude:: pagination/006.php

请注意: ``$segment`` 值不能大于 URI 段数加 1。

*****************
手动分页
*****************

你可能会发现有时你只需要根据已知数据创建分页。你可以使用 ``makeLinks()`` 方法手动创建链接,该方法的参数分别是当前页面、每页结果数和总项数:

.. literalinclude:: pagination/015.php

默认情况下,这将以一系列链接的正常方式显示链接,但你可以通过作为第四个参数传递模板的名称来更改使用的显示模板。更多细节可以在以下部分中找到::

    $pager->makeLinks($page, $perPage, $total, 'template_name');

如前一节所述,也可以使用 URI 段作为页面编号,而不是页面查询参数。将要使用的段编号指定为 ``makeLinks()`` 的第五个参数::

    $pager->makeLinks($page, $perPage, $total, 'template_name', $segment);

请注意: ``$segment`` 值不能大于 URI 段数加 1。

如果你需要在一页上显示多个分页器,那么定义组的额外参数可能会有所帮助:

.. literalinclude:: pagination/007.php

分页库默认使用 **page** 查询参数进行 HTTP 查询(如果未给出组或 ``default`` 组名称)或自定义组名称的 ``page_[groupName]``。

*************************************
仅分页预期查询
*************************************

默认情况下,所有 GET 查询都显示在分页链接中。

例如,在访问 URL **https://domain.tld?search=foo&order=asc&hello=i+am+here&page=2** 时,可以生成页面 3 的链接以及其他链接,如下所示:

.. literalinclude:: pagination/008.php

``only()`` 方法允许你将其限制为仅预期的查询:

.. literalinclude:: pagination/009.php

*page* 查询默认启用。``only()`` 在所有分页链接中都起作用。

*********************
自定义链接
*********************

视图配置
==================

将链接渲染到页面时,它们使用视图文件来描述 HTML。你可以通过编辑 **app/Config/Pager.php** 轻松更改使用的视图:

.. literalinclude:: pagination/010.php

此设置存储要使用的视图的别名和 :doc:`命名空间视图路径 </outgoing/views>`。``default_full`` 和 ``default_simple`` 视图分别用于 ``links()`` 和 ``simpleLinks()`` 方法。要应用程序范围内更改显示方式,可以在此处分配一个新视图。

例如,假设你创建了一个与 Foundation CSS 框架一起使用的新视图文件,并将该文件放在 **app/Views/Pagers/foundation_full.php** 中。由于 **application** 目录用作 ``App`` 命名空间,其下的所有目录直接映射到命名空间的段,因此你可以通过它的命名空间定位视图文件::

    'default_full' => 'App\Views\Pagers\foundation_full'

但是,由于它在标准的 **app/Views** 目录下,你不需要命名空间,因为 ``view()`` 方法可以通过文件名定位它。在这种情况下,你可以简单地提供子目录和文件名::

    'default_full' => 'Pagers/foundation_full'

一旦你创建了视图并在配置中设置了它,它将自动使用。你不需要替换现有模板。你可以在配置文件中创建尽可能多的附加模板。一个常见的情况是前端和后端需要不同的样式。

.. literalinclude:: pagination/011.php

一旦配置完成,你可以将其指定为 ``links()``、``simpleLinks()`` 和 ``makeLinks()`` 方法中的最后一个参数::

    <?= $pager->links('group1', 'front_full') ?>
    <?= $pager->simpleLinks('group2', 'front_full') ?>
    <?= $pager->makeLinks($page, $perPage, $total, 'front_full') ?>

创建视图
=================

创建新视图时,你只需要创建生成分页链接本身所需的代码。你不应该创建不必要的包装 div,因为它可能在多个地方使用,你只会限制它们的有用性。通过展示你如何使用现有的 ``default_full`` 模板来创建一个新视图,可以很容易地演示如何创建新视图:

.. literalinclude:: pagination/012.php

setSurroundCount()
------------------

在第一行中, ``setSurroundCount()`` 方法指定我们希望在当前页面链接的两侧显示两个链接。它只接受显示链接数的参数。

.. note:: 你必须首先调用此方法来生成正确的分页链接。

hasPrevious() & hasNext()
-------------------------

这些方法会返回一个布尔值 ``true``，如果在当前页面的两侧可以显示更多的链接，这取决于传递给 `setSurroundCount()`_ 的值。

例如，假设我们有 20 页的数据。当前的页面是第 3 页。如果周围的数量是 2，那么以下链接会显示如下::

    1  |  2  |  3  |  4  |  5

由于显示的第一个链接是第一页，``hasPrevious()`` 将返回 ``false``，因为没有第零页。然而，
``hasNext()`` 将返回 ``true``，因为在第五页之后还有 15 页的结果。

getPrevious() & getNext()
-------------------------

这些方法返回数字链接两侧的上一页或下一页结果的 **URL**。

例如，你将当前页面设置为 5，你希望在之前和之后的链接（surroundCount）各为 2，那么你会得到如下内容::

    3  |  4  |  5  |  6  |  7

``getPrevious()`` 返回第 2 页的 URL。``getNext()`` 返回第 8 页的 URL。

如果你想要第 4 页和第 6 页,请改用 `getPreviousPage() & getNextPage()`_。

getFirst() & getLast()
----------------------

与 `getPrevious() & getNext()`_ 类似,这些方法返回结果集中的第一页和最后一页的 **URL**。

links()
-------

返回有关所有编号链接的数据数组。每个链接的数组都包含链接的 uri、标题(只是数字)以及一个布尔值,告知链接是否是当前/活动链接:

.. literalinclude:: pagination/013.php

在为标准分页结构提供的代码中,使用 `getPrevious() & getNext()`_ 方法分别获取前一个和下一个分页组的链接。

如果你要使用上一页和下一页将链接到当前页面基于当前页面的上一页和下一页的分页结构,只需分别用 `getPreviousPage() & getNextPage()`_ 替换 `getPrevious() & getNext()`_,以及分别用 `hasPreviousPage() & hasNextPage()`_ 替换 `hasPrevious() & hasNext()`_。

请参阅以下示例及其更改:

.. literalinclude:: pagination/014.php

hasPreviousPage() & hasNextPage()
---------------------------------

这个方法返回一个布尔值 ``true``，如果在当前显示的页面前后各有一个页面的链接。

例如，假设我们有 20 页的数据。当前的页面是第 3 页。如果周围的数量是 2，那么以下链接会显示如下::

    1  |  2  |  3  |  4  |  5

``hasPreviousPage()`` 将返回 ``true``，因为有第 2 页。并且，
``hasNextPage()`` 将返回 ``true``，因为有第 4 页。

.. note:: 与 `hasPrevious() & hasNext()`_ 的区别在于，它们是基于当前页面的，而 `hasPrevious() & hasNext()`_ 是基于在当前页面前后显示的链接集，这取决于传递给 `setSurroundCount()`_ 的值。

getPreviousPage() & getNextPage()
---------------------------------

这些方法返回当前显示页面的前一页和后一页的 **URL**。

例如，你将当前页面设置为 5，你希望在之前和之后的链接（surroundCount）各为 2，那么你会得到如下内容::

    3  |  4  |  5  |  6  |  7

``getPreviousPage()`` 返回第 4 页的 URL。``getNextPage()`` 返回第 6 页的 URL。

.. note:: `getPrevious() & getNext()`_ 返回数字链接两侧的上一页或下一页结果的 URL。

如果你希望得到的是页面数字而不是 URL，你可以使用以下方法：

getPreviousPageNumber() & getNextPageNumber()
---------------------------------------------

这些方法返回当前显示页面之前和之后的页面号。

getFirstPageNumber() & getLastPageNumber()
------------------------------------------

这些方法返回要显示的链接集中第一页和最后一页的页码。例如，如果要显示的链接集如下所示::

    3  |  4  |  5  |  6  |  7

``getFirstPageNumber()`` 将返回 3，而 ``getLastPageNumber()`` 将返回 7。

.. note:: 要获取整个结果集中第一页和最后一页的页码，你可以使用以下方法：第一页的页码总是 1，可以使用 `getPageCount()`_ 来获取最后一页的页码。

getCurrentPageNumber()
----------------------

该方法返回当前页面的页码。

getPageCount()
--------------

该方法返回总页数。
