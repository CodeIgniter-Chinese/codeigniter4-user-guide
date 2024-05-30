升级加密
##################

.. contents::
    :local:
    :depth: 2

文档
**************

- `CodeIgniter 3.x 加密库文档 <http://codeigniter.com/userguide3/libraries/encryption.html>`_
- :doc:`CodeIgniter 4.x 加密服务文档 </libraries/encryption>`

变更点
*********************

- 不再支持 ``MCrypt``,它在 PHP 7.2 中已被弃用。

升级指南
*************

1. 在配置中, ``$config['encryption_key'] = 'abc123';`` 从 **application/config/config.php** 移到了 **app/Config/Encryption.php** 中的 ``public $key = 'abc123';``。
2. 如果需要解密用 CI3 加密的数据,请配置设置以保持兼容性。参见 :ref:`encryption-compatible-with-ci3`。
3. 在使用加密库的任何地方,都必须将 ``$this->load->library('encryption');`` 替换为 ``$encrypter = service('encrypter');``,并如下例代码中更改加密和解密的方法。

代码示例
************

CodeIgniter 3.x 版本
=======================

.. literalinclude:: upgrade_encryption/ci3sample/001.php

CodeIgniter 4.x 版本
=======================

.. literalinclude:: upgrade_encryption/001.php
