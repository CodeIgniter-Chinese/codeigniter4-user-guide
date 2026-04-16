#########################
使用 CodeIgniter 的模型
#########################

.. contents::
    :local:
    :depth: 3

模型
****

CodeIgniter 模型提供了一系列便捷功能与扩展，旨在简化数据库 **单表** 操作。

模型内置了大量开箱即用的辅助方法，涵盖查询、更新、删除记录等常见数据库表交互场景。

.. _accessing-models:

访问模型
****************

模型通常存储在 **app/Models** 目录中。应具有与目录位置匹配的命名空间，例如 ``namespace App\Models``。

在类中访问模型时，可以创建新实例或使用 :php:func:`model()` 辅助函数。

.. literalinclude:: model/001.php

``model()`` 内部使用 ``Factories::models()``。
有关第一个参数的详细信息，请参阅 :ref:`factories-loading-class`。

CodeIgniter 的模型
*******************

CodeIgniter 提供的模型类包含以下特性：

- 自动数据库连接
- 基础 CRUD 方法
- :ref:`模型内验证 <in-model-validation>`
- :ref:`自动分页 <paginating-with-models>`
- 及其他功能

该类为构建自定义模型提供了坚实基础，可快速构建应用程序的模型层。

创建模型
*******************

要使用 CodeIgniter 的模型，只需新建继承自 ``CodeIgniter\Model`` 的模型类：

.. literalinclude:: model/002.php

这个空类提供了对数据库连接、查询构建器和多个便捷方法的访问。

initialize()
============

如需在模型中进行额外设置，可扩展 ``initialize()`` 方法。该方法会在模型构造函数之后立即执行，避免重复构造函数参数，例如扩展其他模型：

.. literalinclude:: model/003.php

连接数据库
==========================

类首次实例化时，如果构造函数未传入数据库连接实例，且未在模型类中设置 ``$DBGroup`` 属性，则会自动连接到数据库配置中的默认数据库组。

通过添加 ``$DBGroup`` 属性可修改每个模型使用的数据库组，确保模型中所有 ``$this->db`` 引用都通过正确的连接进行：

.. literalinclude:: model/004.php

需要将 "group_name" 替换为数据库配置文件中定义的数据库组名称。

配置模型
======================

模型类有一些可配置的选项，让类的方法能够无缝工作。前两个选项由所有 CRUD 方法使用，用于确定操作的表以及如何查找所需记录：

.. literalinclude:: model/005.php

$table
------

指定模型主要操作的数据表。仅适用于内置 CRUD 方法，自定义查询不受限制。

$primaryKey
-----------

该字段名称用于唯一标识表中的记录。不必与数据库主键完全匹配，但会被 ``find()`` 等方法用来确定与指定值匹配的字段。

.. note:: 所有模型都必须指定 primaryKey，以便所有功能按预期工作。

$useAutoIncrement
-----------------

指定表是否对 `$primaryKey`_ 使用自增特性。如果设为 ``false``，则需要为表中的每条记录提供主键值。在需要实现 1:1 关联或使用 UUID 时，此功能非常有用。默认值为 ``true``。

.. note:: 如果将 `$useAutoIncrement`_ 设为 ``false``，请确保数据库中的主键设为 ``unique``，以保证模型功能正常。

$returnType
-----------

模型的 **find*()** 方法会自动返回结果数据，而不是 Result 对象。

此设置用于定义返回数据的类型。有效值为 '**array**'（默认值）、'**object**'，或可与 Result 对象的 ``getCustomResultObject()`` 方法配合使用的 **类的完全限定名**。

使用类的 ``::class`` 常量可让大多数 IDE 自动补全名称，并使重构等功能更好地理解代码。

.. _model-use-soft-deletes:

$useSoftDeletes
---------------

