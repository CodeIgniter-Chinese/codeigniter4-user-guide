升级图像处理类
################################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x 图像处理类文档 <https://www.codeigniter.com/userguide3/libraries/image_lib.html>`_
- :doc:`CodeIgniter 4.x 图像处理类文档 <../libraries/images>`

变更内容
=====================
- 在 CI3 中传递给构造函数或 ``initialize()`` 方法的首选项已更改为在 CI4 中的新方法中指定。
- 一些首选项如 ``create_thumb`` 被移除了。
- 在 CI4 中，必须调用 ``save()`` 方法来保存处理后的图像。
- ``display_errors()`` 已被移除，如果发生错误，将抛出异常。

升级指南
=============
1. 在你的类中，将 ``$this->load->library('image_lib');`` 更改为
   ``$image = \Config\Services::image();``。
2. 更改传递给构造函数或 ``initialize()`` 方法的首选项为在相应方法中指定。
3. 调用 ``save()`` 方法保存文件。

代码示例
============

CodeIgniter 版本 3.x
------------------------

.. literalinclude:: upgrade_images/ci3sample/001.php

CodeIgniter 版本 4.x
-----------------------

.. literalinclude:: upgrade_images/001.php
