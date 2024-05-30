#################
测试响应
#################

``TestResponse`` 类提供了许多有用的函数来解析测试用例中的响应并对其进行测试。通常, ``TestResponse`` 将作为你的结果提供, :doc:`控制器测试 <controllers>` 或 :doc:`HTTP 功能测试 <feature>`,但你始终可以直接使用任何 ``ResponseInterface`` 创建自己的:

.. literalinclude:: response/001.php
   :lines: 2-

.. contents::
    :local:
    :depth: 2

测试响应
********************

无论你是从测试中获得 ``TestResponse`` 还是自己创建,都可以在测试中使用许多新的断言。

访问请求/响应
==========================

request()
---------

如果在测试期间设置了请求,你可以直接访问请求对象:

.. literalinclude:: response/002.php
   :lines: 2-

response()
----------

这允许你直接访问响应对象:

.. literalinclude:: response/003.php
   :lines: 2-

检查响应状态
========================

isOK()
------

根据响应是否被视为“正常”返回布尔值 true/false。这主要由 200 或 300 范围内的响应状态代码确定。如果重定向,空响应正文不被视为有效。

.. literalinclude:: response/004.php
   :lines: 2-

assertOK()
----------

此断言简单地使用 ``isOK()`` 方法来测试响应。``assertNotOK()`` 是此断言的逆。

.. literalinclude:: response/005.php
   :lines: 2-

isRedirect()
------------

根据响应是否重定向返回布尔值 true/false。

.. literalinclude:: response/006.php
   :lines: 2-

assertRedirect()
----------------

断言响应是 RedirectResponse 的一个实例。``assertNotRedirect()`` 是此断言的逆。

.. literalinclude:: response/007.php
   :lines: 2-

assertRedirectTo()
------------------

断言响应是一个 RedirectResponse 实例,且目标与给定的 uri 匹配。

.. literalinclude:: response/008.php
   :lines: 2-

getRedirectUrl()
----------------

返回设置为 RedirectResponse 的 URL,如果失败则为 null。

.. literalinclude:: response/009.php
   :lines: 2-

assertStatus(int $code)
-----------------------

断言返回的 HTTP 状态码匹配 $code。

.. literalinclude:: response/010.php
   :lines: 2-

Session 断言
==================

assertSessionHas(string $key, $value = null)
--------------------------------------------

断言结果 Session 中存在一个值。如果传递了 $value,还将断言变量的值与指定的相匹配。

.. literalinclude:: response/011.php
   :lines: 2-

assertSessionMissing(string $key)
---------------------------------

断言结果 Session 不包括指定的 $key。

.. literalinclude:: response/012.php
   :lines: 2-

Header 断言
=================

assertHeader(string $key, $value = null)
----------------------------------------

断言响应中存在一个名为 ``$key`` 的 Header。如果 ``$value`` 非空,还将断言值匹配。

.. literalinclude:: response/013.php
   :lines: 2-

assertHeaderMissing(string $key)
--------------------------------

断言响应中不存在名为 ``$key`` 的 Header。

.. literalinclude:: response/014.php
   :lines: 2-

Cookie 断言
=================

assertCookie(string $key, $value = null, string $prefix = '')
-------------------------------------------------------------

断言响应中存在一个名为 ``$key`` 的 Cookie。如果 ``$value`` 非空,还将断言值匹配。如有必要,可以通过第三个参数传入前缀来设置 Cookie 前缀。

.. literalinclude:: response/015.php
   :lines: 2-

assertCookieMissing(string $key)
--------------------------------

断言响应中不存在名为 ``$key`` 的 Cookie。

.. literalinclude:: response/016.php
   :lines: 2-

assertCookieExpired(string $key, string $prefix = '')
-----------------------------------------------------

断言一个名为 ``$key`` 的 Cookie 存在,但已过期。如有必要,可以通过第二个参数传入前缀来设置 Cookie 前缀。

.. literalinclude:: response/017.php
   :lines: 2-

DOM 辅助函数
===============

