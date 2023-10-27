###########
视图解析器
###########

.. contents::
    :local:
    :depth: 2

视图解析器可以对视图文件中的伪变量进行简单的文本替换。
它可以解析简单变量或变量标签对。

伪变量名称或控制结构用大括号括起来,像这样::

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

这些变量不是实际的 PHP 变量,而是普通文本表示,允许你从模板(视图文件)中消除 PHP。

.. note:: 由于在视图页面中使用纯 PHP(例如使用 :doc:`视图渲染器 </outgoing/view_renderer>`)
    可以让它们运行得稍快一点,CodeIgniter **不要求** 你使用这个类。
    然而,一些开发人员更喜欢在与设计师合作时使用某种模板引擎,
    因为他们觉得设计师在使用 PHP 时会感到困惑。

***************************
使用视图解析器类
***************************

通过其服务加载解析器类的最简单方法是:

.. literalinclude:: view_parser/001.php

另外,如果你没有使用 ``Parser`` 类作为默认渲染器,
你可以直接实例化它:

.. literalinclude:: view_parser/002.php

然后你可以使用它提供的三种标准渲染方法中的任何一种:``render()``、``setVar()`` 和
``setData()``。你还可以通过 ``setDelimiters()`` 方法直接指定分隔符。

.. important:: 使用 ``Parser``,你的视图模板只由 Parser 本身处理,而不是作为常规视图 PHP 脚本。
    这样的脚本中的 PHP 代码会被解析器忽略,只执行替换。

    这是有意为之的:不包含 PHP 的视图文件。

它的工作原理
============

``Parser`` 类处理存储在应用程序的视图路径中的“PHP/HTML 脚本”。
这些脚本不能包含任何 PHP。

每个视图参数(我们称之为伪变量)都会触发一次替换,基于你为它提供的值的类型。
伪变量不会提取到 PHP 变量中;相反,它们的值是通过伪变量语法访问的,其名称引用在大括号内。

Parser 类在内部使用关联数组来累积伪变量设置,直到你调用 ``render()``。
这意味着你的伪变量名称需要是唯一的,否则后面的参数设置将覆盖较早的设置。

这也会影响根据脚本中的不同上下文对参数值进行转义。
你将必须为每个转义值提供一个唯一的参数名称。

解析器模板
================

你可以使用 ``render()`` 方法来解析(或渲染)简单模板,像这样:

.. literalinclude:: view_parser/003.php

视图参数作为要在模板中替换的数据的关联数组传递给 ``setData()``。在上面的例子中,
模板将包含两个变量:``{blog_title}`` 和 ``{blog_heading}``
``render()`` 的第一个参数包含 :doc:`视图文件 </outgoing/views>` 的名称,其中 *blog_template* 是视图文件的名称。

.. important:: 如果省略了文件扩展名,则视图预计以 .php 扩展名结束。

解析器配置选项
============================

可以将几个选项传递给 ``render()`` 或 ``renderString()`` 方法。

- ``cache`` - 以秒为单位,保存视图结果的时间;对 renderString() 忽略
- ``cache_name`` - 用于保存/检索缓存视图结果的 ID;默认为视图路径;对 renderString() 忽略
- ``saveData`` - 如果为 true,视图数据参数应保留以供随后的调用;默认为 **true**
- ``cascadeData`` - 如果嵌套或循环替换发生时,数据对是否应该传播给内部替换;默认为 **true**

.. literalinclude:: view_parser/004.php

***********************
替换变体
***********************

支持三种替换类型:简单、循环和嵌套。
替换的执行顺序与添加伪变量的顺序相同。

解析器执行的 **简单替换** 是一对一地替换伪变量,其中相应的数据参数具有标量或字符串值,如本例所示:

.. literalinclude:: view_parser/005.php

解析器通过“变量对”大大扩展了替换,用于嵌套替换或循环,以及一些用于条件替换的高级结构。

当解析器执行时,它通常会

- 处理任何条件替换
- 处理任何嵌套/循环替换
- 处理其余的单个替换

循环替换
==================