若设为 true，调用 ``delete()`` 方法时将仅更新数据库中的 ``deleted_at`` 字段，而非执行物理删除。此举有助于保留仍被其他位置引用的数据，或用于实现可恢复的“回收站”功能，亦可作为安全审计轨迹。设为 true 后，**find*()** 系列方法默认仅返回未删除的记录，如需获取包含已删除在内的完整数据，须在查询前调用 ``withDeleted()`` 方法。

根据模型的 `$dateFormat`_ 设置，数据库需要包含 DATETIME 或 INTEGER 类型的字段。默认字段名为 ``deleted_at``，但可通过 `$deletedField`_ 属性配置为任意名称。

.. important:: 数据库中的 ``deleted_at`` 字段必须允许为 null。

.. _model-allowed-fields:

$allowedFields
--------------

此数组应填入可在 ``save()``、``insert()`` 或 ``update()`` 方法中使用的字段名。任何不在此列表中的字段名都会被丢弃。这有助于防止直接将表单数据提交给模型，从而避免潜在的大批量赋值攻击。

.. note:: `$primaryKey`_ 字段不应列入允许字段。

$allowEmptyInserts
------------------

.. versionadded:: 4.3.0

是否允许插入空数据。默认值为 ``false``，这意味着如果你尝试插入空数据，将会抛出带有 "There is no data to insert." 信息的 ``DataException``。

也可以通过 :ref:`model-allow-empty-inserts` 方法更改此设置。

.. _model-update-only-changed:

$updateOnlyChanged
------------------

.. versionadded:: 4.5.0

是否只更新 :doc:`实体 <./entities>` 中已更改的字段。默认值为 ``true``，表示更新数据库时只使用已更改的字段数据。因此，尝试更新没有变化的实体时，会抛出带有 "There is no data to update." 信息的 ``DataException``。

将此属性设为 ``false`` 可确保实体的所有允许字段都提交到数据库并随时更新。

$casts
------

.. versionadded:: 4.5.0

可将从数据库检索的数据转换为适当的 PHP 类型。
此选项应为一个数组，键为字段名，值为数据类型。详细信息请参阅 :ref:`model-field-casting`。

日期配置
--------

$useTimestamps
^^^^^^^^^^^^^^

此布尔值决定是否在所有插入和更新时自动添加当前日期。如果为 ``true``，会按照 `$dateFormat`_ 指定的格式设置当前时间。这要求表包含 **created_at**、**updated_at** 和 **deleted_at** 字段，且数据类型适当。另请参阅 `$createdField`_、`$updatedField`_ 和 `$deletedField`_。

$dateFormat
^^^^^^^^^^^

此值与 `$useTimestamps`_ 和 `$useSoftDeletes`_ 配合使用，确保向数据库插入正确类型的日期值。默认情况下生成 DATETIME 值，但有效选项包括：``'datetime'``、``'date'`` 或 ``'int'`` （UNIX 时间戳）。将 `$useSoftDeletes`_ 或 `$useTimestamps`_ 与无效或缺失的 `$dateFormat`_ 配合使用会抛出异常。

$createdField
^^^^^^^^^^^^^

指定用于记录数据创建时间戳的数据库字段。设为空字符串（``''``）可避免更新（即使启用了 `$useTimestamps`_）。

$updatedField
^^^^^^^^^^^^^

指定用于记录数据更新时间戳的数据库字段。设为空字符串（``''``）可避免更新（即使启用了 `$useTimestamps`_）。

$deletedField
^^^^^^^^^^^^^

指定用于软删除的数据库字段。请参阅 :ref:`model-use-soft-deletes`。

验证
----------

$validationRules
^^^^^^^^^^^^^^^^

包含验证规则数组（如 :ref:`validation-array` 所述）或验证组名称的字符串（同一章节中有说明）。另请参阅 :ref:`model-setting-validation-rules`。

$validationMessages
^^^^^^^^^^^^^^^^^^^

包含验证期间使用的自定义错误消息数组，如 :ref:`validation-custom-errors` 所述。另请参阅 :ref:`model-setting-validation-rules`。

