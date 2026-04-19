.. _api_transformers:

#############
API 资源
#############

构建 API 时，通常需要在将数据模型发送给客户端前，将其转换为统一格式。通过 Transformer 实现的 API 资源提供了一种将实体、数组或对象转换为结构化 API 响应的简洁方式。这有助于将内部数据结构与 API 暴露的内容分离，使 API 的维护和演进更加容易。

.. contents::
    :local:
    :depth: 2

*****************
快速示例
*****************

以下示例展示了应用中 Transformer 的常见使用模式。

.. literalinclude:: api_transformers/001.php

在此示例中，``UserTransformer`` 定义了 API 响应中应包含的 User 实体字段。``transform()`` 方法转换单个资源，而 ``transformMany()`` 则处理资源集合。

**********************
创建 Transformer
**********************

若要创建 Transformer，请继承 ``BaseTransformer`` 类并实现 ``toArray()`` 方法来定义 API 资源结构。``toArray()`` 方法接收被转换的资源作为参数，以便访问并转换其数据。

基础 Transformer
=================

.. literalinclude:: api_transformers/002.php

``toArray()`` 方法接收资源（实体、数组或对象）作为参数，并定义 API 响应的结构。可以根据需要包含资源中的任何字段，也可以重命名或转换其值。

生成 Transformer 文件
=============================

CodeIgniter 提供了一个 CLI 命令，可快速生成 Transformer 骨架文件：

.. code-block:: console

    php spark make:transformer User

这将在 **app/Transformers/User.php** 创建一个新的 Transformer 文件，并已生成基础结构。

命令选项
---------------

``make:transformer`` 命令支持以下选项：

**--suffix**
    在类名后添加 “Transformer”：

    .. code-block:: console

        php spark make:transformer User --suffix

    将创建 **app/Transformers/UserTransformer.php**

**--namespace**
    指定自定义根命名空间：

    .. code-block:: console

        php spark make:transformer User --namespace="MyCompany\\API"

**--force**
    强制覆盖现有文件：

    .. code-block:: console

        php spark make:transformer User --force

子目录
--------------

通过在名称中包含路径，可以将 Transformer 组织到子目录中：

.. code-block:: console

    php spark make:transformer api/v1/User

这将创建 **app/Transformers/Api/V1/User.php**，并带有相应的命名空间 ``App\Transformers\Api\V1``。

在控制器中使用 Transformer
==================================

创建 Transformer 后，即可在控制器中转换数据，然后将其返回给客户端。

.. literalinclude:: api_transformers/003.php

***********************
字段筛选
***********************

Transformer 通过当前 URL 的 ``fields`` 查询参数自动支持字段筛选。这允许 API 客户端仅请求所需的特定字段，从而节省带宽并提高性能。

.. literalinclude:: api_transformers/007.php

若请求 ``/users/1?fields=id,name``，将仅返回：

.. code-block:: json

    {
        "id": 1,
        "name": "John Doe"
    }

限制可用字段
=============================

默认情况下，客户端可以请求 ``toArray()`` 方法中定义的任何字段。可通过重写 ``getAllowedFields()`` 方法来限制允许的字段：

.. literalinclude:: api_transformers/008.php

此时，即使客户端请求 ``/users/1?fields=email``，也会抛出 ``ApiException``，因为 ``email`` 不在允许的字段列表中。

***************************
包含关联资源
***************************

Transformer 支持通过 ``include`` 查询参数加载关联资源。这遵循了常见的 API 模式，即客户端可以指定需要包含哪些关联关系。虽然关联关系是最常见的用例，但也可以通过定义自定义 include 方法来包含任何额外数据。

定义 include 方法
=========================

若要支持包含关联资源，请创建以 ``include`` 为前缀、后跟资源名称的方法。在这些方法中，可以通过 ``$this->resource`` 访问当前正在转换的资源：

.. literalinclude:: api_transformers/009.php

请注意 include 方法如何使用 ``$this->resource['id']`` 访问被转换用户的 ID。调用 ``transform()`` 时，Transformer 会自动设置 ``$this->resource`` 属性。

客户端现在可以请求：``/users/1?include=posts,comments``

响应将包含：

.. code-block:: json

    {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "posts": [
            {
                "id": 1,
                "title": "First Post"
            }
        ],
        "comments": [
            {
                "id": 1,
                "content": "Great article!"
            }
        ]
    }

限制可用 include
===============================

与字段筛选类似，可以通过重写 ``getAllowedIncludes()`` 方法来限制可包含的关联关系：

.. literalinclude:: api_transformers/010.php

如果想禁用所有 include，请返回一个空数组：

.. literalinclude:: api_transformers/011.php

include 验证
==================

Transformer 会自动验证所有请求的 include 是否在 Transformer 类中定义了对应的 ``include*()`` 方法。如果客户端请求了不存在的 include，将抛出 ``ApiException``。

