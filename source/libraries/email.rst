###########
Email 类
###########

CodeIgniter 强大的 Email 类支持以下功能:

- 多种协议:Mail、Sendmail 和 SMTP
- SMTP 的 TLS 和 SSL 加密
- 多个收件人
- 抄送和密送
- HTML 或纯文本电子邮件
- 附件
- 文字换行
- 优先级
- BCC 批量模式,可将大型邮件列表拆分为多个小的 BCC 批次。
- 电子邮件调试工具

.. contents::
    :local:
    :depth: 3

***********************
使用 Email 库
***********************

发送电子邮件
=============

发送电子邮件不仅很简单,而且你可以即时配置或在 **app/Config/Email.php** 文件中设置首选项。

下面是一个基本示例,演示了如何发送电子邮件:

.. literalinclude:: email/001.php

.. _setting-email-preferences:

设置电子邮件首选项
=========================

有 21 个不同的首选项可用于定制电子邮件消息的发送方式。你可以像这里描述的那样手动设置它们,也可以通过存储在配置文件中的首选项自动设置,如下所述:

通过传递数组设置电子邮件首选项
---------------------------------------------

首选项是通过向电子邮件初始化方法传递首选项值数组来设置的。下面是一个如何设置一些首选项的示例:

.. literalinclude:: email/002.php

.. note:: 如果你不设置它们,大多数首选项都有默认值。

在配置文件中设置电子邮件首选项
------------------------------------------

如果你不喜欢使用上述方法设置首选项,你可以将它们放入配置文件中。只需打开
**app/Config/Email.php** 文件,并在电子邮件属性中设置你的配置。然后保存文件,它将被自动使用。
如果你在配置文件中设置了首选项,将 **不需要** 使用 ``$email->initialize()`` 方法。

.. _email-ssl-tls-for-smtp:

SMTP 协议的 SSL 与 TLS
--------------------------------

为了在与 SMTP 服务器通信时保护用户名、密码和电子邮件内容,应该对通道使用加密。已经广泛部署了两种不同的标准,在尝试排除电子邮件发送问题时,了解这些差异很重要。

当提交电子邮件时,大多数 SMTP 服务器允许在端口 465 或 587 上连接。(原始端口 25 很少使用,因为许多 ISP 有屏蔽规则,而且通信完全是明文的)。

关键差异在于端口 465 要求从一开始就使用 TLS 按照 `RFC 8314 <https://tools.ietf.org/html/rfc8314>`_ 来保护通信通道。而端口 587 上的连接允许明文连接,之后会使用 ``STARTTLS`` SMTP 命令升级通道以使用加密。

端口 465 上的连接是否支持升级可能由服务器决定,所以如果服务器不允许, ``STARTTLS`` SMTP 命令可能会失败。如果你将端口设置为 465,你应该尝试设置 ``SMTPCrypto`` 为空字符串（``''``）,因为通信从一开始就是用 TLS 保护的,不需要 ``STARTTLS``。

如果你的配置要求你连接到端口 587,你最好将 ``SMTPCrypto`` 设置为 ``tls``,因为这将在与 SMTP 服务器通信时实现 ``STARTTLS`` 命令,将明文通道切换为加密通道。初始通信将是明文的,并使用 ``STARTTLS`` 命令将通道升级为 TLS。

检查首选项
---------------------

成功发送的最后使用的设置可以从实例属性 ``$archive`` 获取。这对于测试和调试很有帮助,以确定在 ``send()`` 调用时的实际值。

电子邮件首选项
=================

以下是可以在发送电子邮件时设置的所有首选项列表。

=================== ====================== ============================ =======================================================================
首选项              默认值                 选项                         描述
=================== ====================== ============================ =======================================================================
**userAgent**       CodeIgniter            无                           “用户代理”。
**protocol**        mail                   mail、sendmail 或 smtp       邮件发送协议。
**mailPath**        /usr/sbin/sendmail     无                           到 Sendmail 的服务器路径。
**SMTPHost**        无默认值               无                           SMTP 服务器地址。
**SMTPUser**        无默认值               无                           SMTP 用户名。
**SMTPPass**        无默认值               无                           SMTP 密码。
**SMTPPort**        25                     无                           SMTP 端口。(如果设置为 ``465``,不管 ``SMTPCrypto`` 设置如何,
                                                                        都将使用 TLS 建立连接)
**SMTPTimeout**     5                      无                           SMTP 超时(秒)。
**SMTPKeepAlive**   false                  true 或 false(布尔值)        启用持久 SMTP 连接。
**SMTPCrypto**      tls                    tls, ssl 或空字符串          SMTP 加密。将其设置为 ``ssl`` 将使用 SSL 创建与服务器的安全通道，
                                                                        而 ``tls`` 将向服务器发出 ``STARTTLS`` 命令。
                                                                        在端口 465 上的连接应将其设置为空字符串（``''``）。
                                                                        另请参阅 :ref:`email-ssl-tls-for-smtp`。
