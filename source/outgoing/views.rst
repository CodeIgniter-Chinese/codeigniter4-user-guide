#####
视图
#####

.. contents::
    :local:
    :depth: 2

视图本质上是网页或页面片段（如页眉、页脚、侧边栏等）。实际上，视图支持灵活嵌套；如有层级需求，可将视图嵌入其他视图，甚至实现多层嵌套。

视图无法直接调用，必须通过控制器或 :ref:`视图路由 <view-routes>` 加载。

在 MVC 架构中，控制器承担着“交通指挥”的角色，负责调取特定视图。如尚未阅读 :doc:`控制器 </incoming/controllers>` 章节，建议在继续前先行阅读。

下面以此前创建的示例控制器为例，演示如何添加视图。

创建视图
===============

使用文本编辑器创建名为 **blog_view.php** 的文件，内容如下::

    <html>
        <head>
            <title>My Blog</title>
        </head>
        <body>
            <h1>Welcome to my Blog!</h1>
        </body>
    </html>

然后将文件保存到 **app/Views** 目录。

显示视图
=================

要加载并显示特定视图文件，在控制器中使用 :php:func:`view()` 函数，代码如下：

.. literalinclude:: views/001.php
   :lines: 2-

其中 *name* 为视图文件名。

.. important:: 省略文件扩展名时，视图文件默认以 **.php** 为扩展名。

.. note:: ``view()`` 函数内部使用 :doc:`view_renderer`。

在 **app/Controllers** 目录中创建名为 **Blog.php** 的文件，内容如下：

.. literalinclude:: views/002.php

打开位于 **app/Config/Routes.php** 的路由文件，找到"Route Definitions"部分，
添加以下代码：

.. literalinclude:: views/013.php
   :lines: 2-

访问站点即可看到新视图。URL 大致如下::

    example.com/index.php/blog/

加载多个视图
======================

CodeIgniter 会智能处理控制器中对 :php:func:`view()` 的多次调用。如果发生多次调用，结果会拼接在一起。

例如，可能需要一个页眉视图、一个菜单视图、一个内容视图和一个页脚视图。大致如下：

.. literalinclude:: views/003.php

上例中使用了"动态添加的数据"，见下文说明。

将视图存储在子目录中
====================================

如果希望更有条理，视图文件也可以存储在子目录中。
此时加载视图时需要在文件名中包含目录路径。示例：

.. literalinclude:: views/004.php
   :lines: 2-

.. _namespaced-views:

命名空间视图
================

可以将视图存储在命名空间下的 **View** 目录中，然后像使用命名空间一样加载该视图。
虽然 PHP 不支持从命名空间加载非类文件，CodeIgniter 提供了此功能，
使视图可以像模块一样打包，便于复用或分发。

如果 **example/blog** 目录在 :doc:`自动加载器 </concepts/autoloader>` 中配置了 PSR-4 映射，
命名空间为 ``Example\Blog``，则可以像使用命名空间一样加载视图文件。

按照此示例，可以在 **example/blog/Views** 中加载 **blog_view.php** 文件，
只需在视图名前加上命名空间前缀：

.. literalinclude:: views/005.php

.. _caching-views:

缓存视图
=============

使用 :php:func:`view()` 函数可以缓存视图，在第三个参数中传入 ``cache`` 选项，
指定缓存秒数：

.. literalinclude:: views/006.php
   :lines: 2-

默认情况下，视图以视图文件名作为缓存名。可通过传入 ``cache_name`` 和期望的缓存 ID 来自定义：

.. literalinclude:: views/007.php
   :lines: 2-

向视图添加动态数据
===============================

数据通过 :php:func:`view()` 函数的第二个参数（数组形式）从控制器传递给视图。

示例如下：

.. literalinclude:: views/008.php
   :lines: 2-

在控制器文件中试试。打开控制器并添加以下代码：

.. literalinclude:: views/009.php

然后打开视图文件，将文本替换为与数据数组键对应的变量::

    <html>
        <head>
            <title><?= esc($title) ?></title>
        </head>
        <body>
            <h1><?= esc($heading) ?></h1>
        </body>
    </html>

通过之前使用的 URL 加载页面，即可看到变量被替换为对应值。

saveData 选项
-------------------

传入的数据会在后续 :php:func:`view()` 调用中保留。如果
在同一次请求中多次调用该函数，无需在每次 ``view()`` 时重复传入数据。

但这可能导致数据"渗透"到其他视图中，潜在引发问题。如果希望在每次调用后清理数据，
可在第三个参数的 ``$option`` 数组中传入 ``saveData`` 选项。

.. literalinclude:: views/010.php
   :lines: 2-

此外，如果希望 ``view()`` 函数的默认行为就是每次调用后清除数据，
可以在 **app/Config/Views.php** 中将 ``$saveData`` 设置为 ``false``。

创建循环
==============

传递给视图文件的数组不限于简单变量，还可以传递多维数组，
通过循环生成多行数据。例如，从数据库获取的数据通常是多维数组格式。

简单示例如下。在控制器中添加以下代码：

.. literalinclude:: views/011.php

然后打开视图文件，创建循环：

.. literalinclude:: views/012.php
