#########################
使用 CodeIgniter 的 Model
#########################

.. contents::
    :local:
    :depth: 3

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

``model()`` 内部使用 ``Factories::models()``。详情参见 :ref:`factories-loading-class`。

CodeIgniter 的 Model
********************

CodeIgniter 确实提供了一个模型类，该类具有一些不错的功能，包括：

- 自动数据库连接
- 基本的 CRUD 方法
- :ref:`模型内验证 <in-model-validation>`
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

当首次实例化类时，如果没有将数据库连接实例传递给构造函数，并且如果你没有在模型类上设置 ``$DBGroup`` 属性，
它将自动连接到数据库配置中设置的默认数据库组。

你可以通过在类中添加 ``$DBGroup`` 属性来修改每个模型使用的组。
这样可以确保在模型内部，对 ``$this->db`` 的任何引用都通过适当的连接进行。

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

指定表是否使用 `$primaryKey`_ 的自增功能。如果设置为 ``false``,则你有责任为表中的每条记录提供主键值。当我们想实现 1:1 关系或在模型中使用 UUID 时,此功能可能很方便。默认值为 ``true``。

.. note:: 如果你将 `$useAutoIncrement`_ 设置为 ``false``,请确保在数据库中将主键设置为 ``unique``。这样可以确保模型的所有功能与以前一样工作。

$returnType
-----------

模型的 **find*()** 方法将为你减少一些工作，自动返回结果数据，而不是 Result 对象。

此设置允许你定义返回的数据类型。有效值为 '**array**'（默认值）、'**object**' 或者可以与 Result 对象的 ``getCustomResultObject()`` 方法一起使用的 **类的完全限定名**。

使用类的特殊常量 ``::class`` 将允许大多数 IDE 自动补全名称，并使重构等功能更好地理解你的代码。

.. _model-use-soft-deletes:

$useSoftDeletes
---------------

如果为 true,那么任何 ``delete()`` 方法调用都会在数据库中设置 ``deleted_at``,而不是真正删除行。这可以在数据可能在其他地方被引用时保留数据,或者可以维护一个“回收站”,其中的对象可以恢复,或者即使只是保留它作为安全轨迹的一部分。如果为 true,则 **find*()** 方法只返回非已删除行,除非在调用 **find*()** 方法之前调用 ``withDeleted()`` 方法。

这需要数据库中具有与模型的 `$dateFormat`_ 设置相应的数据类型的 DATETIME 或 INTEGER 字段。默认字段名称为 ``deleted_at``,但是可以通过使用 `$deletedField`_ 属性将其配置为你选择的任何名称。

.. important:: 数据库中的 ``deleted_at`` 字段必须是 nullable 的。

.. _model-allowed-fields:

$allowedFields
--------------

当通过 ``save()``、``insert()`` 或 ``update()`` 方法设置时,此数组应更新可以设置的字段名称。这些字段名之外的任何字段都会被丢弃。这有助于防止只从表单获取输入并将其全部抛给模型,从而导致潜在的大规模分配漏洞。

.. note:: `$primaryKey`_ 字段永远不应该是允许的字段。

$allowEmptyInserts
------------------

.. versionadded:: 4.3.0

是否允许插入空数据。默认值是 ``false``，这意味着如果你尝试插入空数据，将会抛出带有 "There is no data to insert." 信息的 ``DataException``。

你也可以通过 :ref:`model-allow-empty-inserts` 方法来改变这个设置。

.. _model-update-only-changed:

$updateOnlyChanged
------------------

.. versionadded:: 4.5.0

是否仅更新 :doc:`Entity <./entities>` 的已更改字段。默认值是 ``true``，这意味着在更新到数据库时仅使用已更改的字段数据。因此，如果你尝试更新一个没有更改的 Entity，将会抛出带有 "There is no data to update." 信息的 ``DataException``。

将此属性设置为 ``false`` 将确保 Entity 的所有允许字段在任何时候都提交到数据库并进行更新。

$casts
------

.. versionadded:: 4.5.0

这允许你将从数据库检索到的数据转换为适当的 PHP 类型。
此选项应为一个数组，其中键是字段的名称，值是数据类型。详情请参见 :ref:`model-field-casting`。

日期
-----

