.. _ci47-rest-part4:

构建 RESTful 控制器
#############################

本章将构建 API 接口，通过规范的 RESTful API 公开 ``book`` 表。我们将使用 :php:class:`CodeIgniter\\RESTful\\ResourceController` 来处理 CRUD 操作，几乎无需编写样板代码。

什么是 RESTful？
================

RESTful API 使用标准 HTTP 方法（``GET``、``POST``、``PUT``、``DELETE``）对通过 URI 识别的资源执行操作。这种方法使 API 具有可预测性且易于使用。关于构成 REST API 的细节可能存在诸多争议，但遵循这些基础知识已足以满足多数用途。通过使用自动路由和 :php:class:`Api\ResponseTrait`，CodeIgniter 可轻松创建 RESTful 接口。

生成控制器
=======================

运行 Spark 命令：

.. code-block:: console

    php spark make:controller Api/Books

这将创建 **app/Controllers/Api/Books.php**。

打开该文件并将其内容替换为以下类定义：

.. literalinclude:: code/009.php

由于使用了自动路由，需要使用 ``index`` 方法名，以免干扰 URI 段的映射。但可以使用 HTTP 方法前缀（``get``、``post``、``put``、``delete``）来指明处理的方法。唯一稍显特殊的是 ``getIndex()``，它必须同时用于映射获取所有资源列表和根据 ID 获取单个资源。

.. tip::

   如果更倾向于其他命名方案，则需在 **app/Config/Routes.php** 中显式定义路由并关闭自动路由。

API Transformer
=================

将数据模型与 API 响应的展示方式分离被视为一种最佳实践。通常使用 Transformer 或资源类来统一数据格式。CodeIgniter 提供了 API Transformer 来协助完成此项工作。

使用生成器命令创建 Transformer：

.. code-block:: console

   php spark make:transformer BookTransformer

Transformer 要求必须包含一个名为 ``toArray()`` 的方法，并接收名为 ``$resource`` 的混合数据类型。该方法将资源转换为适合 API 响应的数组格式。返回的数组随后会被编码为 JSON 或 XML。

编辑 **app/Transformers/BookTransformer.php** 中的 Book Transformer。由于包含相关的作者数据，这个 Transformer 略显复杂：

.. literalinclude:: code/011.php

Transformer 的一个特性是可以有条件地包含关联资源。在本例中，在响应中包含作者信息前，会先检查 book 资源是否已加载 ``author`` 关联。这允许根据请求上下文灵活控制返回的数据量。调用 API 的客户端必须通过查询参数（如 ``/api/books?include=author``）显式请求关联数据。方法名必须以 ``include`` 开头，后接首字母大写的关联资源名称。

可能已经注意到这里没有使用 AuthorTransformer。这是因为作者数据足够简单，无需额外转换即可直接返回。然而，对于更复杂的关联资源，可能也需要为其创建单独的 Transformer。此外，我们将在查询时收集作者信息，以避免后续出现 N+1 查询问题。

书籍列表
=============

通过将 ``$id`` 参数设为可选，使同一个方法既能处理获取所有书籍列表，也能处理根据 ID 获取单本书籍。现在开始实现：

.. literalinclude:: code/012.php
    :language: php
    :lines: 15-41

在此方法中，首先检查是否提供了 ``$id``。如果提供，则尝试查找特定书籍。若无法通过该 ID 找到书籍，则使用 :php:trait:`ResponseTrait` 中的 :php:meth:`failNotFound()` 辅助函数返回 404 Not Found 响应。如果找到了书籍，则使用 BookTransformer 并返回格式化后的响应。

如果未提供 ``$id``，则使用模型获取所有书籍，但并不立即检索记录。这样可以使用 ``ResponseTrait`` 的 :php:meth:`paginate` 方法来自动处理分页。我们将 Transformer 的名称传递给 ``paginate`` 方法，以便其对分页结果集中的每本书籍进行格式化。

在这两种情况下，都使用了模型上的一个新方法 ``withAuthorInfo()``。这是稍后将添加到模型中的自定义方法，用于在检索书籍时连接相关的作者数据。

添加模型辅助方法
---------------------------

在 BookModel 中添加名为 ``withAuthorInfo()`` 的新方法。该方法使用查询构建器连接 ``author`` 表并选择相关的作者字段。这样在检索书籍时，无需为每本书单独进行查询即可获得关联的作者信息。

.. literalinclude:: code/014.php


测试列表接口
-----------------------

启动本地服务器：

.. code-block:: console

   php spark serve

现在访问：

- **浏览器：** ``http://localhost:8080/api/books``
- **cURL：** ``curl http://localhost:8080/api/books``

应该能看到 JSON 格式的分页书籍列表：

.. code-block:: json

    {
        "data": [
            {
                "id": 1,
                "title": "Dune",
                "author": "Frank Herbert",
                "year": 1965,
                "created_at": "2025-11-08 00:00:00",
                "updated_at": "2025-11-08 00:00:00"
            },
            {
                "id": 2,
                "title": "Neuromancer",
                "author": "William Gibson",
                "year": 1984,
                "created_at": "2025-11-08 00:00:00",
                "updated_at": "2025-11-08 00:00:00"
            }
        ],
        "meta": {
            "page": 1,
            "perPage": 20,
            "total": 2,
            "totalPages": 1
        },
        "links": {
            "self": "http://localhost:8080/api/books?page=1",
            "first": "http://localhost:8080/api/books?page=1",
            "last": "http://localhost:8080/api/books?page=1",
            "prev": null,
            "next": null
        }
    }

如果看到了来自数据填充工具的 JSON 数据，恭喜——API 已上线！

实现其余方法
===============================

编辑 **app/Controllers/Api/Books.php** 以包含其余方法：

.. literalinclude:: code/012.php

每个方法都使用 :php:trait:`ResponseTrait` 中的辅助函数来发送正确的 HTTP 状态码和 JSON 数据。

大功告成！现在已拥有一个功能完善的 RESTful API 来管理书籍，包括规范的 HTTP 方法、状态码和数据转换。还可根据需要通过添加身份验证、数据验证等功能来进一步增强此 API。

更具语义化的命名方案
=============================

在之前的示例中，使用了 ``getIndex()``、``putIndex()`` 等方法名，是因为希望完全依赖 HTTP 方法来确定操作。在启用自动路由的情况下，必须使用 ``index`` 方法名以避免与 URI 段冲突。但是，如果更倾向于使用更具语义的方法名，可以修改方法名以反映所执行的操作，例如 ``getList()``、``postCreate()``、``putUpdate()`` 和 ``deleteDelete()``。这将使每个方法的作用一目了然，但会在 URI 中增加一个段。

.. code-block:: text

    GET    /api/books/list         -> getList()
    POST   /api/books/create       -> postCreate()
    PUT    /api/books/update/(:id) -> putUpdate($id)
    DELETE /api/books/delete/(:id) -> deleteDelete($id)
