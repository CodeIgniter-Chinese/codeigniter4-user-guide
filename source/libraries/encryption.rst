##################
加密服务
##################

.. important:: 请勿使用本加密库或其他任何加密库来存储密码！密码应当进行哈希处理，
    可通过 PHP 的 `Password Hashing 扩展 <https://www.php.net/manual/zh/book.password.php>`_ 完成。

加密服务提供双向对称（密钥）数据加密。该服务会根据你的参数实例化和/或初始化加密 **handler** （处理程序），具体说明如下。

加密服务的 handler 必须实现 CodeIgniter 的 ``EncrypterInterface`` 接口。
使用适当的 PHP 加密扩展或第三方库可能需要在服务器上安装额外的软件，
和/或需要在 PHP 实例中显式启用。

目前支持以下 PHP 扩展：

- `OpenSSL <https://www.php.net/manual/zh/book.openssl.php>`_
- `Sodium <https://www.php.net/manual/zh/book.sodium>`_

这不是一个完整的加密解决方案。如需更多功能（如公钥加密），建议直接使用 OpenSSL 或其他 `加密扩展 <https://www.php.net/manual/zh/refs.crypto.php>`_。
也可考虑使用更全面的包，如 `Halite <https://github.com/paragonie/halite>`_ （基于 libsodium 构建的面向对象包）。

.. note:: 已放弃对 ``MCrypt`` 扩展的支持，因为该扩展自 PHP 7.2 起已被弃用。

.. contents::
    :local:
    :depth: 3

.. _usage:

****************************
使用加密类
****************************

与 CodeIgniter 的所有服务一样，可通过 ``Config\Services`` 加载：

.. literalinclude:: encryption/001.php

设置好起始密钥后（参见 :ref:`configuration`），加密和解密数据很简单——将适当的字符串传递给 ``encrypt()`` 和/或 ``decrypt()`` 方法：

.. literalinclude:: encryption/002.php

完成！加密库会自动处理所有必要步骤，确保整个过程的加密安全性，开箱即用。

.. _configuration:

配置类
=======================

上述示例使用 **app/Config/Encryption.php** 中的配置设置。

============== ==========================================================================
选项           可选值（括号内为默认值）
============== ==========================================================================
key            加密密钥起始值
driver         首选 handler，如 OpenSSL 或 Sodium（``OpenSSL``）
digest         消息摘要算法（``SHA512``）
blockSize      [**SodiumHandler** 专用] 填充字节长度（``16``）
cipher         [**OpenSSLHandler** 专用] 使用的加密算法（``AES-256-CTR``）
encryptKeyInfo [**OpenSSLHandler** 专用] 加密密钥信息（``''``）
authKeyInfo    [**OpenSSLHandler** 专用] 认证密钥信息（``''``）
rawData        [**OpenSSLHandler** 专用] 密文是否为原始格式（``true``）
============== ==========================================================================

可以通过向 ``Services`` 调用传递自定义配置对象来替换配置文件中的设置。``$config`` 变量必须是 ``Config\Encryption`` 类的实例。

.. literalinclude:: encryption/003.php

.. _encryption-compatible-with-ci3:

与 CI3 保持兼容的配置
------------------------------------------------

.. versionadded:: 4.3.0

自 v4.3.0 起，可以解密使用 CI3 加密的数据。如需解密此类数据，请使用以下设置以保持兼容。

.. literalinclude:: encryption/013.php

支持的 HMAC 认证算法
----------------------------------------

对于 HMAC 消息认证，加密库支持使用 SHA-2 系列算法：

=========== ==================== ============================
算法        原始长度（字节）     十六进制编码长度（字节）
=========== ==================== ============================
SHA512      64                   128
SHA384      48                   96
SHA256      32                   64
SHA224      28                   56
=========== ==================== ============================

不包含 MD5 或 SHA1 等其他流行算法的原因是它们已不再被视为足够安全，因此不鼓励使用。
如果确实需要使用，可通过 PHP 原生的 `hash_hmac() <https://www.php.net/manual/zh/function.hash-hmac.php>`_ 函数轻松实现。

当然，随着更安全算法的出现和普及，未来会添加更多的算法支持。

默认行为
================

默认情况下，加密库使用 OpenSSL handler。该 handler 使用 AES-256-CTR 算法、你配置的 *key* 和 SHA512 HMAC 认证进行加密。

设置加密密钥
===========================

加密密钥 **必须** 与所用加密算法允许的长度一致。对于 AES-256，即 256 位或 32 字节（字符）长。

密钥应尽可能随机，**绝不能** 是普通文本字符串，也不能是哈希函数的输出等。要创建合适的密钥，可使用加密库的 ``createKey()`` 方法。

.. literalinclude:: encryption/004.php

密钥可以存储在 **app/Config/Encryption.php** 中，也可以设计自己的存储机制，在加密/解密时动态传递密钥。

要将密钥保存到 **app/Config/Encryption.php**，打开文件并设置：

.. literalinclude:: encryption/005.php

编码密钥或结果
------------------------

``createKey()`` 方法输出的是二进制数据，难以处理（例如复制粘贴可能会损坏），因此可以使用 ``bin2hex()`` 或 ``base64_encode`` 以更易用的方式处理密钥。例如：

.. literalinclude:: encryption/006.php

同样的技巧也适用于加密结果：

.. literalinclude:: encryption/007.php

使用前缀存储密钥
------------------------------

存储加密密钥时可以使用两个特殊前缀：``hex2bin:`` 和 ``base64:``。当这些前缀紧接在密钥值之前时，``Encryption`` 会智能解析密钥，并仍将二进制字符串传递给库。

.. literalinclude:: encryption/008.php