你得到的响应包含许多帮助方法来检查响应中的 HTML 输出。这些在测试中的断言中很有用。

see()
-----

根据页面上的文本是否存在，返回一个布尔值 true/false。可以通过 type、class 或 id 来指定文本所在的标签。

.. literalinclude:: response/018.php
   :lines: 2-

``dontSee()`` 方法正好相反:

.. literalinclude:: response/019.php
   :lines: 2-

seeElement()
------------

``seeElement()`` 和 ``dontSeeElement()`` 与前面的方法非常相似,但不检查元素的值。相反,它们仅检查元素是否存在于页面上:

.. literalinclude:: response/020.php
   :lines: 2-

seeLink()
---------

你可以使用 ``seeLink()`` 来确保页面上存在具有指定文本的链接:

.. literalinclude:: response/021.php
   :lines: 2-

seeInField()
------------

``seeInField()`` 方法检查是否存在具有给定名称和值的输入标签:

.. literalinclude:: response/022.php
   :lines: 2-

seeCheckboxIsChecked()
----------------------

最后,你可以使用 ``seeCheckboxIsChecked()`` 方法检查复选框是否存在并已被选中:

.. literalinclude:: response/023.php
   :lines: 2-

seeXPath()
----------

.. versionadded:: 4.5.0

你可以使用 ``seeXPath()`` 来充分利用 xpath 提供的强大功能。
此方法针对的是希望直接使用 DOMXPath 对象编写更复杂表达式的高级用户：

.. literalinclude:: response/033.php
   :lines: 2-

``dontSeeXPath()`` 方法则完全相反：

.. literalinclude:: response/034.php
   :lines: 2-

DOM 断言
==============

你可以使用以下断言来测试响应正文中是否存在特定元素/文本等。

assertSee(string $search = null, string $element = null)
--------------------------------------------------------

断言文本/HTML 存在于页面上,无论是自身存在还是更具体地说是存在于由类型、类或 id 指定的标记内:

.. literalinclude:: response/024.php
   :lines: 2-

assertDontSee(string $search = null, string $element = null)
------------------------------------------------------------

与 ``assertSee()`` 方法完全相反:

.. literalinclude:: response/025.php
   :lines: 2-

assertSeeElement(string $search)
--------------------------------

类似于 ``assertSee()``,但是这只检查存在的元素。它不检查特定文本:

.. literalinclude:: response/026.php
   :lines: 2-

assertDontSeeElement(string $search)
------------------------------------

类似于 ``assertSee()``,但是这只检查缺失的现有元素。它不检查特定文本:

.. literalinclude:: response/027.php
   :lines: 2-

assertSeeLink(string $text, string $details = null)
---------------------------------------------------

断言找到一个锚定标签,其标签体匹配 ``$text``:

.. literalinclude:: response/028.php
   :lines: 2-

assertSeeInField(string $field, string $value = null)
-----------------------------------------------------

断言存在具有给定名称和值的输入标签:

.. literalinclude:: response/029.php
   :lines: 2-

使用 JSON
=================

响应通常会包含 JSON 响应,特别是在使用 API 方法时。以下方法可以帮助测试响应。

getJSON()
---------

此方法将以 JSON 字符串的形式返回响应正文:

.. literalinclude:: response/030.php
   :lines: 2-

你可以使用此方法来确定 ``$response`` 是否确实包含 JSON 内容:

.. literalinclude:: response/031.php
   :lines: 2-

.. note:: 请注意结果中的 JSON 字符串将美化打印。

assertJSONFragment(array $fragment)
-----------------------------------

断言 ``$fragment`` 在 JSON 响应中找到。它不需要匹配整个 JSON 值。

.. literalinclude:: response/032.php
   :lines: 2-

assertJSONExact($test)
----------------------

与 ``assertJSONFragment()`` 类似,但检查整个 JSON 响应以确保完全匹配。

使用 XML
================

getXML()
--------

如果应用程序返回 XML,则可以通过此方法检索它。