$skipValidation
^^^^^^^^^^^^^^^

决定在所有 **插入** 和 **更新** 操作期间是否跳过验证。默认值为 ``false``，表示始终尝试验证数据。这主要由 ``skipValidation()`` 方法使用，但也可以设为 ``true``，使此模型永远不进行验证。

.. _clean-validation-rules:

$cleanValidationRules
^^^^^^^^^^^^^^^^^^^^^

用于 **更新** 操作。该选项决定是否移除传入数据中未包含字段的验证规则。默认值为 ``true``。开启后，在执行验证前会（临时）移除缺失字段的验证规则，从而避免仅更新部分字段时触发不必要的验证错误。

也可以通过 ``cleanRules()`` 方法更改此值。

.. note:: v4.2.7 之前版本中，``$cleanValidationRules`` 因一个 bug 而未生效。

回调
---------

$allowCallbacks
^^^^^^^^^^^^^^^

决定是否使用下方定义的回调。请参阅 :ref:`model-events`。

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

通过这些数组属性可指定回调方法，从而在属性名对应的时间点对数据进行处理。详见 :ref:`model-events`。

.. _model-field-casting:

模型字段类型转换
*******************

.. versionadded:: 4.5.0

从数据库检索数据时，整数类型的数据在 PHP 中可能会转换为字符串类型。也可能需要将日期/时间数据转换为 PHP 中的 Time 对象。

模型字段类型转换允许将从数据库检索的数据转换为适当的 PHP 类型。

.. important::
    如果将此功能与 :doc:`实体 <./entities>` 配合使用，请不要使用
    :ref:`实体属性类型转换 <entities-property-casting>`。同时使用两种类型转换将无法正常工作。

    实体属性类型转换在 (1)(4) 处工作，但此类型转换在 (2)(3) 处工作::

        [应用代码] --- (1) --> [实体] --- (2) --> [数据库]
        [应用代码] <-- (4) --- [实体] <-- (3) --- [数据库]

    使用此类型转换时，实体的属性中将包含正确的类型化 PHP 值。此行为与之前的行为完全不同。
    不要期望属性中保存的是数据库中的原始数据。

定义数据类型
===================

``$casts`` 属性用于设置定义。此选项应为一个数组，键为字段名，值为数据类型：

.. literalinclude:: model/057.php

数据类型
==========

默认提供以下类型。在类型前加问号可将字段标记为可空，例如 ``?int``、``?datetime``。

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

使用 ``csv`` 类型转换会调用 PHP 内置的 ``implode()`` 和 ``explode()`` 函数，
假设所有值对字符串安全且不包含逗号。对于更复杂的数据转换，请尝试 ``array`` 或 ``json``。

datetime
--------

可以传递 ``datetime[ms]`` 参数表示带毫秒的日期/时间，或 ``datetime[us]`` 表示带微秒的日期/时间。

日期时间格式在 **app/Config/Database.php** 文件中
:ref:`数据库配置 <database-config-explanation-of-values>` 的 ``dateFormat`` 数组中设置。

.. note::
    将 ``ms`` 或 ``us`` 设为参数时，**模型** 会自动处理 Time 的小数秒部分。
    由于 **查询构建器** 不具备此功能，向 ``where()`` 等方法传递时间对象时，仍需调用 ``format()`` 方法进行格式化：

    .. literalinclude:: model/063.php
        :lines: 2-

.. note:: v4.6.0 之前的版本不支持将 ``ms`` 或 ``us`` 作为参数。
    这是由于当时存在的 Bug 会导致 Time 的小数秒部分丢失。

timestamp
---------

创建的 ``Time`` 实例的时区将是默认时区（应用的时区），而不是 UTC。

自定义类型转换
==============

可以定义自己的类型转换。

创建自定义处理器
------------------------

首先需要为类型创建处理器类。假设类位于 **app/Models/Cast** 目录：

.. literalinclude:: model/058.php

