###########
视图解析器
###########

.. contents::
    :local:
    :depth: 2

视图解析器可为视图文件中的伪变量执行简单的文本替换。
它能解析简单变量或变量标签对。

伪变量名或控制结构使用大括号包裹，示例如下::

    <html>
    <head>
        <title>{blog_title}</title>
    </head>
    <body>
        <h3>{blog_heading}</h3>

        {blog_entries}
            <h5>{title}</h5>
            <p>{body}</p>
        {/blog_entries}

    </body>
    </html>

这些变量并非实际的 PHP 变量，而是纯文本表示，
用于在模板（视图文件）中消除 PHP 代码。

.. note:: CodeIgniter **并不强制** 使用此类。在视图页面中直接使用原生 PHP（例如
    :doc:`视图渲染器 </outgoing/view_renderer>`）执行效率稍高。
    不过，若需与不熟悉 PHP 的设计师协作，部分开发者可能更倾向于使用模板引擎。

***************************
使用视图 Parser 类
***************************

加载 Parser 类最简便的方式是通过服务加载：

.. literalinclude:: view_parser/001.php

或者，如果未将 ``Parser`` 类设为默认渲染器，
也可直接实例化：

.. literalinclude:: view_parser/002.php

随后可使用其提供的三种标准渲染方法：
``render()``、``setVar()`` 和
``setData()``。还能通过 ``setDelimiters()`` 方法直接指定分隔符。

.. important:: 使用 ``Parser`` 时，视图模板仅由 Parser
    自身处理，而非像常规 PHP 视图脚本那样执行。此类脚本中的 PHP 代码
    会被 Parser 忽略，仅执行替换操作。

    这是设计意图：视图文件不含 PHP。

工作原理
============

``Parser`` 类用于处理存放在应用视图路径下的“PHP/HTML 脚本”。
此类脚本中不可包含任何 PHP 代码。

每个视图参数（称为“伪变量”）都会根据所提供的数值类型触发相应的替换操作。
伪变量不会提取为 PHP 变量，而是通过在大括号内引用变量名的语法来访问其值。

``Parser`` 类内部使用关联数组来存储伪变量设置，直到调用 ``render()`` 方法为止。
因此，伪变量名称必须保持唯一，否则后设置的参数会覆盖先前的配置。

此外，这也会影响脚本内不同上下文环境下的参数转义处理：
必须为每个转义后的数值指定唯一的参数名。

解析器模板
================

可使用 ``render()`` 方法解析（或渲染）简单模板，
示例如下：

.. literalinclude:: view_parser/003.php

视图参数以关联数组形式传递给 ``setData()``，
作为模板中待替换的数据。

上述示例中，模板包含两个变量：``{blog_title}`` 和 ``{blog_heading}``。

``render()`` 的第一个参数为模板名称，
其中 ``blog_template`` 是视图模板文件的名称。

.. important:: 如果省略文件扩展名，则视图文件应以 .php 扩展名结尾。

解析器配置选项
============================

可向 ``render()`` 或 ``renderString()`` 方法传递若干选项。

-   ``cache`` - 保存视图结果的时长（秒）；``renderString()`` 忽略此项
-   ``cache_name`` - 用于保存/获取缓存视图结果的 ID；默认为视图路径；
    ``renderString()`` 忽略此项
-   ``saveData`` - 是否保留视图数据参数以供后续使用；
    默认为 **true**
-   ``cascadeData`` - 嵌套替换时是否继承外部伪变量；
    默认为 **true**

.. literalinclude:: view_parser/004.php

***********************
替换方式
***********************

解析器支持三种替换：简单替换、循环替换和嵌套替换。
替换按伪变量添加的顺序依次执行。

**简单替换** 是一对一地替换伪变量，对应的数据参数
为标量或字符串值，示例如下：

.. literalinclude:: view_parser/005.php

``Parser`` 还支持"变量对"，
用于嵌套替换或循环，以及一些高级
构造来实现条件替换。

解析器执行时，通常按以下顺序处理：

- 处理条件替换
- 处理嵌套/循环替换
- 处理剩余的单一替换

循环替换
==================

当伪变量的值为嵌套数组（如多行记录的集合）时，将触发 **循环替换**。

