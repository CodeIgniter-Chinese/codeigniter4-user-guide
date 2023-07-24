#########################
使用 CodeIgniter 的 Model
#########################

.. contents::
    :local:
    :depth: 2

模型
******

CodeIgniter 的 Model 提供了方便的特性和额外的功能,可以使处理数据库中的 **单个表** 更方便。

它内置了对标准的数据库表交互方式大部分帮助器方法,包括查找记录、更新记录、删除记录等等。

.. _accessing-models:

访问模型
******************

模型通常存储在 **app/Models** 目录中。它们应该具有与目录位置匹配的命名空间,如 ``namespace App\Models``。

你可以通过创建新实例或使用 :php:func:`model()` 辅助函数在类中访问模型。

.. literalinclude:: model/001.php

``model()`` 内部使用 ``Factories::models()``。详情参见 :ref:`factories-example`。

CodeIgniter 的 Model
***********************

CodeIgniter 确实提供了一个模型类,具有一些不错的特性,包括:

- 自动数据库连接
- 基本的 CRUD 方法
- 模型内验证
- :ref:`自动分页 <paginating-with-models>`
- 等等

该类为从中构建自己的模型提供了可靠的基础,允许你快速构建应用程序的模型层。

创建你的模型
*******************

要利用 CodeIgniter 的模型,你只需创建一个扩展 ``CodeIgniter\Model`` 的新模型类:

.. literalinclude:: model/002.php

这个空类方便地访问数据库连接、查询构建器以及其他一些方便的方法。

initialize()
============

如果你需要在模型中进行其他初始化,可以扩展 ``initialize()`` 方法,它将在模型的构造函数之后立即运行。这允许你执行额外的步骤,而不需要重复构造函数参数,例如扩展其他模型:

.. literalinclude:: model/003.php

连接数据库
==========================

当类首次实例化时,如果没有向构造函数传递数据库连接实例,它将自动连接到配置中设置的默认数据库组。你可以通过在类中添加 ``$DBGroup`` 属性为每个模型修改使用的组。这确保模型内对 ``$this->db`` 的任何引用都通过适当的连接进行。

.. literalinclude:: model/004.php

你需要将“group_name”替换为数据库配置文件中定义的数据库组名称。

配置你的模型
======================

模型类具有一些配置选项,可以设置这些选项以使类的方法无缝为你工作。前两个用于 CRUD 方法来确定使用哪个表以及如何查找所需记录:

.. literalinclude:: model/005.php

$table
------

指定此模型主要使用的数据库表。这仅适用于内置的 CRUD 方法。在你自己的查询中不受限于只使用此表。

$primaryKey
-----------

这是唯一标识表中记录的列的名称。这不一定必须与数据库中指定的主键匹配,但与 ``find()`` 等方法一起使用时,用于匹配指定的值的列。

.. note:: 所有模型都必须指定 primaryKey 以使所有功能正常工作。

$useAutoIncrement
-----------------

指定表是否使用 ``$primaryKey`` 的自动增量功能。如果设置为 ``false``,则你有责任为表中的每条记录提供主键值。当我们想实现 1:1 关系或在模型中使用 UUID 时,此功能可能很方便。默认值为 ``true``。

.. note:: 如果你将 ``$useAutoIncrement`` 设置为 ``false``,请确保在数据库中将主键设置为 ``unique``。这样可以确保模型的所有功能与以前一样工作。

$returnType
-----------

模型的 CRUD 方法将一个步骤的工作从你这里带走,自动返回结果数据,而不是结果对象。此设置允许你定义返回的数据类型。有效值为 '**array**' (默认)、 '**object**' 或可以与结果对象的 ``getCustomResultObject()`` 方法一起使用的 **完全限定的类名称**。使用类的特殊常量 ``::class`` 可以让大多数 IDE 自动完成名称并允许诸如重构之类的功能更好地理解你的代码。

.. _model-use-soft-deletes:

$useSoftDeletes
---------------

如果为 true,那么任何 ``delete()`` 方法调用都会在数据库中设置 ``deleted_at``,而不是真正删除行。这可以在数据可能在其他地方被引用时保留数据,或者可以维护一个“回收站”,其中的对象可以恢复,或者即使只是保留它作为安全轨迹的一部分。如果为 true,则 **find*()** 方法只返回非已删除行,除非在调用 **find*()** 方法之前调用 ``withDeleted()`` 方法。

