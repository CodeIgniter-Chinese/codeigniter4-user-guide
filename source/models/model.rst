#########################
使用 CodeIgniter 的模型
#########################

.. contents::
    :local:
    :depth: 3

模型
******

CodeIgniter 的模型提供了便捷功能和额外特性，使得在数据库中操作 **单张表** 更加方便。

它内置了常用数据库表交互的辅助函数，包括查找记录、更新记录、删除记录等标准操作。

.. _accessing-models:

访问模型
****************

模型通常存储在 **app/Models** 目录中，其命名空间应与目录位置匹配，例如 ``namespace App\Models``。

可以通过创建新实例或使用 :php:func:`model()` 辅助函数在类中访问模型：

.. literalinclude:: model/001.php

``model()`` 内部使用 ``Factories::models()``。有关第一个参数的详细信息，请参阅 :ref:`factories-loading-class`。

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

当类首次实例化时，如果没有数据库连接实例传递给构造函数，且未在模型类中设置 ``$DBGroup`` 属性，模型会自动连接到数据库配置中设置的默认组。

通过添加 ``$DBGroup`` 属性可修改每个模型使用的数据库组，确保模型中所有 ``$this->db`` 引用都通过正确的连接进行：

.. literalinclude:: model/004.php

将 "group_name" 替换为数据库配置文件中定义的数据库组名称。

配置模型
======================

模型类提供以下配置选项，使类方法能无缝工作：

.. literalinclude:: model/005.php

$table
------

指定模型主要操作的数据表。仅适用于内置 CRUD 方法，自定义查询不受限制。

$primaryKey
-----------

指定表中唯一标识记录的列名。不必与数据库主键完全匹配，但需与 ``find()`` 等方法使用的匹配列一致。

.. note:: 所有模型必须指定 primaryKey 以确保功能正常。

$useAutoIncrement
-----------------

指定表是否对 `$primaryKey`_ 使用自增特性。设为 ``false`` 时需手动提供主键值，适用于 1:1 关系或 UUID 场景。默认值为 ``true``。

.. note:: 当 `$useAutoIncrement`_ 设为 ``false`` 时，请确保数据库主键设为 ``unique``，以保证模型功能正常。

$returnType
-----------

模型的 **find*()** 方法将自动返回结果数据，而非 Result 对象。

此设置允许你定义返回的数据类型，有效值为 '**array**'（默认）、'**object**' 或可与 Result 对象的 ``getCustomResultObject()`` 方法配合使用的 **类的完全限定名称**。

使用类的特殊 ``::class`` 常量，可使大多数 IDE 实现自动补全，并支持重构等功能以更好地理解你的代码。

.. _model-use-soft-deletes:

$useSoftDeletes
---------------

若设为 ``true``，任何 ``delete()`` 方法调用都会在数据库中设置 ``deleted_at`` 字段值，而非实际删除行。这可以保留可能被其他位置引用的数据，维护可恢复对象的「回收站」，或简单地将其作为安全审计轨迹的一部分。当启用时，**find*()** 方法默认仅返回未删除行，除非在调用 **find*()** 方法前先调用 ``withDeleted()`` 方法。

根据模型的 `$dateFormat`_ 设置，数据库需要包含 DATETIME 或 INTEGER 类型的字段。默认字段名为 ``deleted_at``，但可通过 `$deletedField`_ 属性配置为任意名称。

.. important:: 数据库中的 ``deleted_at`` 字段必须可为空。

.. _model-allowed-fields:

$allowedFields
--------------

定义可通过 ``save()``、``insert()`` 或 ``update()`` 方法设置的字段名列表，防止大规模赋值漏洞。

.. note:: `$primaryKey`_ 字段不应包含在允许字段中。

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

该功能允许你将从数据库检索的数据转换为适当的 PHP 类型。此选项应为数组格式，其中键名对应字段名称，键值对应数据类型。详细信息请参阅 :ref:`model-field-casting`。

日期配置
--------

$useTimestamps
^^^^^^^^^^^^^^