$useTimestamps
^^^^^^^^^^^^^^

此布尔值确定是否会向所有插入和更新自动添加当前日期。如果为 ``true``,将以 `$dateFormat`_ 中指定的格式设置当前时间。这需要表中具有数据类型适当的 **created_at**、**updated_at** 和 **deleted_at** 列。也可参考 `$createdField`_, `$updatedField`_ 和 `$deletedField`_。

$dateFormat
^^^^^^^^^^^

此值与 `$useTimestamps`_ 和 `$useSoftDeletes`_ 一起使用,以确保插入到数据库中的是正确类型的日期值。默认情况下,这会创建 DATETIME 值,但有效选项有: ``'datetime'``、 ``'date'`` 或 ``'int'`` (UNIX 时间戳)。在缺少或无效的 `$dateFormat`_ 情况下使用 `$useSoftDeletes`_ 或 `$useTimestamps`_ 会引发异常。

$createdField
^^^^^^^^^^^^^

指定用于数据记录创建时间戳的数据库字段。如果设置为空字符串 (``''``) 则不更新它(即使启用了 `$useTimestamps`_)。

$updatedField
^^^^^^^^^^^^^

指定应该用于保持数据记录更新时间戳的数据库字段。如果设置为空字符串 (``''``) 则不更新它(即使启用了 `$useTimestamps`_)。

$deletedField
^^^^^^^^^^^^^

指定用于软删除的数据库字段。参见 :ref:`model-use-soft-deletes`。

验证
----------

$validationRules
^^^^^^^^^^^^^^^^

包含一个验证规则数组，如 :ref:`validation-array` 中所述，或者包含验证组名称的字符串，如同一节中所述。
另请参见 :ref:`model-setting-validation-rules`。

$validationMessages
^^^^^^^^^^^^^^^^^^^

包含一个自定义错误消息数组，这些消息将在验证过程中使用，如 :ref:`validation-custom-errors` 中所述。另请参见 :ref:`model-setting-validation-rules`。

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

是否应使用下面定义的回调。参考 :ref:`model-events`。

$beforeInsert
^^^^^^^^^^^^^
$afterInsert
^^^^^^^^^^^^
$beforeUpdate
^^^^^^^^^^^^^
$afterUpdate
^^^^^^^^^^^^^
$beforeFind
^^^^^^^^^^^
$afterFind
^^^^^^^^^^
$beforeDelete
^^^^^^^^^^^^^
$afterDelete
^^^^^^^^^^^^
$beforeInsertBatch
^^^^^^^^^^^^^^^^^^
$afterInsertBatch
^^^^^^^^^^^^^^^^^
$beforeUpdateBatch
^^^^^^^^^^^^^^^^^^
$afterUpdateBatch
^^^^^^^^^^^^^^^^^

这些数组允许你指定在属性名称中指定的时间回调方法。参考 :ref:`model-events`。

.. _model-field-casting:

模型字段类型转换
****************

.. versionadded:: 4.5.0

从数据库检索数据时，整数类型的数据可能会在 PHP 中转换为字符串类型。你可能还希望将日期/时间数据转换为 PHP 中的 Time 对象。

模型字段类型转换允许你将从数据库检索到的数据转换为适当的 PHP 类型。

.. important::
    如果你在使用 :doc:`Entity <./entities>` 时使用了此功能，请不要使用
    :ref:`Entity 属性类型转换 <entities-property-casting>`。同时使用这两种类型转换是无效的。

    Entity 属性类型转换在 (1)(4) 处工作，而此类型转换在 (2)(3) 处工作::

        [应用代码] --- (1) --> [Entity] --- (2) --> [数据库]
        [应用代码] <-- (4) --- [Entity] <-- (3) --- [数据库]

    使用此类型转换时，Entity 将在属性中具有正确类型的 PHP 值。这种行为与之前的行为完全不同。不要期望属性中持有来自数据库的原始数据。

定义数据类型
=============

``$casts`` 属性设置其定义。此选项应为一个数组，其中键是字段的名称，值是数据类型：

.. literalinclude:: model/057.php

数据类型
=========

默认提供以下类型。在类型前添加问号以标记字段为可为空，例如，``?int``，``?datetime``。