若获取或设置值时无需修改数据，则无需实现相应方法：

.. literalinclude:: model/060.php

注册自定义处理器
---------------------------

现在需要注册它：

.. literalinclude:: model/059.php

参数
----------

在某些情况下，一种类型不够用。此时可使用额外参数。额外参数用方括号括起来，用逗号分隔，如 ``type[param1, param2]``。

.. literalinclude:: model/061.php

.. literalinclude:: model/062.php

.. note:: 如果类型转换标记为可空（如 ``?bool``）且传入的值不为 null，则会将值为 ``nullable`` 的参数传递给类型转换处理器。如果类型已有预定义参数，则 ``nullable`` 会添加到列表末尾。

数据处理
*****************

查找数据
============

提供多个函数对表执行基本的 CRUD 操作，包括 ``find()``、``insert()``、``update()``、``delete()`` 等。

find()
------

返回主键与第一个参数匹配的单行数据：

.. literalinclude:: model/006.php

返回值格式由 `$returnType`_ 指定。

可以传递主键值数组来指定多行，而不是仅传递一个值：

.. literalinclude:: model/007.php

.. note:: 如果未传入参数，``find()`` 会返回模型表中的所有记录，效果类似于 ``findAll()``，但不那么明确。

findColumn()
------------

返回 null 或列值的索引数组：

.. literalinclude:: model/008.php

``$columnName`` 应为单个字段名，否则会抛出 ``DataException``。

findAll()
---------

返回所有结果：

.. literalinclude:: model/009.php

可在调用此方法之前通过插入查询构建器命令来修改查询：

.. literalinclude:: model/010.php

可分别将 limit 和 offset 值作为第一个和第二个参数传入：

.. literalinclude:: model/011.php

first()
-------

返回结果集中的第一行。此方法最好与查询构建器配合使用。

.. literalinclude:: model/012.php

withDeleted()
-------------

如果 `$useSoftDeletes`_ 为 true，则 **find*()** 方法不会返回 ``deleted_at IS NOT NULL`` 的任何记录。要临时覆盖此行为，可在调用 **find*()** 方法之前使用 ``withDeleted()`` 方法。

.. literalinclude:: model/013.php

onlyDeleted()
-------------

``withDeleted()`` 会同时返回已删除和未删除的行，而此方法会修改下一个 **find*()** 方法，使其只返回软删除的行：

.. literalinclude:: model/014.php

保存数据
===========

insert()
--------

第一个参数是关联数组，用于在数据库中创建新记录。若传入对象，则会尝试将其转换为数组。

数组键名必须与 `$table`_ 中的字段名一致，键值即为待保存的数据。

第二个参数为可选的布尔值。若设为 false，该方法将返回布尔值，以指示查询执行成功与否。

调用 ``getInsertID()`` 方法可获取最后插入记录的主键。

.. literalinclude:: model/015.php

.. _model-allow-empty-inserts:

allowEmptyInserts()
-------------------

.. versionadded:: 4.3.0

可使用 ``allowEmptyInserts()`` 方法插入空数据。默认情况下，模型在尝试插入空数据时会抛出异常。但调用此方法后，将不再执行此检查。

.. literalinclude:: model/056.php

也可通过 `$allowEmptyInserts`_ 属性更改此设置。

可通过调用 ``allowEmptyInserts(false)`` 重新启用此检查。

update()
--------

更新数据库中的现有记录。第一个参数是要更新的记录的 `$primaryKey`_。关联数组作为第二个参数传入。数组键名必须与 `$table`_ 中的字段名一致，键值即为待保存的数据：

.. literalinclude:: model/016.php

.. important:: v4.3.0 起，此方法在生成不含 WHERE 子句的 SQL 语句时会抛出 ``DatabaseException``。
    在之前版本中，如果未指定 `$primaryKey`_ 且生成了不含 WHERE 子句的 SQL 语句，查询仍会执行，
    表中的所有记录都会被更新。