这个布尔值决定了是否自动将当前日期添加到所有插入和更新操作中。如果为 ``true``，将按照 `$dateFormat`_ 指定的格式设置当前时间。这要求表中存在适当数据类型的 **created_at**、**updated_at** 和 **deleted_at** 列。另请参阅 `$createdField`_、`$updatedField`_ 和 `$deletedField`_。

$dateFormat
^^^^^^^^^^^

该值配合 `$useTimestamps`_ 和 `$useSoftDeletes`_ 使用，确保正确类型的日期值被插入数据库。默认情况下会生成 DATETIME 值，但有效选项包括：``'datetime'``、``'date'`` 或 ``'int'`` （UNIX 时间戳）。如果与无效或缺失的 `$dateFormat`_ 一起使用 `$useSoftDeletes`_ 或 `$useTimestamps`_ 将会引发异常。

$createdField
^^^^^^^^^^^^^

指定用于记录数据创建时间戳的数据库字段。设置为空字符串 (``''``) 可避免更新该字段（即使启用了 `$useTimestamps`_）。

$updatedField
^^^^^^^^^^^^^

指定用于记录数据更新时间戳的数据库字段。设置为空字符串 (``''``) 可避免更新该字段（即使启用了 `$useTimestamps`_）。

$deletedField
^^^^^^^^^^^^^

指定用于软删除操作的数据库字段。详见 :ref:`model-use-soft-deletes`。

验证
----------

$validationRules
^^^^^^^^^^^^^^^^

包含一个验证规则数组（如 :ref:`validation-array` 所述）或一个验证组名称的字符串（如相同章节所述）。另请参阅 :ref:`model-setting-validation-rules`。

$validationMessages
^^^^^^^^^^^^^^^^^^^

包含一个自定义错误消息数组，用于验证过程中（如 :ref:`validation-custom-errors` 所述）。另请参阅 :ref:`model-setting-validation-rules`。

$skipValidation
^^^^^^^^^^^^^^^

是否在所有 **插入** 和 **更新** 操作中跳过验证。默认值为 ``false``，表示始终尝试验证数据。这主要由 ``skipValidation()`` 方法使用，但可更改为 ``true`` 以使模型永不验证。

.. _clean-validation-rules:

$cleanValidationRules
^^^^^^^^^^^^^^^^^^^^^

是否移除传入数据中不存在的验证规则。这用于 **更新** 操作。默认值为 ``true``，表示在验证前会（临时）移除传入数据中不存在字段的验证规则，以避免在仅更新部分字段时出现验证错误。

也可以通过 ``cleanRules()`` 方法更改此值。

.. note:: 在 v4.2.7 之前，由于存在 bug，``$cleanValidationRules`` 无法正常工作。

回调
----------

$allowCallbacks
^^^^^^^^^^^^^^^

是否使用下面定义的回调。详见 :ref:`model-events`。

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

这些数组允许你指定在属性名指定时间点运行的回调方法。详见 :ref:`model-events`。

.. _model-field-casting:

模型字段类型转换
*******************

.. versionadded:: 4.5.0

从数据库检索数据时，整数类型的数据可能在 PHP 中被转换为字符串类型。你可能希望将日期/时间数据转换为 PHP 的 Time 对象。

模型字段类型转换允许你将从数据库检索的数据转换为适当的 PHP 类型。

.. important::
    如果将此功能与 :doc:`实体 <./entities>` 一起使用，请勿同时使用 :ref:`实体属性类型转换 <entities-property-casting>`。同时使用两种类型转换将无法正常工作。

    实体属性类型转换作用于 (1)(4)，而此类型转换作用于 (2)(3)::

        [应用代码] --- (1) --> [实体] --- (2) --> [数据库]
        [应用代码] <-- (4) --- [实体] <-- (3) --- [数据库]

    使用此类型转换时，实体将在属性中持有正确类型的 PHP 值。此行为与之前的行为完全不同。不要期望属性持有数据库的原始数据。

定义数据类型
===================

``$casts`` 属性设置其定义。此选项应为数组，其中键是字段名称，值是数据类型：

.. literalinclude:: model/057.php

数据类型
==========