**wordWrap**        true                   true 或 false(布尔值)        启用自动换行。
**wrapChars**       76                                                  换行处的字符数。
**mailType**        text                   text 或 html                 邮件类型。如果发送 HTML 电子邮件,你必须将其作为完整的网页发送。
                                                                        确保你没有任何相对链接或相对图像路径,否则它们将无法工作。
**charset**         utf-8                                               字符集(utf-8、iso-8859-1 等)。
**validate**        true                   true 或 false(布尔值)        是否验证电子邮件地址。
**priority**        3                      1、2、3、4、5                电子邮件优先级。1 最高。5 最低。3 为正常。
**CRLF**            \\n                    "\\r\\n" 或 "\\n" 或 "\\r"   换行符。(遵循 RFC 822 使用 "\\r\\n")。
**newline**         \\n                    "\\r\\n" 或 "\\n" 或 "\\r"   换行符。(遵循 RFC 822 使用 "\\r\\n")。
**BCCBatchMode**    false                  true 或 false(布尔值)        启用 BCC 批量模式。
**BCCBatchSize**    200                    无                           每个 BCC 批次中的电子邮件数量。
**DSN**             false                  true 或 false(布尔值)        启用来自服务器的通知消息
=================== ====================== ============================ =======================================================================

覆盖文字换行
========================

如果你启用了文字换行(遵循 RFC 822 的推荐)并且电子邮件中有一个非常长的链接,该链接也可能被换行,导致收件人无法点击。
CodeIgniter 允许你在消息的一部分手动覆盖文字换行,如下所示::

    换行显示正常的电子邮件文本。

    {unwrap}http://example.com/a_long_link_that_should_not_be_wrapped.html{/unwrap}

    更多正常显示换行的文本。

将你不想换行的项放在: {unwrap} {/unwrap} 之间。

***************
类参考
***************

.. php:namespace:: CodeIgniter\Email