同样，也可以在 **.env** 文件中使用这些前缀！
::

    // 用于 hex2bin
    encryption.key = hex2bin:<your-hex-encoded-key>

    // 或
    encryption.key = base64:<your-base64-encoded-key>

填充
=======

有时，消息长度本身可能泄露很多关于其性质的信息。如果消息是"yes"、"no"和"maybe"之一，加密消息并无帮助：知道长度就足以判断消息内容。

填充是一种缓解此问题的技术，通过将长度变为给定块大小的倍数来实现。

``SodiumHandler`` 使用 libsodium 原生的 ``sodium_pad`` 和 ``sodium_unpad`` 函数实现填充。这需要在加密前将填充长度（以字节为单位）添加到明文消息，解密后移除。填充可通过 ``Config\Encryption`` 的 ``$blockSize`` 属性配置。该值应大于零。

.. important:: 不建议自行设计填充实现。应始终使用库提供的更安全实现。此外，密码不应进行填充。
    不推荐通过填充来隐藏密码长度。客户端向服务器发送密码时应先进行哈希处理（即使只对哈希函数进行一次迭代）。
    这确保传输数据长度恒定，且服务器不会轻松获得密码副本。

加密处理程序说明
========================

OpenSSL 说明
-------------

`OpenSSL <https://www.php.net/manual/zh/book.openssl.php>`_ 扩展长期以来一直是 PHP 的标准组成部分。

CodeIgniter 的 OpenSSL handler 使用 AES-256-CTR 加密算法。

配置提供的 *key* 用于派生另外两个密钥：一个用于加密，一个用于认证。这是通过 `基于 HMAC 的密钥派生函数 <https://en.wikipedia.org/wiki/HKDF>`_ （HKDF）技术实现的。

Sodium 说明
------------

`Sodium <https://www.php.net/manual/zh/book.sodium>`_ 扩展自 PHP 7.2.0 起默认捆绑在 PHP 中。

Sodium 使用 XSalsa20 算法加密、Poly1305 进行 MAC 认证、XS25519 进行密钥交换，用于端到端场景中的秘密消息传输。要使用共享密钥（如对称加密）加密和/或认证字符串，Sodium 使用 XSalsa20 算法加密，HMAC-SHA512 进行认证。

.. note:: CodeIgniter 的 ``SodiumHandler`` 在每个加密或解密会话后使用 ``sodium_memzero``。
    每次会话后，消息（无论是明文还是密文）和起始密钥都会从缓冲区中清除。开始新会话前可能需要再次提供密钥。

消息长度
==============

加密后的字符串通常比原始明文字符串更长（取决于加密算法）。

这受加密算法本身、添加到密文前部的初始化向量（IV）以及添加的 HMAC 认证消息的影响。此外，加密消息还会进行 Base64 编码，以便无论使用何种字符集都能安全存储和传输。

选择数据存储机制时请考虑此信息。例如，Cookie 只能容纳 4K 信息。

直接使用加密服务
=====================================

除了（或作为替代）使用 :ref:`usage` 中描述的 ``Services`` 外，还可以直接创建"Encrypter"，或更改现有实例的设置。

.. literalinclude:: encryption/009.php

记住，``$config`` 必须是 ``Config\Encryption`` 类的实例。

***************
类参考
***************

.. php:namespace:: CodeIgniter\Encryption

.. php:class:: Encryption

    .. php:staticmethod:: createKey([$length = 32])

        :param int $length: 输出长度
        :returns: 指定长度的伪随机加密密钥，失败时返回 ``false``
        :rtype:    string

        通过从操作系统源（*即* ``/dev/urandom``）获取随机数据创建加密密钥。

    .. php:method:: initialize([Encryption $config = null])

        :param Config\\Encryption $config: 配置参数
        :returns: ``CodeIgniter\Encryption\EncrypterInterface`` 实例
        :rtype:    ``CodeIgniter\Encryption\EncrypterInterface``
        :throws: ``CodeIgniter\Encryption\Exceptions\EncryptionException``

        初始化（配置）库以使用不同的设置。

        示例：

        .. literalinclude:: encryption/010.php

        详细信息请参见 :ref:`configuration` 部分。

.. php:interface:: CodeIgniter\Encryption\EncrypterInterface

    .. php:method:: encrypt($data[, $params = null])

        :param string $data: 要加密的数据
        :param array|string|null $params: 配置参数（密钥）
        :returns: 加密后的数据
        :rtype:    string
        :throws: ``CodeIgniter\Encryption\Exceptions\EncryptionException``

        加密输入数据并返回密文。

        如果将参数作为第二个参数传递，当 ``$params`` 为数组时，``key`` 元素将用作本次操作的起始密钥；或者可以将起始密钥作为字符串传递。

        如果使用 SodiumHandler 并希望在运行时传递不同的 ``blockSize``，请在 ``$params`` 数组中传递 ``blockSize`` 键。

        示例：

        .. literalinclude:: encryption/011.php

    .. php:method:: decrypt($data[, $params = null])

        :param string $data: 要解密的数据
        :param array|string|null $params: 配置参数（密钥）
        :returns: 解密后的数据
        :rtype:    string
        :throws: ``CodeIgniter\Encryption\Exceptions\EncryptionException``

        解密输入数据并以明文返回。

        如果将参数作为第二个参数传递，当 ``$params`` 为数组时，``key`` 元素将用作本次操作的起始密钥；或者可以将起始密钥作为字符串传递。

        如果使用 SodiumHandler 并希望在运行时传递不同的 ``blockSize``，请在 ``$params`` 数组中传递 ``blockSize`` 键。

        示例：

        .. literalinclude:: encryption/012.php
