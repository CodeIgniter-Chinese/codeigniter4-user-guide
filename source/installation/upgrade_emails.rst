升级邮件
##############

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.X 邮件文档 <http://codeigniter.com/userguide3/libraries/email.html>`_
- :doc:`CodeIgniter 4.X 邮件文档 </libraries/email>`

变更点
=====================

- 只是一些小变化,如方法名称和库的加载。
- 使用 SMTP 协议时的行为已经稍有更改。如果你使用 CI3 的设置，可能无法与你的 SMTP 服务器正确通信。请参见 :ref:`email-ssl-tls-for-smtp` 和 :ref:`email-preferences`。

升级指南
=============
1. 在类中,将 ``$this->load->library('email');`` 改为 ``$email = service('email');``。
2. 从那时起,需要将以 ``$this->email`` 开头的每一行改为 ``$email``。
3. Email 类中的方法命名略有不同。除 ``send()``、``attach()``、``printDebugger()`` 和 ``clear()`` 之外的所有方法都有一个 ``set`` 前缀,后跟之前的方法名。``bcc()`` 现在变为 ``setBcc()``,等等。
4. **app/Config/Email.php** 中的配置属性已更改。你应该查看 :ref:`setting-email-preferences` 以获取新的属性列表。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_emails/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_emails/001.php