这需要数据库中具有与模型的 ``$dateFormat`` 设置相应的数据类型的 DATETIME 或 INTEGER 字段。默认字段名称为 ``deleted_at``,但是可以通过使用 ``$deletedField`` 属性将其配置为你选择的任何名称。

.. important:: ``deleted_at`` 字段必须可为空。

$allowedFields
--------------

当通过 ``save()``、``insert()`` 或 ``update()`` 方法设置时,此数组应更新可以设置的字段名称。这些字段名之外的任何字段都会被丢弃。这有助于防止只从表单获取输入并将其全部抛给模型,从而导致潜在的大规模分配漏洞。

.. note:: ``$primaryKey`` 字段永远不应该是允许的字段。

日期
-----

$useTimestamps
^^^^^^^^^^^^^^

此布尔值确定是否会向所有插入和更新自动添加当前日期。如果为 true,将以 ``$dateFormat`` 中指定的格式设置当前时间。这需要表中具有数据类型适当的 **created_at**、**updated_at** 和 **deleted_at** 列。

$dateFormat
^^^^^^^^^^^

此值与 ``$useTimestamps`` 和 ``$useSoftDeletes`` 一起使用,以确保插入到数据库中的是正确类型的日期值。默认情况下,这会创建 DATETIME 值,但有效选项有: ``'datetime'``、 ``'date'`` 或 ``'int'`` (PHP 时间戳)。在缺少或无效的 **dateFormat** 情况下使用 **useSoftDeletes** 或 **useTimestamps** 会引发异常。

$createdField
^^^^^^^^^^^^^

指定用于数据记录创建时间戳的数据库字段。如果留空则不更新它(即使启用了 ``$useTimestamps``)。

$updatedField
^^^^^^^^^^^^^

指定应该用于保持数据记录更新时间戳的数据库字段。如果留空则不更新它(即使启用了 ``$useTimestamps``)。

$deletedField
^^^^^^^^^^^^^

指定用于软删除的数据库字段。参见 :ref:`model-use-soft-deletes`。

验证
----------

$validationRules
^^^^^^^^^^^^^^^^

包含 :ref:`validation-array` 中描述的验证规则数组或包含要应用的验证组名称的字符串,如同一节中所述。下面更详细地描述。

$validationMessages
^^^^^^^^^^^^^^^^^^^

包含应在验证期间使用的自定义错误消息数组,如 :ref:`validation-custom-errors` 中所述。下面更详细地描述。

$skipValidation
^^^^^^^^^^^^^^^

是否应跳过所有 **inserts** 和 **updates** 期间的数据验证。默认值为 ``false``,这意味着数据将始终尝试验证。这主要由 ``skipValidation()`` 方法使用,但可以更改为 ``true``,这样该模型永远不会验证。

.. _clean-validation-rules:

$cleanValidationRules
^^^^^^^^^^^^^^^^^^^^^

是否应删除在传入数据中不存在的验证规则。这在 **updates** 中使用。
默认值为 ``true``,这意味着在验证之前,将(临时)删除传入数据中不存在字段的验证规则。
这是为了避免仅更新某些字段时的验证错误。

你也可以通过 ``cleanRules()`` 方法更改此值。

.. note:: 在 v4.2.7 之前,由于一个 bug, ``$cleanValidationRules`` 不起作用。

回调
---------

$allowCallbacks
^^^^^^^^^^^^^^^

是否应使用下面定义的回调。

$beforeInsert
^^^^^^^^^^^^^
$afterInsert
^^^^^^^^^^^^^
$beforeInsertBatch
^^^^^^^^^^^^^^^^^^
$afterInsertBatch
^^^^^^^^^^^^^^^^^
$beforeUpdate
^^^^^^^^^^^^^
$afterUpdate
^^^^^^^^^^^^^
$beforeUpdateBatch
^^^^^^^^^^^^^^^^^^
$afterUpdateBatch
^^^^^^^^^^^^^^^^^
$beforeFind
^^^^^^^^^^^
$afterFind
^^^^^^^^^^
$beforeDelete
^^^^^^^^^^^^^
$afterDelete
^^^^^^^^^^^^

这些数组允许你指定在属性名称中指定的时间回调方法。

使用数据
*****************

查找数据
============

提供了几个函数来对表执行基本的 CRUD 工作,包括 ``find()``、``insert()``、``update()``、``delete()`` 等等。

