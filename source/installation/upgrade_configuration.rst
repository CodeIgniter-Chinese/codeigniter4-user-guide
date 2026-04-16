升级配置
#####################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x 配置文档 <https://codeigniter.org.cn/userguide3/libraries/config.html>`_
- :doc:`CodeIgniter 4.x 配置文档 </general/configuration>`

变更内容
=====================

- 在 CI4 中，配置现在存储在继承 ``CodeIgniter\Config\BaseConfig`` 的类中。
- CI3 中的 **application/config/config.php** 对应 CI4 的 **app/Config/App.php**，
  以及其他针对特定类的文件，例如 **app/Config/Security.php**。
- 在配置类中，配置值存储为公共类属性。
- 获取配置值的方法已发生变化。

升级指南
=============

1. 根据 CI3 文件中的变更，修改 CI4 默认配置文件中的值。配置名称与 CI3 基本一致。
2. 如果在 CI3 项目中使用了自定义配置文件，需要在 CI4 项目的 **app/Config** 中将其创建为新的 PHP 类。这些类应位于 ``Config`` 命名空间，并继承 ``CodeIgniter\Config\BaseConfig``。
3. 创建所有自定义配置类后，将 CI3 配置中的变量复制到新的 CI4 配置类中，并作为公共类属性。
4. 更新所有获取配置值的代码语法。CI3 的写法类似 ``$this->config->item('item_name');``，需要改为 ``config('MyConfig')->item_name;``。

代码示例
============

CodeIgniter 3.x 版本
------------------------

路径：**application/config/site.php**：

.. literalinclude:: upgrade_configuration/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

路径：**app/Config/Site.php**：

.. literalinclude:: upgrade_configuration/001.php
