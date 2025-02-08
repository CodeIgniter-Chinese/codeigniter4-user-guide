##########
视图单元
##########

许多应用程序都有一些小的视图片段，可以在页面之间重复使用，或者在页面的不同位置使用。这些通常是帮助框、导航控件、广告、登录表单等。CodeIgniter 允许你将这些呈现块的逻辑封装在视图单元中。它们基本上是可以包含在其他视图中的小视图。它们可以内置逻辑来处理任何特定于单元的显示逻辑。它们可以通过将每个单元的逻辑分离到自己的类中，使你的视图更易读和可维护。

.. contents::
    :local:
    :depth: 2

***************************
简单和受控制的单元
***************************

CodeIgniter 支持两种类型的视图单元：简单的和受控制的。

**简单的视图单元** 可以从你选择的任何类和方法生成，不必遵循任何规则，只需返回一个字符串。

**受控制的视图单元** 必须从扩展了 ``Codeigniter\View\Cells\Cell`` 类的类生成，这提供了额外的功能，使你的视图单元更加灵活和快速使用。

.. _app-cells:

*******************
调用视图单元
*******************

无论你使用哪种类型的视图单元，都可以使用 ``view_cell()`` 辅助函数从任何视图中调用它。

第一个参数是（1） *类和方法的名称* （简单单元）或（2） *类的名称和可选方法* （受控制的单元），第二个参数是要传递给该方法的参数数组或字符串：

.. literalinclude:: view_cells/001.php

单元返回的字符串将被插入到调用 ``view_cell()`` 函数的视图中。

省略命名空间
==================

.. versionadded:: 4.3.0

如果你没有包含类的完整命名空间，它将假定可以在 ``App\Cells`` 命名空间中找到。因此，以下示例将尝试在 **app/Cells/MyClass.php** 中查找 ``MyClass`` 类。如果在那里找不到，将扫描所有命名空间，直到找到为止，在每个命名空间的 **Cells** 子目录中搜索：

.. literalinclude:: view_cells/002.php

将参数作为键/值字符串传递
======================================

你还可以将参数作为键/值字符串传递：

.. literalinclude:: view_cells/003.php

************
简单单元
************

简单单元是从所选方法返回字符串的类。一个简单的警告消息单元的示例可能如下所示：

.. literalinclude:: view_cells/004.php

你可以在视图中这样调用它：

.. literalinclude:: view_cells/005.php

此外，你可以使用与方法中的参数变量匹配的参数名称以提高可读性。
当你以这种方式使用时，视图单元调用中必须始终指定所有参数：

.. literalinclude:: view_cells/006.php

.. literalinclude:: view_cells/007.php

.. _controlled-cells:

****************
受控单元
****************

.. versionadded:: 4.3.0

受控单元有两个主要目标：(1) 尽可能快地构建单元，(2) 并为视图提供额外的逻辑和灵活性（如果需要）。

该类必须扩展 ``CodeIgniter\View\Cells\Cell``。它们应该在同一文件夹中有一个视图文件。按照惯例，类名应为 PascalCase，后缀为 ``Cell``，视图应为类名的 snake_case 版本，不包括后缀。例如，如果你有一个 ``MyCell`` 类，视图文件应为 ``my.php``。

.. note:: 在 v4.3.5 之前，生成的视图文件以 ``_cell.php`` 结尾。尽管 v4.3.5 及更高版本将生成不带 ``_cell`` 后缀的视图文件，但现有的视图文件仍将被定位和加载。

创建受控单元
==========================

在类中实现的最基本的级别上，你只需要实现公共属性。这些属性将自动提供给视图文件。

将上面的 AlertMessage 实现为受控单元将如下所示：

.. literalinclude:: view_cells/008.php

.. literalinclude:: view_cells/009.php

.. literalinclude:: view_cells/010.php

.. note:: 如果你使用类型化属性，你必须设置初始值：

    .. literalinclude:: view_cells/023.php

.. _generating-cell-via-command:

通过命令生成单元
===========================

你还可以通过 CLI 中的内置命令创建受控单元。该命令是 ``php spark make:cell``。它接受一个参数，要创建的单元的名称。名称应为 PascalCase，类将在 **app/Cells** 目录中创建。视图文件也将在 **app/Cells** 目录中创建。

.. code-block:: console

    php spark make:cell AlertMessageCell

使用不同的视图
======================

你可以通过在类中设置 ``view`` 属性来指定自定义视图名称。视图将像正常情况下一样被定位：

.. literalinclude:: view_cells/011.php

自定义渲染
=======================

如果你需要更多控制HTML的渲染过程，可以实现一个 ``render()`` 方法。该方法允许你执行其他逻辑并向视图传递额外的数据（如果需要）。``render()`` 方法必须返回一个字符串。

为了充分利用受控单元的全部功能，你应该使用 ``$this->view()`` 而不是普通的 ``view()`` 辅助函数：

.. literalinclude:: view_cells/012.php

计算属性
===================

如果你需要为一个或多个属性执行其他逻辑，可以使用计算属性。这需要将属性设置为 ``protected`` 或 ``private``，并实现一个公共方法，该方法的名称由属性名称包围 ``get`` 和 ``Property`` 组成：

.. literalinclude:: view_cells/013.php

.. literalinclude:: view_cells/014.php

.. literalinclude:: view_cells/015.php

.. important:: 无法设置在单元初始化期间声明为私有的属性。

演示方法
====================

有时你需要为视图执行其他逻辑，但不想将其作为参数传递。你可以实现一个在单元的视图内部调用的方法。这可以提高视图的可读性：

.. literalinclude:: view_cells/016.php

.. literalinclude:: view_cells/017.php

执行设置逻辑
======================

如果你需要在渲染视图之前执行其他逻辑，可以实现一个 ``mount()`` 方法。该方法将在类实例化后立即调用，并可用于设置其他属性或执行其他逻辑：

.. literalinclude:: view_cells/018.php

你可以通过将它们作为数组传递给 ``view_cell()`` 辅助函数来将其他参数传递给 ``mount()`` 方法。任何与 ``mount()`` 方法的参数名称匹配的参数将被传递进去：

.. literalinclude:: view_cells/019.php

.. literalinclude:: view_cells/020.php

************
单元缓存
************

你可以通过将要缓存数据的秒数作为第三个参数传递来缓存视图单元调用的结果。这将使用当前配置的缓存引擎：

.. literalinclude:: view_cells/021.php

如果需要，你可以提供一个自定义名称，而不是自动生成的名称，通过将新名称作为第四个参数传递：

.. literalinclude:: view_cells/022.php