例如，如果客户端请求：

.. code-block:: none

    GET /api/users?include=invalid

而 Transformer 中没有 ``includeInvalid()`` 方法，则会抛出异常，提示：“Missing include method for: invalid”。

这有助于捕获拼写错误并防止非预期行为。

************************
转换集合
************************

使用 ``transformMany()`` 方法可轻松转换资源数组：

.. literalinclude:: api_transformers/012.php

``transformMany()`` 方法会对集合中的每一项应用相同的转换逻辑，包括请求中指定的任何字段筛选或 include。

*********************************
处理不同的数据类型
*********************************

Transformer 不仅能处理实体，还能处理各种数据类型。

转换实体
=====================

将 ``Entity`` 实例传递给 ``transform()`` 时，它会自动调用实体的 ``toArray()`` 方法获取数据：

.. literalinclude:: api_transformers/013.php

转换数组
===================

也可以转换普通数组：

.. literalinclude:: api_transformers/014.php

转换对象
====================

任何对象都可以转换为数组并进行转换：

.. literalinclude:: api_transformers/015.php

仅使用 toArray()
====================

如果未向 ``transform()`` 传递资源，它将使用来自 ``toArray()`` 方法的数据：

.. literalinclude:: api_transformers/016.php

***************
类参考
***************

.. php:namespace:: CodeIgniter\API

.. php:class:: BaseTransformer

    .. php:method:: __construct(?IncomingRequest $request = null)

        :param IncomingRequest|null $request: 可选的请求实例。若未提供，将使用全局请求。

        初始化 Transformer，并从请求中提取 ``fields`` 和 ``include`` 查询参数。

    .. php:method:: toArray(mixed $resource)

        :param mixed $resource: 正在转换的资源（实体、数组、对象或 null）
        :returns: 资源的数组表示
        :rtype: array

        此抽象方法必须由子类实现，用以定义 API 资源的结构。resource 参数包含正在转换的数据。返回一个包含要在 API 响应中显示的字段的数组，并从 ``$resource`` 参数中获取数据。

        .. literalinclude:: api_transformers/017.php

    .. php:method:: transform($resource = null)

        :param mixed $resource: 要转换的资源（实体、数组、对象或 null）
        :returns: 转换后的数组
        :rtype: array

        通过调用包含资源数据的 ``toArray()``，将给定资源转换为数组。如果 ``$resource`` 为 ``null``，则向 ``toArray()`` 传递 ``null``。如果是实体，则先提取其数组表示；否则将其强制转换为数组。

        资源还会存储在 ``$this->resource`` 中，以便 include 方法访问。

        该方法会自动根据查询参数应用字段筛选和 include。

        .. literalinclude:: api_transformers/018.php

    .. php:method:: transformMany(array $resources)

        :param array $resources: 要转换的资源数组
        :returns: 转换后的资源数组
        :rtype: array

        通过对每一项调用 ``transform()`` 来转换资源集合。字段筛选和 include 会一致地应用到所有项。

        .. literalinclude:: api_transformers/019.php

    .. php:method:: getAllowedFields()

        :returns: 允许的字段名数组，或返回 ``null`` 以允许所有字段
        :rtype: array|null

        重写此方法以限制可通过 ``fields`` 查询参数请求的字段。返回 ``null`` （默认值）以允许 ``toArray()`` 中的所有字段。返回字段名数组以创建允许字段的白名单。

        .. literalinclude:: api_transformers/022.php

    .. php:method:: getAllowedIncludes()

        :returns: 允许的 include 名称数组，或返回 ``null`` 以允许所有 include
        :rtype: array|null

        重写此方法以限制可通过 ``include`` 查询参数包含的关联资源。返回 ``null`` （默认值）以允许所有具有对应方法的 include。返回 include 名称数组以创建白名单。返回空数组则禁用所有 include。

        .. literalinclude:: api_transformers/023.php

*******************
异常参考
*******************

.. php:class:: ApiException

    .. php:staticmethod:: forInvalidFields(string $field)

        :param string $field: 无效的字段名
        :returns: ApiException 实例
        :rtype: ApiException

        当客户端通过 ``fields`` 查询参数请求了不在允许字段列表中的字段时抛出。

    .. php:staticmethod:: forInvalidIncludes(string $include)

        :param string $include: 无效的 include 名称
        :returns: ApiException 实例
        :rtype: ApiException

        当客户端通过 ``include`` 查询参数请求了不在允许 include 列表中的内容时抛出。

    .. php:staticmethod:: forMissingInclude(string $include)

        :param string $include: 缺失的 include 方法名
        :returns: ApiException 实例
        :rtype: ApiException

        当客户端通过 ``include`` 查询参数请求了某个 include，但 Transformer 类中不存在对应的 ``include*()`` 方法时抛出。此验证确保所有请求的 include 都有定义的处理方法。
