################
辅助函数
################

.. contents::
    :local:
    :depth: 2

*****************
什么是辅助函数？
*****************

顾名思义，辅助函数就是帮助你完成任务的函数。每个辅助函数文件都只是某个特定类别中的函数集合。
:doc:`URL 辅助函数 <../helpers/url_helper>` 可帮助创建链接，
:doc:`表单辅助函数 <../helpers/form_helper>` 可帮助创建表单元素，
:doc:`文本辅助函数 <../helpers/text_helper>` 执行各种文本格式化操作，
:doc:`Cookie 辅助函数 <../helpers/cookie_helper>` 设置和读取 Cookie，
:doc:`文件系统辅助函数 <../helpers/filesystem_helper>` 帮助处理文件等。

与 CodeIgniter 中的大多数其他系统不同，辅助函数不是以
面向对象格式编写的。它们是简单的、过程化的函数。每个
辅助函数执行一个特定任务，不依赖于其他函数。

CodeIgniter 默认不会加载辅助函数文件，所以使用辅助函数的
第一步是加载它。一旦加载，它就在你的 :doc:`控制器 <../incoming/controllers>` 和
:doc:`视图 <../outgoing/views>` 中全局可用。

辅助函数通常存储在 **system/Helpers** 或 **app/Helpers** 目录中。

***************
加载辅助函数
***************

.. note:: :doc:`../helpers/url_helper` 总是已加载的，所以你不需要自己加载。

加载辅助函数
================

使用以下方法加载辅助函数文件非常简单：

.. literalinclude:: helpers/001.php

上述代码会加载 **name_helper.php** 文件。

.. important:: CodeIgniter 辅助函数文件名全部是小写。
    因此，在区分大小写的文件系统（如 Linux）上，
    ``helper('Name')`` 将无法工作。

例如，要加载名为 **cookie_helper.php** 的 :doc:`../helpers/cookie_helper` 文件，
你需要这样做：

.. literalinclude:: helpers/002.php

.. note:: :php:func:`helper()` 函数不返回值，
    所以不要尝试将其赋值给变量。只需按所示使用即可。

自动发现和 Composer 包
------------------------------------

默认情况下，CodeIgniter 会通过 :ref:`auto-discovery` 在所有已定义的命名空间中
搜索辅助函数文件。
你可以通过 spark 命令检查已定义的命名空间。参见 :ref:`confirming-namespaces`。

如果你使用了许多 Composer 包，你将有许多已定义的命名空间。
CodeIgniter 默认会扫描所有命名空间。

为了避免浪费时间扫描不相关的 Composer 包，你可以手动
指定用于自动发现的包。详细信息参见 :ref:`modules-specify-composer-packages`。

或者你可以为要加载的辅助函数 :ref:`指定命名空间 <helpers-loading-from-specified-namespace>`。

加载顺序
----------

:php:func:`helper()` 函数会扫描所有已定义的命名空间并加载所有
名称匹配的辅助函数。这样可以加载任何模块的辅助函数，
以及你专门为这个应用程序创建的任何辅助函数。

加载顺序如下：

1. app/Helpers - 这里的文件总是首先加载。
2. {namespace}/Helpers - 所有命名空间按照定义的顺序循环处理。
3. system/Helpers - 基础文件最后加载。

加载多个辅助函数
========================

如果需要一次加载多个辅助函数，你可以传入一个文件名数组，
所有这些辅助函数都将被加载：

.. literalinclude:: helpers/003.php

在控制器中加载
=======================

辅助函数可以在控制器方法中的任何地方加载（甚至可以在视图文件中加载，
尽管这不是好的做法），只要在使用之前加载即可。

你可以在控制器构造函数中加载辅助函数，
这样它们在任何方法中都自动可用，或者也可以在需要它们的
特定方法中加载辅助函数。

但是如果你想在控制器构造函数中加载，可以使用 Controller 中的 ``$helpers``
属性。参见 :ref:`控制器 <controllers-helpers>`。

.. _helpers-loading-from-specified-namespace:

从指定命名空间加载
================================

默认情况下，CodeIgniter 会在所有已定义的命名空间中搜索辅助函数文件并加载所有找到的文件。

如果你只想加载特定命名空间中的辅助函数，可以在辅助函数名称前加上
可以找到它的命名空间前缀。在该命名空间目录中，
加载器期望它位于名为 **Helpers** 的子目录中。例子将帮助理解这一点。

在这个例子中，假设我们已将所有与博客相关的代码分组到自己的命名空间 ``Example\Blog`` 中。
文件存在于服务器上的 **Modules/Blog/** 目录中。
因此，我们将博客模块的辅助函数文件放在 **Modules/Blog/Helpers/** 中。
**blog_helper** 文件将位于 **Modules/Blog/Helpers/blog_helper.php**。
在控制器中，我们可以使用以下命令为加载辅助函数：

.. literalinclude:: helpers/004.php

你也可以使用以下方式：

.. literalinclude:: helpers/007.php

.. note:: 以这种方式加载的文件中的函数并非真正具有命名空间。
    命名空间只是作为定位文件的便捷方式。

.. _auto-loading-helpers:

自动加载辅助函数
====================

.. versionadded:: 4.3.0

如果你发现需要在整个应用程序中全局使用某个特定的辅助函数，
你可以告诉 CodeIgniter 在系统初始化期间自动加载它。
这是通过打开 **app/Config/Autoload.php** 文件
并将辅助函数添加到 ``$helpers`` 属性来完成的。

**************
使用辅助函数
**************

一旦加载了包含你打算使用的函数的辅助函数文件，
你就可以像调用标准 PHP 函数一样调用它。

例如，要在视图文件之一中使用 :php:func:`anchor()` 函数创建链接，
你可以这样做：

.. literalinclude:: helpers/005.php

其中 ``Click Here`` 是链接的名称，``blog/comments`` 是你希望链接到的
控制器/方法的 URI。

****************
创建辅助函数
****************

创建自定义辅助函数
=======================

辅助函数文件名是 **辅助函数名称** 加上 **_helper.php**。

例如，要创建 info 辅助函数，你需要创建一个名为
**app/Helpers/info_helper.php** 的文件，并向该文件添加一个函数：

.. literalinclude:: helpers/008.php

你可以根据需要向单个辅助函数文件添加任意数量的函数。

"扩展"辅助函数
===================

要"扩展"辅助函数，请在你的 **app/Helpers** 文件夹中创建一个
与现有辅助函数同名的文件。

如果你只需要为现有辅助函数添加一些功能——
也许添加一两个函数，或更改特定辅助函数函数的操作方式——
那么用你的版本替换整个辅助函数就太过头了。在这种情况下，
最好简单地"扩展"辅助函数。

.. note:: "扩展"这个术语是宽松使用的，因为辅助函数是
    过程化和离散的，不能在传统的程序意义上进行扩展。
    在底层，这使你能够添加或替换辅助函数提供的函数。

例如，要扩展原生 **Array 辅助函数**，你需要创建一个
名为 **app/Helpers/array_helper.php** 的文件，并添加或覆盖函数：

.. literalinclude:: helpers/006.php

.. important:: 不要指定命名空间 ``App\Helpers``。

关于辅助函数文件的加载顺序，请参见 `加载顺序`_。

*********
下一步？
*********

在目录中，你会找到所有可用的 :doc:`辅助函数 <../helpers/index>` 列表。
浏览每个辅助函数以了解它们的功能。
