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

**MockInputOutput** 提供了一种简单的方法来编写需要用户输入的命令的测试，例如 ``CLI::prompt()``、``CLI::wait()`` 和 ``CLI::input()``。

你可以在测试执行期间用 ``MockInputOutput`` 替换 ``InputOutput`` 类来捕获输入和输出。

.. note:: 当你使用 ``MockInputOutput`` 时，你不需要使用
    :ref:`stream-filter-trait`、:ref:`ci-test-stream-filter` 和
    :ref:`php-stream-wrapper`。

辅助方法
---------------

getOutput(?int $index = null): string
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

获取输出。

- 如果你像 ``$io->getOutput()`` 这样调用它，它会返回整个输出字符串。
- 如果你指定 ``0`` 或一个正数，它会返回输出数组项。每个项都有一个 ``CLI::fwrite()`` 调用的输出。
- 如果你指定一个负数 ``-n``，它会返回输出数组的倒数第 ``n`` 项。

getOutputs(): array
^^^^^^^^^^^^^^^^^^^

返回输出数组。每个项都有一个 ``CLI::fwrite()`` 调用的输出。

如何使用
==========

- ``CLI::setInputOutput()`` 可以将 ``MockInputOutput`` 实例设置到 ``CLI`` 类。
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

**StreamFilterTrait** 提供了这些辅助方法的替代方案。

你可能需要测试一些难以测试的东西。有时，捕获一个流，比如 PHP 自己的 STDOUT 或 STDERR，可能会有所帮助。``StreamFilterTrait`` 帮助你捕获所选流的输出。

如何使用
^^^^^^^^^^

- ``StreamFilterTrait::getStreamFilterBuffer()`` 从缓冲区获取捕获的数据。
- ``StreamFilterTrait::resetStreamFilterBuffer()`` 重置捕获的数据。

在你的一个测试用例中演示这一点的示例：

.. literalinclude:: overview/018.php

``StreamFilterTrait`` 有一个自动调用的配置器。
参见 :ref:`Testing Traits <testing-overview-traits>`。

如果你在测试中重写了 ``setUp()`` 或 ``tearDown()`` 方法，那么你必须分别调用 ``parent::setUp()`` 和 ``parent::tearDown()`` 方法来配置 ``StreamFilterTrait``。

.. _ci-test-stream-filter:

CITestStreamFilter
------------------

**CITestStreamFilter** 用于手动/单次使用。

如果你只需要在一个测试中捕获流，那么可以手动向流添加过滤器，而不是使用 StreamFilterTrait trait。

如何使用
^^^^^^^^^^

- ``CITestStreamFilter::registration()`` 过滤器注册。
- ``CITestStreamFilter::addOutputFilter()`` 向输出流添加过滤器。
- ``CITestStreamFilter::addErrorFilter()`` 向错误流添加过滤器。
- ``CITestStreamFilter::removeOutputFilter()`` 从输出流中移除过滤器。
- ``CITestStreamFilter::removeErrorFilter()`` 从错误流中移除过滤器。

.. literalinclude:: overview/020.php

.. _testing-cli-input:

测试 CLI 输入
=================

.. _php-stream-wrapper:

PhpStreamWrapper
----------------

.. versionadded:: 4.3.0

**PhpStreamWrapper** 提供了一种方法来编写需要用户输入的方法的测试，例如 ``CLI::prompt()``、``CLI::wait()`` 和 ``CLI::input()``。

.. note:: PhpStreamWrapper 是一个流包装类。
    如果你不了解 PHP 的流包装器，
    请参见 PHP 手册中的 `The streamWrapper class <https://www.php.net/manual/en/class.streamwrapper.php>`_。

如何使用
^^^^^^^^^^

- ``PhpStreamWrapper::register()`` 将 ``PhpStreamWrapper`` 注册到 ``php`` 协议。
- ``PhpStreamWrapper::restore()`` 将 php 协议包装器恢复为 PHP 内置包装器。
- ``PhpStreamWrapper::setContent()`` 设置输入数据。

.. important:: PhpStreamWrapper 仅用于测试 ``php://stdin``。
    但是当你注册它时，它会处理所有 `php 协议 <https://www.php.net/manual/en/wrappers.php.php>`_ 流，
    例如 ``php://stdout``、``php://stderr``、``php://memory``。
    因此强烈建议仅在需要时注册/注销 ``PhpStreamWrapper``。否则，它在注册时会干扰其他内置的 php 流。

在你的一个测试用例中演示这一点的示例：

.. literalinclude:: overview/019.php