当伪变量的值是数组的序列化数组时,就会发生循环替换,例如数据库记录的数组。

上面的示例代码允许简单变量被替换。如果你想让整个变量块重复,每个迭代都包含新值呢?
考虑我们在页面顶部显示的模板示例::

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

在上面的代码中,你会注意到一对变量:``{blog_entries}`` 数据... ``{/blog_entries}``。在这种情况下,这对变量之间的数据的整个块将重复多次,对应于参数数组中的“blog_entries”元素的行数。

解析变量对使用与解析单个变量完全相同的代码,不同之处在于,你需要添加一个与变量对数据对应的多维数组。考虑这个例子:

.. literalinclude:: view_parser/006.php

伪变量 ``blog_entries`` 的值是一个关联数组的顺序数组。外部级别与嵌套的“行”没有关联的键。

如果你的“pair”数据来自数据库结果,它已经是一个多维数组,你可以简单地使用数据库的 ``getResultArray()`` 方法:

.. literalinclude:: view_parser/007.php

如果要循环的数组包含对象而不是数组,解析器将首先在对象上查找 ``asArray()`` 方法。如果存在,则调用该方法并像上面描述的那样循环结果数组。如果没有 ``asArray()`` 方法,对象将转换为数组,它的公共属性将可用于解析器。

当与实体类一起使用时,这尤其有用,因为它有一个 ``asArray()`` 方法,该方法返回所有公共和受保护的属性(减去 _options 属性),并使它们可用于解析器。

嵌套替换
====================

当伪变量的值是关联数组时,就会发生嵌套替换,例如来自数据库的记录:

.. literalinclude:: view_parser/008.php

伪变量 ``blog_entries`` 的值是一个关联数组。在它内部定义的键/值对将在该变量对循环内为该变量公开。

可能适用于上述内容的 **blog_template.php** ::

    <h1>{blog_title} - {blog_heading}</h1>
    {blog_entries}
        <div>
            <h2>{title}</h2>
            <p>{body}</p>
        </div>
    {/blog_entries}

如果希望 ``blog_entries`` 作用域内的其他伪变量可用,请确保 ``cascadeData`` 选项设置为 true。

注释
========

