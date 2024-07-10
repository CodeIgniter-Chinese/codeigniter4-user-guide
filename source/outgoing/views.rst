#####
视图
#####

.. contents::
    :local:
    :depth: 2

视图只是一个网页或页面片段,例如头部、尾部、侧边栏等。事实上,如果需要这种层次结构,可以将视图灵活地嵌入其他视图(嵌入其他视图等)。

视图从不直接调用,它们必须由控制器或 :ref:`视图路由 <view-routes>` 加载。

请记住,在 MVC 框架中,控制器充当交通警察角色,因此它负责获取特定视图。如果你还没有阅读 :doc:`控制器 </incoming/controllers>` 页面,在继续之前应该阅读它。

使用你在控制器页面中创建的示例控制器,让我们为它添加一个视图。

创建视图
===============

使用你的文本编辑器,创建一个名为 **blog_view.php** 的文件,并将此内容放入其中::

    <html>
        <head>
            <title>我的博客</title>
        </head>
        <body>
            <h1>欢迎访问我的博客!</h1>
        </body>
    </html>

然后将该文件保存到你的 **app/Views** 目录中。

显示视图
=================

要加载和显示特定的视图文件，你可以在控制器中使用 :php:func:`view()` 函数，如以下代码所示：

.. literalinclude:: views/001.php
   :lines: 2-

其中 *name* 是你的视图文件的名称。

.. important:: 如果省略了文件扩展名,则视图预期以 **.php** 扩展名结尾。

.. note:: ``view()`` 函数内部使用了 :doc:`view_renderer`。

现在,在 **app/Controllers** 目录中创建一个名为 **Blog.php** 的文件,并将此内容放入其中:

.. literalinclude:: views/002.php

打开位于 **app/Config/Routes.php** 的路由文件,并查找“路由定义”。
添加以下代码:

.. literalinclude:: views/013.php
   :lines: 2-

如果你访问你的网站,应该可以看到你的新视图。URL 类似于这样::

    example.com/index.php/blog/

加载多个视图
======================

CodeIgniter 会智能地处理控制器内对 :php:func:`view()` 的多次调用。如果发生多次调用，它们将被拼接在一起。

例如，你可能希望有一个头部视图、一个菜单视图、一个内容视图和一个底部视图。代码可能如下所示：

.. literalinclude:: views/003.php

在上面的示例中,我们使用了“动态添加的数据”,稍后你会看到。

在子目录中存储视图
====================================

如果你更喜欢那种组织方式,也可以将视图文件存储在子目录中。
在这种情况下,在加载视图时需要包括目录名称。例如:

.. literalinclude:: views/004.php
   :lines: 2-

.. _namespaced-views:

命名空间视图
================

你可以在命名空间下的 **View** 目录中存储视图,并加载那个视图,就像它带有命名空间一样。
尽管 PHP 不支持从命名空间加载非类文件,但 CodeIgniter 提供了这个功能,以便以模块化的方式打包视图以进行轻松重用或分发。

如果你在 :doc:`自动加载器 </concepts/autoloader>` 中有一个映射了 PSR-4 命名空间 ``Example\Blog`` 的
**example/blog** 目录,你可以像命名空间一样检索视图文件。

按照此示例,你可以通过在视图名称前加上命名空间来加载 **example/blog/Views** 中的 **blog_view.php** 文件:

.. literalinclude:: views/005.php

.. _caching-views:

缓存视图
=============

你可以通过在 :php:func:`view()` 函数的第三个参数中传递一个 ``cache`` 选项，并指定缓存视图的秒数来缓存视图：

.. literalinclude:: views/006.php
   :lines: 2-

默认情况下,视图将使用视图文件本身的相同名称进行缓存。你可以通过传递 ``cache_name`` 和希望使用的缓存 ID 来自定义此名称:

.. literalinclude:: views/007.php
   :lines: 2-

向视图添加动态数据
===============================

数据通过 :php:func:`view()` 函数的第二个参数以数组的形式从控制器传递到视图。

这里有个例子：

.. literalinclude:: views/008.php
   :lines: 2-

让我们在控制器文件中试一试。打开它并添加这段代码:

.. literalinclude:: views/009.php

现在打开你的视图文件,并将文本更改为与数据数组中的数组键对应的参数:

.. literalinclude:: views/012.php

然后在你一直使用的 URL 加载页面,你应该可以看到变量被替换了。

saveData 选项
-------------------

传递的数据在后续对 :php:func:`view()` 的调用中会被保留。如果你在单个请求中多次调用该函数，你不需要每次都将所需数据传递给每个 ``view()``。

但这可能无法防止任何数据“渗透”到其他视图中,从而潜在地造成问题。如果你更喜欢在一次调用后清除数据,可以将 ``saveData`` 选项传递到第三个参数中的 ``$option`` 数组中。

.. literalinclude:: views/010.php
   :lines: 2-

另外,如果你希望 ``view()`` 函数的默认功能是在调用之间清除数据,可以在 **app/Config/Views.php** 中将 ``$saveData`` 设置为 ``false``。

创建循环
==============

你传递给视图文件的数组不限于简单变量。你可以传递多维数组,它可以循环以生成多行。例如,如果从数据库中拉取数据,它通常以多维数组的形式出现。

这是一个简单的例子。将此内容添加到你的控制器中:

.. literalinclude:: views/011.php

现在打开你的视图文件并创建一个循环:

.. literalinclude:: views/012.php