可通过将主键数组作为第一个参数传入来单次更新多条记录：

.. literalinclude:: model/017.php

当需要更灵活的解决方案时，可以留空参数，其功能类似于查询构建器的 update 命令，并额外享受验证、事件等功能：

.. literalinclude:: model/018.php

.. _model-save:

save()
------

这是 ``insert()`` 和 ``update()`` 方法的包装器，根据是否找到与 **主键** 值匹配的数组键来自动处理插入或更新：

.. literalinclude:: model/019.php

save 方法支持处理自定义类对象，极大简化了相关操作。该方法能自动识别非简单对象，将其 public 与 protected 属性提取为数组，并传递给相应的插入或更新方法。这种机制使得实体类的使用更加简洁。实体类是代表特定对象类型实例（如用户、博文或职位）的基础类，负责维护与对象相关的业务逻辑（如数据格式化等），且无需关注底层数据库的保存逻辑。最简单的实体类示例如下：

.. literalinclude:: model/020.php

一个与之配合的非常简单的模型如下所示：

.. literalinclude:: model/021.php

此模型处理来自 ``jobs`` 表的数据，并将所有结果作为 ``App\Entities\Job`` 实例返回。需要将该记录持久化到数据库时，需要编写自定义方法，或使用模型的 ``save()`` 方法来检查类，获取所有 public 和 private 属性并保存到数据库：

.. literalinclude:: model/022.php

.. note:: 如果经常使用实体，CodeIgniter 提供了内置的 :doc:`实体类 </models/entities>`，具备多个实用功能，让开发实体更简单。

.. _model-saving-dates:

保存日期
------------

.. versionadded:: 4.5.0

保存数据时，如果传入 :doc:`Time <../libraries/time>` 实例，会转换为字符串，
格式由 :ref:`数据库配置 <database-config-explanation-of-values>` 中的
``dateFormat['datetime']`` 和 ``dateFormat['date']`` 定义。

.. note:: v4.5.0 之前的版本中，日期/时间格式在模型类中硬编码为 ``Y-m-d H:i:s`` 和 ``Y-m-d``。

删除数据
=============

delete()
--------

以主键值作为第一个参数，从模型表中删除匹配的记录：

.. literalinclude:: model/023.php

如果模型的 `$useSoftDeletes`_ 值为 true，此操作会将记录的 ``deleted_at`` 字段更新为当前日期和时间。将第二个参数设为 true 即可强制执行永久删除。

可以传入主键数组作为第一个参数来一次删除多条记录：

.. literalinclude:: model/024.php

不传递参数时，其行为类似于查询构建器的 delete 方法，需要预先调用 where 条件：

.. literalinclude:: model/025.php

purgeDeleted()
--------------

通过永久删除所有 ``deleted_at IS NOT NULL`` 的记录来清理数据库表。

.. literalinclude:: model/026.php

.. _in-model-validation:

模型内验证
===================

.. warning:: 模型内验证在数据存入数据库之前执行。在此之前的数据尚未经过验证。
    在验证之前处理用户输入数据可能会引入漏洞。

验证数据
---------------

模型类支持在调用 ``insert()``、``update()`` 或 ``save()`` 方法保存数据前，自动对所有数据进行验证。

.. important:: 更新数据时，模型类默认仅验证传入字段。旨在避免仅更新部分字段时触发验证错误。

    然而，这也意味着更新期间并非所有预设验证规则都会生效，导致不完整的数据可能通过验证。

    例如，``required*`` 规则或依赖其他字段值的 ``is_unique`` 规则可能无法按预期工作。

    若要避免此类问题，可通过配置更改此行为。详见 :ref:`clean-validation-rules`。

.. _model-setting-validation-rules:

设置验证规则
------------------------

第一步是在 `$validationRules`_ 类属性中填写要应用的字段和规则。

.. note:: 内置验证规则的完整列表请参阅 :ref:`validation-available-rules`。