+---------------+----------------+---------------------------+
| 类型          | PHP 类型       | 数据库字段类型            |
+===============+================+===========================+
|``int``        | int            | int 类型                  |
+---------------+----------------+---------------------------+
|``float``      | float          | float（数值）类型         |
+---------------+----------------+---------------------------+
|``bool``       | bool           | bool/int/string 类型      |
+---------------+----------------+---------------------------+
|``int-bool``   | bool           | int 类型（1 或 0）        |
+---------------+----------------+---------------------------+
|``array``      | array          | string 类型（序列化）     |
+---------------+----------------+---------------------------+
|``csv``        | array          | string 类型（CSV）        |
+---------------+----------------+---------------------------+
|``json``       | stdClass       | json/string 类型          |
+---------------+----------------+---------------------------+
|``json-array`` | array          | json/string 类型          |
+---------------+----------------+---------------------------+
|``datetime``   | Time           | datetime 类型             |
+---------------+----------------+---------------------------+
|``timestamp``  | Time           | int 类型（UNIX 时间戳）   |
+---------------+----------------+---------------------------+
|``uri``        | URI            | string 类型               |
+---------------+----------------+---------------------------+

csv
---

将类型转换为 ``csv`` 使用 PHP 的内部 ``implode()`` 和 ``explode()`` 函数，并假设所有值都是字符串安全且不含逗号。对于更复杂的数据类型转换，尝试使用 ``array`` 或 ``json``。

datetime
--------

你可以传递类似 ``datetime[ms]`` 的参数表示带有毫秒的日期/时间，或 ``datetime[us]`` 表示带有微秒的日期/时间。

日期时间格式在 **app/Config/Database.php** 文件中的 :ref:`数据库配置 <database-config-explanation-of-values>` 的 ``dateFormat`` 数组中设置。

自定义类型转换
===============

你可以定义自己的转换类型。

创建自定义处理程序
--------------------

首先，你需要为你的类型创建一个处理程序类。假设该类位于 **app/Models/Cast** 目录中：

.. literalinclude:: model/058.php

如果你不需要在获取或设置值时更改值，那么只需不实现相应的方法：

.. literalinclude:: model/060.php

注册自定义处理程序
--------------------

现在你需要注册它：

.. literalinclude:: model/059.php

参数
----

在某些情况下，一种类型是不够的。在这种情况下，你可以使用附加参数。附加参数在方括号中指示，并用逗号列出，例如 ``type[param1, param2]``。

.. literalinclude:: model/061.php

.. literalinclude:: model/062.php

.. note:: 如果类型转换类型标记为 nullable，例如 ``?bool``，并且传递的值不为空，那么值为 ``nullable`` 的参数将传递给类型转换处理程序。如果类型转换具有预定义参数，则 ``nullable`` 将添加到列表的末尾。

使用数据
*****************

查找数据
============

提供了几个函数来对表执行基本的 CRUD 工作,包括 ``find()``、``insert()``、``update()``、``delete()`` 等等。

find()
------

在主键与作为第一参数传递的值匹配的情况下,返回单行。

.. literalinclude:: model/006.php

该值以 `$returnType`_ 中指定的格式返回。

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

如果 `$useSoftDeletes`_ 为 true,则 **find*()** 方法不会返回任何 ``deleted_at IS NOT NULL`` 的行。
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

数组的键必须与 `$table`_ 中的列名匹配,而数组的值是要为该键保存的值。

可选的第二个参数为布尔类型,如果设置为 false,该方法将返回一个布尔值,表示查询的成功或失败。

你可以使用 ``getInsertID()`` 方法检索最后插入的行的主键。

.. literalinclude:: model/015.php

.. _model-allow-empty-inserts:

allowEmptyInserts()
-------------------

.. versionadded:: 4.3.0

你可以使用 ``allowEmptyInserts()`` 方法插入空数据。默认情况下,模型在你尝试插入空数据时会抛出异常。但是如果调用此方法,将不再执行检查。

.. literalinclude:: model/056.php

你也可以通过 `$allowEmptyInserts`_ 属性来改变这个设置。

你可以通过调用 ``allowEmptyInserts(false)`` 再次启用检查。

update()
--------