上述示例演示了如何替换简单变量。如果需要重复渲染整个代码块，并在每次迭代中填充新值，
请参考页面顶部的模板示例::

    <html>
    <head>
        <title>{blog_title}</title>
    </head>
    <body>
        <h3>{blog_heading}</h3>

        {blog_entries}
            <h5>{title}</h5>
            <p>{body}</p>
        {/blog_entries}

    </body>
    </html>

上述代码中有一对变量：``{blog_entries}``
数据... ``{/blog_entries}``。此类情况下，
这对标签之间的整块数据会重复多次，次数对应
参数数组中 "blog_entries" 元素的行数。

解析变量对的方法与解析单一变量相同，
只是需要添加与变量对数据对应的多维数组。示例如下：

.. literalinclude:: view_parser/006.php

伪变量 ``blog_entries`` 的值是关联数组的数组。
其外层结构并不包含指向各嵌套“行”的关联键。

如果"成对"数据来自数据库结果（本身已是
多维数组），可直接使用数据库的 ``getResultArray()``
方法：

.. literalinclude:: view_parser/007.php

如果要循环的数组包含对象而非数组，
解析器会先在对象上查找 ``asArray()`` 方法。如果存在，
则调用该方法，并对返回的数组按上述方式循环。
如果不存在 ``asArray()`` 方法，则将对象强制转换为
数组，并将其公共属性提供给解析器使用。

这在实体类中特别实用，实体类具有 ``asArray()`` 方法，
返回所有公共和受保护的属性（排除 _options 属性），
并使其可供解析器使用。

嵌套替换
====================

当伪变量的值是关联数组（例如数据库中的记录）时，
会发生嵌套替换：

.. literalinclude:: view_parser/008.php

伪变量 ``blog_entries`` 的值是关联数组。
其中定义的键/值对将在该变量的变量对循环内部暴露。

适用于上述数据的 **blog_template.php** 示例::

    <h1>{blog_title} - {blog_heading}</h1>
    {blog_entries}
        <div>
            <h2>{title}</h2>
            <p>{body}</p>
        </div>
    {/blog_entries}

如果希望在 ``blog_entries`` 作用域内也能访问其他伪变量，
请确保 ``cascadeData`` 选项设为 true。

注释
========

