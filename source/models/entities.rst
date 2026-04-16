#####################
使用实体类
#####################

CodeIgniter 将实体类作为一等公民支持，同时保持它们完全可选。它们通常作为仓储模式的一部分使用，但也可以直接与 :doc:`模型 </models/model>` 配合使用，视具体需求而定。

.. contents::
    :local:
    :depth: 2

************
实体用法
************

实体类本质上是代表单条数据库记录的类。类属性对应数据库字段，并提供实现该记录业务逻辑的相关方法。

.. note:: 为便于理解，此处的说明基于使用数据库的场景。但实体也可用于非数据库来源的数据。

核心特性在于对象本身不关心任何持久化逻辑，该职责由模型或 Repository 类承担。这样，即便保存方式发生变更，也无需修改该对象在整个应用中的调用代码。

由此可以在快速原型阶段使用 JSON 或 XML 文件存储对象，验证概念可行后轻松切换到数据库。

下面通过一个简单的用户实体来演示如何使用。

假设有一个名为 ``users`` 的数据库表，结构如下::

    id          - integer
    username    - string
    email       - string
    password    - string
    created_at  - datetime

.. important:: ``attributes`` 是内部保留字。如果将其用作字段名，实体将无法正常工作。

创建实体类
=======================

现在创建一个实体类。由于没有默认的存储位置，且不符合现有目录结构，请在 **app/Entities** 创建一个新目录。然后在 **app/Entities/User.php** 创建实体。

.. literalinclude:: entities/001.php

就这么简单，不过接下来会让它更有用。

创建模型
================

首先在 **app/Models/UserModel.php** 创建模型，以便与实体交互：

.. literalinclude:: entities/002.php

模型使用数据库中的 ``users`` 表执行所有操作。

我们设置了 ``$allowedFields`` 属性，包含所有允许外部类修改的字段。``id``、``created_at`` 和 ``updated_at`` 字段由类或数据库自动处理，因此不需要手动更改。

最后，将实体类设为 ``$returnType``。由此可确保模型中所有返回数据库记录的内置方法，都会返回 User 实体类的实例，而非默认的对象或数组。

.. note::
    当然，如果在模型中添加自定义方法，必须自行实现，确保返回 ``$returnType`` 的实例。

使用实体类
=============================

所有组件就位后，可以像使用任何其他类一样使用实体类：

.. literalinclude:: entities/003.php

``User`` 类并未针对数据库字段定义任何属性，但仍可像访问公共属性一样直接访问。基类 ``CodeIgniter\Entity\Entity`` 会自动处理这些逻辑，并支持使用 ``isset()`` 或 ``unset()`` 检查或重置属性，同时还能追踪对象创建或从数据库读取后发生变更的字段。

.. note:: 实体类在内部将数据存储在类属性 ``$attributes`` 中。

当 User 传递给模型的 ``save()`` 方法时，会自动读取属性并保存 ``$allowedFields`` 属性中列出的任何更改。它还知道是创建新记录还是更新现有记录。

.. note:: 调用 ``insert()`` 时，实体的所有值都会传递给该方法，但调用 ``update()`` 时，只传递已更改的值。

快速填充属性
==========================

实体类还提供了 ``fill()`` 方法，允许将关联数组批量填入实体，自动填充类属性。数组中的所有属性都会设置到实体上。不过，通过模型保存时，只有 ``$allowedFields`` 中的字段才会实际保存到数据库，因此可以在实体上存储额外数据，而不必担心多余字段被错误保存。

.. literalinclude:: entities/004.php

也可以在构造函数中传入数据，实例化时数据会通过 ``fill()`` 方法处理。

.. literalinclude:: entities/005.php

批量访问属性
=========================

实体类提供了 ``toArray()`` 和 ``toRawArray()`` 两个方法，用于将所有可用属性提取到数组中。
使用 ``toRawArray()`` 会绕过魔术 “getter” 方法和类型转换。这两个方法均接受两个布尔参数：第一个参数用于指定是否仅返回已更改的属性；最后一个参数用于在处理嵌套实体时开启递归。