更新数据库中的现有记录。第一个参数是要更新的记录的 `$primaryKey`_。关联数组作为第二个参数传递给此方法。数组的键必须与 `$table`_ 中的列名匹配,而数组的值是要为该键保存的值:

.. literalinclude:: model/016.php

.. important:: 从 v4.3.0 开始,如果它生成没有 WHERE 子句的 SQL 语句,此方法会抛出 ``DatabaseException``。
    在以前的版本中,如果在没有指定 `$primaryKey`_ 的情况下调用它并生成没有 WHERE 子句的 SQL 语句,查询仍会执行,表中的所有记录都会被更新。

可以通过作为第一个参数传递主键数组来一次更新多条记录:

.. literalinclude:: model/017.php

当你需要更灵活的解决方案时,可以留空参数,它的作用类似于查询构建器的 update 命令,具有验证、事件等的额外优势:

.. literalinclude:: model/018.php

.. _model-save:

save()
------

这是 ``insert()`` 和 ``update()`` 方法的包装器,可以根据是否找到与 **主键** 值匹配的数组键来自动处理插入或更新记录。

.. literalinclude:: model/019.php

save 方法还可以通过识别非简单对象并将其公共和受保护的值抓取到一个数组中，然后将该数组传递给适当的 insert 或 update 方法，从而使处理自定义类结果对象变得更加简单。这使你可以非常简洁地使用 Entity 类。Entity 类是表示某种对象类型的单个实例的简单类，比如用户、博客文章、工作等。这个类负责维护围绕对象本身的业务逻辑，比如以某种方式格式化元素等。它们不应该知道如何将自己保存到数据库中。最简单的情况下，它们可能看起来像这样：

.. literalinclude:: model/020.php

与此配合使用的一个非常简单的模型可能如下所示:

.. literalinclude:: model/021.php

该模型使用来自 ``jobs`` 表的数据,并将所有结果返回为 ``App\Entities\Job`` 的实例。
当你需要将该记录持久化到数据库时,你需要编写自定义方法,或者使用模型的 ``save()`` 方法检查类、获取任何公共和私有属性,并将它们保存到数据库:

.. literalinclude:: model/022.php

.. note:: 如果你发现自己频繁使用实体,CodeIgniter 提供了一个内置的 :doc:`实体类 </models/entities>`,
    它提供了使开发实体更简单的几个方便的功能。

.. _model-saving-dates:

保存日期
--------

.. versionadded:: 4.5.0

在保存数据时，如果你传递 :doc:`Time <../libraries/time>` 实例，它们会根据
:ref:`数据库配置 <database-config-explanation-of-values>` 中 ``dateFormat['datetime']`` 和 ``dateFormat['date']`` 定义的格式转换为字符串。

.. note:: 在 v4.5.0 之前，日期/时间格式在 Model 类中是硬编码为 ``Y-m-d H:i:s`` 和 ``Y-m-d``。

删除数据
=============

delete()
--------

以主键值作为第一个参数,从模型的表中删除匹配的记录:

.. literalinclude:: model/023.php

如果模型的 `$useSoftDeletes`_ 值为 true,这将更新行以将 ``deleted_at`` 设置为当前日期和时间。你可以通过将第二个参数设置为 true 来强制永久删除。

可以作为第一个参数传递主键数组,以一次删除多条记录:

.. literalinclude:: model/024.php

如果没有传递参数,将像查询构建器的 delete 方法一样操作,需要事先进行 where 调用:

.. literalinclude:: model/025.php

purgeDeleted()
--------------

通过永久删除所有 'deleted_at IS NOT NULL' 的行来清理数据库表。

.. literalinclude:: model/026.php

.. _in-model-validation:

模型内验证
===================

.. warning:: 在模型内验证是在数据存储到数据库之前进行的。在此之前，数据尚未经过验证。在验证之前处理用户输入的数据可能会引入漏洞。

验证数据
---------------

Model 类提供了一种方法，可以在使用 ``insert()``、``update()`` 或 ``save()`` 方法保存到数据库之前自动验证所有数据。