find()
------

在主键与作为第一参数传递的值匹配的情况下,返回单行。

.. literalinclude:: model/006.php

该值以 ``$returnType`` 中指定的格式返回。

你可以通过传递主键值数组而不是一个来指定要返回多行。

.. literalinclude:: model/007.php

.. note:: 如果没有传递参数, ``find()`` 将返回该模型的表中的所有行,
    效果与 ``findAll()`` 相同,尽管不太明确。

findColumn()
------------

返回 null 或索引数组的列值:

.. literalinclude:: model/008.php

``$column_name`` 应该是单个列的名称,否则你会获得 ``DataException``。

findAll()
---------

返回所有结果:

.. literalinclude:: model/009.php

可以在调用此方法之前根据需要插入查询构建器命令来修改此查询:

.. literalinclude:: model/010.php

你可以分别作为第一个和第二个参数传递限制和偏移值:

.. literalinclude:: model/011.php

first()
-------

返回结果集中的第一行。这与查询构建器一起使用时最好。

.. literalinclude:: model/012.php

withDeleted()
-------------

如果 ``$useSoftDeletes`` 为 true,则 **find*()** 方法不会返回任何 ``deleted_at IS NOT NULL`` 的行。
要暂时覆盖此设置,可以在调用 **find*()** 方法之前使用 ``withDeleted()`` 方法。

.. literalinclude:: model/013.php

onlyDeleted()
-------------

而 ``withDeleted()`` 将返回已删除和未删除的行,此方法会修改下一个 **find*()** 方法仅返回软删除的行:

.. literalinclude:: model/014.php

保存数据
===========

insert()
--------

第一个参数是一个关联数组,用于在数据库中创建新行数据。
如果传递对象而不是数组,它将尝试将其转换为数组。

数组的键必须与 ``$table`` 中的列名匹配,而数组的值是要为该键保存的值。

可选的第二个参数为布尔类型,如果设置为 false,该方法将返回一个布尔值,表示查询的成功或失败。

你可以使用 ``getInsertID()`` 方法检索最后插入的行的主键。

.. literalinclude:: model/015.php

.. _model-allow-empty-inserts:

allowEmptyInserts()
-------------------

.. versionadded:: 4.3.0

你可以使用 ``allowEmptyInserts()`` 方法插入空数据。默认情况下,模型在你尝试插入空数据时会抛出异常。但是如果调用此方法,将不再执行检查。

.. literalinclude:: model/056.php

你可以通过调用 ``allowEmptyInserts(false)`` 再次启用检查。

update()
--------

更新数据库中的现有记录。第一个参数是要更新的记录的 ``$primaryKey``。关联数组作为第二个参数传递给此方法。数组的键必须与 ``$table`` 中的列名匹配,而数组的值是要为该键保存的值:

.. literalinclude:: model/016.php

.. important:: 从 v4.3.0 开始,如果它生成没有 WHERE 子句的 SQL 语句,此方法会抛出 ``DatabaseException``。
    在以前的版本中,如果在没有指定 ``$primaryKey`` 的情况下调用它并生成没有 WHERE 子句的 SQL 语句,查询仍会执行,表中的所有记录都会被更新。

可以通过作为第一个参数传递主键数组来一次更新多条记录:

.. literalinclude:: model/017.php

当你需要更灵活的解决方案时,可以留空参数,它的作用类似于查询构建器的 update 命令,具有验证、事件等的额外优势:

.. literalinclude:: model/018.php

.. _model-save:

save()
------

这是 ``insert()`` 和 ``update()`` 方法的包装器,可以根据是否找到与 **主键** 值匹配的数组键来自动处理插入或更新记录。

.. literalinclude:: model/019.php

save 方法在使用自定义类结果对象时也可以大大简化工作,它会识别非简单对象并将其公共和受保护的值提取到一个数组中,然后传递给适当的 insert 或 update 方法。这允许你以非常简洁的方式使用实体类。实体类是表示单个对象实例的简单类,如用户、博客文章、工作等。此类负责维护与对象本身相关的业务逻辑,如以某种方式格式化元素等。它们不应该知道它们是如何保存到数据库的。最简单的,它们可能看起来像这样:

.. literalinclude:: model/020.php

与此配合使用的一个非常简单的模型可能如下所示:

