##########
视图单元
##########

许多应用包含可在页面间或页面不同位置重复使用的视图片段，常见的如提示框、导航控件、广告或登录表单等。CodeIgniter 可将此类展示块的逻辑封装到视图单元中。视图单元本质上是可嵌入其他视图的微型视图，支持通过内置逻辑处理特定的显示需求。通过将各单元逻辑分离到独立类中，可显著提升视图的可读性与可维护性。

.. contents::
    :local:
    :depth: 2

***************************
简单单元与受控单元
***************************

CodeIgniter 支持两种视图单元：简单单元和受控单元。

**简单视图单元** 可由任意类和方法生成，只需遵循一条规则：必须返回字符串。

**受控视图单元** 必须通过继承 ``Codeigniter\View\Cells\Cell`` 类的子类生成。该基类提供的额外功能可显著提升视图单元的灵活性与开发效率。

.. _app-cells:

*******************
调用视图单元
*******************

无论使用哪种类型的视图单元，都可以在任何视图中通过 ``view_cell()`` 辅助函数调用。

第一个参数为（1）*类名和方法名* （简单单元）或（2）*类名及可选方法名* （受控单元），第二个参数是传递给方法的参数数组或字符串：

.. literalinclude:: view_cells/001.php

单元返回的字符串将插入到视图中调用 ``view_cell()`` 函数的位置。

省略命名空间
==================

.. versionadded:: 4.3.0

如未提供类的完整命名空间，将默认在 ``App\Cells`` 命名空间中查找。例如，以下示例会尝试在 **app/Cells/MyClass.php** 中查找 ``MyClass`` 类。如果未找到，将扫描所有命名空间，在各命名空间的 **Cells** 子目录中继续查找：

.. literalinclude:: view_cells/002.php

以键值对字符串形式传递参数
======================================

也可以将参数以键值对字符串形式传递：

.. literalinclude:: view_cells/003.php

************
简单单元
************

简单单元是从所选方法返回字符串的类。以下是一个简单的 Alert Message 单元示例：

.. literalinclude:: view_cells/004.php

在视图中调用方式如下：

.. literalinclude:: view_cells/005.php

此外，还可使用与方法中参数变量同名的参数名以提高可读性。
采用此方式时，调用视图单元时必须始终指定所有参数：

.. literalinclude:: view_cells/006.php

.. literalinclude:: view_cells/007.php

.. _controlled-cells:

****************
受控单元
****************

.. versionadded:: 4.3.0

受控单元有两个主要目标：（1）尽可能快速构建单元；（2）在需要时为视图提供额外逻辑和灵活性。

该类必须继承 ``CodeIgniter\View\Cells\Cell``。视图文件应与类放在同一目录下。按约定，类名应采用 PascalCase 命名并以 ``Cell`` 为后缀，视图文件则为类名的 snake_case 形式（去掉后缀）。例如，``MyCell`` 类对应的视图文件应为 ``my.php``。

.. note:: v4.3.5 之前，生成的视图文件以 ``_cell.php`` 结尾。v4.3.5 及更新版本生成的视图文件不再包含 ``_cell`` 后缀，但已有的 ``_cell`` 文件仍可被定位和加载。

创建受控单元
==========================

最基础的实现只需在类中定义 public 属性。这些属性将自动在视图文件中可用。

将上方的 AlertMessage 实现为受控单元如下所示：

.. literalinclude:: view_cells/008.php

.. literalinclude:: view_cells/009.php

.. literalinclude:: view_cells/010.php

.. note:: 如使用类型化属性，必须设置初始值：

    .. literalinclude:: view_cells/023.php

.. _generating-cell-via-command:

通过命令生成单元
===========================

还可以通过 CLI 内置命令创建受控单元。命令为 ``php spark make:cell``。该命令接受一个参数，即要创建的单元名称。名称应采用 PascalCase，类将创建在 **app/Cells** 目录下，视图文件同样创建在 **app/Cells** 目录中。

.. code-block:: console

    php spark make:cell AlertMessageCell

使用不同的视图
======================

可在类中设置 ``view`` 属性来指定自定义视图文件路径。视图的查找方式与普通视图相同：

.. literalinclude:: view_cells/011.php

自定义渲染
=======================

如需更精细地控制 HTML 渲染，可实现 ``render()`` 方法。该方法允许执行额外逻辑，并在需要时向视图传递额外数据。``render()`` 方法必须返回字符串。

要充分利用受控单元的全部功能，应使用 ``$this->view()`` 而非普通的 ``view()`` 辅助函数：

.. literalinclude:: view_cells/012.php

计算属性
===================

如需对一个或多个属性执行额外逻辑，可使用计算属性。这需要将属性设为 ``protected`` 或 ``private``，并实现一个 public 方法，方法名由 ``get`` + 属性名 + ``Property`` 组成：

.. literalinclude:: view_cells/013.php

.. literalinclude:: view_cells/014.php

.. literalinclude:: view_cells/015.php

.. important:: 初始化单元时，无法设置声明为 private 的属性。``getDataProperty()`` 与 ``getViewProperty()`` 方法不可调用，它们仅供内部处理使用。

展示方法
====================

有时需要为视图执行额外逻辑，但不希望将其作为参数传递。此时可在单元内部实现一个方法，并在其视图中直接调用。这有助于提高视图的可读性：
可能已经注意到，模板中不仅允许调用方法：整个单元对象及其公有属性均可在模板中使用。

.. literalinclude:: view_cells/016.php

.. literalinclude:: view_cells/017.php

执行初始化逻辑
======================

如需在视图渲染前执行额外逻辑，可实现 ``mount()`` 方法。该方法在类实例化后立即调用，可用于设置额外属性或执行其他逻辑：

.. literalinclude:: view_cells/018.php

通过 ``view_cell()`` 辅助函数以数组形式传递参数，即可向 ``mount()`` 方法传递额外参数。任何与 ``mount()`` 方法参数名匹配的参数都将被传入：

.. literalinclude:: view_cells/019.php

.. literalinclude:: view_cells/020.php

************
单元缓存
************

可通过向 ``view_cell()`` 传递第三个参数（缓存秒数）来缓存视图单元调用的结果。将使用当前配置的缓存引擎：

.. literalinclude:: view_cells/021.php

如需要，可通过第四个参数传入自定义缓存名称，替代自动生成的名称：

.. literalinclude:: view_cells/022.php
