#########
加密服务
#########

.. important:: 请勿使任何 *encryption* 库来存储密码！
    密码必须使用 *散列* ，而你应该通过 `PHP的密码散列扩展 <http://php.net/password>`_ 进行散列 。

加密服务提供双向对称（密钥）数据加密。该服务将实例化或初始化 **加密程序** 以适配你的参数，如下所述。

加密处理程序必须兼容CodeIgniter的 ``EncrypterInterface`` 。使用 PHP 密码扩展或其它第三方库可能需要在服务器上安装其他软件，
并且可能需要在 PHP 实例启用。

支持以下拓展：

- `OpenSSL <https://www.php.net/openssl>`_

这并不是一套完整的密码解决方案。如果您需要更多功能（例如公钥加密），建议你考虑直接使用 OpenSSL 或其他 `密码学扩展 <https://www.php.net/manual/en/refs.crypto.php>`_ 。
还有一种更全面的软件包，例如 `Halite <https://github.com/paragonie/halite>`_ （基于libsodium构建的 O-O 软件包）。

.. note:: 自从PHP 7.2起就已弃用了对MCrypt扩展的支持。

.. contents::
  :local:

.. raw:: html

  <div class="custom-index container"></div>

.. _用途:

****************************
使用加密类库
****************************

就像CodeIgniter的其他服务，它可以通过 ``Config/Services`` 来调用： ::

    $encrypter = \Config\Services::encrypter();

如果你已设置了启动密钥（请参阅 :ref:`配置库` ），那么加密和解密数据很简单，将适当的字符串传递给 ``encrypt()`` 或 ``decrypt()`` 方法： ::

	$plainText = 'This is a plain-text message!';
	$ciphertext = $encrypter->encrypt($plainText);

	// 输出: This is a plain-text message!
	echo $encrypter->decrypt($ciphertext);


就是这样！加密库将为加密整个过程提供开箱即用的加密安全性。 你无需担心。

.. _配置库:

配置加密类库
=======================

上面的示例将使用 ``app/Config/Encryption.php`` 中的配置设置。

它只有两个设置选项

======== ===============================================
选项     可能的值
======== ===============================================
key      加密密钥启动器
driver   首选加密程序 (默认为OpenSSL)
======== ===============================================

你可以通过将自己的配置对象传递给 ``Services`` 调用来替换配置文件的设置。
``$config`` 的值必须是 `Config\\Encryption` 类的实例或扩展 `CodeIgniter\\Config\\BaseConfig` 的实例。

::

    $config         = new Config\Encryption();
    $config->key    = 'aBigsecret_ofAtleast32Characters';
    $config->driver = 'OpenSSL';

    $encrypter = \Config\Services::encrypter($config);


默认行为
================

默认情况下，加密库使用 OpenSSL 加密程序。该处理程序使用 AES-256-CTR 算法、你配置的密钥和SHA512 HMAC身份验证进行加密。

配置你的密钥
===============

你的加密密钥的长度 **必须** 在使用的加密算法允许的范围内。比如对于AES-256来说，则为256位或32个字节长。

密钥应该尽可能随机，并且不能是常规文本字符串，也不能是哈希函数的输出等。要创建正确的密钥，可以使用加密库的 ``createKey()`` 方法。

::

	// $key 将被分配一个32字节（256位）随机密钥
	$key = Encryption::createKey(32);

密钥可以存储在 *app/Config/Encryption.php* 中，或者您可以设计自己的存储机制，并在加解密时动态传递密钥。

要将密钥保存到 *app/Config/Encryption.php* ，请打开文件并进行以下设置：::

	public $key = 'YOUR KEY';

对密钥或结果编码
------------------------

你会注意到 ``createKey()`` 方法会输出二进制数据，这是很难解决（即复制粘贴可能会损坏），
所以你可以使用 ``bin2hex()`` 、 ``hex2bin()`` 或编码的 ``Base64`` 处理以更友好的密钥。例如：::

	// 获取一个十六进制形式的密钥
	$encoded = bin2hex(Encryption::createKey(32));

	// 使用 hex2bin() 将相同的值放入配置中，
	// 这样它仍会以二进制形式传递给库配置：
	$key = hex2bin(<your hex-encoded key>);

