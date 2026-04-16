####################
测试 CLI 命令
####################

.. contents::
    :local:
    :depth: 3

.. _using-mock-input-output:

*********************
使用 MockInputOutput
*********************

.. versionadded:: 4.5.0

MockInputOutput
===============

**MockInputOutput** 提供了一种便捷的方式来测试需要用户输入的命令，例如 ``CLI::prompt()``、``CLI::wait()`` 和 ``CLI::input()``。

测试执行期间，可用 ``MockInputOutput`` 替换 ``InputOutput`` 类，从而捕获输入和输出。

.. note:: 使用 ``MockInputOutput`` 时，无需再使用
    :ref:`stream-filter-trait`、:ref:`ci-test-stream-filter` 和
    :ref:`php-stream-wrapper`。

辅助方法
---------------

getOutput(?int $index = null): string
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

获取输出内容。

- 调用 ``$io->getOutput()`` 时，返回完整输出字符串。
- 指定 ``0`` 或正数时，返回输出数组中对应索引的项。
  每项是单次 ``CLI::fwrite()`` 调用的输出。
- 指定负数 ``-n`` 时，返回输出数组倒数第 ``n`` 项。

getOutputs(): array
^^^^^^^^^^^^^^^^^^^

返回输出数组。每项是单次 ``CLI::fwrite()`` 调用的输出。

使用方法
==========

- ``CLI::setInputOutput()`` 可将 ``MockInputOutput`` 实例设置到 ``CLI`` 类。
- ``CLI::resetInputOutput()`` 重置 ``CLI`` 类中的 ``InputOutput`` 实例。
- ``MockInputOutput::setInputs()`` 设置用户输入数组。
- ``MockInputOutput::getOutput()`` 获取命令输出。

以下测试代码用于测试命令 ``spark db:table``：

.. literalinclude:: cli/001.php

***********************
不使用 MockInputOutput
***********************

.. _testing-cli-output:

测试 CLI 输出
==================

.. _stream-filter-trait:

StreamFilterTrait
-----------------

.. versionadded:: 4.3.0

**StreamFilterTrait** 提供了一组替代方法。

有些情况测试起来比较困难。此时捕获流（如 PHP 自身的 STDOUT 或 STDERR）可能会有帮助。``StreamFilterTrait`` 可用于捕获指定流的输出。

使用方法
^^^^^^^^^^

- ``StreamFilterTrait::getStreamFilterBuffer()`` 获取缓冲区捕获的数据。
- ``StreamFilterTrait::resetStreamFilterBuffer()`` 重置捕获的数据。

测试用例中的使用示例：

.. literalinclude:: overview/018.php

``StreamFilterTrait`` 包含一个会自动调用的配置方法。
详见 :ref:`测试 Trait <testing-overview-traits>`。

如果测试中重写了 ``setUp()`` 或 ``tearDown()`` 方法，则必须分别调用 ``parent::setUp()`` 和
``parent::tearDown()`` 方法以完成 ``StreamFilterTrait`` 的配置。

.. _ci-test-stream-filter:

CITestStreamFilter
------------------

**CITestStreamFilter** 用于手动/单次场景。

如果只需在单个测试中捕获流，可以不使用 StreamFilterTrait trait，改为手动
为流添加过滤器。

使用方法
^^^^^^^^^^

- ``CITestStreamFilter::registration()`` 注册过滤器。
- ``CITestStreamFilter::addOutputFilter()`` 为输出流添加过滤器。
- ``CITestStreamFilter::addErrorFilter()`` 为错误流添加过滤器。
- ``CITestStreamFilter::removeOutputFilter()`` 从输出流移除过滤器。
- ``CITestStreamFilter::removeErrorFilter()`` 从错误流移除过滤器。

.. literalinclude:: overview/020.php

.. _testing-cli-input:

测试 CLI 输入
=================

.. _php-stream-wrapper:

PhpStreamWrapper
----------------

.. versionadded:: 4.3.0

**PhpStreamWrapper** 提供了一种方式来测试需要用户输入的方法，
例如 ``CLI::prompt()``、``CLI::wait()`` 和 ``CLI::input()``。

.. note:: PhpStreamWrapper 是一个流封装类。
    如果不了解 PHP 的流封装，请参阅 PHP 手册中的
    `streamWrapper 类 <https://www.php.net/manual/zh/class.streamwrapper.php>`_。

使用方法
^^^^^^^^^^

- ``PhpStreamWrapper::register()`` 将 ``PhpStreamWrapper`` 注册到 ``php`` 协议。
- ``PhpStreamWrapper::restore()`` 将 php 协议恢复为 PHP 内置的流封装。
- ``PhpStreamWrapper::setContent()`` 设置输入数据。

.. important:: PhpStreamWrapper 仅用于测试 ``php://stdin``。
    但注册后，它将处理所有 `php 协议 <https://www.php.net/manual/zh/wrappers.php.php>`_ 流，
    例如 ``php://stdout``、``php://stderr``、``php://memory``。
    因此强烈建议仅在需要时注册/取消注册 ``PhpStreamWrapper``。
    否则，注册期间会干扰其他 PHP 内置流。

测试用例中的使用示例：

.. literalinclude:: overview/019.php
