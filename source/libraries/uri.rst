*****************
处理 URI
*****************

CodeIgniter 提供了面向对象的方式处理应用中的 URI。使用该类可轻松确保 URI 结构始终正确，
无论 URI 多复杂都能应对，同时也支持将相对 URI 安全地解析到已有 URI 中。

.. contents::
    :local:
    :depth: 2

======================
创建 URI 实例
======================

创建 URI 实例就像创建一个新的类实例一样简单。

创建新实例时，可以在构造函数中传入完整或部分 URL，将解析为对应的各部分：

.. literalinclude:: uri/001.php
    :lines: 2-

或者，也可以使用 :php:func:`service()` 函数返回实例：

.. literalinclude:: uri/003.php
    :lines: 2-

v4.4.0 起，如果不传入 URL，将返回当前 URI：

.. literalinclude:: uri/002.php
    :lines: 2-

.. note:: 上述代码返回 ``SiteURI`` 实例，该类继承自 ``URI`` 类。
    ``URI`` 类用于通用 URI，而 ``SiteURI`` 类用于站点 URI。

当前 URI
---------------

当需要一个表示当前请求 URL 的对象时，可使用 :php:func:`current_url()` 函数，该函数位于
:doc:`../helpers/url_helper` 中：

.. literalinclude:: uri/004.php
    :lines: 2-

必须传入 ``true`` 作为第一个参数，否则将返回当前 URL 的字符串表示。

该 URI 基于当前请求对象和 ``Config\App`` 中的配置（``baseURL``、``indexPage`` 和
``forceGlobalSecureRequests``）确定的路径（相对于 ``baseURL``）。

假设在继承 ``CodeIgniter\Controller`` 的控制器中，也可以这样获取当前 SiteURI 实例：

.. literalinclude:: uri/005.php
    :lines: 2-

===========
URI 字符串
===========

很多时候，只需获取 URI 的字符串表示。将 URI 转为字符串即可：

.. literalinclude:: uri/006.php

如果已知 URI 的各部分，只想确保格式正确，可以使用 URI 类的静态方法 ``createURIString()`` 生成字符串：

.. literalinclude:: uri/007.php

.. important:: 将 ``URI`` 转为字符串时，会根据 ``Config\App`` 中定义的配置自动调整项目 URL。
    如果需要精确且未经调整的版本，请改用 ``URI::createURIString()``。

=============
URI 各部分
=============

获取 URI 实例后，可以设置或获取 URI 的各个部分。本节将介绍这些部分的含义及操作方法。

Scheme
------

Scheme 通常是 'http' 或 'https'，但也支持其他 Scheme，如 'file'、'mailto' 等。

.. literalinclude:: uri/008.php

Authority
---------

许多 URI 包含多个统称为 'Authority' 的元素，包括用户信息、主机名和端口号。
可以使用 ``getAuthority()`` 方法将其作为单个字符串获取，也可以操作各独立部分。

.. literalinclude:: uri/009.php

默认情况下不会显示密码部分。如需显示密码，可使用 ``showPassword()`` 方法。
该 URI 实例将持续显示密码，直到关闭该功能，因此使用完毕后务必立即关闭：

.. literalinclude:: uri/010.php

如果不想显示端口，传入 ``true`` 作为唯一参数：

.. literalinclude:: uri/011.php

.. note:: 如果当前端口是该 Scheme 的默认端口，则永远不会显示。

UserInfo
--------

UserInfo 部分就是 FTP URI 中可能看到的用户名和密码。虽然可以作为 Authority 的一部分获取，
也可以单独获取：

.. literalinclude:: uri/012.php

默认不显示密码，但可通过 ``showPassword()`` 方法覆盖此行为：

.. literalinclude:: uri/013.php

Host
----

URI 的 Host 部分通常是域名。使用 ``getHost()`` 和 ``setHost()`` 方法可以轻松设置和获取：

.. literalinclude:: uri/014.php

Port
----