如果有自定义错误消息，可放入 `$validationMessages`_ 数组：

.. literalinclude:: model/027.php

如果更倾向于在 :ref:`验证配置文件 <saving-validation-rules-to-config-file>` 中组织规则和错误消息，可以这样做，然后只需将 `$validationRules`_ 设为创建的验证规则组名称：

.. literalinclude:: model/034.php

另一种通过函数设置字段验证规则的方式：

.. php:namespace:: CodeIgniter

.. php:class:: Model

.. php:method:: setValidationRule($field, $fieldRules)

    :param  string  $field:
    :param  array   $fieldRules:

    此函数用于设置字段的验证规则。

    使用示例：

    .. literalinclude:: model/028.php

.. php:method:: setValidationRules($validationRules)

    :param  array   $validationRules:

    此函数用于设置验证规则。

    使用示例：

    .. literalinclude:: model/029.php

另一种通过函数设置字段验证消息的方式：

.. php:method:: setValidationMessage($field, $fieldMessages)

    :param  string  $field:
    :param  array   $fieldMessages:

    此函数用于设置字段的错误消息。

    使用示例：

    .. literalinclude:: model/030.php

.. php:method:: setValidationMessages($fieldMessages)

    :param  array   $fieldMessages:

    此函数用于设置字段消息。

    使用示例：

    .. literalinclude:: model/031.php

获取验证结果
-------------------------

现在，每当调用 ``insert()``、``update()`` 或 ``save()`` 方法时，数据都会被验证。如果验证失败，模型将返回布尔值 **false**。

.. _model-getting-validation-errors:

获取验证错误
-------------------------

可使用 ``errors()`` 方法获取验证错误：

.. literalinclude:: model/032.php

返回一个包含字段名和相关错误的数组，可用于在表单顶部显示所有错误，或单独显示：

.. literalinclude:: model/033.php

检索验证规则
---------------------------

可以通过访问模型的 ``validationRules`` 属性来获取验证规则：

.. literalinclude:: model/035.php

也可通过调用访问方法直接检索规则子集（带选项）：

.. literalinclude:: model/036.php

``$options`` 参数是一个关联数组，包含一个元素，键为 ``'except'`` 或 ``'only'``，值为相关字段名数组：

.. literalinclude:: model/037.php

验证占位符
-----------------------

模型提供了一种简单方法，可根据传入数据动态替换部分规则内容。该功能虽然初看有些晦涩，但在处理 ``is_unique`` 验证规则时非常有用。占位符由花括号包裹 ``$data`` 中的字段名（或数组键名）组成，执行时会被对应字段的 **值** 替换。示例如下：

.. literalinclude:: model/038.php

.. note:: v4.3.5 起，必须为占位符字段（``id``）设置验证规则。

在这组规则中，数据库中的 Email 地址必须唯一，但主键 ID 与占位符值匹配的记录除外。假设表单 POST 数据如下：

.. literalinclude:: model/039.php

