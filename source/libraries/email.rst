###########
Email 类
###########

CodeIgniter 强大的 Email 类支持以下功能：

-  多种协议：Mail、Sendmail 和 SMTP
-  SMTP 的 TLS 和 SSL 加密
-  多个收件人
-  抄送（CC）和密送（BCC）
-  HTML 或纯文本邮件
-  附件
-  自动换行
-  邮件优先级
-  BCC 批处理模式，可将大型邮件列表分割为小型 BCC 批次
-  邮件调试工具

.. contents::
    :local:
    :depth: 3

***********************
使用 Email 类
***********************

发送邮件
=============

发送邮件不仅简单，还可即时配置或在 **app/Config/Email.php** 文件中设置首选项。

以下是一个发送邮件的基本示例：

.. literalinclude:: email/001.php

.. _setting-email-preferences:

设置邮件首选项
=========================

有 22 种不同的首选项可用于定制邮件发送方式。既可手动设置（如本节所述），也可通过配置文件中存储的首选项自动设置（详见 `邮件首选项`_）。

通过传递数组设置邮件首选项
---------------------------------------------

通过向邮件初始化方法传递数组来设置首选项。以下是设置部分首选项的示例：

.. literalinclude:: email/002.php

.. note:: 大多数首选项都有默认值，未设置时将自动使用。

在配置文件中设置邮件首选项
------------------------------------------

如不希望使用上述方法设置首选项，可将其放入配置文件。只需打开 **app/Config/Email.php** 文件，在 Email 属性中设置配置项，然后保存文件即可自动使用。在配置文件中设置首选项后，无需使用 ``$email->initialize()`` 方法。

.. _email-ssl-tls-for-smtp:

SMTP 协议的 SSL 与 TLS
--------------------------------

为保护与 SMTP 服务器通信时的用户名、密码和邮件内容，应使用通道加密。两种不同的标准已被广泛部署，排查邮件发送问题时理解其差异非常重要。

大多数 SMTP 服务器允许通过 465 或 587 端口连接发送邮件。（原始 25 端口已很少使用，因为许多 ISP 设置了阻止规则，且通信完全为明文）。

关键区别在于，根据 `RFC 8314 <https://tools.ietf.org/html/rfc8314>`_，465 端口要求通信通道从一开始就使用 TLS 加密。而 587 端口连接允许明文通信，后续通过 ``STARTTLS`` SMTP 命令升级通道以使用加密。

465 端口的连接升级可能受服务器支持也可能不受支持，若服务器不允许，``STARTTLS`` SMTP 命令可能会失败。若将端口设置为 465，应尝试将 ``SMTPCrypto`` 设置为空字符串（``''``），因为通信从一开始就使用 TLS 加密，无需 ``STARTTLS``。

若配置要求连接到 587 端口，很可能应将 ``SMTPCrypto`` 设置为 ``tls``，因为这将在与 SMTP 服务器通信时执行 ``STARTTLS`` 命令，从明文切换到加密通道。初始通信为明文，随后通过 ``STARTTLS`` 命令将通道升级为 TLS。

查看首选项
---------------------

上次成功发送使用的设置可从实例属性 ``$archive`` 获取。这有助于测试和调试，以确定 ``send()`` 调用时的实际值。

.. _email-preferences:

邮件首选项
=================

以下是发送邮件时可设置的所有首选项列表。

=================== =================== ============================ =======================================================================
首选项              默认值              选项                         说明
=================== =================== ============================ =======================================================================
**fromEmail**                                                        要在"from"标头中设置的邮件地址。
**fromName**                                                         要在"from"标头中设置的名称。
**userAgent**       CodeIgniter                                      "用户代理"。
**protocol**        mail                ``mail``、``sendmail``、     邮件发送协议。
                                        或 ``smtp``
**mailPath**        /usr/sbin/sendmail                               Sendmail 的服务器路径。
**SMTPHost**                                                         SMTP 服务器主机名。
**SMTPAuthMethod**  login               ``login``、``plain``         SMTP 身份验证方式。（自 4.7.0 版本起可用）
**SMTPUser**                                                         SMTP 用户名。
**SMTPPass**                                                         SMTP 密码。
**SMTPPort**        25                                               SMTP 端口。（若设置为 ``465``，无论 ``SMTPCrypto`` 设置如何，
                                                                     都将使用 TLS 连接。）
**SMTPTimeout**     5                                                SMTP 超时时间（秒）。
**SMTPKeepAlive**   false               ``true``/``false``           启用持久 SMTP 连接。
**SMTPCrypto**      tls                 ``tls``、``ssl``、或         SMTP 加密。设置为 ``ssl`` 将使用 SSL 创建到服务器的安全通道；
                                                                     设置为 ``tls`` 将向服务器发出
                                        空字符串（``''``）           ``STARTTLS`` 命令。465 端口的连接应将此设置为空字符串（``''``）。
                                                                     另请参阅 :ref:`email-ssl-tls-for-smtp`。