.. literalinclude:: model/021.php

该模型使用来自 ``jobs`` 表的数据,并将所有结果返回为 ``App\Entities\Job`` 的实例。
当你需要将该记录持久化到数据库时,你需要编写自定义方法,或者使用模型的 ``save()`` 方法检查类、获取任何公共和私有属性,并将它们保存到数据库:

.. literalinclude:: model/022.php

.. note:: 如果你发现自己频繁使用实体,CodeIgniter 提供了一个内置的 :doc:`实体类 </models/entities>`,
    它提供了使开发实体更简单的几个方便的功能。

删除数据
=============

delete()
--------

以主键值作为第一个参数,从模型的表中删除匹配的记录:

.. literalinclude:: model/023.php

如果模型的 ``$useSoftDeletes`` 值为 true,这将更新行以将 ``deleted_at`` 设置为当前日期和时间。你可以通过将第二个参数设置为 true 来强制永久删除。

可以作为第一个参数传递主键数组,以一次删除多条记录:

.. literalinclude:: model/024.php

如果没有传递参数,将像查询构建器的 delete 方法一样操作,需要事先进行 where 调用:

.. literalinclude:: model/025.php

purgeDeleted()
--------------

通过永久删除所有 'deleted_at IS NOT NULL' 的行来清理数据库表。

.. literalinclude:: model/026.php

模型内验证
===================

验证数据
---------------

对许多人来说,在模型中验证数据是确保数据符合单一标准的首选方法,而不重复代码。模型类提供了一种方法,可以在使用 ``insert()``、``update()`` 或 ``save()`` 方法保存到数据库之前自动验证所有数据。

.. important:: 在更新数据时,默认情况下,模型类中的验证仅验证提供的字段。这是为了避免仅更新某些字段时出现验证错误。

    但这意味着 ``required*`` 规则在更新时不像预期的那样工作。
    如果你想检查必填字段,可以通过配置更改行为。
    详情参见 :ref:`clean-validation-rules`。

第一步是用将应用的字段和规则填充 ``$validationRules`` 类属性。如果你有要使用的自定义错误消息,请将其放入 ``$validationMessages`` 数组中:

.. literalinclude:: model/027.php

向字段设置验证规则的另一种方法是使用函数:

.. php:namespace:: CodeIgniter

.. php:class:: Model

.. php:method:: setValidationRule($field, $fieldRules)

    :param  string  $field:
    :param  array   $fieldRules:

    此函数将设置字段验证规则。

    使用示例:

    .. literalinclude:: model/028.php

.. php:method:: setValidationRules($validationRules)

    :param  array   $validationRules:

    此函数将设置验证规则。

    使用示例:

    .. literalinclude:: model/029.php

向字段设置验证消息的另一种方法是使用函数:

.. php:method:: setValidationMessage($field, $fieldMessages)

    :param  string  $field:
    :param  array   $fieldMessages:

    此函数将设置字段的错误消息。

    使用示例:

    .. literalinclude:: model/030.php

.. php:method:: setValidationMessages($validationMessages)

    :param  array   $validationMessages:

    此函数将设置字段的错误消息。

    使用示例:

    .. literalinclude:: model/031.php

现在,每当调用 ``insert()``、``update()`` 或 ``save()`` 方法时,数据都会被验证。如果失败,模型将返回布尔值 **false**。你可以使用 ``errors()`` 方法检索验证错误:

.. literalinclude:: model/032.php

这会返回一个包含字段名称及其关联错误的数组,可以用来显示表单顶部的所有错误,或单独显示它们:

.. literalinclude:: model/033.php

如果你更喜欢在验证配置文件中组织规则和错误消息,你可以这样做,并简单地将 ``$validationRules`` 设置为你创建的验证规则组的名称:

.. literalinclude:: model/034.php

检索验证规则
---------------------------

你可以通过访问其 ``validationRules`` 属性来检索模型的验证规则:

.. literalinclude:: model/035.php

你还可以只检索这些规则的一个子集,通过直接调用访问器方法并带上选项:

.. literalinclude:: model/036.php

``$options`` 参数是一个包含一个元素的关联数组,其关键字是 ``'except'`` 或 ``'only'``,值是一个感兴趣的字段名数组:

.. literalinclude:: model/037.php

验证占位符
-----------------------