你可以在模板中用 ``{# #}`` 符号将注释括起来,它们在解析期间将被忽略并删除。

::

    {# 这个注释在解析过程中会被删除。#}
    {blog_entry}
        <div>
            <h2>{title}</h2>
            <p>{body}</p>
        </div>
    {/blog_entry}

数据级联
==============

对于嵌套替换和循环替换,你可以选择将数据对级联到内部替换。

以下示例不受级联的影响:

.. literalinclude:: view_parser/009.php

这个例子的结果与级联的不同:

.. literalinclude:: view_parser/010.php

阻止解析
==================

你可以使用 ``{noparse}`` ``{/noparse}`` 标签对指定不要解析的页面部分。这对括号之间的任何内容都将完全保持原样,不会发生变量替换、循环等。

::

    {noparse}
        <h1>Untouched Code</h1>
    {/noparse}

条件逻辑
=================

解析器类支持一些基本条件来处理 ``if``、``else`` 和 ``elseif`` 语法。所有 ``if`` 块必须用 ``endif`` 标签关闭::

    {if $role=='admin'}
        <h1>Welcome, Admin!</h1>
    {endif}

这简单的块在解析期间转换为以下内容:

.. literalinclude:: view_parser/011.php

if 语句中使用的所有变量必须先以相同的名称设置过。除此之外,它的处理方式与标准 PHP 条件完全相同,这里也将应用所有标准 PHP 规则。你可以使用通常会用到的任何比较运算符,如 ``==``、``===``、``!==``、``<``、``>`` 等。

::

    {if $role=='admin'}
        <h1>Welcome, Admin</h1>
    {elseif $role=='moderator'}
        <h1>Welcome, Moderator</h1>
    {else}
        <h1>Welcome, User</h1>
    {endif}

.. warning:: 在后台,条件语句使用 ``eval()`` 进行解析,所以你必须确保在条件语句中使用的数据来自可信来源,否则可能会面临安全风险。

更改条件分隔符
-----------------------------------

如果你的模板中有像下面的 JavaScript 代码,解析器会抛出语法错误,因为存在可以解释为条件的字符串::

    <script type="text/javascript">
        var f = function() {
            if (hasAlert) {
                alert('{message}');
            }
        }
    </script>

在这种情况下,你可以使用 ``setConditionalDelimiters()`` 方法更改条件分隔符,以避免误解:

.. literalinclude:: view_parser/027.php

在这种情况下,你可以在模板中编写代码::

    {% if $role=='admin' %}
        <h1>Welcome, Admin</h1>
    {% else %}
        <h1>Welcome, User</h1>
    {% endif %}

转义数据
=============

默认情况下,所有变量替换都被转义,以帮助防止页面上的 XSS 攻击。CodeIgniter 的 ``esc()`` 方法支持几种不同的上下文,如常规的 ``html``、HTML ``attr`` 中的、``css`` 中的、``js`` 中的等。如果没有指定其他内容,数据将假定在 HTML 上下文中。你可以使用 ``esc()`` 过滤器指定所使用的上下文::

    { user_styles | esc(css) }
    <a href="{ user_link | esc(attr) }">{ title }</a>

有时你绝对需要使用而不转义的数据。你可以在打开和关闭括号中添加感叹号来实现这一点::

    {! unescaped_var !}

过滤器
=======

可以对单个变量替换应用一个或多个过滤器以修改其呈现方式。这些旨在修改输出,而不是大幅改变它。上面讨论的 ``esc`` 过滤器就是一个例子。日期是另一个常见的用例,其中你可能需要以页面上的几个部分不同的方式格式化同一数据。

过滤器是在伪变量名称之后、用竖线符号 ``|`` 分隔的命令::

    // 显示 -55 为 55
    { value|abs }

如果参数需要任何参数,必须用逗号分隔并用括号括起来::

    { created_at|date(Y-m-d) }

可以通过管道连接多个过滤器来应用值。它们从左到右处理::

    { created_at|date_modify(+5 days)|date(Y-m-d) }

提供的过滤器
----------------

使用解析器时,可用以下过滤器:

================ ================= =========================================================== ======================================
过滤器           参数               描述                                                       示例
================ ================= =========================================================== ======================================
abs                                显示数字的绝对值。                                          { v|abs }

capitalize                         以句子大小写显示字符串:全部小写,第一个字母大写。            { v|capitalize}

date              格式(Y-m-d)      与 PHP **date** 兼容的格式化字符串。                        { v|date(Y-m-d) }

date_modify       要添加/减去的值  与 **strtotime** 兼容的字符串,用于修改日期,                 { v|date_modify(+1 day) }
                                   如 ``+5 day`` 或 ``-1 week``。

default           默认值           如果变量为空或未定义,显示默认值。                           { v|default(just in case) }

esc               html、attr、     指定转义数据的上下文。                                      { v|esc(attr) }
                  css、js

excerpt           短语、半径词数   返回给定短语半径词数内的文本。与 **excerpt** 辅助函数相同。 { v|excerpt(green giant, 20) }

highlight         短语             使用 '<mark></mark>' 标记在文本中突出显示给定短语。         { v|highlight(view parser) }

highlight_code                     使用 HTML/CSS 突出显示代码示例。                            { v|highlight_code }

limit_chars       限制个数         将字符数限制为 $limit。                                     { v|limit_chars(100) }

limit_words       限制个数         将词数限制为 $limit。                                       { v|limit_words(20) }

local_currency    货币、区域设置、 显示货币的本地化版本。“货币”值是任何 3 字节 ISO 4217        { v|local_currency(EUR,en_US) }
                  小数位数         货币代码。

local_number      类型、精度、     显示数字的本地化版本。“类型”可以是:decimal、currency、      { v|local_number(decimal,2,en_US) }
                  区域设置         percent、scientific、spellout、ordinal、duration之一。

lower                              转换字符串为小写。                                          { v|lower }

nl2br                              用 HTML <br/> 标签替换所有换行符(\n)。                      { v|nl2br }

number_format     小数位数         封装 PHP **number_format** 函数以在解析器中使用。           { v|number_format(3) }

prose                              获取一段文本,使用 **auto_typography()** 方法将它转换为      { v|prose }
                                   更美观、更易读的散文。

round             小数位数、类型   按指定位数四舍五入数字。可传递 **ceil** 和 **floor** 类型   { v|round(3) } { v|round(ceil) }
                                   以使用这些函数。

strip_tags        允许的标签       封装 PHP **strip_tags**。可以接受允许的标签字符串。         { v|strip_tags(<br>) }

title                              以“标题大小写”显示字符串,所有小写,每个单词首字母大写。      { v|title }

upper                              将字符串显示为全部大写。                                    { v|upper }
================ ================= =========================================================== ======================================

有关与“local_number”过滤器相关的详细信息，请参阅 `PHP 的 NumberFormatter <https://www.php.net/manual/en/numberformatter.create.php>`_。

自定义过滤器
--------------

您可以通过编辑 **app/Config/View.php** 并向 ``$filters`` 数组中添加新条目来轻松创建自己的过滤器。每个键是视图中调用过滤器的名称，其值是任何有效的 PHP 可调用对象：

.. literalinclude:: view_parser/012.php

解析器插件
==============

插件允许你扩展解析器,为每个项目添加自定义功能。它们可以是任何 PHP 可调用的,因此实现起来非常简单。在模板中,插件由 ``{+ +}`` 标记指定::

    {+ foo +} inner content {+ /foo +}

这个示例显示了一个名为 **foo** 的插件。它可以操作在其打开和关闭标记之间的任何内容。在这个例子中,它可以使用文本 “inner content”。插件在任何伪变量替换发生之前进行处理。

虽然插件通常由标签对组成,如上所示,但它们也可以是一个单标签,没有闭合标签::

    {+ foo +}

打开标签也可以包含可自定义插件工作方式的参数。参数表示为键/值对::

    {+ foo bar=2 baz="x y" +}

参数也可以是单个值::

    {+ include somefile.php +}

提供的插件
----------------

使用解析器时,可用以下插件:

================== ========================= ============================================ ================================================================
插件               参数                      描述                                         示例
================== ========================= ============================================ ================================================================
current_url                                  current_url 辅助函数的别名。                 {+ current_url +}
previous_url                                 previous_url 辅助函数的别名。                {+ previous_url +}
siteURL            “login”                   site_url 辅助函数的别名。                    {+ siteURL "login" +}
mailto             email、标题、属性         mailto 辅助函数的别名。                      {+ mailto email=foo@example.com title="Stranger Things" +}
safe_mailto        email、标题、属性         safe_mailto 辅助函数的别名。                 {+ safe_mailto email=foo@example.com title="Stranger Things" +}
lang               语言字符串                lang 辅助函数的别名。                        {+ lang number.terabyteAbbr +}
validation_errors  字段名(可选)              返回字段的错误字符串(如果指定),              {+ validation_errors +} , {+ validation_errors field="email" +}
route              route 名称                route_to 辅助函数的别名。                    {+ route "login" +}
csp_script_nonce                             csp_script_nonce 辅助函数的别名。            {+ csp_script_nonce +}
csp_style_nonce                              csp_style_nonce 辅助函数的别名。             {+ csp_style_nonce +}
================== ========================= ============================================ ================================================================

注册插件
--------------------

最简单的方法是将新插件添加到 **app/Config/View.php** 中的 ``$plugins`` 数组,即可注册并准备使用新插件。键是模板文件中使用的插件名称。值是任何有效的 PHP 可调用项,包括静态类方法:

.. literalinclude:: view_parser/014.php

你也可以使用闭包,但只能在配置文件的构造函数中定义它们:

.. literalinclude:: view_parser/015.php

如果可调用的独立存在,则将其视为单标签,而不是打开/关闭标签。它将被插件的返回值替换:

.. literalinclude:: view_parser/016.php

如果可调用项包含在数组中,则将其视为打开/关闭标签对,可以操作其标记之间的任何内容:

.. literalinclude:: view_parser/017.php

***********
使用说明
***********

如果包含了模板中未引用的替换参数,会被忽略:

.. literalinclude:: view_parser/018.php

如果不包含模板中引用的替换参数,将显示原始伪变量:

.. literalinclude:: view_parser/019.php

如果为应该是数组的变量对提供字符串替换参数,
即用于变量对,则仅为开始变量对标记执行替换,
但不正确渲染结束变量对标记:

.. literalinclude:: view_parser/020.php

视图片段
==============

你不必使用变量对在视图中实现迭代。可以使用视图片段代替变量对内部的内容,并在控制器中控制迭代。

在视图中控制迭代的示例::

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

在控制器中控制迭代、使用视图片段的示例:

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

        :param  string  $view: 视图源文件的名称
        :param  array   $options: 选项的键/值对数组
        :param  boolean $saveData: 如果为 true,将保存数据供随后调用,如果为 false,在渲染视图后清除数据
        :returns: 所选视图的渲染文本
        :rtype: string

        根据文件名和已设置的任何数据构建输出:

        .. literalinclude:: view_parser/022.php

        支持的选项:

            - ``cache`` - 以秒为单位,保存视图结果的时间
            - ``cache_name`` - 用于保存/检索缓存视图结果的 ID;默认为视图路径
            - ``cascadeData`` - 嵌套或循环替换发生时,当前生效的数据对是否应传播
            - ``saveData`` - 视图数据参数是否应保留以供后续调用

        首先执行任何条件替换,然后对每个数据对执行其余替换。

    .. php:method:: renderString($template[, $options[, $saveData]])

        :param  string  $template: 作为字符串提供的视图源
        :param  array   $options: 选项的键/值对数组
        :param  boolean $saveData: 如果为 true,将保存数据供随后调用,如果为 false,在渲染视图后清除数据
        :returns: 所选视图的渲染文本
        :rtype: string

        根据提供的模板源和已设置的任何数据构建输出:

        .. literalinclude:: view_parser/023.php

        支持的选项和行为与上述相同。

    .. php:method:: setData([$data[, $context = null]])

        :param  array   $data: 视图数据字符串的关联数组,作为键/值对
        :param  string  $context: 用于数据转义的上下文
        :returns: 渲染器,用于方法链
        :rtype: CodeIgniter\\View\\RendererInterface

        一次设置多个视图数据:

        .. literalinclude:: view_parser/024.php

        支持的转义上下文:html、css、js、url 或 attr 或 raw。
        如果是 'raw',将不进行转义。

    .. php:method:: setVar($name[, $value = null[, $context = null]])

        :param  string  $name: 视图数据变量的名称
        :param  mixed   $value: 此视图数据的值
        :param  string  $context: 用于数据转义的上下文
        :returns: 渲染器,用于方法链
        :rtype: CodeIgniter\\View\\RendererInterface

        设置单个视图数据:

        .. literalinclude:: view_parser/025.php

        支持的转义上下文:html、css、js、url、attr 或 raw。
        如果是 'raw',将不进行转义。

    .. php:method:: setDelimiters($leftDelimiter = '{', $rightDelimiter = '}')

        :param  string  $leftDelimiter: 替换字段的左分隔符
        :param  string  $rightDelimiter: 替换字段的右分隔符
        :returns: 渲染器,用于方法链
        :rtype: CodeIgniter\\View\\RendererInterface

        覆盖替换字段分隔符:

        .. literalinclude:: view_parser/026.php

    .. php:method:: setConditionalDelimiters($leftDelimiter = '{', $rightDelimiter = '}')

        :param  string  $leftDelimiter: 条件的左分隔符
        :param  string  $rightDelimiter: 条件的右分隔符
        :returns: 渲染器,用于方法链
        :rtype: CodeIgniter\\View\\RendererInterface

        覆盖条件分隔符:

        .. literalinclude:: view_parser/027.php
