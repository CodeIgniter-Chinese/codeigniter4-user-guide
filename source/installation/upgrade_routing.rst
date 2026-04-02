升级路由
##################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x URI 路由文档 <https://codeigniter.org.cn/userguide3/general/routing.html>`_
- :doc:`CodeIgniter 4.x URI 路由文档 </incoming/routing>`

变更内容
=====================

- 在 CI4 中，自动路由默认已禁用。
- 在 CI4 中，引入了新的、更安全的 :ref:`auto-routing-improved`。
- 在 CI4 中，路由不再通过将路由设置为数组来配置。
- CI3 中的通配符 ``(:any)``，在 CI4 中对应为占位符 ``(:segment)``。CI4 中的 ``(:any)`` 会匹配多个段。参见 :ref:`URI 路由 <routing-placeholder-any>`。

升级指南
=============

1. 如果以与 CI3 相同的方式使用自动路由，则需要启用 :ref:`auto-routing-legacy`。
2. 必须修改每一条路由的语法，并将其追加到 **app/Config/Routes.php** 中。例如：

    - ``$route['journals'] = 'blogs';`` 改为 ``$routes->add('journals', 'Blogs::index');``。这会映射到 ``Blogs`` 控制器中的 ``index()`` 方法。
    - ``$route['product/(:any)'] = 'catalog/product_lookup';`` 改为 ``$routes->add('product/(:segment)', 'Catalog::productLookup');``。不要忘记将 ``(:any)`` 替换为 ``(:segment)``。
    - ``$route['login/(.+)'] = 'auth/login/$1';`` 改为 ``$routes->add('login/(.+)', 'Auth::login/$1');``

    .. note:: 为了向后兼容，这里使用了 ``$routes->add()``。但是，出于安全原因，
        强烈建议使用 :ref:`routing-http-verb-routes`，例如
        ``$routes->get()``，而不是 ``$routes->add()``。

代码示例
============

CodeIgniter 3.x 版本
------------------------
路径：**application/config/routes.php**：

.. literalinclude:: upgrade_routing/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------
路径：**app/Config/Routes.php**：

.. literalinclude:: upgrade_routing/001.php

.. note:: 为了向后兼容，这里使用了 ``$routes->add()``。但是，出于安全原因，
    强烈建议使用 :ref:`routing-http-verb-routes`，例如
    ``$routes->get()``，而不是 ``$routes->add()``。