***********************
处理业务逻辑
***********************

上述示例虽然方便，但无法帮助执行业务逻辑。基类实体实现了一些智能的 ``__get()`` 和 ``__set()`` 方法，会检查特殊方法并使用这些方法来代替直接操作属性，从而允许执行所需的任何业务逻辑或数据转换。

以下是更新后的用户实体，展示如何使用：

.. literalinclude:: entities/006.php

首先注意到的是添加的方法名。每个方法都需要将 snake_case 字段名转换为 PascalCase，并加上 ``set`` 或 ``get`` 前缀。使用直接语法（即 ``$user->email``）设置或获取类属性时，这些方法会自动调用。除非需要从其他类访问，否则这些方法不需要是公共的。例如，``created_at`` 类属性会通过 ``setCreatedAt()`` 和 ``getCreatedAt()`` 方法访问。

.. note:: 这只适用于从类外部访问属性。类内部的任何方法都必须直接调用 ``setX()`` 和 ``getX()`` 方法。

在 ``setPassword()`` 方法中，确保密码始终进行哈希处理。

在 ``setCreatedAt()`` 中，将模型传入的字符串转换为 DateTime 对象，确保时区为 UTC，以便轻松转换为查看者的当前时区。在 ``getCreatedAt()`` 中，将时间转换为应用当前时区的格式化字符串。

虽然相当简单，但这些示例展示了使用实体类可以提供非常灵活的方式来执行业务逻辑，并创建易于使用的对象。

.. literalinclude:: entities/007.php

.. _entities-special-getter-setter:

特殊的 Getter/Setter
=====================

.. versionadded:: 4.4.0

例如，如果实体的父类已经定义了 ``getParent()`` 方法，而实体也有一个名为 ``parent`` 的字段，尝试在实体类中为 ``getParent()`` 方法添加业务逻辑时，该方法已经存在。

在这种情况下，可以使用特殊的 getter/setter。使用 ``_getX()``/``_setX()`` 代替 ``getX()``/``setX()``。

在上面的示例中，如果实体有 ``_getParent()`` 方法，获取 ``$entity->parent`` 时会使用该方法，设置 ``$entity->parent`` 时会使用 ``_setParent()`` 方法。

************
数据映射
************

在你的职业生涯中，常会遇到应用需求变更导致原数据库字段名不再适用，或是代码规范偏好 camelCase（小驼峰）类属性、但数据库结构要求使用 snake_case 命名的情况。利用实体类的数据映射功能，可以轻松处理此类场景。

假设有一个在整个应用中使用的简化用户实体：

.. literalinclude:: entities/008.php

假设业务需求发生变更，应用不再使用用户名登录，转而统一使用 Email。同时为了提升个性化体验，需要将原有的 ``name`` 字段用途从“用户名”改为“全名”。为了确保数据库结构的清晰与严谨，可编写迁移脚本将 ``name`` 字段重命名为 ``full_name``。

抛开这个示例多么牵强不谈，现在有两种修复 User 类的方式。可以将类属性从 ``$name`` 修改为 ``$full_name``，但这需要在整个应用中进行更改。相反，可以简单地将数据库中的 ``full_name`` 字段映射到 ``$name`` 属性，即可完成实体的修改：

.. literalinclude:: entities/009.php

将数据库字段名添加到 ``$datamap`` 数组中，即可指定该字段对应的类属性。数组的键为类属性名，值为数据库中的字段名。

在此示例中，当模型在 User 类上设置 ``full_name`` 字段时，实际上会将该值赋给类的 ``$name`` 属性，因此可以通过 ``$user->name`` 设置和获取。该值仍然可以通过原始的 ``$user->full_name`` 访问，这也是模型获取数据并保存回数据库所需的。不过，``unset()`` 和 ``isset()`` 只对映射后的属性 ``$user->name`` 生效，对数据库字段名 ``$user->full_name`` 不生效。

