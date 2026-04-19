.. _incoming/controller_attributes:

#####################
控制器注解
#####################

PHP 注解可用于在控制器类和方法上定义过滤器及其他元数据。这样能让配置紧邻受影响的代码，且一眼即可看出特定控制器或方法应用了哪些过滤器。此方式适用于所有路由方式（包含自动路由），使得自动路由在功能上几乎能与更为强大的路由声明相媲美。

.. contents::
    :local:
    :depth: 2

快速入门
***************

控制器注解既可应用于整个类，也可应用于特定方法。以下示例展示了如何在控制器类上应用 ``Filters`` 注解：

.. literalinclude:: controller_attributes/001.php

在此示例中，``Auth`` 过滤器将应用于 ``AdminController`` 中的所有方法。

也可以将 ``Filters`` 注解应用于控制器内的特定方法。这样可以仅对部分方法应用过滤器，而不影响其他方法。示例如下：

.. literalinclude:: controller_attributes/002.php

类级别注解和方法级别注解可协同工作，为控制器层级的路由管理提供灵活方案。

禁用注解
--------------------

如果确认应用中不使用注解，可将 ``app/Config/Routing.php`` 文件中的 ``$useControllerAttributes`` 注解设置为 ``false`` 以禁用此功能。

内置注解
*******************

过滤器
-------

``Filters`` 注解允许指定一个或多个过滤器，并将其应用于控制器类或方法。可指定在控制器动作执行前或执行后运行过滤器，并为过滤器传递参数。以下是 ``Filters`` 注解的使用示例：

.. literalinclude:: controller_attributes/003.php

.. note::

    当注解和过滤器配置文件中同时定义了过滤器时，两者都会生效，但可能会产生非预期结果。

.. note::

    请注意，传递给过滤器的所有参数都会被转换为字符串。此行为仅影响过滤器。

Restrict
--------

``Restrict`` 注解允许根据域名、子域名或应用运行环境来限制对类或方法的访问。以下是 ``Restrict`` 注解的使用示例：

.. literalinclude:: controller_attributes/004.php

缓存
-----

``Cache`` 注解允许将控制器方法的输出缓存指定时长。可以以秒为单位指定时长，并可选择性地设置缓存键。以下是 ``Cache`` 注解的使用示例：

.. literalinclude:: controller_attributes/005.php

自定义注解
*****************

也可以创建自定义注解，为控制器和方法添加元数据或行为。自定义注解必须实现 ``CodeIgniter\Router\Attributes\RouteAttributeInterface`` 接口。以下示例展示了如何通过自定义注解在响应中添加自定义标头：

.. literalinclude:: controller_attributes/006.php

随后可以像使用内置注解一样，将此自定义注解应用于控制器类或方法：

.. literalinclude:: controller_attributes/007.php
