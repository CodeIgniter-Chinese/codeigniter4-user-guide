#################
测试响应
#################

``TestResponse`` 类提供了一系列实用方法，用于解析并验证测试用例返回的响应。通常，在进行 :doc:`控制器测试 <controllers>` 或 :doc:`HTTP 功能测试 <feature>` 时会自动生成该对象，但也可以使用任何 ``ResponseInterface`` 实例直接创建：

.. literalinclude:: response/001.php
   :lines: 2-

.. contents::
    :local:
    :depth: 2

测试响应
********************

无论是通过测试获取还是手动创建的 ``TestResponse``，都提供了一系列断言方法供测试使用。

访问请求/响应
==========================

request()
---------

如果测试期间设置了 Request 对象，可直接进行访问：

.. literalinclude:: response/002.php
   :lines: 2-

response()
----------

用于直接访问 Response 对象：

.. literalinclude:: response/003.php
   :lines: 2-

检查响应状态
========================

isOK()
------

根据响应是否正常返回布尔值。判断标准主要是状态码是否在 200 或 300 范围内。除非是重定向，否则空的响应体会被视为无效。

.. literalinclude:: response/004.php
   :lines: 2-

assertOK()
----------

此断言使用 ``isOK()`` 方法测试响应。``assertNotOK()`` 是其反向断言。

.. literalinclude:: response/005.php
   :lines: 2-

isRedirect()
------------

根据响应是否为重定向返回布尔值。

.. literalinclude:: response/006.php
   :lines: 2-

assertRedirect()
----------------

断言响应为 RedirectResponse 实例。``assertNotRedirect()`` 是其反向断言。

.. literalinclude:: response/007.php
   :lines: 2-

assertRedirectTo()
------------------

断言响应为 RedirectResponse 实例，且目标地址与指定的 URI 匹配。

.. literalinclude:: response/008.php
   :lines: 2-

getRedirectUrl()
----------------

返回 RedirectResponse 设置的 URL，失败时返回 null。

.. literalinclude:: response/009.php
   :lines: 2-

assertStatus(int $code)
-----------------------

断言返回的 HTTP 状态码与 $code 匹配。

.. literalinclude:: response/010.php
   :lines: 2-

.. _response-session-assertions:

Session 断言
==================

assertSessionHas(string $key, $value = null)
--------------------------------------------

断言最终的 Session 中存在指定键值。如果传入 $value，还会断言该变量的值与预期一致。

.. literalinclude:: response/011.php
   :lines: 2-

assertSessionMissing(string $key)
---------------------------------

断言最终的 Session 中不包含指定的 $key。

.. literalinclude:: response/012.php
   :lines: 2-

HTTP 标头断言
=================

assertHeader(string $key, $value = null)
----------------------------------------

断言响应中存在名为 ``$key`` 的 HTTP 标头。如果 ``$value`` 不为空，还将断言其值是否匹配。

.. literalinclude:: response/013.php
   :lines: 2-

assertHeaderMissing(string $key)
--------------------------------

断言响应中不存在名为 ``$key`` 的 HTTP 标头。

.. literalinclude:: response/014.php
   :lines: 2-

Cookie 断言
=================

assertCookie(string $key, $value = null, string $prefix = '')
-------------------------------------------------------------

断言响应中存在名为 ``$key`` 的 Cookie。如果 ``$value`` 不为空，还将断言其值是否匹配。如有需要，可通过第三个参数设置 Cookie 前缀。

.. literalinclude:: response/015.php
   :lines: 2-

assertCookieMissing(string $key)
--------------------------------

断言响应中不存在名为 ``$key`` 的 Cookie。

.. literalinclude:: response/016.php
   :lines: 2-

assertCookieExpired(string $key, string $prefix = '')
-----------------------------------------------------

断言名为 ``$key`` 的 Cookie 存在但已过期。如有需要，可通过第二个参数设置 Cookie 前缀。

.. literalinclude:: response/017.php
   :lines: 2-