**wordWrap**        true                ``true``/``false``           启用自动换行。
**wrapChars**       76                                               换行的字符数。
**mailType**        text                ``text`` 或 ``html``         邮件类型。若发送 HTML 邮件，必须将其作为完整网页发送。
                                                                     确保没有相对链接或相对图片路径，否则将无法正常工作。
**charset**         UTF-8                                            字符集（``utf-8``、``iso-8859-1`` 等）。
**validate**        true                ``true``/``false``           是否验证邮件地址。
**priority**        3                   1、2、3、4、5                邮件优先级。``1`` = 最高。``5`` = 最低。``3`` = 正常。
**CRLF**            \\r\\n              ``\r\n``、``\n`` 或 ``\r``   换行字符。（使用 ``\r\n`` 以符合 RFC 822）。
**newline**         \\r\\n              ``\r\n``、``\n`` 或 ``\r``   换行字符。（使用 ``\r\n`` 以符合 RFC 822）。
**BCCBatchMode**    false               ``true``/``false``           启用 BCC 批处理模式。
**BCCBatchSize**    200                                              每个 BCC 批次中的邮件数量。
**DSN**             false               ``true``/``false``           启用服务器通知消息。
=================== =================== ============================ =======================================================================

覆盖自动换行
========================

若启用了自动换行（建议遵循 RFC 822），且邮件中有很长的链接，它可能会被换行，导致收件人无法点击。CodeIgniter 允许在邮件内容的部分区域手动覆盖自动换行，如下所示::

    邮件文本中
    正常换行的部分。

    {unwrap}http://example.com/a_long_link_that_should_not_be_wrapped.html{/unwrap}

    更多将正常
    换行的文本。

将不希望被自动换行的项目放置在：{unwrap} {/unwrap} 之间。

***************
类参考
***************

.. php:namespace:: CodeIgniter\Email

