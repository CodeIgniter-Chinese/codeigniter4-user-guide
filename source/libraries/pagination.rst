##########
分页
##########

CodeIgniter 提供了一个非常简洁但灵活的分页库，易于主题化，可与模型配合使用，并支持在单个页面上使用多个分页器。

.. contents::
    :local:
    :depth: 2

*******************
加载库文件
*******************

与 CodeIgniter 中的所有服务一样，可以通过 ``Config\Services`` 加载分页库，不过通常你不需要手动加载它：

.. literalinclude:: pagination/001.php

.. _paginating-with-models:

**********************
使用模型进行分页
**********************

在大多数情况下，你会使用 Pager 库来对从数据库检索的结果进行分页。当使用 :doc:`模型 </models/model>` 类时，可以使用其内置的 ``paginate()`` 方法自动检索当前批次的查询结果，并设置 Pager 库以便在控制器中使用。该方法还会通过 ``page=X`` 查询变量从当前 URL 中读取应显示的当前页码。

要在应用程序中提供分页的用户列表，控制器的方法应如下所示：

.. literalinclude:: pagination/002.php

在此示例中，我们首先创建 ``UserModel`` 的新实例。然后将数据填充到要发送到视图的数据中。第一个元素是从数据库检索的 **users** 结果，该结果会针对正确的页面返回，每页返回 10 个用户。必须发送到视图的第二个项是 Pager 实例本身。为了方便起见，模型会保留其使用的实例并将其存储在公共属性 ``$pager`` 中。因此，我们获取该实例并将其分配给视图中的 ``$pager`` 变量。

自定义分页查询
================

要自定义模型中的分页查询，可以在 ``paginate()`` 方法之前添加 :doc:`查询构建器 <../database/query_builder>` 方法。

添加 WHERE 条件
---------------

如果要添加 WHERE 条件，可以直接指定条件：

.. literalinclude:: pagination/003.php
    :lines: 2-

也可以将条件移动到单独的方法中：

.. literalinclude:: pagination/017.php

.. literalinclude:: pagination/018.php
    :lines: 2-

添加 JOIN
---------

可以连接其他表：

.. literalinclude:: pagination/016.php

.. important:: 需要理解的是，``Model::paginate()`` 方法使用 **模型** 和模型中的 **查询构建器** 实例。因此，尝试将 ``Model::paginate()`` 与 :ref:`db-query` 结合使用 **将无法工作**，因为 ``$db->query()`` 会立即执行查询且不与查询构建器关联。

如果需要编写无法通过查询构建器实现的复杂 SQL 查询，请尝试使用 :ref:`db-query` 和 `手动分页`_。

显示分页链接
======================

在视图中，我们需要指定显示分页链接的位置::

    <?= $pager->links() ?>

这样就完成了所有设置。Pager 类将渲染首页和末页链接，以及当前页两侧超过两页的任何页面的下一页和上一页链接。

需要注意的是，该库的下一页和上一页模式与传统分页结果的方式不同。

此处的下一页和上一页链接到分页结构中要显示的链接组，而不是记录的下一页或上一页。

如果更喜欢简单的输出，可以使用 ``simpleLinks()`` 方法，该方法仅使用 "较旧" 和 "较新" 链接，而不是详细的分页链接::

    <?= $pager->simpleLinks() ?>

在底层，该库加载一个视图文件来确定链接的格式化方式，这使得根据需求进行修改变得简单。有关如何完全自定义输出的详细信息，请参阅下文。

分页多个结果
===========================

如果需要从两个不同的结果集提供链接，可以将组名传递给大多数分页方法以保持数据分离：

.. literalinclude:: pagination/004.php

手动设置页码
=====================

如果需要指定要返回的结果页码，可以将页码作为第三个参数。当使用不同于默认 ``$_GET`` 变量的方式控制显示页面时，这会非常方便。

.. literalinclude:: pagination/005.php

指定页码的 URI 段
===================================

也可以使用 URI 段作为页码，而不是页面查询参数。只需将段编号指定为第四个参数。由分页器生成的 URI 将类似于 **https://domain.tld/foo/bar/[pageNumber]** 而不是 **https://domain.tld/foo/bar?page=[pageNumber]**。

.. literalinclude:: pagination/006.php

注意：``$segment`` 值不能大于 URI 段数加 1。

*****************
手动分页
*****************