默认提供以下类型。在类型前添加问号可将字段标记为可空，例如 ``?int``、``?datetime``。

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

使用 ``csv`` 类型转换时，使用 PHP 内置的 ``implode()`` 和 ``explode()`` 函数，并假定所有值都是字符串安全且不含逗号。对于更复杂的数据转换，请尝试 ``array`` 或 ``json``。

datetime
--------

你可以传递类似 ``datetime[ms]`` 的参数表示带毫秒的日期/时间，或 ``datetime[us]`` 表示带微秒的日期/时间。

日期时间格式在 :ref:`数据库配置 <database-config-explanation-of-values>` 的 ``dateFormat`` 数组中设置，位于 **app/Config/Database.php** 文件。

.. note::
    当使用 ``ms`` 或 ``us`` 作为参数时，**模型** 会处理 Time 的秒的小数部分。但 **查询构建器** 不会。因此在将 Time 传递给查询构建器的方法（如 ``where()``）时，仍需使用 ``format()`` 方法：

    .. literalinclude:: model/063.php
        :lines: 2-

.. note:: 在 v4.6.0 之前，由于存在 bug，无法使用 ``ms`` 或 ``us`` 作为参数，因为 Time 的秒的小数部分会丢失。

timestamp
---------

创建的 ``Time`` 实例的时区将是默认时区（应用的时区），而非 UTC。

自定义类型转换
==============

你可以定义自己的转换类型。

创建自定义处理器
------------------------

首先需要为你的类型创建一个处理器类。假设类位于 **app/Models/Cast** 目录：

.. literalinclude:: model/058.php

如果不需要在获取或设置值时更改值，只需不实现相应方法：

.. literalinclude:: model/060.php

注册自定义处理器
---------------------------

现在需要注册它：

.. literalinclude:: model/059.php

参数
----------

在某些情况下，单一类型可能不够。此时可以使用附加参数。附加参数用方括号表示，并用逗号分隔，例如 ``type[param1, param2]``。

.. literalinclude:: model/061.php

.. literalinclude:: model/062.php

.. note:: 如果类型标记为可空（如 ``?bool``）且传递的值不为 null，则会将带有 ``nullable`` 值的参数传递给类型转换处理器。如果类型转换已有预定义参数，则 ``nullable`` 将添加到列表末尾。

处理数据
*****************

查找数据
============

提供了多个函数用于对表执行基本的 CRUD 操作，包括 ``find()``、``insert()``、``update()``、``delete()`` 等。

find()
------

返回主键与第一个参数匹配的单行数据：

.. literalinclude:: model/006.php

返回值格式由 `$returnType`_ 指定。

通过传递主键值数组（而非单个值）可返回多行数据：

.. literalinclude:: model/007.php

.. note:: 如果不传递参数，``find()`` 将返回模型表中的所有行，实际上等同于 ``findAll()``，但不够明确。

findColumn()
------------

返回 null 或列值的索引数组：

.. literalinclude:: model/008.php

``$columnName`` 应为单个字段名，否则将抛出 ``DataException``。

findAll()
---------

返回所有结果：

.. literalinclude:: model/009.php

可在调用此方法前插入查询构建器命令来修改查询：

.. literalinclude:: model/010.php

可分别传递限制和偏移值作为第一和第二个参数：

.. literalinclude:: model/011.php

first()
-------

返回结果集中的第一行。最好与查询构建器结合使用。

.. literalinclude:: model/012.php

withDeleted()
-------------

如果 `$useSoftDeletes`_ 为 true，则 **find*()** 方法不会返回 ``deleted_at IS NOT NULL`` 的行。要临时覆盖此行为，可在调用 **find*()** 方法前使用 ``withDeleted()`` 方法。

.. literalinclude:: model/013.php

onlyDeleted()
-------------

``withDeleted()`` 会返回已删除和未删除的行，而此方法会修改后续的 **find*()** 方法仅返回软删除的行：

.. literalinclude:: model/014.php

保存数据
===========

insert()
--------

第一个参数是关联数组，用于在数据库中创建新行数据。如果传递对象而非数组，将尝试将其转换为数组。

