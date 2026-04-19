.. _ci47-rest-part2:

自动路由与第一个接口
##################################

.. contents::
    :local:
    :depth: 2

本节将启用 CodeIgniter 的 *自动路由（改进版）* 功能，并创建一个简单的 JSON 接口以确认配置无误。

为什么使用自动路由？
====================

前面的教程展示了如何在 **app/Config/Routes.php** 中手动定义路由。虽然这种方式功能强大且灵活，但对于拥有众多遵循相同模式的 RESTful API 来说，手动配置会显得极其繁琐。自动路由通过基于约定的规则将 URL 模式映射到控制器类和方法，极大地简化了这一过程，并且重点关注 HTTP 方法，非常契合 RESTful API 的开发需求。

启用自动路由（改进版）
============================

自动路由默认处于关闭状态。需将其启用，以便控制器能够自动处理 REST 风格的方法。

打开 **app/Config/Feature.php** 并确认此标志为 ``true`` （此为默认值）：

.. code-block:: php

    public bool $autoRoutesImproved = true;

“改进版”自动路由比传统版更加安全可靠，因此推荐所有新项目使用。

接着，在 **app/Config/Routing.php** 中，确认自动路由 **已启用**：

.. code-block:: php

    public bool $autoRoute = true;

完成这些配置后，CodeIgniter 就会自动将控制器类映射到类似 ``GET /api/ping`` 或 ``POST /api/ping`` 的 URI 上。

创建 Ping 控制器
========================

为了理解基本 API 接口的工作原理，我们来生成一个控制器作为首个 API 接口。它将提供一个简单的“ping”响应，以确认环境搭建无误。

.. code-block:: console

   php spark make:controller Api/Ping

该命令会生成 **app/Controllers/Api/Ping.php**。

编辑该文件，使其内容如下：

.. literalinclude:: code/001.php

此处执行了以下操作：

- 使用了 :php:class:`ResponseTrait`，其中已包含 :php:meth:`respond()` 等 REST 辅助函数以及适当的状态码。
- 定义了 ``getIndex()`` 方法。前缀 ``get`` 表示响应 ``GET`` 请求，名称 ``Index`` 表示匹配基础 URI（``/api/ping``）。

测试路由
==============

如果开发服务器尚未运行，请启动：

.. code-block:: console

   php spark serve

现在访问：

- **浏览器：** ``http://localhost:8080/api/ping``
- **cURL：** ``curl http://localhost:8080/api/ping``

预期响应：

.. code-block:: json

    {
        "status": "ok"
    }

恭喜，首个可用的 JSON 接口创建成功！

原理说明
=======================

请求 ``/api/ping`` 时：

1. **自动路由（改进版）** 定位到 ``App\Controllers\Api\Ping`` 类。
2. 检测到 HTTP 方法（``GET``）。
3. 调用对应的方法名称：``getIndex()``。
4. :php:trait:`ResponseTrait` 提供辅助函数以生成一致的输出结果。

若后续添加其他 HTTP 方法，映射关系如下表所示：

+-----------------------+--------------------------------+
| HTTP 方法             | 方法名称                       |
+=======================+================================+
| ``GET /api/ping``     | ``getIndex()``                 |
| ``POST /api/ping``    | ``postIndex()``                |
| ``DELETE /api/ping``  | ``deleteIndex()``              |
+-----------------------+--------------------------------+

使用 Format 类进行内容协商
=========================================

CodeIgniter 默认使用 :php:class:`CodeIgniter\\Format\\Format` 类自动进行响应格式协商。系统会根据客户端的请求，返回 JSON 或 XML 格式的响应。

:php:trait:`ResponseTrait` 默认将格式设为 JSON。如需返回 XML 也可修改此配置，但本教程将专注于 JSON 响应。

.. literalinclude:: code/002.php

可选：返回更多数据
==========================

``respond()`` 方法还能返回其他数据：

.. literalinclude:: code/003.php

至此已拥有一个可在浏览器和 cURL 中测试的可用接口。下一节将创建首个真正的数据库资源，通过定义 **迁移**、**数据填充** 以及针对 ``books`` 表的 **模型**，为 API 的 CRUD 接口提供支持。
