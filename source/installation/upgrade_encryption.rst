升级加密
##################

.. contents::
    :local:
    :depth: 2

文档
**************

- `CodeIgniter 3.x 加密类文档 <https://codeigniter.org.cn/userguide3/libraries/encryption.html>`_
- :doc:`CodeIgniter 4.x 加密服务文档 </libraries/encryption>`

变更内容
*********************

- 对 ``MCrypt`` 的支持已被移除，因为它自 PHP 7.2 起已被弃用。

升级指南
*************

1. 在配置中，``$config['encryption_key'] = 'abc123';`` 已从 **application/config/config.php** 移到 **app/Config/Encryption.php** 中的 ``public $key = 'abc123';``。
2. 如果需要解密由 CI3 的 Encryption 加密的数据，请配置兼容性设置。请参见 :ref:`encryption-compatible-with-ci3`。
3. 在所有使用加密类的地方，都需要将 ``$this->load->library('encryption');`` 替换为 ``$encrypter = service('encrypter');``，并按下面的代码示例修改加密和解密的方法。

代码示例
************

CodeIgniter 3.x 版本
=======================

.. literalinclude:: upgrade_encryption/ci3sample/001.php

CodeIgniter 4.x 版本
=======================

.. literalinclude:: upgrade_encryption/001.php