.. note:: 使用数据映射时，必须为数据库字段名定义 ``set*()`` 和 ``get*()`` 方法。在此示例中，必须定义 ``setFullName()`` 和 ``getFullName()``。

********
转换器
********

日期转换
=============

默认情况下，实体类在设置或读取 `created_at`、`updated_at` 或 `deleted_at` 字段时，会自动将其转换为 :doc:`Time </libraries/time>` 实例。Time 类提供了大量实用的方法，并支持不可变操作与本地化。

可以通过将名称添加到 ``$dates`` 属性来定义哪些属性会自动转换：

.. literalinclude:: entities/010.php

现在，设置这些属性中的任何一个时，都会使用 **app/Config/App.php** 中设置的应用当前时区，转换为 Time 实例：

.. literalinclude:: entities/011.php

.. _entities-property-casting:

属性类型转换
================

通过 ``$casts`` 属性可将实体属性转换为常见的数据类型。该属性应为数组，键为类属性名，值为目标数据类型。

属性类型转换同时影响读取（get）和写入（set），但某些类型仅影响读取（get）。

标量类型转换
-------------------

属性可以转换为以下数据类型：
**integer**、**float**、**double**、**string**、**boolean**、**object**、**array**、**datetime**、**timestamp**、**uri** 和 **int-bool**。
在类型前加问号可将属性标记为可空，例如 **?string**、**?integer**。

.. note:: **int-bool** 自 v4.3.0 起可用。

例如，如果有一个包含 ``is_banned`` 属性的 User 实体，可以将其转换为布尔值：

.. literalinclude:: entities/012.php

数组/JSON 转换
------------------

数组/JSON 转换对存储序列化数组或 JSON 的字段特别有用。当转换为：

* **array** 时，会自动反序列化，
* **json** 时，会自动设置为 ``json_decode($value, false)`` 的值，
* **json-array** 时，会自动设置为 ``json_decode($value, true)`` 的值，

在设置属性值时生效。
与可以转换的其他数据类型不同：

* **array** 转换类型会序列化，
* **json** 和 **json-array** 转换会使用 json_encode 函数对

属性值进行编码：

.. literalinclude:: entities/013.php

.. literalinclude:: entities/014.php

CSV 转换
-----------

如果确定是一个简单的扁平值数组，将其编码为序列化或 JSON 字符串可能比原始结构更复杂。使用逗号分隔值（CSV）转换是更简单的替代方案，生成的字符串占用更少空间，也更易于人类阅读：

.. literalinclude:: entities/015.php

在数据库中存储为 "red,yellow,green"：

.. literalinclude:: entities/016.php

.. note:: CSV 转换使用 PHP 内部的 ``implode`` 和 ``explode`` 方法，假设所有值都是字符串安全的且不包含逗号。对于更复杂的数据转换，请尝试 ``array`` 或 ``json``。

自定义转换
--------------

可以定义自己的转换类型用于获取和设置数据。

首先需要为类型创建处理器类。
假设该类位于 **app/Entities/Cast** 目录：

.. literalinclude:: entities/017.php

现在需要注册它：

.. literalinclude:: entities/018.php

如果不需要在获取或设置值时更改值，那么就不要实现相应的方法：

.. literalinclude:: entities/019.php

参数
----------

某些情况下，一种类型不够用。此时可以使用额外参数。
额外参数用方括号表示，以逗号分隔，如 ``type[param1, param2]``。

.. literalinclude:: entities/020.php

.. literalinclude:: entities/021.php

.. note:: 若转换类型标记为可空（如 ``?bool``），且传入值不为 null，``nullable`` 参数将传递至转换类型处理器。
    若已有预定义参数，``nullable`` 将追加至列表末尾。

*******************************
检查已更改的属性
*******************************

可以检查实体属性自创建以来是否发生了更改。唯一参数是要检查的属性名称：

.. literalinclude:: entities/022.php

或者省略参数，检查整个实体中已更改的值：

.. literalinclude:: entities/023.php
