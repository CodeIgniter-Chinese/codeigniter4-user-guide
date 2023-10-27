*****************
使用 URI
*****************

CodeIgniter 提供了面向对象的方式来在你的应用中使用 URI。这使得确保 URI 结构始终正确变得很简单,无论 URI 有多复杂,都可以安全正确地添加相对 URI 到现有的 URI。

.. contents::
    :local:
    :depth: 2

======================
创建 URI 实例
======================

创建一个 URI 实例就像创建一个新的类实例一样简单。

当你创建新实例时，可以在构造函数中传递完整或部分 URL，并将其解析为相应的部分：

.. literalinclude:: uri/001.php
    :lines: 2-

或者,你可以使用 :php:func:`service()` 函数来获取一个实例:

.. literalinclude:: uri/003.php
    :lines: 2-

自 v4.4.0 起，如果你没有传递 URL，则返回当前的 URI：

.. literalinclude:: uri/002.php
    :lines: 2-

.. note:: 上述代码返回 ``SiteURI`` 实例，它扩展了 ``URI`` 类。``URI`` 类用于一般的 URI，而 ``SiteURI`` 类用于你的站点 URI。

当前 URI
---------------

很多时候，你只需要一个表示当前请求的 URL 的对象。你可以使用 :doc:`../helpers/url_helper` 中提供的 :php:func:`current_url()` 函数：

.. literalinclude:: uri/004.php
    :lines: 2-

你必须传递 ``true`` 作为第一个参数,否则它会返回当前 URL 的字符串表示。

这个 URI 基于当前请求对象和你在 ``Config\App`` 中的设置(``baseURL``、``indexPage`` 和 ``forceGlobalSecureRequests``)确定的相对路径。

假设你在一个扩展了 ``CodeIgniter\Controller`` 的控制器中，你还可以获取当前的 SiteURI 实例：

.. literalinclude:: uri/005.php
    :lines: 2-

===========
URI 字符串
===========

很多时候,你真正想要的只是获取一个 URI 的字符串表示。把 URI 转换为字符串就可以简单地做到这一点:

.. literalinclude:: uri/006.php

如果你知道 URI 的各个部分,只是想确保它们都格式化正确,可以使用 URI 类的静态 ``createURIString()`` 方法生成一个字符串:

.. literalinclude:: uri/007.php

.. important:: 当 ``URI`` 被转换为字符串时,它会尝试根据 ``Config\App`` 中定义的设置调整项目 URL。如果你需要完全不变的字符串表示,请改用 ``URI::createURIString()``。

=============
URI 各部分
=============

一旦你有了一个 URI 实例,你就可以设置或检索 URI 的各个部分。本节将详细介绍这些部分是什么,以及如何使用它们。

Scheme(方案)
-----------------

Scheme 常常是 'http' 或 'https',但任何 scheme 都是被支持的,包括 'file'、'mailto' 等。

.. literalinclude:: uri/008.php

Authority(权限)
-----------------

许多 URI 包含一些统称为 'authority' 的元素。这包括任何用户信息、主机和端口号。你可以使用 ``getAuthority()``
方法作为一个字符串检索所有这些部分,或者可以操作各个部分。

.. literalinclude:: uri/009.php

默认情况下,它不会显示密码部分,因为你不会想把它展示给任何人。如果你想展示密码,可以使用 ``showPassword()`` 方法。
这个 URI 实例会一直展示密码,直到你再次关闭它,所以一定要在使用完以后立即关闭它:

.. literalinclude:: uri/010.php

如果你不想显示端口,请只传入 ``true`` 作为唯一参数:

.. literalinclude:: uri/011.php

.. note:: 如果当前端口是 scheme 的默认端口则不会显示。

UserInfo(用户信息)
-------------------

userinfo 部分简单就是你在 FTP URI 中可能看到的用户名和密码。虽然你可以作为 Authority 的一部分获取它,但你也可以自己获取它:

.. literalinclude:: uri/012.php

默认情况下,它不会显示密码,但是你可以用 ``showPassword()`` 方法覆盖:

.. literalinclude:: uri/013.php

Host(主机)
----------------

