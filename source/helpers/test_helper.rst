##############
测试辅助函数
##############

测试辅助函数文件包含帮助测试项目的函数。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
===================

使用以下代码加载此辅助函数:

.. literalinclude:: test_helper/001.php

可用函数
===================

以下函数可用:

.. php:function:: fake($model, array $overrides = null)

    :param    Model|object|string    $model: 要与 Fabricator 一起使用的模型的实例或名称
    :param    array|null $overrides: 要传递给 Fabricator::setOverrides() 的覆盖数据
    :returns:    Fabricator 创建的随机假数据并添加到数据库中的项目
    :rtype:    object|array

    使用 ``CodeIgniter\Test\Fabricator`` 创建一个随机项并将其添加到数据库中。

    使用示例:

    .. literalinclude:: test_helper/002.php