有时可能需要基于已知数据创建分页。可以使用 ``makeLinks()`` 方法手动创建链接，该方法分别将当前页码、每页结果数和总项数作为第一、第二和第三个参数：

.. literalinclude:: pagination/015.php

默认情况下，这将以正常方式显示链接，作为一系列链接，但可以通过将模板名称作为第四个参数传递来更改使用的显示模板。更多细节可以在以下部分找到::

    $pager->makeLinks($page, $perPage, $total, 'template_name');

如前一节所述，也可以使用 URI 段作为页码，而不是页面查询参数。将段编号指定为 ``makeLinks()`` 的第五个参数::

    $pager->makeLinks($page, $perPage, $total, 'template_name', $segment);

注意：``$segment`` 值不能大于 URI 段数加 1。

如果需要在单个页面上显示多个分页器，则定义组的附加参数会很有帮助：

.. literalinclude:: pagination/007.php

分页库默认使用 **page** 查询参数进行 HTTP 查询（如果未指定组或给定 ``default`` 组名），或使用 ``page_[groupName]`` 作为自定义组名。

*************************************
仅使用预期查询进行分页
*************************************

默认情况下，所有 GET 查询都会显示在分页链接中。

例如，当访问 URL **https://domain.tld?search=foo&order=asc&hello=i+am+here&page=2** 时，可以生成第 3 页链接以及其他链接，如下所示：

.. literalinclude:: pagination/008.php

``only()`` 方法允许将此限制为已预期的查询：

.. literalinclude:: pagination/009.php

*page* 查询默认启用。并且 ``only()`` 作用于所有分页链接。

*********************
自定义链接
*********************

视图配置
==================

当链接渲染到页面时，它们使用视图文件来描述 HTML。可以通过编辑 **app/Config/Pager.php** 轻松更改使用的视图：

.. literalinclude:: pagination/010.php

此设置存储应使用的视图的别名和 :doc:`命名空间视图路径 </outgoing/views>`。``default_full`` 和 ``default_simple`` 视图分别用于 ``links()`` 和 ``simpleLinks()`` 方法。要全局更改这些显示方式，可以在此处分配新视图。

例如，假设你创建了一个与 Foundation CSS 框架配合使用的新视图文件，并将其放置在 **app/Views/Pagers/foundation_full.php**。由于 **application** 目录的命名空间为 ``App``，并且其下的所有目录直接映射到命名空间的段，因此可以通过其命名空间定位视图文件::

    'default_full' => 'App\Views\Pagers\foundation_full'

由于它位于标准的 **app/Views** 目录下，因此不需要使用命名空间，因为 ``view()`` 方法可以通过文件名定位它。在这种情况下，只需提供子目录和文件名::

    'default_full' => 'Pagers/foundation_full'

创建视图并在配置中设置后，它将自动被使用。你无需替换现有模板。你可以在配置文件中创建任意数量的附加模板。常见情况是在应用程序的前端和后端需要不同的样式。

.. literalinclude:: pagination/011.php

配置完成后，可以将其指定为 ``links()``、``simpleLinks()`` 和 ``makeLinks()`` 方法的最后一个参数::

    <?= $pager->links('group1', 'front_full') ?>
    <?= $pager->simpleLinks('group2', 'front_full') ?>
    <?= $pager->makeLinks($page, $perPage, $total, 'front_full') ?>

创建视图
=================

创建新视图时，只需编写用于创建分页链接本身的代码。不应创建不必要的包装 div，因为它可能在多个位置使用，这只会限制其可用性。通过展示现有的 ``default_full`` 模板，可以最容易地演示如何创建新视图：

.. literalinclude:: pagination/012.php

setSurroundCount()
------------------

在第一行中，``setSurroundCount()`` 方法指定我们希望在当前页面链接两侧显示两个链接。它接受的唯一参数是要显示的链接数。

.. note:: 必须首先调用此方法以生成正确的分页链接。

hasPrevious() 和 hasNext()
--------------------------

如果基于传递给 `setSurroundCount()`_ 的值，在当前页面任一侧有更多链接可以显示，则这些方法返回布尔值 ``true``。

例如，假设我们有 20 页数据。当前页是第 3 页。如果周围计数为 2，则显示的链接如下所示::

    1  |  2  |  3  |  4  |  5

