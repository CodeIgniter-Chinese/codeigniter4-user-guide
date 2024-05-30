升级上传文件处理
###################################

.. contents::
    :local:
    :depth: 2

文档
==============
- `CodeIgniter 3.x 文件上传类文档 <http://codeigniter.com/userguide3/libraries/file_uploading.html>`_
- :doc:`CodeIgniter 4.x 上传文件处理文档 </libraries/uploaded_files>`

变更点
=====================
- 文件上传的功能发生了很大变化。你现在可以检查文件是否成功上传,移动/存储文件也更简单了。

升级指南
=============
在 CI4 中,通过 ``$file = $this->request->getFile('userfile')`` 访问上传的文件。然后可以使用 ``$file->isValid()`` 检验文件是否成功上传。
要存储文件,可以使用 ``$path = $this->request->getFile('userfile')->store('head_img/', 'user_name.jpg');``。这将文件存储在 **writable/uploads/head_img/user_name.jpg**。

你必须根据新方法更改文件上传代码。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_file_upload/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_file_upload/001.php
