升级图像处理类
################################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x 图像处理类文档 <https://codeigniter.org.cn/userguide3/libraries/image_lib.html>`_
- :doc:`CodeIgniter 4.x 图像处理类文档 <../libraries/images>`

变更内容
=====================
- 在 CI3 中传递给构造函数或 ``initialize()`` 方法的首选项，在 CI4 中已改为在新方法中指定。
- 移除了 ``create_thumb`` 等部分首选项。
- 在 CI4 中，必须调用 ``save()`` 方法来保存处理后的图像。
- ``display_errors()`` 已被移除；如果发生错误，将抛出异常。

升级指南
=============
1. 在类中，将 ``$this->load->library('image_lib');`` 改为
   ``$image = \Config\Services::image();``。
2. 将传递给构造函数或 ``initialize()`` 方法的首选项，改为在对应的方法中指定。
3. 调用 ``save()`` 方法保存文件。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_images/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_images/001.php