数组的键必须与 `$table`_ 中的列名匹配，数组的值是要保存的值。

可选的第二个参数为布尔类型，若设为 false，方法将返回布尔值表示查询成功与否。

可使用 ``getInsertID()`` 方法获取最后插入行的主键。

.. literalinclude:: model/015.php

.. _model-allow-empty-inserts:

allowEmptyInserts()
-------------------

.. versionadded:: 4.3.0

可使用 ``allowEmptyInserts()`` 方法插入空数据。默认情况下，模型在尝试插入空数据时会抛出异常。但调用此方法后，将不再执行检查。

.. literalinclude:: model/056.php

也可通过 `$allowEmptyInserts`_ 属性更改此设置。

通过调用 ``allowEmptyInserts(false)`` 可重新启用检查。

update()
--------

更新数据库中的现有记录。第一个参数是要更新记录的 `$primaryKey`_。第二个参数是包含数据的关联数组。数组的键必须与 `$table`_ 中的列名匹配，数组的值则是要保存的对应值：

.. literalinclude:: model/016.php

.. important:: 自 v4.3.0 起，如果生成的 SQL 语句没有 WHERE 子句，此方法会抛出 ``DatabaseException``。在早期版本中，如果调用时未指定 `$primaryKey`_ 且生成的 SQL 语句没有 WHERE 子句，查询仍会执行并更新表中的所有记录。

通过将主键数组作为第一个参数传递，可以在一次调用中更新多条记录：

.. literalinclude:: model/017.php

当需要更灵活的解决方案时，可以留空参数，此时其功能类似于查询构建器的 update 命令，并额外具备验证、事件等优势：

.. literalinclude:: model/018.php

.. _model-save:

save()
------

这是对 ``insert()`` 和 ``update()`` 方法的封装，根据是否找到匹配 **主键** 值的数组键来自动处理记录的插入或更新：

.. literalinclude:: model/019.php

save 方法还能通过识别非简单对象并将其公共和受保护值提取到数组，简化与自定义类结果对象的交互。这使得你可以非常简洁地使用实体类。实体类是表示单个对象类型实例的简单类（如用户、博客文章、任务等），负责维护围绕对象本身的业务逻辑（如特定格式的元素处理等），不应了解如何保存到数据库。最简单的实体类可能如下所示：

.. literalinclude:: model/020.php

与之配合的简单模型可能如下：

.. literalinclude:: model/021.php

此模型处理来自 ``jobs`` 表的数据，并将所有结果作为 ``App\Entities\Job`` 实例返回。当需要将记录持久化到数据库时，你可以编写自定义方法，或使用模型的 ``save()`` 方法来检查类、提取公共和私有属性并保存到数据库：

.. literalinclude:: model/022.php

.. note:: 如果你需要频繁使用实体类，CodeIgniter 提供了内置的 :doc:`实体类 </models/entities>`，其中包含多个便捷功能可简化实体开发。

.. _model-saving-dates:

保存日期
------------

.. versionadded:: 4.5.0

保存数据时，如果传递 :doc:`Time <../libraries/time>` 实例，它们会被转换为字符串格式。转换使用的格式定义在 :ref:`数据库配置 <database-config-explanation-of-values>` 的 ``dateFormat['datetime']`` 和 ``dateFormat['date']`` 中。

.. note:: 在 v4.5.0 之前，Model 类中日期/时间格式硬编码为 ``Y-m-d H:i:s`` 和 ``Y-m-d``。

删除数据
=============

delete()
--------

以主键值作为第一个参数，从模型表中删除匹配记录：

.. literalinclude:: model/023.php

如果模型的 `$useSoftDeletes`_ 值为 true，此操作会将行的 ``deleted_at`` 设为当前日期时间。通过将第二个参数设为 true 可强制永久删除。

传递主键数组作为第一个参数可批量删除多条记录：

.. literalinclude:: model/024.php

不传递参数时，其行为类似于 查询构建器 的 delete 方法，需要预先调用 where 条件：

.. literalinclude:: model/025.php

purgeDeleted()
--------------