.. php:class:: Email

    .. php:method:: setFrom($from[, $name = ''[, $returnPath = null]])

        :param    string    $from: “From” 电子邮件地址
        :param    string    $name: “From” 显示名称
        :param    string    $returnPath: 可选的电子邮件地址,用于重定向未送达的电子邮件
        :returns:    CodeIgniter\\Email\\Email 实例(方法链式调用)
        :rtype:    CodeIgniter\\Email\\Email

        设置发送电子邮件的电子邮件地址和名称:

        .. literalinclude:: email/003.php

        你还可以设置 Return-Path 来帮助重定向未送达的邮件:

        .. literalinclude:: email/004.php

        .. note:: 如果你已将协议配置为 'smtp',则无法使用 Return-Path。

    .. php:method:: setReplyTo($replyto[, $name = ''])

        :param    string    $replyto: 回复电子邮件地址
        :param    string    $name: 回复电子邮件地址的显示名称
        :returns:    CodeIgniter\\Email\\Email 实例(方法链式调用)
        :rtype:    CodeIgniter\\Email\\Email

        设置回复地址。如果没有提供信息,将使用 `setFrom <#setFrom>`_ 方法中的信息。例如:

        .. literalinclude:: email/005.php

    .. php:method:: setTo($to)

        :param    mixed    $to: 逗号分隔的电子邮件地址字符串或电子邮件地址数组
        :returns:    CodeIgniter\\Email\\Email 实例(方法链式调用)
        :rtype:    CodeIgniter\\Email\\Email

        设置收件人的电子邮件地址。可以是单个电子邮件,用逗号分隔的列表或数组:

        .. literalinclude:: email/006.php

        .. literalinclude:: email/007.php

        .. literalinclude:: email/008.php

    .. php:method:: setCC($cc)

        :param    mixed    $cc: 逗号分隔的电子邮件地址字符串或电子邮件地址数组
        :returns:    CodeIgniter\\Email\\Email 实例(方法链式调用)
        :rtype:    CodeIgniter\\Email\\Email

        设置抄送电子邮件地址。就像“to”,可以是单个电子邮件、用逗号分隔的列表或数组。

    .. php:method:: setBCC($bcc[, $limit = ''])

        :param    mixed    $bcc: 逗号分隔的电子邮件地址字符串或电子邮件地址数组
        :param    int    $limit: 每批发送的最大电子邮件数
        :returns:    CodeIgniter\\Email\\Email 实例(方法链式调用)
        :rtype:    CodeIgniter\\Email\\Email

        设置密送电子邮件地址。就像 ``setTo()`` 方法一样,可以是单个电子邮件、用逗号分隔的列表或数组。

        如果设置了 ``$limit``,将启用“批量模式”,它将以不超过指定的 ``$limit`` 为一批发送电子邮件。

    .. php:method:: setSubject($subject)

        :param    string    $subject: 电子邮件主题
        :returns:    CodeIgniter\\Email\\Email 实例(方法链式调用)
        :rtype:    CodeIgniter\\Email\\Email

        设置电子邮件主题:

        .. literalinclude:: email/009.php

    .. php:method:: setMessage($body)

        :param    string    $body: 电子邮件消息体
        :returns:    CodeIgniter\\Email\\Email 实例(方法链式调用)
        :rtype:    CodeIgniter\\Email\\Email

        设置电子邮件消息体:

        .. literalinclude:: email/010.php

    .. php:method:: setAltMessage($str)

        :param    string    $str: 备用电子邮件消息体
        :returns:    CodeIgniter\\Email\\Email 实例(方法链式调用)
        :rtype:    CodeIgniter\\Email\\Email

        设置备用电子邮件消息体:

        .. literalinclude:: email/011.php

        如果你发送 HTML 格式的电子邮件,这是一个可选的消息字符串,可以使用它。它允许你指定一个不含 HTML 格式的备用消息,该消息将添加到头字符串中,供不接受 HTML 电子邮件的人使用。如果你没有设置自己的消息,CodeIgniter 将从你的 HTML 电子邮件中提取消息并剥离标签。

    .. php:method:: setHeader($header, $value)

        :param    string    $header: 标题名称
        :param    string    $value: 标题值
        :returns:    CodeIgniter\\Email\\Email 实例(方法链式调用)
        :rtype: CodeIgniter\\Email\\Email

        追加其他标题到电子邮件:

        .. literalinclude:: email/012.php

    .. php:method:: clear($clearAttachments = false)

        :param    bool    $clearAttachments: 是否清除附件
        :returns:    CodeIgniter\\Email\\Email 实例(方法链式调用)
        :rtype: CodeIgniter\\Email\\Email

        将所有电子邮件变量初始化为空状态。如果你在循环中运行电子邮件发送方法,这种方法很有用,它允许在循环之间重置数据。

        .. literalinclude:: email/013.php

        如果你将参数设置为 true,任何附件也将被清除:

        .. literalinclude:: email/014.php

    .. php:method:: send($autoClear = true)

        :param    bool    $autoClear: 是否自动清除消息数据
        :returns:    成功为 true,失败为 false
        :rtype:    bool

        电子邮件发送方法。根据成功或失败返回布尔值 true 或 false,使其可用于条件语句:

        .. literalinclude:: email/015.php

        如果请求成功,此方法将自动清除所有参数。要停止此行为,请传递 false:

        .. literalinclude:: email/016.php

        .. note:: 为了使用 ``printDebugger()`` 方法,你需要避免清除电子邮件参数。

        .. note:: 如果启用了 ``BCCBatchMode``,收件人多于 ``BCCBatchSize``,此方法将始终返回布尔值 ``true``。

    .. php:method:: attach($filename[, $disposition = ''[, $newname = null[, $mime = '']]])

        :param    string    $filename: 文件名
        :param    string    $disposition: 附件的 'disposition'。大多数电子邮件客户端会忽略这里使用的 MIME 规范并自行决定。https://www.iana.org/assignments/cont-disp/cont-disp.xhtml
        :param    string    $newname: 要在电子邮件中使用的自定义文件名
        :param    string    $mime: 要使用的 MIME 类型(对缓冲数据有用)
        :returns:    CodeIgniter\\Email\\Email 实例(方法链式调用)
        :rtype:    CodeIgniter\\Email\\Email

        启用你发送一个附件。在第一个参数中放置文件路径/名称。对于多个附件,多次使用该方法。例如:

        .. literalinclude:: email/017.php

        要使用默认 disposition(attachment),请将第二个参数留空,否则使用自定义 disposition:

        .. literalinclude:: email/018.php

        你也可以使用 URL:

        .. literalinclude:: email/019.php

        如果你想使用自定义文件名,可以使用第三个参数:

        .. literalinclude:: email/020.php

        如果你需要使用缓冲字符串而不是真实的物理文件,可以使用第一个参数作为缓冲区,第三个参数作为文件名,第四个参数为 MIME 类型:

        .. literalinclude:: email/021.php

    .. php:method:: setAttachmentCID($filename)

        :param    string    $filename: 已存在的附件文件名
        :returns:    附件内容 ID,如果未找到则为 false
        :rtype:    string

        设置并返回附件的内容 ID,这使你可以将内嵌(图片)附件嵌入 HTML 中。第一个参数必须已附加的文件名。

        .. literalinclude:: email/022.php

        .. note:: 为了使内容 ID 在每封电子邮件中都是唯一的,必须对其进行重新创建。

    .. php:method:: printDebugger($include = ['headers', 'subject', 'body'])

        :param    array    $include: 要打印的消息部分
        :returns:    格式化的调试数据
        :rtype:    string

        返回包含任何服务器消息、电子邮件标头和电子邮件消息的字符串。用于调试。

        你可以选择只打印指定的消息部分。有效选项为:**headers**、**subject**、**body**。

        例如:

        .. literalinclude:: email/023.php

        .. note:: 默认情况下,所有原始数据都将被打印。
