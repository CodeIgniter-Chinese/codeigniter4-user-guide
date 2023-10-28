##################
Encryption 服务
##################

.. important:: 不要使用这个或任何其他 *加密* 库来存储密码!密码必须是 *哈希过的* ,你应该通过 PHP 的 `Password Hashing 扩展 <https://www.php.net/password>`_ 来完成。

Encryption 服务提供对称(密钥)数据的双向加密。正如下面所解释的,该服务将实例化和/或初始化一个加密 **处理程序** 以适应你的参数。

Encryption 服务处理程序必须实现 CodeIgniter 的简单 ``EncrypterInterface``。使用适当的 PHP 加密扩展或第三方库可能需要在你的服务器上安装额外的软件和/或需要在你的 PHP 实例中明确启用。

目前支持以下 PHP 扩展:

- `OpenSSL <https://www.php.net/openssl>`_
- `Sodium <https://www.php.net/manual/en/book.sodium>`_

这不是一个完整的加密解决方案。例如,如果你需要更多功能,比如公钥加密,我们建议你考虑直接使用 OpenSSL 或其他 `Cryptography Extensions <https://www.php.net/manual/en/refs.crypto.php>`_。像 `Halite <https://github.com/paragonie/halite>`_ 这样更全面的包(在 libsodium 上构建的面向对象包)也是一个选择。

.. note:: 对 ``MCrypt`` 扩展的支持已经放弃,因为从 PHP 7.2 开始它已被废弃。

.. contents::
    :local:
    :depth: 3

.. _usage:

****************************
使用 Encryption 库
****************************

与 CodeIgniter 中的所有服务一样,它可以通过 ``Config\Services`` 加载:

.. literalinclude:: encryption/001.php

假设你已经设置了起始密钥(参见 :ref:`configuration`),加密和解密数据很简单 - 只需将适当的字符串传递给 ``encrypt()`` 和/或 ``decrypt()`` 方法:

.. literalinclude:: encryption/002.php

就是这样!Encryption 库将自动完成整个过程中所有必要的加密安全性。你不需要担心它。

.. _configuration:

配置库
=======================

上面的示例使用了在 **app/Config/Encryption.php** 中找到的配置设置。

============== ==========================================================================
选项            可能的值(默认值在括号中)
============== ==========================================================================
key            加密密钥起始值
driver         首选处理程序,例如 OpenSSL 或 Sodium (``OpenSSL``)
digest         消息摘要算法 (``SHA512``)
blockSize      [**仅 SodiumHandler**] 填充长度,以字节为单位 (``16``)
cipher         [**仅 OpenSSLHandler**] 要使用的密码 (``AES-256-CTR``)
encryptKeyInfo [**仅 OpenSSLHandler**] 加密密钥信息 (``''``)
authKeyInfo    [**仅 OpenSSLHandler**] 认证密钥信息 (``''``)
rawData        [**仅 OpenSSLHandler**] 密文是否应为原始数据 (``true``)
============== ==========================================================================

你可以通过向 ``Services`` 调用传入自己的配置对象来替换配置文件中的设置。``$config`` 变量必须是 ``Config\Encryption`` 类的一个实例。

.. literalinclude:: encryption/003.php

.. _encryption-compatible-with-ci3:

用于与 CI3 保持兼容性的配置
------------------------------------------------

.. versionadded:: 4.3.0

从 v4.3.0 开始,你可以解密用 CI3 加密的数据。如果你需要解密这样的数据,请使用以下设置来保持兼容性。

.. literalinclude:: encryption/013.php

支持的 HMAC 认证算法
----------------------------------------

对于 HMAC 消息认证,Encryption 库支持使用 SHA-2 系列算法:

=========== ==================== ============================
算法         原始长度(字节)         十六进制编码长度(字节)
=========== ==================== ============================
SHA512      64                   128
SHA384      48                   96
SHA256      32                   64
SHA224      28                   56
=========== ==================== ============================