通过永久删除所有 'deleted_at IS NOT NULL' 的行来清理数据库表：

.. literalinclude:: model/026.php

.. _in-model-validation:

模型内验证
===================

.. warning:: 模型内验证在数据存储到数据库之前执行。在此之前数据尚未验证。在验证前处理用户输入数据可能引入安全漏洞。

验证数据
---------------

Model 类提供在通过 ``insert()``、``update()`` 或 ``save()`` 方法保存到数据库前自动验证数据的功能。

.. important:: 更新数据时，默认情况下模型类中的验证仅验证提供的字段，以避免在更新部分字段时出现验证错误。

    这意味着并非所有设置的验证规则都会在更新时检查。因此不完整数据可能通过验证。

    例如，需要其他字段值的 ``required*`` 规则或 ``is_unique`` 规则可能无法按预期工作。

    为避免此类问题，可通过配置更改此行为。详见 :ref:`clean-validation-rules`。

.. _model-setting-validation-rules:

设置验证规则
------------------------

第一步是在 `$validationRules`_ 类属性中填写要应用的字段和规则。

.. note:: 内置验证规则列表参见 :ref:`validation-available-rules`。

如果有自定义错误信息，可将其放入 `$validationMessages`_ 数组：

.. literalinclude:: model/027.php

如果更愿意在 :ref:`验证配置文件 <saving-validation-rules-to-config-file>` 中组织规则和错误信息，可创建验证规则组并将 `$validationRules`_ 设为组名：

.. literalinclude:: model/034.php

也可以通过函数设置字段验证规则：

.. php:namespace:: CodeIgniter

.. php:class:: Model

.. php:method:: setValidationRule($field, $fieldRules)

    :param  string  $field:
    :param  array   $fieldRules:

    此函数设置字段验证规则。

    使用示例：

    .. literalinclude:: model/028.php

.. php:method:: setValidationRules($validationRules)

    :param  array   $validationRules:

    此函数设置验证规则。

    使用示例：

    .. literalinclude:: model/029.php

通过函数设置字段验证信息：

.. php:method:: setValidationMessage($field, $fieldMessages)

    :param  string  $field:
    :param  array   $fieldMessages:

    此函数设置字段错误信息。

    使用示例：

    .. literalinclude:: model/030.php

.. php:method:: setValidationMessages($fieldMessages)

    :param  array   $fieldMessages:

    此函数设置字段信息。

    使用示例：

    .. literalinclude:: model/031.php

获取验证结果
-------------------------

当调用 ``insert()``、``update()`` 或 ``save()`` 方法时，数据会被验证。如果验证失败，模型返回布尔值 **false**。

.. _model-getting-validation-errors:

获取验证错误
-------------------------

使用 ``errors()`` 方法获取验证错误：

.. literalinclude:: model/032.php

返回包含字段名及其关联错误的数组，可用于在表单顶部显示所有错误或单独显示：

.. literalinclude:: model/033.php

检索验证规则
---------------------------

可通过访问 ``validationRules`` 属性检索模型的验证规则：

.. literalinclude:: model/035.php

也可通过调用访问方法直接检索规则子集（带选项）：

.. literalinclude:: model/036.php

``$options`` 参数是包含一个元素的关联数组，其键为 ``'except'`` 或 ``'only'``，值为相关字段名数组：

.. literalinclude:: model/037.php

验证占位符
-----------------------

模型提供简单方法来替换规则中基于传入数据的部分。这在 ``is_unique`` 验证规则中特别有用。占位符是由花括号包围的字段名（或数组键），会被匹配传入字段的 **值** 替换。示例：

.. literalinclude:: model/038.php

.. note:: 自 v4.3.5 起，必须为占位符字段（``id``）设置验证规则。

在此规则集中，声明电子邮件地址在数据库中应唯一，除了 id 匹配占位符值的行。假设表单 POST 数据如下：

.. literalinclude:: model/039.php

则 ``{id}`` 占位符会被替换为数字 **4**，生成修订后的规则：

.. literalinclude:: model/040.php

因此在校验电子邮件唯一性时，会忽略数据库中 ``id=4`` 的行。