模型提供了一个简单的方法,根据传入的数据替换规则的一部分。这听起来相当模糊,但在使用 ``is_unique`` 验证规则时特别方便。占位符只是传入的数据(或数组键)周围的字段名称,用大括号括起来。它将被匹配的传入字段的 **值** 替换。一个示例应该可以澄清这一点:

.. literalinclude:: model/038.php

在这组规则中,它说明电子邮件地址在数据库中应该是唯一的,除了具有与占位符的值匹配的 id 的行。假设表单 POST 数据如下:

.. literalinclude:: model/039.php

那么 ``{id}`` 占位符会被数字 **4** 替换,得到这条修改后的规则:

.. literalinclude:: model/040.php

所以在验证电子邮件唯一性时,它会忽略数据库中 ``id=4`` 的行。

这也可以用于在运行时创建更动态的规则,只要你注意传入的动态键不与你的表单数据冲突即可。

保护字段
=================

为了帮助防止大规模分配攻击,模型类 **要求** 你列出可以在插入和更新期间更改的所有字段名称在 ``$allowedFields`` 类属性中。除这些字段外提供的任何数据在插入数据库之前都将被删除。这对确保时间戳或主键不被更改非常有用。

.. literalinclude:: model/041.php

有时,你会发现有时需要能够更改这些元素。这通常发生在测试、迁移或种子期间。在这种情况下,可以打开或关闭保护:

.. literalinclude:: model/042.php

运行时返回类型更改
===========================

你可以将 ``find*()`` 方法返回的数据格式指定为类属性 ``$returnType``。但是,有时你可能希望以不同的格式返回数据。模型提供了允许你做到这一点的方法。

.. note:: 这些方法仅更改下一个 **find*()** 方法调用的返回类型。之后,它将重置为默认值。

asArray()
---------

将下一个 **find*()** 方法的数据作为关联数组返回:

.. literalinclude:: model/047.php

asObject()
----------

将下一个 **find*()** 方法的数据作为标准对象或自定义类实例返回:

.. literalinclude:: model/048.php

处理大量数据
================================

有时,你需要处理大量数据,存在耗尽内存的风险。为了简化这一点,你可以使用 chunk() 方法获取较小的块,然后对其执行操作。第一个参数是要在单个块中检索的行数。第二个参数是一个闭包,将为每一行数据调用。

这最适合在定时任务、数据导出或其他大型任务期间使用。

.. literalinclude:: model/049.php

.. _model-events-callbacks:

使用查询构建器
**************************

获取模型表的查询构建器
===========================================

CodeIgniter 模型对该模型的数据库连接有一个查询构建器实例。
你可以在任何需要时访问 **共享** 的查询构建器实例:

.. literalinclude:: model/043.php

此构建器已经使用模型的 ``$table`` 设置。

.. note:: 一旦你获取查询构建器实例,你就可以调用查询构建器的方法。
    但是,由于查询构建器不是模型,你无法调用模型的方法。

获取另一个表的查询构建器
=======================================

如果你需要访问另一个表,你可以获取查询构建器的另一个实例。
将表名称作为参数传递,但要注意这 **不会** 返回共享实例:

.. literalinclude:: model/044.php

混合使用查询构建器和模型的方法
=========================================

你还可以在同一链式调用中使用查询构建器方法和模型的 CRUD 方法,这允许非常优雅地使用:

.. literalinclude:: model/045.php

在这种情况下,它在模型持有的共享查询构建器实例上操作。

.. important:: 模型不为查询构建器提供完美的接口。
    模型和查询构建器是具有不同目的的单独类。
    它们不应该期望返回相同的数据。

如果查询构建器返回结果,它将原封不动地返回。
在这种情况下,结果可能与模型方法返回的不同,可能不是预期的。不会触发模型的事件。

为了防止意外行为,请不要在方法链的末尾使用查询构建器方法并指定模型的方法。

.. note:: 你也可以无缝访问模型的数据库连接:

    .. literalinclude:: model/046.php

模型事件
************

在模型执行的几个点上,你可以指定多个回调方法来运行。这些方法可以用于规范化数据、散列密码、保存相关实体等等。可以影响以下模型执行点,每个都通过一个类属性:``$beforeInsert``、``$afterInsert``、``$beforeUpdate``、``$afterUpdate``、``$afterFind`` 和 ``$afterDelete``。