URI 的 host 部分通常是 URL 的域名。可以使用 ``getHost()`` 和 ``setHost()`` 方法简单设置和获取它:

.. literalinclude:: uri/014.php

Port(端口)
---------------

端口是一个介于 0 和 65535 之间的整数。每个 scheme 都有一个默认值与之关联。

.. literalinclude:: uri/015.php

使用 ``setPort()`` 方法时,会检查端口是否在有效范围内,然后进行分配。

Path(路径)
---------------

path 是站点本身内的所有段。如你所料,可以使用 ``getPath()`` 和 ``setPath()`` 方法来操作它:

.. literalinclude:: uri/016.php

.. note:: 当用这种或类允许的任何其他方式设置路径时,它会被编码以对任何危险字符进行转义,并移除段点以确保安全。

.. note:: 自 v4.4.0 起，``SiteURI::getRoutePath()`` 方法返回相对于 baseURL 的 URI 路径，而 ``SiteURI::getPath()`` 方法始终返回带有前导 ``/`` 的完整 URI 路径。

Query(查询)
-----------

可以通过类使用简单的字符串表示来操作查询数据。

获取/设置查询
^^^^^^^^^^^^^^^^^^^^^

当前查询值只能作为字符串进行设置。

.. literalinclude:: uri/017.php

``setQuery()`` 方法会覆盖任何现有的查询变量。

.. note:: 查询值不能包含片段。如果包含,会抛出一个 InvalidArgumentException。

从数组设置查询
^^^^^^^^^^^^^^^^^^^^^^^^

你可以使用数组设置查询值:

.. literalinclude:: uri/018.php

``setQueryArray()`` 方法会覆盖任何现有的查询变量。

添加查询值
^^^^^^^^^^^^^^^^^^

你可以使用 ``addQuery()`` 方法向查询变量集合中添加一个值,而不会破坏现有的查询变量。第一个参数是变量名称,第二个参数是值:

.. literalinclude:: uri/019.php

过滤查询值
^^^^^^^^^^^^^^^^^^^^^^

你可以通过向 ``getQuery()`` 方法传递一个选项数组来过滤返回的查询值,包含一个 *only* 键或一个 *except* 键:

.. literalinclude:: uri/020.php

这只改变此次调用返回的值。如果你需要更永久地修改 URI 的查询值,

更改查询值
^^^^^^^^^^^^^^^^^^^^^

你可以使用 ``stripQuery()`` 和 ``keepQuery()`` 方法改变实际对象的查询变量集合:

.. literalinclude:: uri/021.php

.. note:: 默认情况下, ``setQuery()`` 和 ``setQueryArray()`` 方法使用原生的 ``parse_str()`` 函数来准备数据。
    如果你想使用更宽松的规则(允许键名包含点),你可以先使用特殊的 ``useRawQueryString()`` 方法。

Fragment(片段)
-----------------

片段是 URL 末尾以井号 (``#``) 开头的部分。在 HTML URL 中它们链接到页面内的锚点。媒体 URI 可以以各种其他方式使用它们。

.. literalinclude:: uri/022.php

============
URI 段
============

路径之间的每个斜杠之间的部分都是单个段。

.. note:: 对于你的站点 URI 来说,URI 段仅指相对于 baseURL 的 URI 路径部分。
    如果你的 baseURL 包含子文件夹,则值会与当前 URI 路径不同。

URI 类提供了一个简单的方法来确定段的值。段从最左边的路径开始编号 1。

.. literalinclude:: uri/023.php

你也可以通过 ``getSegment()`` 方法的第二个参数为特定段设置不同的默认值。默认值为空字符串。

.. literalinclude:: uri/024.php

.. note:: 你可以获取最后的 +1 段。当你试图获取最后的 +2 或更多段时,默认情况下会抛出异常。你可以使用 ``setSilent()`` 方法来防止抛出异常。

你可以获取总段数:

.. literalinclude:: uri/025.php

最后,你可以检索所有段的数组:

.. literalinclude:: uri/026.php

===========================
禁用抛出异常
===========================

默认情况下,此类的某些方法可能会抛出异常。如果你要禁用它,可以设置一个特殊标志来防止抛出异常。

.. literalinclude:: uri/027.php