.. important:: 当你更新数据时，默认情况下，模型类中的验证只会验证提供的字段。这是为了避免在仅更新某些字段时出现验证错误。

    然而，这意味着在更新期间并不会检查你设置的所有验证规则。因此，不完整的数据可能会通过验证。

    例如，``required*`` 规则或需要其他字段值的 ``is_unique`` 规则可能不会按预期工作。

    为了避免这种问题，可以通过配置更改此行为。详情请参见 :ref:`clean-validation-rules`。

.. _model-setting-validation-rules:

设置验证规则
------------------------

第一步是填写 `$validationRules`_ 类属性，包含需要应用的字段和规则。

.. note:: 你可以在 :ref:`validation-available-rules` 中查看内置验证规则的列表。

如果你有自定义的错误消息，可以将它们放在 `$validationMessages`_ 数组中：

.. literalinclude:: model/027.php

如果你更愿意在 :ref:`Validation Config File <saving-validation-rules-to-config-file>` 中组织你的规则和错误消息，你可以这样做，然后只需将 `$validationRules`_ 设置为你创建的验证规则组的名称：

.. literalinclude:: model/034.php

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

获取验证结果
-------------------------

现在，每当你调用 ``insert()``、``update()`` 或 ``save()`` 方法时，数据将被验证。如果验证失败，模型将返回布尔值 **false**。

.. _model-getting-validation-errors:

获取验证错误
-------------------------

你可以使用 ``errors()`` 方法来检索验证错误：

.. literalinclude:: model/032.php

这会返回一个包含字段名称及其关联错误的数组,可以用来显示表单顶部的所有错误,或单独显示它们:

.. literalinclude:: model/033.php

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

.. note:: 自 v4.3.5 起，你必须为占位符字段（``id``）设置验证规则。

在这组规则中,它说明电子邮件地址在数据库中应该是唯一的,除了具有与占位符的值匹配的 id 的行。假设表单 POST 数据如下:

.. literalinclude:: model/039.php

那么 ``{id}`` 占位符会被数字 **4** 替换,得到这条修改后的规则:

.. literalinclude:: model/040.php

所以在验证电子邮件唯一性时,它会忽略数据库中 ``id=4`` 的行。

.. note:: 自 v4.3.5 起，如果占位符（``id``）的值未通过验证，占位符将不会被替换。

这也可以用于在运行时创建更动态的规则,只要你注意传入的动态键不与你的表单数据冲突即可。

保护字段
=================

为了帮助防止大规模分配攻击,模型类 **要求** 你列出可以在插入和更新期间更改的所有字段名称在 `$allowedFields`_ 类属性中。除这些字段外提供的任何数据在插入数据库之前都将被删除。这对确保时间戳或主键不被更改非常有用。

.. literalinclude:: model/041.php

有时,你会发现有时需要能够更改这些元素。这通常发生在测试、迁移或种子期间。在这种情况下,可以打开或关闭保护:

.. literalinclude:: model/042.php

运行时返回类型更改
===========================

你可以将 ``find*()`` 方法返回的数据格式指定为类属性 `$returnType`_。但是,有时你可能希望以不同的格式返回数据。模型提供了允许你做到这一点的方法。

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

此构建器已经使用模型的 `$table`_ 设置。

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

.. _model-events:

模型事件
************

在模型执行的几个点上,你可以指定多个回调方法来运行。这些方法可以用于规范化数据、散列密码、保存相关实体等等。

可以影响以下模型执行点,每个都通过一个类属性:

- `$beforeInsert`_, `$afterInsert`_
- `$beforeUpdate`_, `$afterUpdate`_
- `$beforeFind`_, `$afterFind`_
- `$beforeDelete`_, `$afterDelete`_
- `$beforeInsertBatch`_, `$afterInsertBatch`_
- `$beforeUpdateBatch`_, `$afterUpdateBatch`_

.. note:: ``$beforeInsertBatch``、``$afterInsertBatch``、``$beforeUpdateBatch`` 和
    ``$afterUpdateBatch`` 可以从 v4.3.0 开始使用。

定义回调函数
==================

你可以通过在模型中创建一个新的类方法来指定回调函数。

这个类方法总是会接收一个 ``$data`` 数组作为唯一的参数。

``$data`` 数组的具体内容会因事件而异，但总是会包含一个名为 ``data`` 的键，该键包含传递给原始方法的主要数据。在 **insert*()** 或 **update*()** 方法的情况下，这将是正在插入到数据库中的键/值对。主要的 ``$data`` 数组也会包含传递给方法的其他值，并在 `事件参数`_ 中详细说明。