那么 ``{id}``` 占位符会被替换为数字 **4**，得到以下修订后的规则：

.. literalinclude:: model/040.php

因此，在验证 Email 唯一性时，会忽略 ``id=4`` 的行。

.. note:: v4.3.5 起，如果占位符（``id``）值未通过验证，占位符将不会被替换。

只要确保传入的动态键不与表单数据冲突，即可利用该特性在运行时创建更灵活的动态规则。

保护字段
=================

为防御批量赋值攻击，模型类 **要求** 在 `$allowedFields`_ 属性中列出所有允许在插入和更新时修改的字段名。超出此范围的字段数据将在写入数据库前被自动移除。此举可有效防止时间戳或主键被意外修改。

.. literalinclude:: model/041.php

有时（如执行测试、迁移或数据填充时）可能需要修改这些受保护的字段。此时可手动开启或关闭保护功能：

.. literalinclude:: model/042.php

运行时返回类型变更
===========================

使用 **find*()** 方法时，可指定数据返回的格式作为类属性 `$returnType`_。不过，有时可能需要以不同的格式返回数据。模型提供了方法来实现这一点。

.. note:: 这些方法仅更改下一个 **find*()** 方法调用的返回类型。之后会重置为默认值。

asArray()
---------

将下一个 **find*()** 方法的数据作为关联数组返回：

.. literalinclude:: model/047.php

asObject()
----------

将下一个 **find*()** 方法的数据作为标准对象或自定义类实例返回：

.. literalinclude:: model/048.php

处理大量数据
================================

有时，需要处理大量数据，可能会面临内存不足的风险。为了简化这一过程，可以使用 chunk() 方法获取较小的数据块，然后对其进行处理。第一个参数是单次检索的记录数。第二个参数是每条记录都会调用的闭包函数。

此方法最适合用于定时任务、数据导出或其他大型任务。

.. literalinclude:: model/049.php

.. _model-events-callbacks:

使用查询构建器
**************************

获取模型的查询构建器
===========================================

CodeIgniter 模型有一个针对模型数据库连接的查询构建器实例。可随时访问查询构建器的 **共享** 实例：

.. literalinclude:: model/043.php

此构建器已设置为模型的 `$table`_。

.. note:: 获取查询构建器实例后，可以调用
    :doc:`查询构建器 <../database/query_builder>` 的方法。
    但是，由于查询构建器不是模型，因此不能调用模型的方法。

获取其他表的查询构建器
=======================================

如果需要访问另一个表，可以获取查询构建器的另一个实例。将表名作为参数传入，但请注意，这 **不会** 返回共享实例：

.. literalinclude:: model/044.php

混合使用查询构建器和模型方法
=========================================

可以在同一个链式调用中使用查询构建器方法和模型的 CRUD 方法，实现非常优雅的用法：

.. literalinclude:: model/045.php

在这种情况下，它操作模型持有的查询构建器共享实例。

.. important:: 模型并不提供查询构建器的完美接口。
    模型和查询构建器是具有不同用途的独立类。
    不应期望返回相同的数据。

如果查询构建器返回结果，则按原样返回。
在这种情况下，结果可能与模型方法返回的结果不同，也可能不是预期的结果。不会触发模型事件。

为防止意外行为，不要在方法链的末尾使用返回结果的查询构建器方法并指定模型的方法。

.. note:: 也可以无缝访问模型的数据库连接：

    .. literalinclude:: model/046.php

.. _model-events:

模型事件
************

模型在执行过程中的多个时间点均支持运行自定义回调方法。这些方法可用于数据规范化、密码哈希处理、保存关联实体等多种场景。

以下是模型执行过程中受影响的各个时间点，每个时间点通过一个类属性控制：

- `$beforeInsert`_、`$afterInsert`_
- `$beforeUpdate`_、`$afterUpdate`_
- `$beforeFind`_、`$afterFind`_
- `$beforeDelete`_、`$afterDelete`_
- `$beforeInsertBatch`_、`$afterInsertBatch`_
- `$beforeUpdateBatch`_、`$afterUpdateBatch`_

.. note:: ``$beforeInsertBatch``、``$afterInsertBatch``、``$beforeUpdateBatch`` 和
    ``$afterUpdateBatch`` 自 v4.3.0 起可用。

定义回调
==================

首先在模型中创建新方法作为回调。

此方法始终接收 ``$data`` 数组作为唯一参数。

``$data`` 数组的确切内容因事件而异，但始终包含一个名为 ``data`` 的键，其中包含传递给原始方法的主要数据。在 **insert*()** 或 **update*()** 方法的情况下，这是要插入数据库的键值对。主 ``$data`` 数组还将包含传递给方法的其他值，并在`事件参数`中详细说明。

回调方法必须返回原始的 ``$data`` 数组，以便其他回调拥有完整信息。

.. literalinclude:: model/050.php

指定运行的回调
===========================

通过将方法名添加到适当的类属性（`$beforeInsert`_、`$afterUpdate`_ 等）来指定回调的运行时机。可以向单个事件添加多个回调，按顺序逐一处理。可以在多个事件中使用相同的回调：

.. literalinclude:: model/051.php

此外，每个模型可通过设置 `$allowCallbacks`_ 属性来全局允许（默认）或拒绝回调：

.. literalinclude:: model/052.php

也可使用 ``allowCallbacks()`` 方法临时更改单个模型调用的设置：

.. literalinclude:: model/053.php

事件参数
================

由于传递给每个回调的数据略有不同，以下是传递给每个事件的 ``$data`` 参数中的详细内容：

================= =========================================================================================================
事件              $data 内容
================= =========================================================================================================
beforeInsert      **data** = 要插入的键值对。如果将对象或实体类传递给 ``insert()`` 方法，会先转换为数组。
afterInsert       **id** = 新行的主键，失败时为 0。
                  **data** = 要插入的键值对。
                  **result** = 通过查询构建器使用的 ``insert()`` 方法的结果。
beforeUpdate      **id** = 传递给 ``update()`` 方法的主键数组。
                  **data** = 要更新的键值对。如果将对象或实体类传递给 ``update()`` 方法，会先转换为数组。
afterUpdate       **id** = 传递给 ``update()`` 方法的主键数组。
                  **data** = 要更新的键值对。
                  **result** = 通过查询构建器使用的 ``update()`` 方法的结果。
beforeFind        调用的 **方法** 名称，是否请求 **单例**，以及以下附加字段：
- ``first()``     无附加字段
- ``find()``      **id** = 要搜索行的主键。
- ``findAll()``   **limit** = 要查找的行数。
                  **offset** = 搜索期间跳过的行数。
afterFind         与 **beforeFind** 相同，但包含结果数据，如果未找到结果则为 null。
beforeDelete      **id** = 传递给 ``delete()`` 方法的主键数组。
                  **purge** = 布尔值，软删除的记录是否应硬删除。
afterDelete       **id** = 传递给 ``delete()`` 方法的主键数组。
                  **purge** = 布尔值，软删除的记录是否应硬删除。
                  **result** = 查询构建器上 ``delete()`` 调用的结果。
                  **data** = 未使用。
beforeInsertBatch **data** = 要插入的值的关联数组。如果将对象或实体类传递给 ``insertBatch()`` 方法，会先转换为数组。
afterInsertBatch  **data** = 要插入的值的关联数组。
                  **result** = 通过查询构建器使用的 ``insertbatch()`` 方法的结果。
beforeUpdateBatch **data** = 要更新的值的关联数组。如果将对象或实体类传递给 ``updateBatch()`` 方法，会先转换为数组。
afterUpdateBatch  **data** = 要更新的键值对。
                  **result** = 通过查询构建器使用的 ``updateBatch()`` 方法的结果。
================= =========================================================================================================

.. note:: 将 ``paginate()`` 方法与 ``beforeFind`` 事件配合使用来修改查询时，结果可能不会按预期工作。

    这是因为 ``beforeFind`` 事件仅影响结果的实际检索（``findAll()``），
    但 **不会** 影响用于计算分页总行数的查询。

    因此，用于生成分页链接的总行数可能无法反映修改后的查询条件，
    导致分页不一致。

修改 Find* 数据
====================

``beforeFind`` 与 ``afterFind`` 方法均可返回修改后的数据集，用于覆盖模型的默认响应。对于 ``afterFind``，返回数组中对 ``data`` 的任何修改都会自动传递回调用处。若要利用 ``beforeFind`` 拦截查询流程，还必须额外返回一个布尔值 ``returnData``：

.. literalinclude:: model/054.php

手动创建模型
*********************

创建应用模型时无需继承任何特定类。只需获取数据库连接实例即可开始。由此可绕过 CodeIgniter 模型内置的功能，实现完全自定义的开发。

.. literalinclude:: model/055.php
