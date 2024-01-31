升级路由
##################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.X URI 路由文档 <http://codeigniter.com/userguide3/general/routing.html>`_
- :doc:`CodeIgniter 4.X URI 路由文档 </incoming/routing>`

变更点
=====================

- 在 CI4 中,默认关闭自动路由。
- 在 CI4 中引入了新的更安全的 :ref:`auto-routing-improved`。
- 在 CI4 中,路由配置不再通过设置路由数组来完成。
- CI3 中的通配符 ``(:any)`` 在 CI4 中将会是占位符 ``(:segment)``。在 CI4 中的 ``(:any)`` 匹配多个段。请参见 :ref:`URI 路由 <routing-placeholder-any>`。

升级指南
=============

1. 如果你以与 CI3 相同的方式使用自动路由,则需要启用 :ref:`auto-routing-legacy`。
2. 你必须更改每个路由行的语法,并将其附加到 **app/Config/Routes.php** 中。例如:

    - ``$route['journals'] = 'blogs';`` 改为 ``$routes->add('journals', 'Blogs::index');``。这将映射到 ``Blogs`` 控制器中的 ``index()`` 方法。
    - ``$route['product/(:any)'] = 'catalog/product_lookup';`` 改为 ``$routes->add('product/(:segment)', 'Catalog::productLookup');``。别忘了将 ``(:any)`` 替换为 ``(:segment)``。
    - ``$route['login/(.+)'] = 'auth/login/$1';`` 改为 ``$routes->add('login/(.+)', 'Auth::login/$1');``

    .. note:: 为了向后兼容，这里使用了 ``$routes->add()``。但我们强烈建议使用 :ref:`routing-http-verb-routes` 中的
        ``$routes->get()`` 替代 ``$routes->add()``，以增强安全性。

代码示例
============

CodeIgniter 3.x 版本
------------------------
路径:**application/config/routes.php**:

.. literalinclude:: upgrade_routing/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------
路径:**app/Config/Routes.php**:

.. literalinclude:: upgrade_routing/001.php

.. note:: 为了向后兼容，这里使用了 ``$routes->add()``。但我们强烈建议使用 :ref:`routing-http-verb-routes` 中的
    ``$routes->get()`` 替代 ``$routes->add()``，以增强安全性。