.. note:: 自 v4.3.5 起，如果占位符（``id``）值未通过验证，占位符不会被替换。

只要注意动态键不与表单数据冲突，这也可用于在运行时创建更动态的规则。

保护字段
=================

为防止大规模赋值攻击，Model 类 **要求** 在 `$allowedFields`_ 类属性中列出所有可在插入和更新时修改的字段名。超出这些字段的数据会在触及数据库前被移除。这能有效防止时间戳或主键被修改。

.. literalinclude:: model/041.php

有时需要在测试、迁移或种子数据时修改这些元素。此时可开关保护：

.. literalinclude:: model/042.php

运行时返回类型变更
===========================

可通过类属性 `$returnType`_ 指定使用 **find*()** 方法时数据的返回格式。有时可能需要不同格式的数据。模型提供方法实现这一点。

.. note:: 这些方法仅改变下一次 **find*()** 方法调用的返回类型，之后会重置为默认值。

asArray()
---------

将下一次 **find*()** 方法的数据作为关联数组返回：

.. literalinclude:: model/047.php

asObject()
----------

将下一次 **find*()** 方法的数据作为标准对象或自定义类实例返回：

.. literalinclude:: model/048.php

处理大量数据
================================

处理大量数据时可能存在内存不足风险。可使用 chunk() 方法获取小块数据进行处理。第一个参数是单块检索的行数，第二个参数是处理每行数据的闭包。

此方法适用于定时任务、数据导出等大型任务。

.. literalinclude:: model/049.php

.. _model-events-callbacks:

使用查询构建器
**************************

获取模型的查询构建器
===========================================

CodeIgniter 模型有一个针对模型数据库连接的查询构建器实例。可随时访问此 **共享** 实例：

.. literalinclude:: model/043.php

此构建器已配置模型的 `$table`_。

.. note:: 获取查询构建器实例后，可调用 :doc:`查询构建器 <../database/query_builder>` 的方法。但由于查询构建器不是模型，不能调用模型的方法。

获取其他表的查询构建器
=======================================

如需访问其他表，可获取另一个查询构建器实例。传递表名作为参数，但注意这会返回 **非共享** 实例：

.. literalinclude:: model/044.php

混合使用查询构建器和模型方法
==========================================

可在同一链式调用中混合使用查询构建器方法和模型的 CRUD 方法，实现优雅操作：

.. literalinclude:: model/045.php

此例中，操作的是模型持有的查询构建器共享实例。

.. important:: 模型并非查询构建器的完美接口。模型和查询构建器是不同目的的独立类，不应期望返回相同数据。

如果查询构建器返回结果，则原样返回。此时结果可能与模型方法返回的不同，且可能不符合预期。不会触发模型事件。

为避免意外行为，请勿在方法链末尾使用返回结果的查询构建器方法并指定模型方法。

.. note:: 也可无缝访问模型的数据库连接：

    .. literalinclude:: model/046.php

.. _model-events:

模型事件
************

在模型执行的多个节点可指定多个回调方法。这些方法可用于规范化数据、哈希密码、保存关联实体等。

以下执行节点可通过类属性设置回调：

- `$beforeInsert`_, `$afterInsert`_
- `$beforeUpdate`_, `$afterUpdate`_
- `$beforeFind`_, `$afterFind`_
- `$beforeDelete`_, `$afterDelete`_
- `$beforeInsertBatch`_, `$afterInsertBatch`_
- `$beforeUpdateBatch`_, `$afterUpdateBatch`_

.. note:: ``$beforeInsertBatch``、``$afterInsertBatch``、``$beforeUpdateBatch`` 和 ``$afterUpdateBatch`` 自 v4.3.0 起可用。

定义回调
==================

首先在模型中创建新类方法作为回调。

此方法始终接收 ``$data`` 数组作为唯一参数。

``$data`` 数组的具体内容因事件而异，但始终包含键名为 ``data`` 的主要数据。对于 **insert*()** 或 **update*()** 方法，这是要插入/更新到数据库的键值对。主 ``$data`` 数组还包含传递给方法的其他值，详见 `事件参数`_。