不包括其他流行算法,例如 MD5 或 SHA1 的原因是它们不再被认为足够安全,因此我们不想鼓励它们的使用。如果你绝对需要使用它们,可以轻松地通过 PHP 的原生 `hash_hmac() <http://php.net/manual/en/function.hash-hmac.php>`_ 函数来实现。

当然,更强大的算法在未来随着它们出现和广泛可用时也会加入。

默认行为
================

默认情况下,Encryption 库使用 OpenSSL 处理程序。该处理程序使用 AES-256-CTR 算法、你配置的 *key* 和 SHA512 HMAC 认证来加密。

设置加密密钥
===========================

你的加密密钥的长度 **必须** 与正在使用的加密算法所允许的一样长。对于 AES-256 来说,那是 32 字节(字符)。

该密钥应该尽可能随机,而且它 **不能** 是一个常规的文本字符串,也不能是散列函数的输出等。要创建一个适当的密钥,你可以使用 Encryption 库的 ``createKey()`` 方法。

.. literalinclude:: encryption/004.php

可以将密钥存储在 **app/Config/Encryption.php** 中,或者你可以设计自己的存储机制,并在加密/解密时动态传递密钥。

要将你的密钥保存到 **app/Config/Encryption.php** 中,打开该文件并设置:

.. literalinclude:: encryption/005.php

编码密钥或结果
------------------------

你会注意到 ``createKey()`` 方法输出二进制数据,这很难处理(即,复制粘贴可能会损坏它),所以你可以使用 ``bin2hex()`` 或 ``base64_encode`` 以更友好的方式处理密钥。例如:

.. literalinclude:: encryption/006.php

对加密结果,你可能也会发现同样的技术很有用:

.. literalinclude:: encryption/007.php

使用前缀存储密钥
------------------------------

在存储加密密钥时,你可以利用两个特殊前缀:``hex2bin:`` 和 ``base64:``。当这些前缀紧接在密钥值之前时, ``Encryption`` 将智能解析密钥,并仍然将二进制字符串传递给库。

.. literalinclude:: encryption/008.php

类似地,你也可以在 **.env** 文件中使用这些前缀!
::

    // 对于 hex2bin
    encryption.key = hex2bin:<your-hex-encoded-key>

    // 或者
    encryption.key = base64:<your-base64-encoded-key>

填充
=======

有时,消息的长度可能会提供大量关于其性质的信息。如果消息之一是“yes”、“no”和“maybe”,则加密消息无济于事:知道长度就足够知道消息是什么。

填充是一种通过使长度成为给定块大小的倍数来缓解这种情况的技术。

填充是在 ``SodiumHandler`` 中使用 libsodium 的原生 ``sodium_pad`` 和 ``sodium_unpad`` 函数实现的。这需要在加密之前向纯文本消息添加填充长度(以字节为单位),并在解密后删除它。填充通过 ``Config\Encryption`` 的 ``$blockSize`` 属性进行配置。该值应大于零。

.. important:: 建议你不要设计自己的填充实现。你必须始终使用库的更安全实现。另外,密码不应进行填充。使用填充来隐藏密码的长度是不推荐的。愿意向服务器发送密码的客户端应该对其进行散列(即使只对散列函数进行一次迭代)。这可以确保传输数据的长度是常量的,并且服务器不会轻易获得密码的副本。

加密处理程序注意事项
========================

OpenSSL 说明
-------------

`OpenSSL <https://www.php.net/openssl>`_ 扩展在 PHP 中已经存在很长时间了。

CodeIgniter 的 OpenSSL 处理程序使用 AES-256-CTR 密码。

配置中提供的 *key* 用于生成另外两个密钥,一个用于加密,一个用于认证。这是通过称为 `HMAC 键导出函数 <https://en.wikipedia.org/wiki/HKDF>`_ (HKDF)的技术实现的。

Sodium 说明
------------