由于显示的第一个链接是首页，因此 ``hasPrevious()`` 将返回 ``false``，因为不存在第 0 页。但是，``hasNext()`` 将返回 ``true``，因为在第 5 页之后还有 15 页结果。

getPrevious() 和 getNext()
--------------------------

这些方法返回当前页面编号链接任一侧的上一组或下一组结果的 **URL**。

例如，当前页设置为 5，你希望前后链接（surroundCount）各为 2 个，这将给出如下内容::

    3  |  4  |  5  |  6  |  7

``getPrevious()`` 返回第 2 页的 URL。``getNext()`` 返回第 8 页的 URL。

如果要获取第 4 页和第 6 页，请改用 `getPreviousPage() 和 getNextPage()`_。

getFirst() 和 getLast()
-----------------------

与 `getPrevious() 和 getNext()`_ 类似，这些方法返回结果集中首页和末页的 **URL**。

links()
-------

返回有关所有编号链接的数据数组。每个链接的数组包含链接的 uri、标题（即数字）以及一个布尔值，指示该链接是否是当前/活动链接：

.. literalinclude:: pagination/013.php

在标准分页结构的代码中，`getPrevious() 和 getNext()`_ 方法用于分别获取上一组和下一组分页链接的 URL。

如果希望使用基于当前页的上一页和下一页链接的分页结构，只需将 `getPrevious() 和 getNext()`_ 方法替换为 `getPreviousPage() 和 getNextPage()`_，并将 `hasPrevious() 和 hasNext()`_ 方法分别替换为 `hasPreviousPage() 和 hasNextPage()`_。

请参阅以下示例：

.. literalinclude:: pagination/014.php

hasPreviousPage() 和 hasNextPage()
----------------------------------

如果当前显示页面的前后存在页面链接，则这些方法返回布尔值 ``true``。

例如，假设我们有 20 页数据。当前页是第 3 页。如果周围计数为 2，则显示的链接如下所示::

    1  |  2  |  3  |  4  |  5

``hasPreviousPage()`` 将返回 ``true``，因为存在第 2 页。而 ``hasNextPage()`` 将返回 ``true``，因为存在第 4 页。

.. note:: 与 `hasPrevious() 和 hasNext()`_ 的区别在于，这些方法基于当前页，而 `hasPrevious() 和 hasNext()`_ 基于根据 `setSurroundCount()`_ 传递的值在当前页前后显示的链接组。

getPreviousPage() 和 getNextPage()
----------------------------------

这些方法返回与当前显示页面前后页面对应的 **URL**。

例如，当前页设置为 5，你希望前后链接（surroundCount）各为 2 个，这将给出如下内容::

    3  |  4  |  5  |  6  |  7

``getPreviousPage()`` 返回第 4 页的 URL。``getNextPage()`` 返回第 6 页的 URL。

.. note:: `getPrevious() 和 getNext()`_ 返回编号链接任一侧的上一组或下一组结果的 URL。

如果需要页码而不是 URL，可以使用以下方法：

getPreviousPageNumber() 和 getNextPageNumber()
----------------------------------------------

这些方法返回与当前显示页面前后页面对应的页码。

getFirstPageNumber() 和 getLastPageNumber()
-------------------------------------------

这些方法返回要显示的链接组中首页和末页的页码。例如，如果要显示的链接组如下所示::

    3  |  4  |  5  |  6  |  7

``getFirstPageNumber()`` 将返回 3，而 ``getLastPageNumber()`` 将返回 7。

.. note:: 要获取整个结果集的首页和末页页码，可以使用以下方法：首页页码始终为 1，`getPageCount()`_ 可用于检索末页页码。

getCurrentPageNumber()
----------------------

此方法返回当前页的页码。

getPageCount()
--------------

此方法返回总页数。

.. _displaying-the-number-of-items-on-the-page:

显示页面项数
==========================================

.. versionadded:: 4.6.0

在对项进行分页时，显示总项数以及当前页显示的项范围通常很有帮助。为了简化此任务，新增了以下方法。这些方法使管理和显示分页详细信息更加容易。示例如下：

.. literalinclude:: pagination/019.php

getTotal()
----------
返回页面的总项数。

getPerPage()
------------
返回页面上显示的项数。

getPerPageStart()
-----------------
返回页面起始项的编号。

getPerPageEnd()
---------------
返回页面结束项的编号。
