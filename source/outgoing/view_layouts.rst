############
视图布局
############

.. contents::
    :local:
    :depth: 2

CodeIgniter 支持一个简单且非常灵活的布局系统,可以轻松地在整个应用程序中使用一个或多个基本页面布局。布局支持可以从任何被渲染的视图中插入的内容部分。您可以创建不同的布局以支持单列、双列、博客存档页面等。布局从不直接渲染。相反,你渲染一个视图,它指定了它想要扩展的布局。

*****************
创建布局
*****************

布局与任何其他视图一样。唯一的区别在于它们的预期用途。布局是唯一会使用 ``renderSection()`` 方法的视图文件。此方法充当内容的占位符。

例如 **app/Views/default.php**::

    <!doctype html>
    <html>
    <head>
        <title>我的布局</title>
    </head>
    <body>
        <?= $this->renderSection('content') ?>
    </body>
    </html>

``renderSection()`` 方法只有一个参数 - 部分的名称。这样任何子视图都知道要命名内容部分的名称。

**********************
在视图中使用布局
**********************

当一个视图想要插入布局时,它必须在文件顶部使用 ``extend()`` 方法::

    <?= $this->extend('default') ?>

``extend()`` 方法获取希望使用的任何视图文件的名称。由于它们是标准视图,定位它们的方式与定位视图相同。默认情况下,它将在应用程序的视图目录中查找,但也会扫描其他 PSR-4 定义的命名空间。你可以包含命名空间以在特定命名空间的视图目录中查找视图::

    <?= $this->extend('Blog\Views\default') ?>

扩展布局的视图中的所有内容必须包含在 ``section()`` 和 ``endSection()`` 方法调用中。这些调用之间的任何内容都将被插入布局中 ``renderSection($name)`` 调用与部分名称匹配的位置。

例如 **app/Views/some_view.php**::

    <?= $this->extend('default') ?>

    <?= $this->section('content') ?>
        <h1>Hello World!</h1>
    <?= $this->endSection() ?>

``endSection()`` 不需要部分名称。它会自动知道要关闭哪一个。

部分可以包含嵌套部分::

    <?= $this->extend('default') ?>

    <?= $this->section('content') ?>
        <h1>Hello World!</h1>
        <?= $this->section('javascript') ?>
           let a = 'a';
        <?= $this->endSection() ?>
    <?= $this->endSection() ?>

******************
渲染视图
******************

渲染视图及其布局的方式与控制器中显示任何其他视图完全相同:

.. literalinclude:: view_layouts/001.php

它渲染了视图 **app/Views/some_view.php**,如果它扩展了 ``default``,
布局 **app/Views/default.php** 也会自动使用。
渲染器智能到足以检测视图是否应该自行渲染,还是需要布局。

***********************
包含视图局部
***********************

视图局部是不扩展任何布局的视图文件。它们通常包含可以在视图之间重用的内容。当使用视图布局时,你必须使用 ``$this->include()`` 来包含任何视图局部。

::

    <?= $this->extend('default') ?>

    <?= $this->section('content') ?>
        <h1>Hello World!</h1>

        <?= $this->include('sidebar') ?>
    <?= $this->endSection() ?>

调用 ``include()`` 方法时,你可以传递渲染普通视图时可以传递的所有相同选项,包括缓存指令等。
