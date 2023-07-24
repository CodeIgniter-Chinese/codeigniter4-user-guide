#############
视图渲染器
#############

.. contents::
    :local:
    :depth: 2

***********************
使用视图渲染器
***********************

:php:func:`view()` 函数是一个方便的函数,它获取 ``renderer`` 服务的一个实例,设置数据并渲染视图。尽管这通常正是你想要的,但你可能会发现有时你更希望直接与它一起工作。在这种情况下,你可以直接访问视图服务:

.. literalinclude:: view_renderer/001.php
   :lines: 2-

或者,如果你没有使用 ``View`` 类作为默认渲染器,你可以直接实例化它:

.. literalinclude:: view_renderer/002.php
   :lines: 2-

.. important:: 你应该仅在控制器中创建服务。如果你需要从库中访问 View 类,
    应该在库的构造函数中将其设置为依赖项。

然后,你可以使用它提供的三种标准方法中的任何一种:
:php:meth:`render() <CodeIgniter\\View\\View::render()>`、
:php:meth:`setVar() <CodeIgniter\\View\\View::setVar()>` 和
:php:meth:`setData() <CodeIgniter\\View\\View::setData()`。

它的工作原理
============

``View`` 类在提取视图参数为 PHP 变量后处理应用程序视图路径中的常规 HTML/PHP 脚本,
使脚本可以访问它们。这意味着视图参数名称需要是合法的 PHP 变量名称。

View 类在内部使用关联数组来累积视图参数,直到你调用它的 ``render()``。
这意味着你的参数(或变量)名称需要是唯一的,否则后面的变量设置将覆盖早期的设置。

这也会影响根据脚本中的不同上下文对参数值进行转义。
你将必须为每个转义值提供一个唯一的参数名称。

值为数组的参数没有特殊含义。需要你在 PHP 代码中适当处理数组。

设置视图参数
=======================

:php:meth:`setVar() <CodeIgniter\\View\\View::setVar()>` 方法设置一个视图参数。

.. literalinclude:: view_renderer/008.php
   :lines: 2-

:php:meth:`setData() <CodeIgniter\\View\\View::setData()>` 方法一次设置多个视图参数。

.. literalinclude:: view_renderer/007.php
   :lines: 2-

方法链式调用
===============

``setVar()`` 和 ``setData()`` 方法是可链式调用的,允许你将许多不同的调用组合在一起:

.. literalinclude:: view_renderer/003.php
   :lines: 2-

转义数据
=============

当你将数据传递给 ``setVar()`` 和 ``setData()`` 函数时,你可以选择对数据进行转义以防止跨站脚本攻击。作为这两种方法中的最后一个参数,你可以传递所需的上下文来转义数据。请参见下文了解上下文描述。

如果你不想转义数据,可以将 ``'raw'`` 或 ``null`` 作为每个函数的最后一个参数传递:

.. literalinclude:: view_renderer/004.php
   :lines: 2-

如果选择不转义数据,或者正在传递对象实例,则可以在视图中使用 :php:func:`esc()` 函数手动转义数据。第一个参数是要转义的字符串。第二个参数是转义数据的上下文(见下文)::

    <?= esc($object->getStat()) ?>

转义上下文
-----------------

默认情况下, ``esc()`` 以及转而 ``setVar()`` 和 ``setData()`` 函数假设你要转义的数据打算在标准 HTML 中使用。
然而,如果数据打算用于 JavaScript、CSS 或 href 属性中,你需要不同的转义规则才能有效。
你可以将上下文的名称作为第二个参数传递。有效的上下文是 ``'html'``、 ``'js'``、 ``'css'``、 ``'url'`` 和 ``'attr'`` ::

    <a href="<?= esc($url, 'url') ?>" data-foo="<?= esc($bar, 'attr') ?>">Some Link</a>

    <script>
        var siteName = '<?= esc($siteName, 'js') ?>';
    </script>

    <style>
        body {
            background-color: <?= esc('bgColor', 'css') ?>
        }
    </style>

视图渲染器选项
=====================

可以将几个选项传递给 ``render()`` 或 ``renderString()`` 方法:

- ``cache`` - 以秒为单位,保存视图结果的时间;对 renderString() 忽略
- ``cache_name`` - 用于保存/检索缓存视图结果的 ID;默认为视图路径;对 renderString() 忽略
- ``saveData`` - 如果为 true,视图数据参数应保留以供随后的调用

.. note:: 接口要求 ``saveData()`` 必须是布尔值,但实现类(如下面的 ``View``)可以扩展它以包含 ``null`` 值。

***************
类参考
***************

.. php:namespace:: CodeIgniter\View

.. php:class:: View

    .. php:method:: render($view[, $options[, $saveData = false]])

        :param  string       $view: 视图源文件的名称
        :param  array        $options: 选项的键/值对数组
        :param  boolean|null $saveData: 如果为 true,将保存数据供任何其他调用使用。如果为 false,渲染视图后将清除数据。如果为 null,使用配置设置。
        :returns: 所选视图的渲染文本
        :rtype: string

        根据文件名和已设置的数据构建输出:

        .. literalinclude:: view_renderer/005.php
           :lines: 2-

    .. php:method:: renderString($view[, $options[, $saveData = false]])

        :param  string       $view: 要渲染的视图内容,例如从数据库检索的内容
        :param  array        $options: 选项的键/值对数组
        :param  boolean|null $saveData: 如果为 true,将保存数据供任何其他调用使用。如果为 false,渲染视图后将清除数据。如果为 null,使用配置设置。
        :returns: 所选视图的渲染文本
        :rtype: string

        根据视图片段和已设置的数据构建输出:

        .. literalinclude:: view_renderer/006.php
           :lines: 2-

    .. warning:: 这可以用来显示可能存储在数据库中的内容,但你需要注意这是一个潜在的安全漏洞,
        并且你 **必须** 验证任何此类数据,可能适当地对其进行转义!

    .. php:method:: setData([$data[, $context = null]])

        :param  array   $data: 视图数据字符串的关联数组,作为键/值对
        :param  string  $context: 用于数据转义的上下文
        :returns: 渲染器,用于方法链
        :rtype: CodeIgniter\\View\\RendererInterface

        一次设置多个视图数据:

        .. literalinclude:: view_renderer/007.php
           :lines: 2-

        支持的转义上下文:``html``、``css``、``js``、``url`` 或 ``attr`` 或 ``raw``。
        如果是 ``'raw'``,将不进行转义。

        每次调用都会向对象累积的数据数组添加数据,直到渲染视图为止。

    .. php:method:: setVar($name[, $value = null[, $context = null]])

        :param  string  $name: 视图数据变量的名称
        :param  mixed   $value: 此视图数据的值
        :param  string  $context: 用于数据转义的上下文
        :returns: 渲染器,用于方法链
        :rtype: CodeIgniter\\View\\RendererInterface

        设置单个视图数据:

        .. literalinclude:: view_renderer/008.php
           :lines: 2-

        支持的转义上下文: ``html``、``css``、``js``、``url``、``attr`` 或 ``raw``。
        如果是 ``'raw'``,将不进行转义。

        如果你使用先前已对此对象使用过的视图数据变量,新值将替换现有值。