.. note:: ``$beforeInsertBatch``、``$afterInsertBatch``、``$beforeUpdateBatch`` 和
    ``$afterUpdateBatch`` 可以从 v4.3.0 开始使用。

定义回调
==================

你通过在模型中首先创建要使用的新类方法来指定回调。此类将始终以 ``$data`` 数组作为其唯一参数接收。 ``$data`` 数组的确切内容将因事件而异,但将始终包含一个名为 **data** 的键,其中包含传递给原始方法的主要数据。对于 insert* 或 update* 方法,这将是要插入数据库的键/值对。主数组还将包含传递给方法的其他值,并在后面详细描述。回调方法必须返回原始的 $data 数组,以便其他回调具有完整的信息。

.. literalinclude:: model/050.php

指定要运行的回调
===========================

你可以通过将方法名称添加到适当的类属性(``$beforeInsert``、``$afterUpdate`` 等)来指定运行回调时机。可以向单个事件添加多个回调,并且它们将一个接一个地处理。你可以在多个事件中使用相同的回调:

.. literalinclude:: model/051.php

此外,每个模型可以通过设置其 ``$allowCallbacks`` 属性在类级别允许(默认)或拒绝回调。

.. literalinclude:: model/052.php

你也可以使用 ``allowCallbacks()`` 方法针对单个模型调用暂时更改此设置:

.. literalinclude:: model/053.php

事件参数
================

由于传递给每个回调的确切数据各不相同,因此这里详细介绍了传递给每个事件的 ``$data`` 参数中的内容:

================= =========================================================================================================
事件               $data 内容
================= =========================================================================================================
beforeInsert      **data** = 正在插入的键/值对。如果向 insert 方法传递对象或实体类,则首先转换为数组。
afterInsert       **id** = 新行的主键,如果失败则为 0。
                  **data** = 正在插入的键/值对。
                  **result** = 通过查询构建器使用的 insert() 方法的结果。
beforeInsertBatch **data** = 正在插入的值的关联数组。如果向 insertBatch 方法传递对象或实体类,则首先转换为数组。
afterInsertBatch  **data** = 正在插入的值的关联数组。
                  **result** = 通过查询构建器使用的 insertBatch() 方法的结果。
beforeUpdate      **id** = 正在更新的行的主键数组。
                  **data** = 正在更新的键/值对。如果向 update 方法传递对象或实体类,则首先转换为数组。
afterUpdate       **id** = 正在更新的行的主键数组。
                  **data** = 正在更新的键/值对。
                  **result** = 通过查询构建器使用的 update() 方法的结果。
beforeUpdateBatch **data** = 正在更新的值的关联数组。如果向 updateBatch 方法传递对象或实体类,则首先转换为数组。
afterUpdateBatch  **data** = 正在更新的键/值对。
                  **result** = 通过查询构建器使用的 updateBatch() 方法的结果。
beforeFind        调用的 **方法** 名称,是否请求了 **单例**,以及这些附加字段:
- first()         无附加字段
- find()          **id** = 正在搜索的行的主键。
- findAll()       **limit** = 要找到的行数。
                  **offset** = 在搜索期间要跳过的行数。
afterFind         与 **beforeFind** 相同,但包括结果行数据,如果未找到结果则为 null。
beforeDelete      根据 delete* 方法而变化。参见以下内容:
- delete()        **id** = 正在删除的行的主键。
                  **purge** = 是否应该硬删除软删除的行的布尔值。
afterDelete       **id** = 正在删除的行的主键。
                  **purge** = 是否应该硬删除软删除的行的布尔值。
                  **result** = 在查询构建器上的 delete() 调用的结果。
                  **data** = 未使用。
================= =========================================================================================================

修改 Find* 数据
====================

``beforeFind`` 和 ``afterFind`` 方法都可以返回修改后的数据集以覆盖正常的模型响应。 对于 ``afterFind`` 返回数组中对 ``data`` 所做的任何更改都将自动传递回调用上下文。 为了使 ``beforeFind`` 拦截查找工作流,它还必须返回一个额外的布尔值 ``returnData``:

.. literalinclude:: model/054.php

手动创建模型
*********************

你不需要扩展任何特殊类就可以为应用程序创建模型。你所需要的只是获取数据库连接的一个实例,就可以开始了。这允许你绕过 CodeIgniter 模型提供的开箱即用的功能,并创建一个完全自定义的体验。

.. literalinclude:: model/055.php