可在模板中添加注释，使用 ``{#  #}`` 符号包裹。
这些注释在解析时会被忽略并移除。

::

    {# 这个注释在解析过程中会被删除。 #}
    {blog_entry}
        <div>
            <h2>{title}</h2>
            <p>{body}</p>
        </div>
    {/blog_entry}

数据级联
==============

嵌套替换和循环替换均可选择将
数据级联到内部替换中。

以下示例不受级联影响：

.. literalinclude:: view_parser/009.php

以下示例的结果取决于是否级联：

.. literalinclude:: view_parser/010.php

禁止解析
==================

可使用 ``{noparse}`` ``{/noparse}`` 标签指定页面中不解析的部分。
该区域内的内容将保持原样，不会进行变量替换、循环等操作。

::

    {noparse}
        <h1>Untouched Code</h1>
    {/noparse}

条件逻辑
=================

Parser 类支持一些基本条件语法，用于处理 ``if``、``else`` 和 ``elseif``。
所有 ``if`` 块都必须以 ``endif`` 标签闭合::

    {if $role=='admin'}
        <h1>Welcome, Admin!</h1>
    {endif}

此简单块在解析时会转换为以下代码：

.. literalinclude:: view_parser/011.php

if 语句中使用的所有变量必须预先定义。除此之外，
其逻辑与标准 PHP 条件表达式完全一致，并遵循所有 PHP 原生规则。
支持各种常用的比较运算符，如 ``==``、``===``、``!==``、``<``、``>`` 等。

::

    {if $role=='admin'}
        <h1>Welcome, Admin</h1>
    {elseif $role=='moderator'}
        <h1>Welcome, Moderator</h1>
    {else}
        <h1>Welcome, User</h1>
    {endif}

.. warning:: 条件语句在后台使用 ``eval()`` 进行解析，因此必须注意
    条件语句中使用的用户数据，否则可能使应用面临安全风险。

修改条件分隔符
-----------------------------------

如果模板中包含如下 JavaScript 代码，解析器会抛出语法错误，因为存在可能被解释为条件语句的字符串::

    <script type="text/javascript">
        var f = function() {
            if (hasAlert) {
                alert('{message}');
            }
        }
    </script>

此时，可使用 ``setConditionalDelimiters()`` 方法修改条件分隔符，避免误判：

.. literalinclude:: view_parser/027.php

此时，模板中的代码应写为::

    {% if $role=='admin' %}
        <h1>Welcome, Admin</h1>
    {% else %}
        <h1>Welcome, User</h1>
    {% endif %}

数据转义
=============

默认情况下，所有变量替换均会自动转义，以防范 XSS 攻击。
CodeIgniter 的 ``esc()`` 方法支持多种上下文环境，例如通用的 ``html``、HTML 属性（``attr``）及 ``css`` 等。
若未明确指定，系统将默认按 HTML 上下文处理数据。可通过 ``esc()`` 过滤器指定所需的上下文::

    { user_styles | esc(css) }
    <a href="{ user_link | esc(attr) }">{ title }</a>

有时确实需要使用未转义的内容。可在左右大括号中添加感叹号实现::

    {! unescaped_var !}

过滤器
=======

每个变量替换均可应用一个或多个过滤器，以改变其展示方式。
过滤器的目的不在于大幅改变输出，而是为了以不同形式重用同一变量。
前文提到的 ``esc`` 过滤器便是一例；日期处理也是常见的应用场景，
即在同一页面的不同位置，按需对同一原始数据进行不同的格式化。

过滤器是位于伪变量名之后的命令，使用管道符号 ``|`` 分隔::

    // -55 显示为 55
    { value|abs }

如果参数需要传入实参，实参必须以逗号分隔并置于括号内::

    { created_at|date(Y-m-d) }

可对值应用多个过滤器，通过管道符号串联。过滤器按从左到右的顺序处理::

    { created_at|date_modify(+5 days)|date(Y-m-d) }

内置过滤器
----------------

使用解析器时可用以下过滤器：

================ ================= =========================================================== ======================================
过滤器           参数              说明                                                        示例
================ ================= =========================================================== ======================================
abs                                显示数字的绝对值。                                          { v|abs }

capitalize                         将字符串按句首大写形式显示：仅首字母大写，                  { v|capitalize}
                                   其余字符均转为小写。

date              格式 (Y-m-d)     与 PHP **date** 兼容的格式化字符串。                        { v|date(Y-m-d) }

date_modify       要添加/减去      与 **strtotime** 兼容的修改日期的字符串，                   { v|date_modify(+1 day) }
                  的值             如 ``+5 day`` 或 ``-1 week``。

default           默认值           如果变量为 `empty()`_，则显示默认值。                       { v|default(just in case) }

esc               html, attr,      指定数据转义的上下文。                                      { v|esc(attr) }
                  css, js

excerpt           短语，词数范围   返回指定短语前后指定词数范围内的文本。                      { v|excerpt(green giant, 20) }
                                   功能与 **excerpt** 辅助函数一致。

highlight         短语             使用 '<mark></mark>' 标签高亮文本中的给定短语。             { v|highlight(view parser) }

highlight_code                     使用 HTML/CSS 高亮代码示例。                                { v|highlight_code }

limit_chars       限制个数         将字符数限制为 $limit。                                     { v|limit_chars(100) }

limit_words       限制个数         将词数限制为 $limit。                                       { v|limit_words(20) }

local_currency    货币，区域，     显示货币的本地化版本。"currency" 值为任意                   { v|local_currency(EUR,en_US) }
                  小数             3 位 ISO 4217 货币代码。

local_number      类型，精度，     显示数字的本地化版本。"type" 可为：decimal、currency、      { v|local_number(decimal,2,en_US) }
                  区域             percent、scientific、spellout、ordinal、duration。

lower                              将字符串转换为小写。                                        { v|lower }

nl2br                              将所有换行符（\n）替换为 HTML <br/> 标签。                  { v|nl2br }

number_format     小数位数         封装 PHP **number_format** 函数，供解析器使用。             { v|number_format(3) }

prose                              获取正文并使用 **auto_typography()** 方法                   { v|prose }
                                   将其转换为更美观、更易读的排版。

round             小数位数，类型   将数字舍入到指定小数位数。可传入 **ceil**                   { v|round(3) } { v|round(ceil) }
                                   和 **floor** 来使用对应函数。

strip_tags        允许的标签       封装 PHP **strip_tags**。可传递允许的标签字符串。           { v|strip_tags(<br>) }

title                              将字符串按“标题格式”显示：每个单词首字母大写，              { v|title }
                                   其余部分小写。

upper                              全部大写显示。                                              { v|upper }
================ ================= =========================================================== ======================================

.. _empty(): https://www.php.net/manual/zh/function.empty.php

"local_number" 过滤器的相关细节请参阅 `PHP 的 NumberFormatter <https://www.php.net/manual/zh/numberformatter.create.php>`_。

自定义过滤器
--------------

可通过编辑 **app/Config/View.php** 并在 ``$filters`` 数组中添加新条目来轻松创建自定义过滤器。
每个键是视图中调用过滤器的名称，值为任何有效的 PHP 可调用对象：

.. literalinclude:: view_parser/012.php

解析器插件
==============

插件可扩展解析器，为每个项目添加自定义功能。可以是任何 PHP 可调用对象，
实现非常简单。在模板中，插件通过 ``{+ +}`` 标签指定::

    {+ foo +} inner content {+ /foo +}

此示例展示了名为 **foo** 的插件。可操作开闭标签之间的任何内容。
在此示例中，可处理文本" inner content "。插件在伪变量
替换之前处理。

虽然插件通常由标签对组成（如上所示），但也可是单一标签，无需闭合标签::

    {+ foo +}

起始标签还可包含可自定义插件工作方式的参数。参数以键/值对形式表示::

    {+ foo bar=2 baz="x y" +}

参数也可是单一值::

    {+ include somefile.php +}

内置插件
----------------

使用解析器时可用以下插件：

================== ========================= ============================================ ===================================================================
插件               参数                      说明                                         示例
================== ========================= ============================================ ===================================================================
current_url                                  current_url 辅助函数的别名。                 ``{+ current_url +}``
previous_url                                 previous_url 辅助函数的别名。                ``{+ previous_url +}``
siteURL                                      site_url 辅助函数的别名。                    ``{+ siteURL "login" +}``
mailto             email, title, attributes  mailto 辅助函数的别名。                      ``{+ mailto email=foo@example.com title="Stranger Things" +}``
safe_mailto        email, title, attributes  safe_mailto 辅助函数的别名。                 ``{+ safe_mailto email=foo@example.com title="Stranger Things" +}``
lang               语言字符串                lang 辅助函数的别名。                        ``{+ lang number.terabyteAbbr +}``
validation_errors  字段名（可选）            返回指定字段的错误字符串（如已指定），       ``{+ validation_errors +} , {+ validation_errors field="email" +}``
                                             或返回所有验证错误。
route              路由名称                  route_to 辅助函数的别名。                    ``{+ route "login" +}``
csp_script_nonce                             csp_script_nonce 辅助函数的别名。            ``{+ csp_script_nonce +}``
csp_style_nonce                              csp_style_nonce 辅助函数的别名。             ``{+ csp_style_nonce +}``
================== ========================= ============================================ ===================================================================

注册插件
--------------------

注册新插件最简便的方式是将其添加到 **app/Config/View.php** 的 ``$plugins`` 数组中。
键为模板文件中使用的插件名称。值为任何有效的 PHP 可调用对象，包括静态类方法：

.. literalinclude:: view_parser/014.php

也可使用闭包，但只能在配置文件的构造函数中定义：

.. literalinclude:: view_parser/015.php

如果可调用对象单独使用，则视为单一标签，而非开/闭标签对。
它将被插件的返回值替换：

.. literalinclude:: view_parser/016.php

如果可调用对象包裹在数组中，则视为开/闭标签对，可操作标签之间的内容：

.. literalinclude:: view_parser/017.php

***********
注意事项
***********

模板中未引用的替换参数将被忽略：

.. literalinclude:: view_parser/018.php

若模板中引用的替换参数未定义，结果将直接显示原始伪变量：

.. literalinclude:: view_parser/019.php

若在预期接收数组（即变量对）时提供了字符串参数，
起始标签会被替换，但闭合标签将无法正确渲染：

.. literalinclude:: view_parser/020.php

视图片段
==============

在视图中实现循环效果并非必须使用变量对。
也可将原本属于变量对内部的内容提取为视图片段，
转而在控制器中控制循环逻辑，而非在视图中处理。

以下示例在视图中控制迭代::

    $template = '<ul>{menuitems}
        <li><a href="{link}">{title}</a></li>
    {/menuitems}</ul>';

    $data = [
        'menuitems' => [
            ['title' => 'First Link', 'link' => '/first'],
            ['title' => 'Second Link', 'link' => '/second'],
        ]
    ];

    return $parser->setData($data)->renderString($template);

结果::

    <ul>
        <li><a href="/first">First Link</a></li>
        <li><a href="/second">Second Link</a></li>
    </ul>

以下示例在控制器中控制迭代，
使用视图片段：

.. literalinclude:: view_parser/021.php

结果::

    <ul>
        <li><a href="/first">First Link</a></li>
        <li><a href="/second">Second Link</a></li>
    </ul>

***************
类参考
***************

.. php:namespace:: CodeIgniter\View

.. php:class:: Parser

    .. php:method:: render($view[, $options[, $saveData]])

        :param  string  $view: 视图源文件的文件名
        :param  array   $options: 选项数组，以键/值对表示
        :param  boolean $saveData: 如果为 true，将保存数据以供其他调用使用；如果为 false，将在渲染视图后清除数据。
        :returns: 所选视图的渲染文本
        :rtype: string

        基于文件名和已设置的数据构建输出：

        .. literalinclude:: view_parser/022.php

        支持的选项：

            - ``cache`` - 保存视图结果的时长（秒）
            - ``cache_name`` - 用于保存/获取缓存视图结果的 ID；默认为视图路径
            - ``cascadeData`` - 如果为 true，发生嵌套或循环替换时，生效的数据对将传递到内部
            - ``saveData`` - 如果为 true，视图数据参数将保留以供后续使用

        首先执行条件替换，然后对每个数据对执行剩余替换。

    .. php:method:: renderString($template[, $options[, $saveData]])

        :param  string  $template: 以字符串形式提供的视图源
        :param  array   $options: 选项数组，以键/值对表示
        :param  boolean $saveData: 如果为 true，将保存数据以供其他调用使用；如果为 false，将在渲染视图后清除数据。
        :returns: 所选视图的渲染文本
        :rtype: string

        基于提供的模板源和已设置的数据构建输出：

        .. literalinclude:: view_parser/023.php

        支持的选项及行为同上。

    .. php:method:: setData([$data[, $context = null]])

        :param  array   $data: 视图数据数组，以键/值对表示
        :param  string  $context: 数据转义使用的上下文。
        :returns: Renderer 实例，用于方法链
        :rtype: CodeIgniter\\View\\RendererInterface

        一次性设置多组视图数据：

        .. literalinclude:: view_parser/024.php

        支持的转义上下文：html、css、js、url、attr 或 raw。
        如果为 'raw'，则不进行转义。

    .. php:method:: setVar($name[, $value = null[, $context = null]])

        :param  string  $name: 视图数据变量名
        :param  mixed   $value: 此视图数据的值
        :param  string  $context: 数据转义使用的上下文。
        :returns: Renderer 实例，用于方法链
        :rtype: CodeIgniter\\View\\RendererInterface

        设置单个视图数据：

        .. literalinclude:: view_parser/025.php

        支持的转义上下文：html、css、js、url、attr 或 raw。
        如果为 'raw'，则不进行转义。

    .. php:method:: setDelimiters($leftDelimiter = '{', $rightDelimiter = '}')

        :param  string  $leftDelimiter: 替换字段的左分隔符
        :param  string  $rightDelimiter: 替换字段的右分隔符
        :returns: Renderer 实例，用于方法链
        :rtype: CodeIgniter\\View\\RendererInterface

        覆盖替换字段的分隔符：

        .. literalinclude:: view_parser/026.php

    .. php:method:: setConditionalDelimiters($leftDelimiter = '{', $rightDelimiter = '}')

        :param  string  $leftDelimiter: 条件语句的左分隔符
        :param  string  $rightDelimiter: 条件语句的右分隔符
        :returns: Renderer 实例，用于方法链
        :rtype: CodeIgniter\\View\\RendererInterface

        覆盖条件分隔符：

        .. literalinclude:: view_parser/027.php
