升级配置
#####################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.X 配置文档 <http://codeigniter.com/userguide3/libraries/config.html>`_
- :doc:`CodeIgniter 4.X 配置文档 </general/configuration>`

变更点
=====================

- 在 CI4 中,配置现在存储在扩展 ``CodeIgniter\Config\BaseConfig`` 的类中。
- CI3 中的 **application/config/config.php** 将变为 **app/Config/App.php**
  以及一些像 **app/Config/Security.php** 这样的特定类文件。
- 在配置类中,配置值存储为公共类属性。
- 获取配置值的方法也进行了更改。

升级指南
=============

1. 你需要根据 CI3 文件中的更改来更改 CI4 默认配置文件的值。配置名称与 CI3 中的名称大体相同。
2. 如果你在 CI3 项目中使用自定义配置文件,则需要在 CI4 项目中的 **app/Config** 内将这些文件创建为新的 PHP 类。
   这些类应该在 ``Config`` 命名空间内,并继承 ``CodeIgniter\Config\BaseConfig``。
3. 创建所有自定义配置类后,你需要将 CI3 配置中的变量复制为新的 CI4 配置类中的公共类属性。
4. 现在,你需要在所有获取配置值的地方更改配置获取语法。CI3 语法类似于 ``$this->config->item('item_name');``。
   你需要将其更改为 ``config('MyConfig')->item_name;``。

代码示例
============

CodeIgniter 3.x 版本
-----------------------

路径:**application/config/site.php**:

.. literalinclude:: upgrade_configuration/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

路径:**app/Config/Site.php**:

.. literalinclude:: upgrade_configuration/001.php