你可能会发现对加密结果有用的相同技术：::

	// Encrypt some text & make the results text
	// 加密一些文本并生成密文
	$encoded = base64_encode($encrypter->encrypt($plaintext));

加密处理程序说明
===================

OpenSSL 说明
-------------

一直以来， `OpenSSL <https://www.php.net/openssl>`_ 扩展一直是PHP的标配。

CodeIgniter的OpenSSL处理程序使用AES-256-CTR算法。

你的配置提供的 *密钥* 用于派生另外两个密钥，一个用于加密，另一个用于身份验证。
这是通过一种叫做 `基于HMAC的密钥派生函数 <https://en.wikipedia.org/wiki/HKDF>`_
（HKDF）的技术来实现的。

消息长度
===========

加密后的字符串通常长于原始的纯文本字符串（取决于算法）。

这受密码算法本身，加在密码文本之前的初始化向量（IV）以及HMAC身份验证消息的影响。
此外，加密的消息也会经过Base64编码，因此无论使用什么字符集，它都可以安全地存储和传输。

但是选择数据存储机制时，请记住，Cookie只能保存4K信息。

直接使用加密服务
===================

除了使用 :ref:`用途` 中 ``Services`` 那样的方法外，你还可以直接创建“加密器”，或更改现有实例的设置。

::

    // create an Encrypter instance
    // 创建一个加密器实例
    $encryption = new \Encryption\Encryption();

    // reconfigure an instance with different settings
    // 用不同的设置重新配置实例
    $encrypter = $encryption->initialize($config);

请记住， ``$config`` 必须是 `Config\Encryption` 类或扩展 `CodeIgniter\Config\BaseConfig` 类的实例。

***************
类参考
***************

.. php:class:: CodeIgniter\\Encryption\\Encryption

	.. php:staticmethod:: createKey($length)

		:param	int	$length: 输出密钥的长度
		:returns:	具有指定长度的随机密码密钥，创建失败则为FALSE
		:rtype:	string

        通过从操作系统的源（即/dev/urandom）获取随机数据来创建加密密钥。


	.. php:method:: initialize($config)

		:param	BaseConfig	$config: Configuration parameters
		:returns:	CodeIgniter\\Encryption\\EncrypterInterface instance
		:rtype:	CodeIgniter\\Encryption\\EncrypterInterface
		:throws:	CodeIgniter\\Encryption\\EncryptionException

        初始化（或配置）库以使用不同的设置。

		例::

			$encrypter = $encryption->initialize(['cipher' => '3des']);

        请参阅 :ref:`配置库` 部分以获取详细信息。

.. php:interface:: CodeIgniter\\Encryption\\EncrypterInterface

	.. php:method:: encrypt($data, $params = null)

		:param	string	$data: 要加密的数据
		:param		$params: 配置参数（或键）
		:returns:	加密后的数据，加密失败时返回FALSE
		:rtype:	string
		:throws:	CodeIgniter\\Encryption\\EncryptionException

        加密输入数据并返回其密文。

                将配置参数作为第二个参数传递时，如果 ``$params`` 是数组，
                则 ``密钥`` 将用作这次加密的起始键；
                或者也可以把这次加密的密钥作为字符串传递。

		例::

			$ciphertext = $encrypter->encrypt('My secret message');
			$ciphertext = $encrypter->encrypt('My secret message', ['key' => 'New secret key']);
			$ciphertext = $encrypter->encrypt('My secret message', 'New secret key');

	.. php:method:: decrypt($data, $params = null)

		:param	string	$data: 要解密的数据
		:param		$params: 配置参数（或键）
		:returns:	解密后的数据，解密失败时返回FALSE
		:rtype:	string
		:throws:	CodeIgniter\\Encryption\\EncryptionException

        加密输入数据并返回其密文。

                将配置参数作为第二个参数传递时，如果 ``$params`` 是数组，
                则 ``密钥`` 将用作这次解密的起始键；
                或者也可以把这次解密的密钥作为字符串传递。

		例::

			echo $encrypter->decrypt($ciphertext);
			echo $encrypter->decrypt($ciphertext, ['key' => 'New secret key']);
			echo $encrypter->decrypt($ciphertext, 'New secret key');