.. php:class:: Email

    .. php:method:: setFrom($from[, $name = ''[, $returnPath = null]])

        :param    string    $from: "From" 邮件地址
        :param    string    $name: "From" 显示名称
        :param    string    $returnPath: 用于重定向未送达邮件的可选邮件地址
        :returns:    CodeIgniter\\Email\\Email 实例（方法链式调用）
        :rtype:    CodeIgniter\\Email\\Email

        设置发件人的邮件地址和名称：

        .. literalinclude:: email/003.php

        还可设置 Return-Path 以帮助重定向未送达的邮件：

        .. literalinclude:: email/004.php

        .. note:: 若将协议配置为 'smtp'，则无法使用 Return-Path。

    .. php:method:: setReplyTo($replyto[, $name = ''])

        :param    string    $replyto: 回复邮件地址
        :param    string    $name: 回复邮件地址的显示名称
        :returns:    CodeIgniter\\Email\\Email 实例（方法链式调用）
        :rtype:    CodeIgniter\\Email\\Email

        设置回复地址。若未提供信息，则使用 `setFrom <#setFrom>`_ 方法中的信息。示例：

        .. literalinclude:: email/005.php

    .. php:method:: setTo($to)

        :param    mixed    $to: 逗号分隔的字符串或邮件地址数组
        :returns:    CodeIgniter\\Email\\Email 实例（方法链调用）
        :rtype:    CodeIgniter\\Email\\Email

        设置收件人的邮件地址。可以是单个邮件、逗号分隔列表或数组：

        .. literalinclude:: email/006.php

        .. literalinclude:: email/007.php

        .. literalinclude:: email/008.php

    .. php:method:: setCC($cc)

        :param    mixed    $cc: 逗号分隔的字符串或邮件地址数组
        :returns:    CodeIgniter\\Email\\Email 实例（方法链调用）
        :rtype:    CodeIgniter\\Email\\Email

        设置抄送（CC）邮件地址。与 "to" 相同，可以是单个邮件、逗号分隔列表或数组。

    .. php:method:: setBCC($bcc[, $limit = ''])

        :param    mixed    $bcc: 逗号分隔的字符串或邮件地址数组
        :param    int    $limit: 每批次发送的最大邮件数量
        :returns:    CodeIgniter\\Email\\Email 实例（方法链调用）
        :rtype:    CodeIgniter\\Email\\Email

        设置密送（BCC）邮件地址。与 ``setTo()`` 方法相同，可以是单个邮件、逗号分隔列表或数组。

        若设置了 ``$limit``，将启用"批处理模式"，邮件将分批发送，每批不超过指定的 ``$limit``。

    .. php:method:: setSubject($subject)

        :param    string    $subject: 邮件主题
        :returns:    CodeIgniter\\Email\\Email 实例（方法链调用）
        :rtype:    CodeIgniter\\Email\\Email

        设置邮件主题：

        .. literalinclude:: email/009.php

    .. php:method:: setMessage($body)

        :param    string    $body: 邮件消息正文
        :returns:    CodeIgniter\\Email\\Email 实例（方法链调用）
        :rtype:    CodeIgniter\\Email\\Email

        设置邮件消息正文：

        .. literalinclude:: email/010.php

    .. php:method:: setAltMessage($str)

        :param    string    $str: 备选邮件消息正文
        :returns:    CodeIgniter\\Email\\Email 实例（方法链调用）
        :rtype:    CodeIgniter\\Email\\Email

        设置备选邮件消息正文：

        .. literalinclude:: email/011.php

        这是可选的消息字符串，用于发送 HTML 格式邮件时指定无 HTML 格式的备选消息，添加到标头字符串中供不接受 HTML 邮件的人使用。若未设置自己的消息，CodeIgniter 将从 HTML 邮件中提取消息并去除标签。

    .. php:method:: setHeader($header, $value)

        :param    string    $header: 标头名称
        :param    string    $value: 标头值
        :returns:    CodeIgniter\\Email\\Email 实例（方法链调用）
        :rtype: CodeIgniter\\Email\\Email

        向邮件追加额外标头：

        .. literalinclude:: email/012.php

    .. php:method:: clear($clearAttachments = false)

        :param    bool    $clearAttachments: 是否清除附件
        :returns:    CodeIgniter\\Email\\Email 实例（方法链调用）
        :rtype: CodeIgniter\\Email\\Email

        将所有邮件变量初始化为空状态。此方法用于在循环中运行邮件发送方法时，允许在每个周期之间重置数据。

        .. literalinclude:: email/013.php

        若将参数设置为 true，附件也将被清除：

        .. literalinclude:: email/014.php

    .. php:method:: send($autoClear = true)

        :param    bool    $autoClear: 是否自动清除消息数据
        :returns:    成功返回 true，失败返回 false
        :rtype:    bool

        邮件发送方法。根据成功或失败返回布尔值 true 或 false，可用于条件判断：

        .. literalinclude:: email/015.php

        若请求成功，此方法将自动清除所有参数。要阻止此行为，请传递 false：

        .. literalinclude:: email/016.php

        .. note:: 为使用 ``printDebugger()`` 方法，需要避免清除邮件参数。

        .. note:: 若启用 ``BCCBatchMode``，且收件人数量超过 ``BCCBatchSize``，此方法将始终返回布尔值 ``true``。

    .. php:method:: attach($filename[, $disposition = ''[, $newname = null[, $mime = '']]])

        :param    string    $filename: 文件名
        :param    string    $disposition: 附件的 'disposition'。大多数邮件客户端会无视此处使用的 MIME 规范自行决定。https://www.iana.org/assignments/cont-disp/cont-disp.xhtml
        :param    string    $newname: 邮件中使用的自定义文件名
        :param    string    $mime: 使用的 MIME 类型（对缓冲数据有用）
        :returns:    CodeIgniter\\Email\\Email 实例（方法链调用）
        :rtype:    CodeIgniter\\Email\\Email

        用于发送附件。将文件路径/名称放在第一个参数中。要附加多个附件，多次使用此方法。例如：

        .. literalinclude:: email/017.php

        要使用默认的 disposition（附件），将第二个参数留空，否则使用自定义 disposition：

        .. literalinclude:: email/018.php

        也可使用 URL：

        .. literalinclude:: email/019.php

        若想使用自定义文件名，可使用第三个参数：

        .. literalinclude:: email/020.php

        若需要使用缓冲字符串而非真实的物理文件，可将第一个参数用作缓冲，第三个参数用作文件名，第四个参数用作 MIME 类型：

        .. literalinclude:: email/021.php

    .. php:method:: setAttachmentCID($filename)

        :param    string    $filename: 现有附件文件名
        :returns:    附件的 Content-ID，若未找到则返回 false
        :rtype:    string

        设置并返回附件的 Content-ID，用于将内联（图片）附件嵌入 HTML。第一个参数必须是已附加的文件名。

        .. literalinclude:: email/022.php

        .. note:: 每封邮件的 Content-ID 必须重新创建以确保唯一性。

    .. php:method:: printDebugger($include = ['headers', 'subject', 'body'])

        :param    array    $include: 要打印的消息部分
        :returns:    格式化的调试数据
        :rtype:    string

        返回包含任何服务器消息、邮件标头和邮件消息的字符串。对调试很有用。

        可选择指定应打印消息的哪些部分。有效选项为：**headers**、**subject**、**body**。

        示例：

        .. literalinclude:: email/023.php

        .. note:: 默认情况下，将打印所有原始数据。