`Sodium <https://www.php.net/manual/en/book.sodium>`_ 扩展默认打包在 PHP 7.2.0 及更高版本中。

Sodium 在端到端方案中发送秘密消息时使用 XSalsa20 加密、Poly1305 进行 MAC 和 XS25519 进行密钥交换。要使用共享密钥(例如对称加密)对字符串进行加密和/或认证,Sodium 使用 XSalsa20 算法进行加密和 HMAC-SHA512 进行认证。

.. note:: CodeIgniter 的 ``SodiumHandler`` 在每次加密或解密会话中都使用 ``sodium_memzero``。在每个会话之后,无论是纯文本还是密文,启动密钥都会从缓冲区中清除。在启动新会话之前,你可能需要再次提供密钥。

消息长度
==============

加密后的字符串通常比原始的纯文本字符串长(取决于密码)。

这受密码算法本身的影响,前缀为密文的初始化向量(IV),以及也前缀的 HMAC 认证消息。此外,加密消息也进行了 Base64 编码,以便无论使用的字符集如何,都可以安全地存储和传输。

在选择数据存储机制时,请记住这一信息。例如,Cookie 只能容纳 4K 的信息。

直接使用加密服务
=====================================

除了如 :ref:`usage` 所述通过 ``Services`` 使用之外,你还可以直接创建一个“Encrypter”,或更改现有实例的设置。

.. literalinclude:: encryption/009.php

记住, ``$config`` 必须是 ``Config\Encryption`` 类的一个实例。

***************
类参考
***************

.. php:namespace:: CodeIgniter\Encryption

.. php:class:: Encryption

    .. php:staticmethod:: createKey([$length = 32])

        :param int $length: 输出长度
        :returns: 具有指定长度的伪随机加密密钥,如果失败则为 ``false``
        :rtype:    string

        通过从操作系统的来源(即 ``/dev/urandom``)获取随机数据来创建加密密钥。

    .. php:method:: initialize([Encryption $config = null])

        :param Config\\Encryption $config: 配置参数
        :returns: ``CodeIgniter\Encryption\EncrypterInterface`` 实例
        :rtype:    ``CodeIgniter\Encryption\EncrypterInterface``
        :throws: ``CodeIgniter\Encryption\Exceptions\EncryptionException``

        使用不同的设置初始化(配置)库。

        示例:

        .. literalinclude:: encryption/010.php

        详细信息请参阅 :ref:`configuration` 部分。

.. php:interface:: CodeIgniter\Encryption\EncrypterInterface

    .. php:method:: encrypt($data[, $params = null])

        :param string $data: 要加密的数据
        :param array|string|null $params: 配置参数(密钥)
        :returns: 加密数据
        :rtype:    string
        :throws: ``CodeIgniter\Encryption\Exceptions\EncryptionException``

        加密输入数据并返回其密文。

        如果你在第二个参数中传入参数,则如果 ``$params`` 为数组, ``key`` 元素将用作此操作的起始密钥;或者可以作为字符串传入起始密钥。

        如果你使用 SodiumHandler 并希望在运行时传递不同的 ``blockSize``,请在 ``$params`` 数组中传递 ``blockSize`` 键。

        示例:

        .. literalinclude:: encryption/011.php

    .. php:method:: decrypt($data[, $params = null])

        :param string $data: 要解密的数据
        :param array|string|null $params: 配置参数(密钥)
        :returns: 解密数据
        :rtype:    string
        :throws: ``CodeIgniter\Encryption\Exceptions\EncryptionException``

        解密输入数据并返回纯文本。

        如果你在第二个参数中传入参数,则如果 ``$params`` 为数组, ``key`` 元素将用作此操作的起始密钥;或者可以作为字符串传入起始密钥。

        如果你使用 SodiumHandler 并希望在运行时传递不同的 ``blockSize``,请在 ``$params`` 数组中传递 ``blockSize`` 键。

        示例:

        .. literalinclude:: encryption/012.php
