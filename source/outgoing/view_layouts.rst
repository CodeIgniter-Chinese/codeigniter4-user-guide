########
视图布局
########

.. contents::
    :local:
    :depth: 2

CodeIgniter 提供了一个简单但非常灵活的布局系统，使你可以轻松地在整个 web 应用程序中使用一个或多个基本页面布局。
布局支持在任何渲染视图中插入内容节。你可以通过创建不同的布局来支持一栏、两栏或博客存档页面等。布局不会直接被渲染，
但可以通过渲染一个视图（View），而该视图可以指定要扩展的布局（Layout）来实现（渲染布局）。

********
创建布局
********

布局和其他视图一样。它们唯一的区别是它们的用途。布局就是使用 ``renderSection()`` 方法的视图文件。这个方法会充当内容的占位符。

::

    <!doctype html>
    <html>
    <head>
        <title>My Layout</title>
    </head>
    <body>
        <?= $this->renderSection('content') ?>
    </body>
    </html>

renderSection() 方法只有一个参数，那就是节的名称，这样所有子视图就都可以知道节的名称。

****************
在视图中使用布局
****************

无论何时需要把视图插入到布局中时，都必须在文件开头使用 ``extend()`` 方法： ::

    <?= $this->extend('default') ?>

extend() 方法采用你所希望使用的视图文件的名称。由于它们也是视图，因此它们的位置就像视图一样。默认情况下，
会在应用程序的 View 目录中查找它们，但还会扫描其他 PSR-4 定义的命名空间。你还可以加上一个命名空间以在特定名称空间的 View 目录中定位视图： ::

    <?= $this->extend('Blog\Views\default') ?>

拓展布局所有内容时，必须包含 ``section($name)`` 和 ``endSection()`` 方法的调用。这些调用之间的任何内容都将插入到与节名称匹配的
``renderSection($name)`` 调用所在的布局中：::

    <?= $this->extend('default') ?>

    <?= $this->section('content') ?>
        <h1>Hello World!</h1>
    <?= $this->endSection() ?>

``endSection()`` 不需要节的名称，它会自动结束需要结束的节。

********
渲染视图
********

渲染视图及其布局的方法与在控制器中显示的任何其他视图的方法完全相同： ::

    public function index()
    {
        echo view('some_view');
    }

渲染器足够强大，它可以检测视图是需要单独渲染还是需要布局。

************
引用局部视图
************

局部视图是不扩展任何布局的视图文件。它们通常是可以在视图之间重复使用的内容。 使用视图布局时，必须使用 ``$this->include()``
来引用。

::

    <?= $this->extend('default') ?>

    <?= $this->section('content') ?>
        <h1>Hello World!</h1>

        <?= $this->include('sidebar') ?>
    <?= $this->endSection() ?>


调用 include() 方法时，可以将渲染普通视图时可以使用的所有选项都传递给它，包括缓存指令等。
