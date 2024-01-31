################
辅助函数
################

.. contents::
    :local:
    :depth: 2

*****************
什么是辅助函数?
*****************

顾名思义，辅助函数可以帮助你完成任务。每个 helper 文件只是某个特定类别的函数集合。有 :doc:`URL 辅助函数 <../helpers/url_helper>`，可以帮助创建链接，有 :doc:`表单辅助函数 <../helpers/form_helper>` 可以帮助创建表单元素，:doc:`文本辅助函数 <../helpers/text_helper>` 执行各种文本格式化，:doc:`Cookie 辅助函数 <../helpers/cookie_helper>` 设置和读取 Cookie，:doc:`文件系统辅助函数 <../helpers/filesystem_helper>` 帮助处理文件等等。

与 CodeIgniter 中的大多数其他系统不同,辅助函数不是面向对象的格式。它们是简单的程序性函数。每个辅助函数执行一个特定的任务,不依赖于其他函数。

CodeIgniter 默认不加载辅助文件,所以使用辅助函数的第一步是加载它。一旦加载,它就可以在你的 :doc:`控制器 <../incoming/controllers>` 和 :doc:`视图 <../outgoing/views>` 中全局使用。

辅助函数通常存储在 **system/Helpers** 或 **app/Helpers** 目录中。

****************
加载辅助函数
****************

.. note:: :doc:`../helpers/url_helper` 总是加载的,所以你不需要自己加载它。

加载单个辅助函数
================

使用以下方法加载辅助函数文件非常简单:

.. literalinclude:: helpers/001.php

上述代码会加载 **name_helper.php** 文件。

.. important:: CodeIgniter 辅助函数文件名全部小写。因此,在区分大小写的文件系统(如 Linux)上, ``helper('Name')`` 将无法工作。

例如,要加载名为 **cookie_helper.php** 的 :doc:`../helpers/cookie_helper` 文件,你会这样做:

.. literalinclude:: helpers/002.php

.. note:: :php:func:`helper()` 函数不返回值,所以不要试图将其分配给变量。只按上面示例的方式使用它。

自动发现和 Composer 包
------------------------

默认情况下，CodeIgniter 会通过 :ref:`auto-discovery` 在所有定义的命名空间中搜索辅助函数文件。
你可以使用 spark 命令来检查你定义的命名空间。请参阅 :ref:`confirming-namespaces`。

如果你使用了许多 Composer 包，那么你将有许多已定义的命名空间。
CodeIgniter 默认会扫描所有命名空间。

为了避免浪费时间扫描不相关的 Composer 包，你可以手动指定要进行自动发现的包。请参阅 :ref:`modules-specify-composer-packages` 了解详细信息。

或者，你可以为要加载的辅助函数 :ref:`指定一个命名空间 <helpers-loading-from-specified-namespace>`。

加载顺序
----------

:php:func:`helper()` 函数会扫描通过所有定义的命名空间，并加载所有名称匹配的辅助函数。这样可以加载任何模块的辅助函数，以及你为此应用专门创建的任何辅助函数。

加载顺序如下：

1. app/Helpers - 这里的文件总是首先加载。
2. {namespace}/Helpers - 所有的命名空间都会按照它们定义的顺序依次循环。
3. system/Helpers - 基础文件最后加载。

加载多个辅助函数
========================

如果你需要一次加载多个辅助函数,可以传递一个文件名数组,它们都会被加载:

.. literalinclude:: helpers/003.php

在控制器中加载
=======================

可以在控制器方法中的任何位置加载辅助函数(甚至在视图文件中,尽管这不是一个好的实践),只要在使用它之前加载它即可。

你可以在控制器构造函数中加载辅助函数,以使它们自动在任何方法中可用,或者你可以在需要它的特定方法中加载辅助函数。

但是,如果你想在控制器构造函数中加载,则可以改用 Controller 中的 ``$helpers`` 属性。参见 :ref:`控制器 <controllers-helpers>`。

.. _helpers-loading-from-specified-namespace:

从指定命名空间加载
================================

默认情况下，CodeIgniter 会在所有定义的命名空间中搜索辅助函数文件，并加载所有找到的文件。

如果你只想加载特定命名空间中的一个辅助函数，在辅助函数的名称前加上它所在的命名空间作为前缀。在该命名空间目录中，加载器预期它位于一个名为 **Helpers** 的子目录内。以示例来帮助理解这一点。

对于此示例,假设我们已经将所有与博客相关的代码分组到自己的命名空间 ``Example\Blog`` 中。文件存在于我们的服务器上的 **Modules/Blog/** 中。因此,我们会将博客模块的辅助函数文件放在 **Modules/Blog/Helpers/** 中。**blog_helper** 文件将位于 **Modules/Blog/Helpers/blog_helper.php**。在我们的控制器中,我们可以使用以下命令加载辅助函数:

.. literalinclude:: helpers/004.php

你也可以使用以下方式:

.. literalinclude:: helpers/007.php

.. note:: 以这种方式加载的文件中的函数并不是真正的命名空间化的。命名空间只是用作方便定位文件的一种方式。

.. _auto-loading-helpers:

自动加载辅助函数
====================

.. versionadded:: 4.3.0

如果你发现整个应用程序都需要一个特定的辅助函数,你可以告诉 CodeIgniter 在系统初始化期间自动加载它。
这是通过打开 **app/Config/Autoload.php** 文件,并将辅助函数添加到 ``$helpers`` 属性来完成的。

**************
使用辅助函数
**************

一旦你加载了包含要使用的函数的辅助文件,你就可以像调用标准 PHP 函数一样调用它。

例如,要在视图文件中使用 :php:func:`anchor()` 函数创建一个链接,你会这样做:

.. literalinclude:: helpers/005.php

其中 “Click Here” 是链接的名称,“blog/comments” 是你想要链接到的控制器/方法的 URI。

****************
创建辅助函数
****************

创建自定义辅助函数
=======================

辅助函数文件名是 **辅助函数名** 和 **_helper.php**。

例如，要创建 info 辅助函数，你需要创建一个名为
**app/Helpers/info_helper.php** 的文件，并向文件中添加一个函数：

.. literalinclude:: helpers/008.php

你可以在一个辅助函数文件中添加尽可能多的函数。

“扩展”辅助函数
===================

要“扩展”辅助函数,请在 **app/Helpers** 文件夹中创建一个与现有辅助函数相同名称的文件。

如果你只需要为现有辅助函数添加一些功能 - 可能添加一个或两个函数,或者更改某个特定辅助函数的工作方式 - 那么用你的版本完全替换整个辅助函数有点过度设计。在这种情况下,最好只是“扩展”辅助函数。

.. note:: 这里“扩展”一词使用很宽松,因为辅助函数是程序性的和离散的,在传统意义上无法扩展。在底层,这为你提供了添加或替换辅助函数提供的函数的能力。

例如,要扩展原生的 **Array 辅助函数**,你需要创建一个名为 **app/Helpers/array_helper.php** 的文件,并添加或覆盖函数:

.. literalinclude:: helpers/006.php

.. important:: 不要指定命名空间 ``App\Helpers``。

参见 `加载顺序`_ 了解辅助函数文件的加载顺序。

*********
接下来呢?
*********

在目录中,你会找到所有可用 :doc:`辅助函数 <../helpers/index>` 的列表。浏览每个函数以查看它们的作用。
