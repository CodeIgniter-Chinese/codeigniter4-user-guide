升级上传文件处理
###################################

.. contents::
    :local:
    :depth: 2

文档
==============
- `CodeIgniter 3.x 文件上传类文档 <https://codeigniter.org.cn/userguide3/libraries/file_uploading.html>`_
- :doc:`CodeIgniter 4.x 上传文件处理文档 </libraries/uploaded_files>`

变更内容
=====================
- 文件上传的功能有很大变化。现在，你可以检查文件是否上传成功且没有错误，移动或存储文件也更简单了。

升级指南
=============
在 CI4 中，你可以使用 ``$file = $this->request->getFile('userfile')`` 访问已上传的文件。然后，可以通过 ``$file->isValid()`` 验证文件是否已成功上传。
要存储文件，可以使用 ``$path = $this->request->getFile('userfile')->store('head_img/', 'user_name.jpg');``。这会将文件存储到 **writable/uploads/head_img/user_name.jpg**。

必须修改文件上传代码，以适配这些新方法。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_file_upload/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_file_upload/001.php