回调方法必须返回原始 ``$data`` 数组以便其他回调使用完整信息。

.. literalinclude:: model/050.php

指定运行的回调
===========================

通过将方法名添加到相应的类属性（`$beforeInsert`_、`$afterUpdate`_ 等）来指定回调运行时机。单个事件可添加多个回调并按序处理。同一回调可用于多个事件：

.. literalinclude:: model/051.php

此外，每个模型可通过设置 `$allowCallbacks`_ 属性全局允许（默认）或禁止回调：

.. literalinclude:: model/052.php

也可使用 ``allowCallbacks()`` 方法临时更改单个模型调用的设置：

.. literalinclude:: model/053.php

事件参数
================

各事件传递给回调的 ``$data`` 参数内容如下：

================= =========================================================================================================
事件              $data 内容
================= =========================================================================================================
beforeInsert      **data** = 要插入的键值对。如果向 ``insert()`` 传递对象或 Entity 类，会先转换为数组。
afterInsert       **id** = 新行的主键，失败时为 0。
                  **data** = 要插入的键值对。
                  **result** = 通过查询构建器使用的 ``insert()`` 方法结果。
beforeUpdate      **id** = 传递给 ``update()`` 方法的主键数组。
                  **data** = 要更新的键值对。如果向 ``update()`` 传递对象或 Entity 类，会先转换为数组。
afterUpdate       **id** = 传递给 ``update()`` 方法的主键数组。
                  **data** = 要更新的键值对。
                  **result** = 通过查询构建器使用的 ``update()`` 方法结果。
beforeFind        调用 **方法** 的名称，是否请求 **单例**，以及以下附加字段：
- ``first()``     无附加字段
- ``find()``      **id** = 要搜索行的主键。
- ``findAll()``   **limit** = 要查找的行数。
                  **offset** = 搜索期间跳过的行数。
afterFind         同 **beforeFind**，但包含结果数据行（无结果时为 null）。
beforeDelete      **id** = 传递给 ``delete()`` 方法的主键数组。
                  **purge** = 是否硬删除软删除行的布尔值。
afterDelete       **id** = 传递给 ``delete()`` 方法的主键数组。
                  **purge** = 是否硬删除软删除行的布尔值。
                  **result** = 查询构建器上 ``delete()`` 调用的结果。
                  **data** = 未使用。
beforeInsertBatch **data** = 要插入的值的关联数组。如果向 ``insertBatch()`` 传递对象或 Entity 类，会先转换为数组。
afterInsertBatch  **data** = 要插入的值的关联数组。
                  **result** = 通过查询构建器使用的 ``insertbatch()`` 方法结果。
beforeUpdateBatch **data** = 要更新的值的关联数组。如果向 ``updateBatch()`` 传递对象或 Entity 类，会先转换为数组。
afterUpdateBatch  **data** = 要更新的键值对。
                  **result** = 通过查询构建器使用的 ``updateBatch()`` 方法结果。
================= =========================================================================================================

.. note:: 当结合使用 ``paginate()`` 方法和 ``beforeFind`` 事件来修改查询时，
   结果可能不会按预期的方式运行。

   这是因为 ``beforeFind`` 事件只影响结果的实际检索（``findAll()``），
   但 **不会** 影响用于统计分页总行数的查询。

   因此，用于生成分页链接的总行数可能不会反映修改后的查询条件，
   从而导致分页中的不一致性。

修改 Find* 数据
====================

``beforeFind`` 和 ``afterFind`` 方法都可以返回修改后的数据集来覆盖模型的正常响应。对于 ``afterFind``，返回数组中 ``data`` 的任何修改都会自动传递回调用上下文。为了让 ``beforeFind`` 拦截查找工作流，它还必须返回一个额外的布尔值 ``returnData``：

.. literalinclude:: model/054.php

手动创建模型
*********************

你不需要继承任何特殊类来为应用程序创建模型。你只需要获取数据库连接的实例即可开始使用。这允许你绕过 CodeIgniter 模型开箱即用的功能，创建完全自定义的体验。

.. literalinclude:: model/055.php
