升级 Email
##############

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x Email 文档 <https://codeigniter.org.cn/userguide3/libraries/email.html>`_
- :doc:`CodeIgniter 4.x Email 文档 </libraries/email>`

变更内容
=====================
- 只有一些小改动，例如方法名以及类的加载方式发生了变化。
- 使用 SMTP 协议时，其行为也有一些细微变化。如果沿用 CI3 的设置，可能无法与 SMTP 服务器正常通信。请参见 :ref:`email-ssl-tls-for-smtp` 和 :ref:`email-preferences`。

升级指南
=============
1. 在类中，将 ``$this->load->library('email');`` 改为 ``$email = service('email');``。
2. 之后，需要将所有以 ``$this->email`` 开头的代码替换为 ``$email``。
3. Email 类中的方法名略有不同。除 ``send()``、``attach()``、``printDebugger()`` 和 ``clear()`` 外，所有方法都以 ``set`` 为前缀，后接原来的方法名。例如，``bcc()`` 现在是 ``setBcc()``，其他方法同理。
4. **app/Config/Email.php** 中的配置属性已经变更。请参见 :ref:`setting-email-preferences`，查看新的属性列表。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_emails/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_emails/001.php
