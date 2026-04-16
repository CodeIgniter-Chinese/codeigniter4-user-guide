#############
视图渲染器
#############

.. contents::
    :local:
    :depth: 2

***********************
使用视图渲染器
***********************

:php:func:`view()` 函数是一个便捷函数，用于获取 ``renderer`` 服务实例、设置数据并渲染视图。虽然该函数通常能满足大部分需求，但有时可能需要更直接的操作。此时可直接访问视图服务：

.. literalinclude:: view_renderer/001.php
   :lines: 2-

此外，如果没有使用 ``View`` 类作为默认渲染器，也可以直接实例化：

.. literalinclude:: view_renderer/002.php
   :lines: 2-

.. important:: 请仅在控制器中创建服务。如果需要在类库中访问 View 类，应在类库的构造函数中将其设置为依赖项。

然后可使用该类提供的三个标准方法：
:php:meth:`render() <CodeIgniter\\View\\View::render()>`、
:php:meth:`setVar() <CodeIgniter\\View\\View::setVar()>` 和
:php:meth:`setData() <CodeIgniter\\View\\View::setData()>`。

工作原理
============

``View`` 类用于处理存储在应用视图路径下的常规 HTML/PHP 脚本。该类会将视图参数提取为 PHP 变量，
以便在脚本中直接访问。因此，视图参数名必须符合 PHP 变量命名规范。

View 类内部使用关联数组累积视图参数，直到调用 ``render()``。
由于这一机制，参数（或变量）名必须唯一，否则后续设置的变量将覆盖先前的值。

这也涉及到脚本中针对不同上下文的参数转义：
每个转义值都必须分配唯一的参数名。

框架不对值为数组的参数作特殊处理，需在 PHP 代码中自行处理该数组。

设置视图参数
=======================

:php:meth:`setVar() <CodeIgniter\\View\\View::setVar()>` 方法用于设置单个视图参数。

.. literalinclude:: view_renderer/008.php
   :lines: 2-

:php:meth:`setData() <CodeIgniter\\View\\View::setData()>` 方法可一次性设置多个视图参数。

.. literalinclude:: view_renderer/007.php
   :lines: 2-

方法链式调用
===============

``setVar()`` 和 ``setData()`` 方法支持链式调用，可以将多个调用串联在一起：

.. literalinclude:: view_renderer/003.php
   :lines: 2-

转义数据
=============

向 ``setVar()`` 和 ``setData()`` 函数传递数据时，可选择转义数据以防止跨站脚本攻击（XSS）。在这两个方法的最后一个参数中，可传入目标上下文来转义数据。详见下面的上下文说明。

如果无需转义数据，可向每个函数的最后一个参数传入 ``null`` 或 ``'raw'``：

.. literalinclude:: view_renderer/004.php
   :lines: 2-

如果选择不转义数据，或者传入的是对象实例，可在视图中通过 :php:func:`esc()` 函数手动转义数据。第一个参数是要转义的字符串，第二个参数是数据的目标上下文（见下文）::

    <?= esc($object->getStat()) ?>

转义上下文
-----------------

默认情况下，``esc()`` 函数以及间接调用的 ``setVar()`` 和 ``setData()`` 函数会假设要转义的数据用于标准 HTML 环境。但如果数据用于 JavaScript、CSS 或 href 属性，则需要不同的转义规则才能生效。可将上下文名称作为第二个参数传入。有效的上下文有 ``'html'``、``'js'``、``'css'``、``'url'`` 和 ``'attr'``::

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

可以向 ``render()`` 或 ``renderString()`` 方法传入以下选项：

- ``$options``

    - ``cache`` - 保存视图结果的缓存时间（秒）；``renderString()`` 忽略此项。
    - ``cache_name`` - 用于保存/检索缓存视图结果的 ID；默认为 ``$viewPath``；``renderString()`` 忽略此项。
    - ``debug`` - 可设置为 ``false`` 以禁用调试代码的添加，用于 :ref:`调试工具栏 <the-debug-toolbar>`。
- ``$saveData`` - 为 ``true`` 时，视图数据参数将在后续调用中保留。

.. note:: 接口定义的 ``$saveData`` 必须是布尔值，但实现类（如下文的 ``View``）可扩展为支持 ``null`` 值。

***************
类参考
***************

.. php:namespace:: CodeIgniter\View

.. php:class:: View

    .. php:method:: render($view[, $options[, $saveData = false]])

        :param  string       $view: 视图源文件的文件名
        :param  array        $options: 选项数组，以键值对形式
        :param  boolean|null $saveData: 如果为 true，将保存数据供其他调用使用。如果为 false，将在渲染视图后清除数据。如果为 null，将使用配置设置。
        :returns: 所选视图渲染后的文本
        :rtype: string

        根据文件名和已设置的数据构建输出：

        .. literalinclude:: view_renderer/005.php
           :lines: 2-

    .. php:method:: renderString($view[, $options[, $saveData = false]])

        :param  string       $view: 要渲染的视图片段内容，例如从数据库获取的内容
        :param  array        $options: 选项数组，以键值对形式
        :param  boolean|null $saveData: 如果为 true，将保存数据供其他调用使用。如果为 false，将在渲染视图后清除数据。如果为 null，将使用配置设置。
        :returns: 所选视图渲染后的文本
        :rtype: string

        根据视图片段和已设置的数据构建输出：

        .. literalinclude:: view_renderer/006.php
           :lines: 2-

    .. warning:: 此方法可用于展示可能存储在数据库中的内容，
        但需要注意这是潜在的安全隐患，
        必须对这类数据进行验证，并且可能需要适当转义！

    .. php:method:: setData([$data[, $context = null]])

        :param  array   $data: 视图数据的关联数组
        :param  string  $context: 用于数据转义的上下文。
        :returns: Renderer 实例，用于方法链
        :rtype: CodeIgniter\\View\\RendererInterface。

        一次性设置多段视图数据：

        .. literalinclude:: view_renderer/007.php
           :lines: 2-

        支持的转义上下文：``html``、``css``、``js``、``url``、``attr`` 或 ``raw``。
        如果为 ``'raw'``，则不进行转义。

        每次调用都会向对象正在累积的数据数组中添加内容，
        直到视图被渲染为止。

    .. php:method:: setVar($name[, $value = null[, $context = null]])

        :param  string  $name: 视图数据变量名
        :param  mixed   $value: 此视图数据的值
        :param  string  $context: 用于数据转义的上下文。
        :returns: Renderer 实例，用于方法链
        :rtype: CodeIgniter\\View\\RendererInterface。

        设置单个视图数据：

        .. literalinclude:: view_renderer/008.php
           :lines: 2-

        支持的转义上下文：``html``、``css``、``js``、``url``、``attr`` 或 ``raw``。
        如果为 ``'raw'``，则不进行转义。

        如果使用之前已为该对象使用过的视图数据变量名，
        新值将替换旧值。
