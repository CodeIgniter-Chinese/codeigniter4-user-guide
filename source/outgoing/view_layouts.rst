############
视图布局
############

.. contents::
    :local:
    :depth: 2

CodeIgniter 提供了一套简洁且灵活的布局系统，支持在整个应用中轻松复用一个或多个基础页面布局。
布局支持内容区块，可从任何渲染的视图中注入内容。开发者可根据需求创建单栏、双栏、博客归档等多种布局方案。
布局文件本身并不直接渲染，而是在渲染视图时，由视图指定其需要扩展的布局。

.. _creating-a-layout:

*****************
创建布局
*****************

布局本质上与普通视图相同，唯一的区别在于用途。布局是唯一会使用
``renderSection()`` 方法的视图文件。该方法充当内容的占位符。

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

``renderSection()`` 方法接受两个参数：``$sectionName`` 和 ``$saveData``。
``$sectionName`` 是子视图用来命名内容区块的名称。如果布尔参数 ``$saveData``
设为 true，该方法会保存数据以供后续调用使用；否则，方法会在显示内容后清除数据。

例如 **app/Views/welcome_message.php**::

    <!doctype html>
    <html>
    <head>
        <title><?= $this->renderSection('page_title', true) ?></title>
    </head>
    <body>
        <h1><?= $this->renderSection('page_title') ?><h1>
        <p><?= $this->renderSection('content') ?></p>
    </body>
    </html>

.. note:: ``$saveData`` 自 v4.4.0 起可用。

**********************
在视图中使用布局
**********************

视图如需嵌入布局，必须在文件顶部调用 ``extend()`` 方法::

    <?= $this->extend('default') ?>

``extend()`` 方法接收所需视图文件的名称。由于此类文件属于标准视图，其定位方式与普通视图完全一致。
默认情况下，系统会在应用的视图目录中查找，同时也会扫描其他符合 PSR-4 规范的命名空间。
若需从特定命名空间的视图目录中加载，可在路径中指定命名空间::

    <?= $this->extend('Blog\Views\default') ?>

扩展布局的视图中，所有内容都必须包含在 ``section($name)`` 和 ``endSection()``
方法调用之间。这些调用之间的内容将插入到布局中匹配的 ``renderSection($name)``
调用所在的位置。

例如 **app/Views/some_view.php**::

    <?= $this->extend('default') ?>

    <?= $this->section('content') ?>
        <h1>Hello World!</h1>
    <?= $this->endSection() ?>

``endSection()`` 无需指定区块名称，系统会自动识别并关闭当前区块。

区块可以嵌套::

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

在控制器中渲染视图及其布局的方式与渲染其他视图完全相同：

.. literalinclude:: view_layouts/001.php

系统渲染 **app/Views/some_view.php** 视图时，若该视图扩展了 ``default``，
则会自动应用 **app/Views/default.php** 布局。
渲染器能智能检测视图是应当独立渲染，还是需要配合布局。

***********************
引入视图局部组件
***********************

视图局部组件是指不扩展任何布局的视图文件，通常用于存放可在不同视图间复用的内容。
在使用视图布局时，必须通过 ``$this->include()`` 引入局部组件。

::

    <?= $this->extend('default') ?>

    <?= $this->section('content') ?>
        <h1>Hello World!</h1>

        <?= $this->include('sidebar') ?>
    <?= $this->endSection() ?>

调用 ``include()`` 方法时，可传入与渲染普通视图相同的所有选项，包括缓存指令等。