回调方法必须返回原始的 ``$data`` 数组，以便其他回调函数获取完整信息。

.. literalinclude:: model/050.php

指定要运行的回调
===========================

你可以通过将方法名称添加到适当的类属性(`$beforeInsert`_, `$afterUpdate`_ 等)来指定运行回调时机。可以向单个事件添加多个回调,并且它们将一个接一个地处理。你可以在多个事件中使用相同的回调:

.. literalinclude:: model/051.php

此外,每个模型可以通过设置其 `$allowCallbacks`_ 属性在类级别允许(默认)或拒绝回调。

.. literalinclude:: model/052.php

你也可以使用 ``allowCallbacks()`` 方法针对单个模型调用暂时更改此设置:

.. literalinclude:: model/053.php

事件参数
================

由于传递给每个回调的确切数据各不相同,因此这里详细介绍了传递给每个事件的 ``$data`` 参数中的内容:

================= =========================================================================================================
事件               $data 内容
================= =========================================================================================================
beforeInsert      **data** = 正在插入的键/值对。如果将对象或 Entity 类传递给
                  ``insert()`` 方法，它首先会被转换为数组。
afterInsert       **id** = 新行的主键，如果失败则为 0。
                  **data** = 正在插入的键/值对。
                  **result** = 通过查询构建器使用的 ``insert()`` 方法的结果。
beforeUpdate      **id** = 传递给 ``update()`` 方法的行的主键数组。
                  **data** = 正在更新的键/值对。如果将对象或 Entity 类传递给
                  ``update()`` 方法，它首先会被转换为数组。
afterUpdate       **id** = 传递给 ``update()`` 方法的行的主键数组。
                  **data** = 正在更新的键/值对。
                  **result** = 通过查询构建器使用的 ``update()`` 方法的结果。
beforeFind        调用 **method** 的名称，是否请求了 **singleton**，以及以下附加字段：
- ``first()``     没有附加字段
- ``find()``      **id** = 正在搜索的行的主键。
- ``findAll()``   **limit** = 要查找的行数。
                  **offset** = 在搜索过程中要跳过的行数。
afterFind         与 **beforeFind** 相同，但包括找到的行的数据结果，如果没有找到结果则为 null。
beforeDelete      **id** = 被传递给 ``delete()`` 方法的行的主键。
                  **purge** = 是否应硬删除软删除的行的布尔值。
afterDelete       **id** = 被传递给 ``delete()`` 方法的行的主键。
                  **purge** = 是否应硬删除软删除的行的布尔值。
                  **result** = 在查询构建器上调用 ``delete()`` 的结果。
                  **data** = 未使用。
beforeInsertBatch **data** = 正在插入的值的关联数组。如果将对象或 Entity 类传递给
                  ``insertBatch()`` 方法，它首先会被转换为数组。
afterInsertBatch  **data** = 正在插入的值的关联数组。
                  **result** = 通过查询构建器使用的 ``insertBatch()`` 方法的结果。
beforeUpdateBatch **data** = 正在更新的值的关联数组。如果将对象或 Entity 类传递给
                  ``updateBatch()`` 方法，它首先会被转换为数组。
afterUpdateBatch  **data** = 正在更新的键/值对。
                  **result** = 通过查询构建器使用的 ``updateBatch()`` 方法的结果。
================= =========================================================================================================

修改 Find* 数据
====================

``beforeFind`` 和 ``afterFind`` 方法都可以返回修改后的数据集以覆盖正常的模型响应。 对于 ``afterFind`` 返回数组中对 ``data`` 所做的任何更改都将自动传递回调用上下文。 为了使 ``beforeFind`` 拦截查找工作流,它还必须返回一个额外的布尔值 ``returnData``:

.. literalinclude:: model/054.php

手动创建模型
*********************

你不需要扩展任何特殊类就可以为应用程序创建模型。你所需要的只是获取数据库连接的一个实例,就可以开始了。这允许你绕过 CodeIgniter 模型提供的开箱即用的功能,并创建一个完全自定义的体验。

.. literalinclude:: model/055.php