Port 是 0 到 65535 之间的整数。每个 Scheme 都有对应的默认值。

.. literalinclude:: uri/015.php

使用 ``setPort()`` 方法时，会检查端口是否在有效范围内，然后赋值。

Path
----

Path 是站点内部的所有段。正如预期的那样，可以使用 ``getPath()`` 和 ``setPath()`` 方法进行操作：

.. literalinclude:: uri/016.php

.. note:: 设置 Path 时，会进行清理以编码危险字符，并移除点号段（dot segment）以确保安全。

.. note:: v4.4.0 起，``SiteURI::getRoutePath()`` 方法返回相对于 baseURL 的 URI 路径，
    而 ``SiteURI::getPath()`` 方法始终返回带前导 ``/`` 的完整 URI 路径。

Query
-----

可以通过类提供的简单字符串表示法来操作 Query 数据。

获取/设置 Query
^^^^^^^^^^^^^^^^^^^^^

当前 Query 值只能以字符串形式设置。

.. literalinclude:: uri/017.php

``setQuery()`` 方法会覆盖现有的查询变量。

.. note:: Query 值不能包含 Fragment。如果包含，将抛出 InvalidArgumentException。

从数组设置 Query
^^^^^^^^^^^^^^^^^^^^^^^^

可以使用数组设置 Query 值：

.. literalinclude:: uri/018.php

``setQueryArray()`` 方法会覆盖现有的 Query 变量。

添加 Query 值
^^^^^^^^^^^^^^^^^^

使用 ``addQuery()`` 方法可以向 Query 变量集合添加值，而不会破坏现有 Query 变量。
第一个参数是变量名，第二个参数是值：

.. literalinclude:: uri/019.php

过滤 Query 值
^^^^^^^^^^^^^^^^^^^^^^

可以向 ``getQuery()`` 方法传入包含 *only* 或 *except* 键的选项数组来过滤返回的 Query 值：

.. literalinclude:: uri/020.php

这仅改变本次调用返回的值。

修改 Query 值
^^^^^^^^^^^^^^^^^^^^^

如需更永久地修改 URI 的 Query 值，可以使用 ``stripQuery()`` 和 ``keepQuery()`` 方法
来更改对象实际的 Query 变量集合：

.. literalinclude:: uri/021.php

.. note:: 默认情况下，``setQuery()`` 和 ``setQueryArray()`` 方法使用原生 ``parse_str()`` 函数准备数据。
    如需使用更宽松的规则（允许键名包含点），可提前调用专用方法 ``useRawQueryString()``。

Fragment
--------

Fragment 是 URL 末尾由井号（``#``）开头的部分。在 HTML URL 中，用于链接到页面内的锚点。
而在媒体 URI 中，则可能有多种其他用途。

.. literalinclude:: uri/022.php

============
URI 段
============

路径中每两个斜杠之间的部分就是一个段。

.. note:: 对于站点 URI，URI 段仅指相对于 baseURL 的 URI 路径部分。
    如果 ``baseURL`` 包含子文件夹，其值将与当前 URI 路径不同。

URI 类提供了一种简单的方法来确定各段的值。段从 1 开始计数，最左侧的段为 1。

.. literalinclude:: uri/023.php

也可以使用 ``getSegment()`` 方法的第二个参数为特定段设置不同的默认值。默认值为空字符串。

.. literalinclude:: uri/024.php

.. note:: 可以获取最后一个段的下一个段。尝试获取最后一个段的下两个或更后面的段时，
    默认会抛出异常。可通过 ``setSilent()`` 方法阻止抛出异常。

可以获取段的总数：

.. literalinclude:: uri/025.php

最后，还可以获取包含所有段的数组：

.. literalinclude:: uri/026.php

===========================
禁用抛出异常
===========================

默认情况下，该类的某些方法可能会抛出异常。如需禁用，可设置特殊标志阻止抛出异常。

.. literalinclude:: uri/027.php
