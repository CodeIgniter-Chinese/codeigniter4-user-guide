*****************
使用 URI 工作
*****************

CodeIgniter 提供了一个面向对象的解决方案来在你的应用程序中使用 URI。使用它可以简化确保结构始终正确的过程,无论 URI 有多复杂,以及安全正确地向现有 URI 添加相对 URI。

.. contents::
    :local:
    :depth: 2

======================
创建 URI 实例
======================

创建一个 URI 实例就和创建一个新类实例一样简单:

.. literalinclude:: uri/001.php

另外,你也可以使用 ``service()`` 函数返回一个实例:

.. literalinclude:: uri/002.php

当你创建新实例时,可以在构造函数中传递完整或部分 URL,它会被解析成适当的部分:

.. literalinclude:: uri/003.php

当前 URI
---------------

很多时候,你真正想要的只是一个代表当前请求的这个 URL 的对象。
你可以使用 :doc:`../helpers/url_helper` 中的一些可用函数:

.. literalinclude:: uri/004.php

你必须传递 ``true`` 作为第一个参数,否则它会返回当前 URL 的字符串表示。

这个 URI 基于路径(相对于你的 ``baseURL``)由当前请求对象和你在 ``Config\App`` 中的设置确定(``baseURL``、``indexPage`` 和 ``forceGlobalSecureRequests``)。
假设你在一个扩展 ``CodeIgniter\Controller`` 的控制器中,你可以获取这个相对路径:

.. literalinclude:: uri/005.php

===========
URI 字符串
===========

很多时候,你真正想要的只是一个 URI 的字符串表示。把 URI 转换成字符串很简单:

.. literalinclude:: uri/006.php

如果你知道 URI 的各个部分,只是想确保它们都格式化正确,你可以使用 URI 类的静态方法 ``createURIString()`` 来生成字符串:

.. literalinclude:: uri/007.php

.. important:: 当 ``URI`` 被转换成字符串时,它会尝试根据 ``Config\App`` 中定义的设置调整项目 URL。如果你需要精确的、未改变的字符串表示,请使用 ``URI::createURIString()``。

=============
URI 的各部分
=============

一旦你有了一个 URI 实例,你就可以设置或获取 URI 的各个部分。本节将详细介绍这些部分是什么,以及如何使用它们。

Scheme
------

Scheme 通常是 'http' 或 'https',但任何 scheme 都是被支持的,包括 'file'、'mailto' 等。

.. literalinclude:: uri/008.php

Authority
---------

很多 URI 包含一些统称为 'authority' 的元素。这包括任何用户信息、主机和端口号。你可以使用 ``getAuthority()`` 方法作为一个字符串获取所有这些部分,或者你可以操作各个部分。

.. literalinclude:: uri/009.php

默认情况下,不会显示密码部分,因为你不会想展示给任何人看。如果你想展示密码,可以使用 ``showPassword()`` 方法。这个 URI 实例会一直展示密码,直到你再次关闭它,所以在不需要时一定要关掉:

.. literalinclude:: uri/010.php

如果你不想展示端口,传递 ``true`` 作为唯一参数:

.. literalinclude:: uri/011.php

.. note:: 如果当前端口是该 scheme 的默认端口则它永远不会被显示。

UserInfo
--------

UserInfo 部分简单地是你可能在 FTP URI 中看到的用户名和密码。尽管你可以作为 Authority 的一部分获取它,但你也可以自己获取它:

.. literalinclude:: uri/012.php

默认情况下,不会显示密码,但你可以使用 ``showPassword()`` 方法覆盖:

.. literalinclude:: uri/013.php

Host
----

URI 的 host 部分通常是 URL 的域名。可以轻松地使用 ``getHost()`` 和 ``setHost()`` 方法设置和获取它:

.. literalinclude:: uri/014.php

Port
----

端口是一个介于 0 和 65535 之间的整数。每个 scheme 都有一个默认值与之相关联。

.. literalinclude:: uri/015.php

使用 ``setPort()`` 方法时,会检查端口是否在有效范围内然后赋值。

Path
----

路径是站点本身内的所有段。如预期的那样,可以使用 ``getPath()`` 和 ``setPath()`` 方法来操作它:

.. literalinclude:: uri/016.php

.. note:: 设置路径时,或者类允许的任何其他方式,都会对任何危险字符进行编码来提高安全性,并移除点段。

Query
-----

可以通过类使用简单的字符串表示来操作查询数据。

获取/设置 Query
^^^^^^^^^^^^^^^^^^^^^

当前 Query 值只能被设置为字符串。

.. literalinclude:: uri/017.php

``setQuery()`` 方法会覆盖任何存在的查询变量。

.. note:: 查询值不能包含片段。如果包含会抛出一个 InvalidArgumentException。

从数组设置 Query
^^^^^^^^^^^^^^^^^^^^^^^^

你可以使用数组设置查询值:

.. literalinclude:: uri/018.php

``setQueryArray()`` 方法会覆盖任何存在的查询变量。

添加 Query 值
^^^^^^^^^^^^^^^^^^

你可以使用 ``addQuery()`` 方法在不销毁现有查询变量的情况下向查询变量集合添加一个值。第一个参数是变量名称,第二个参数是值:

.. literalinclude:: uri/019.php

过滤 Query 值
^^^^^^^^^^^^^^^^^^^^^^

你可以通过向 ``getQuery()`` 方法传递一个选项数组来过滤返回的查询值,其中包含一个 *only* 或 *except* 键:

.. literalinclude:: uri/020.php

这只改变了这一次调用期间返回的值。如果你需要更持久地修改 URI 的查询值,

更改 Query 值
^^^^^^^^^^^^^^^^^^^^^

你可以使用 ``stripQuery()`` 和 ``keepQuery()`` 方法来实际更改对象的查询变量集合:

.. literalinclude:: uri/021.php

.. note:: 默认情况下 ``setQuery()`` 和 ``setQueryArray()`` 方法使用原生的 ``parse_str()`` 函数来准备数据。如果你想使用更自由的规则(允许键名包含点),你可以先使用一个特殊的方法 ``useRawQueryString()``。

Fragment
--------

片段是 URL 末尾以井号 (``#``) 开头的部分。在 HTML URL 中这些是页面内的锚链接。媒体 URI 可以以各种其他方式使用它们。

.. literalinclude:: uri/022.php

============
URI 段
============

斜杠之间的每个部分都是一个单独的段。

.. note:: 对于你的站点 URI 来说,URI 段意味着只有相对于 baseURL 的 URI 路径部分。如果你的 baseURL 包含子文件夹,则值会与当前 URI 路径不同。

URI 类提供了一个简单的方法来确定这些段的值。段从最左的路径开始,编号为 1。

.. literalinclude:: uri/023.php

你也可以为特定段设置不同的默认值,使用 ``getSegment()`` 方法的第二个参数。默认是空字符串。

.. literalinclude:: uri/024.php

.. note:: 你可以获取最后再加 1 的段。当你试图获取最后再加 2 或更多段时,默认会抛出异常。你可以使用 ``setSilent()`` 方法来防止抛出异常。

你可以获取段的总数:

.. literalinclude:: uri/025.php

最后,你可以检索所有段的数组:

.. literalinclude:: uri/026.php

===========================
禁用抛出异常
===========================

默认情况下,这个类的一些方法可能会抛出异常。如果你想禁用它,可以设置一个特殊的标志来防止抛出异常。

.. literalinclude:: uri/027.php