DOM 辅助方法
============

Response 对象包含多个辅助方法，用于检查响应中的 HTML 输出。这些方法在执行测试断言时非常有用。

see()
-----

根据页面上是否存在指定文本返回布尔值。支持直接查找文本，或根据类型、class、id 在特定标签内查找：

.. literalinclude:: response/018.php
   :lines: 2-

``dontSee()`` 方法的效果则完全相反：

.. literalinclude:: response/019.php
   :lines: 2-

seeElement()
------------

``seeElement()`` 和 ``dontSeeElement()`` 与前述方法类似，但它们不比对元素的值，而仅检查元素是否存在于页面上：

.. literalinclude:: response/020.php
   :lines: 2-

seeLink()
---------

使用 ``seeLink()`` 确保页面上出现了包含指定文本的链接：

.. literalinclude:: response/021.php
   :lines: 2-

seeInField()
------------

``seeInField()`` 方法用于检查是否存在具有指定 name 和 value 的 input 标签：

.. literalinclude:: response/022.php
   :lines: 2-

seeCheckboxIsChecked()
----------------------

使用 ``seeCheckboxIsChecked()`` 方法检查复选框是否存在且已被选中：

.. literalinclude:: response/023.php
   :lines: 2-

seeXPath()
----------

.. versionadded:: 4.5.0

使用 ``seeXPath()`` 可发挥 XPath 的强大功能。此方法面向高级用户，支持直接利用 DOMXPath 对象编写复杂的表达式：

.. literalinclude:: response/033.php
   :lines: 2-

``dontSeeXPath()`` 方法的效果则完全相反：

.. literalinclude:: response/034.php
   :lines: 2-

DOM 断言
==============

可使用下列断言测试响应正文中是否存在特定的元素或文本。

assertSee(string $search = null, string $element = null)
--------------------------------------------------------

断言页面上存在特定的文本或 HTML。支持直接查找，或根据类型、class、id 在特定标签内查找：

.. literalinclude:: response/024.php
   :lines: 2-

assertDontSee(string $search = null, string $element = null)
------------------------------------------------------------

断言效果与 ``assertSee()`` 方法完全相反：

.. literalinclude:: response/025.php
   :lines: 2-

assertSeeElement(string $search)
--------------------------------

与 ``assertSee()`` 类似，但仅检查元素是否存在，不检查具体的文本内容：

.. literalinclude:: response/026.php
   :lines: 2-

assertDontSeeElement(string $search)
------------------------------------

与 ``assertSee()`` 类似，但仅检查指定的元素是否不存在，不检查具体的文本内容：

.. literalinclude:: response/027.php
   :lines: 2-

assertSeeLink(string $text, string $details = null)
---------------------------------------------------

断言存在一个以 ``$text`` 作为正文的 a 标签：

.. literalinclude:: response/028.php
   :lines: 2-

assertSeeInField(string $field, string $value = null)
-----------------------------------------------------

断言存在具有指定 name 和 value 的 input 标签：

.. literalinclude:: response/029.php
   :lines: 2-

处理 JSON
=================

API 接口通常会返回 JSON 响应。下列方法可用于测试此类响应。

getJSON()
---------

以 JSON 字符串形式返回响应正文：

.. literalinclude:: response/030.php
   :lines: 2-

可使用此方法判断 ``$response`` 是否确实包含 JSON 内容：

.. literalinclude:: response/031.php
   :lines: 2-

.. note:: 注意，结果中的 JSON 字符串将进行格式美化。

assertJSONFragment(array $fragment)
-----------------------------------

断言 JSON 响应中包含指定的 ``$fragment``。无需匹配整个 JSON 值。

.. literalinclude:: response/032.php
   :lines: 2-

assertJSONExact($test)
----------------------

与 ``assertJSONFragment()`` 类似，但会检查整个 JSON 响应以确保完全匹配。

处理 XML
================

getXML()
--------

如果应用返回 XML 内容，可通过此方法获取。
