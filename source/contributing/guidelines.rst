=======================
贡献原则
=======================

你的出栈请求（PRs）需要满足我们的原则。如果出栈请求没有通过这些原则，它会被婉拒而当你做出修改后你需要再次确认。上述方式听上去有点不容易，但这个方法可以让我们继续维持编码基数的质量。

PHP 代码风格
============

所有的代码必须符合我们的  `风格指引
<./styleguide.html>`_, 实质性的风格是 `Allman indent style
<https://en.wikipedia.org/wiki/Indent_style#Allman_style>`_ ,及命名中的详细阐述和清晰的操作标记。

代码要同现存的代码有同样的格式而这么做必然让 PHP 代码的样式尽可能清晰易读。

我们的样式引导类似于 PSR-1和 PSR-2 ，源自 PHP-FIG ，但却没有必要取相同或者一致的样式。

单元测试
============

所有 CodeIgniter（CI）组件单元测试均在预期中。我们运用 PHP 单元，并且为每一出栈请求的确认或者修改运行单元测试时使用 travis-ci 。

在 CodeIgniter 项目中, 有一个 ``tests`` 文件夹，有一个结构类似的 ``system`` 与之匹配。

正常的实际项目里系统 ``system`` 中类的每一个类都将有一个单元测试类，它会配有适当的命名。例如，``BananaTest``  类将会测试 ``Banana`` 类。
单元测试将会在时机恰当时更方便的拥有独立的类去测试一个单独 CodeIgniter 功能组件的不同功能。


更多信息请参看  `PHPUnit website <https://phpunit.de/>`_ .

PHP 文档注释
===============

源代码应该使用 PHP 文档程序块注释。完成注释去解释潜在难以理解的代码段，而且文档注释要标注在每一个 public 或者 protected 类/接口/特性，方法和变量前面。


更多信息请参见  `phpDocumentor website <https://phpdoc.org/>`_ .

我们为了构架使用 ``phpDocumentor2`` 去产生 API  文件， 又在 ``phpdoc.dist.xml`` 项目根目录中做详细配置。


文档编制
=============

用户指南是 CodeIgniter 构架的一个重要组成部分。
在用户指南中每一构架组成部分或者多视窗组件会有一个对应的节点。一些基础的组成部分将会显现不止一处。

变更日志
==========
在用户根目录变更日志需要保持更新。在日志里并不是所有的修改都需要记录，除了新类，大变更或者现存类的代码（BC)变更，以及可能的程序错误修正。


事例参见 `CodeIgniter 3 change log 
<https://github.com/bcit-ci/CodeIgniter/blob/develop/user_guide_src/source/changelog.rst>`_ .

PHP 兼容性
=================

CodeIgniter4 要配置 PHP 7.

在你的系统中首要的提示请参看  `CodeIgniter4-developer-setup <https://github.com/bcit-ci/CodeIgniter4-developer-setup>`_  的内容.

为了配置你的 IDE 或者以 PHP7 和 CodeIgniter4 的编辑器去更好的工作上述地址的内容也包含了大量提示。

向后兼容性
=======================

总体而言，我们的目的去维持构架中次要版本间的向后兼容性。任意一个破坏兼容性的修改需要更好的原因去执行，并且它们也需要在 `Upgrading <../installation/upgrading.html>`_ 指南中被明确指出。

Codeigniter4 更早版本的构架示范了有效的向后兼容性的分隔。

归并能力
============

在你需要出栈请求以前要考虑到它们的归并能力。

我们建议你在确定出栈请求主要内容确定以前你要同步你内容的 ``develop`` 分支。

自从你着手工作以来你将要在你的贡献中修改的具体表现内解决一些归并冲突的引荐。
