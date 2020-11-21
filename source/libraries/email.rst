###########
Email 类
###########

Codeigniter 的健全的 Email 类支持下面的特征:

- 多样的协议: Mail，Sendmail，以及 SMTP（简单邮件传送协议）
- SMTP TLS 和 SSL 加密
- 多接收方
- CC（抄送）和暗送（BCCs）
- HTML 或文本邮件
- 附件
- 文字换行
- 优先权
- BCC Batch Mode, enabling large email lists to be broken into small BCC batches.
- Email 调试工具


.. contents::
    :local:
    :depth: 2

.. raw:: html

  <div class="custom-index container"></div>

***********************
使用 Email 类库
***********************


发送邮件
=============

发送邮件不仅是简单的，而是你要赶紧配置它，或者在 **app/Config/Email.php** 文件里设定你的优先选项。

下面的基础示例展示你要如何发送电子邮件::


	$email = \Config\Services::email();

	$email->setFrom('your@example.com', 'Your Name');
	$email->setTo('someone@example.com');
	$email->setCC('another@another-example.com');
	$email->setBCC('them@their-example.com');

	$email->setSubject('Email Test');
	$email->setMessage('Testing the email class.');

	$email->send();


设定邮件偏好
=========================

有 21 个不同可用的偏好去修改你已经发送的邮件消息。你也能像这里描述过般自动地设定他们，或者自动地在你的配置文件里通过偏好储存，描述如下:

通过偏好数组值到邮件初始化方法的偏好已设置。下面的例子里是你或许已经设定的一些偏好::


	$config['protocol'] = 'sendmail';
	$config['mailPath'] = '/usr/sbin/sendmail';
	$config['charset']  = 'iso-8859-1';
	$config['wordWrap'] = true;

	$email->initialize($config);


.. note:: 如果你没有设置他们大多数的偏好，则默认值将会被使用。



在配置文件里设置邮件偏好
------------------------------------------

如果你不喜欢使用上面的方法设置偏好，你能更换他们放到设置文件里。
简单地打开 **app/Config/Email.php** 文件，并且在你的邮件属性里设定你的配置。
然后保存文件，接着配置会被自动地使用。

如果你在配置文件里设置你的偏好，你不需要使用 ``$email->initialize()`` 方法。



邮件偏好
=================

下面是所有偏好列表，当发送邮件时它们可能被设定了。


=================== ====================== ============================ =======================================================================
Preference/偏好      Default Value/默认值   Options/选项                  Description/描述
=================== ====================== ============================ =======================================================================
**userAgent**       CodeIgniter            None                         用户代理人
**protocol**        mail                   mail, sendmail, or smtp      邮件发送协议
**mailpath**        /usr/sbin/sendmail     None                         发送邮件服务器路径
**SMTPHost**        No Default             None                         SMTP 服务器地址
**SMTPUser**        No Default             None                         SMTP 用户名
**SMTPPass**        No Default             None                         SMTP 密码
**SMTPPort**        25                     None                         SMTP 端口
**SMTPTimeout**     5                      None                         SMTP 超时（几秒时间）
**SMTPKeepAlive**   FALSE                  TRUE or FALSE (boolean)      坚持授权 SMTP 连接
**SMTPCrypto**      No Default             tls or ssl                   SMTP 加密
**wordWrap**        TRUE                   TRUE or FALSE (boolean)      授权自动换行
**wrapChars**       76                                                  换行字符数
**mailType**        text                   text or html                 邮件类型。如果你发送 HTML 邮件你必须发送完整 web 页面。
                                                                        确保你没有任何有关系的链接或者有关系的图片地址否则他们将不 工作。                                                                          
**charset**         utf-8                                               字符设定(utf-8, iso-8859-1, etc.)
**validate**        TRUE                   TRUE or FALSE (boolean)      是否邮件地址会生效
**priority**        3                      1, 2, 3, 4, 5                邮件优先权 1 = 最高. 5 = 最低. 3 = 普通.
**CRLF**            \\n                    "\\r\\n" or "\\n" or "\\r"   新行字符 (遵循 RFC 822 使用 "\\r\\n" )
**newline**         \\n                    "\\r\\n" or "\\n" or "\\r"   新行字符 (遵循 RFC 822 使用 "\\r\\n" )
**BCCBatchMode**    FALSE                  TRUE or FALSE (boolean)      授权 BCC 批处理模式
**BCCBatchSize**    200                    None                         在每一个 BCC 批处理内的邮件数目
**DSN**             FALSE                  TRUE or FALSE (boolean)      从服务器授权通告消息
=================== ====================== ============================ =======================================================================


撤销语句换行
========================

如果你有语句换行授权（推荐遵守 RFC822 ）并且在你的电子邮件里有非常长的连接，它也能换行，由于某人接收而导致连接变成不可点击。
Codeigniter 让你自动地撤销你的消息的部分文字换行像下面一样::

	你的邮件的文本会正常地换行

	{unwrap}http://example.com/a_long_link_that_should_not_be_wrapped.html{/unwrap}

	
	更多文本将会被正常地换行。


在 : {unwrap} {/unwrap} 之间放置你不想字段跨行的菜单项。


***************
类参考
***************

.. php:class:: CodeIgniter\\Email\\Email

	.. php:method:: setFrom($from[, $name = ''[, $returnPath = null]])

		:param	string	$from: "From" 电子邮件地址
		:param	string	$name: "From" 显示名字
		:param	string	$returnPath: 可选择的邮件地址到重定向未送达的电子邮件 
		:returns:	CodeIgniter\\Email(电子邮件)\\Email instance[电子邮件接口(锚链方法)]
		:rtype:	CodeIgniter\\Email\\Email

                设定发送电子邮件的邮件地址和某人的名字::

			$email->setFrom('you@example.com', 'Your Name');

                你也能设定返回路径，去帮助重定向未送达的电子邮件::

			$email->setFrom('you@example.com', 'Your Name', 'returned_emails@example.com');

                           
		.. note:: 如果你已经设置 'smtp' 作为你的协议，则返回路径不能使用。
		

	.. php:method:: setReplyTo($replyto[, $name = ''])

		:param	string	$replyto: 用于回复的电子邮件地址
		:param	string	$name: 对回复电子邮件地址显示名称
		:returns:	CodeIgniter\\Email(电子邮件)\\Email instance[电子邮件接口(锚链方法)]
		:rtype:	CodeIgniter\\Email\\Email
                
		设定答复地址。如果不提供信息，信息在 `setFrom <#setFrom>`_  方法里已被使用。例如::

			$email->setReplyTo('you@example.com', 'Your Name');

	.. php:method:: setTo($to)

		:param	mixed	$to: 逗号分隔字符串或者电子邮件地址数组
		:returns:	CodeIgniter\\Email(电子邮件)\\Email instance[电子邮件接口(锚链方法)]
		:rtype:	CodeIgniter\\Email\\Email
                
		设定接收器的电子邮件地址。可以是单独的电子邮件，逗号分隔列表或者数组::

			$email->setTo('someone@example.com');

		::

			$email->setTo('one@example.com, two@example.com, three@example.com');

		::

			$email->setTo(['one@example.com', 'two@example.com', 'three@example.com']);

	.. php:method:: setCC($cc)

		:param	mixed	$cc: 逗号分隔字符串或者电子邮件地址数组
		:returns:	CodeIgniter\\Email(电子邮件)\\Email instance[电子邮件接口(锚链方法)]
		:rtype:	CodeIgniter\\Email\\Email
                
		设定抄送电子邮件地址。就像 "to" ，可以是单独的电子邮件，逗号分隔列表或者数组。

	.. php:method:: setBCC($bcc[, $limit = ''])

		:param	mixed	$bcc: 逗号分隔字符串或者电子邮件地址的数组
		:param	int	$limit: 电子邮件的最大数目发送到每个批处理
		:returns:	CodeIgniter\\Email(电子邮件)\\Email instance[电子邮件接口(锚链方法)]
		:rtype:	CodeIgniter\\Email\\Email

                设定密件抄送邮件地址。就像 ``setTo()`` 方法，可以是单独的电子邮件，逗号分隔列表或者数组。
                如果 ``$limit`` 已经设定，"batch mode" 是可授权的，"batch mode" 将发送邮件到批处理，每一个批处理不会超过具体指定的 ``$limit``。
		

	.. php:method:: setSubject($subject)

		:param	string	$subject: 电子邮件主题行
		:returns:	CodeIgniter\\Email(电子邮件)\\Email instance[电子邮件接口(锚链方法)]
		:rtype:	CodeIgniter\\Email\\Email

		设定电子邮件主题::

			$email->setSubject('This is my subject');

	.. php:method:: setMessage($body)

		:param	string	$body: 电子邮件信息正文
		:returns:	CodeIgniter\\Email(电子邮件)\\Email instance[电子邮件接口(锚链方法)]
		:rtype:	CodeIgniter\\Email\\Email

		设定电子邮件信息正文::
		

			$email->setMessage('This is my message');

	.. php:method:: setAltMessage($str)

		:param	string	$str: 替代电子邮件信息正文
		:returns:	CodeIgniter\\Email(电子邮件)\\Email instance[电子邮件接口(锚链方法)]
		:rtype:	CodeIgniter\\Email\\Email

		设定替代电子邮件信息正文::
		

			$email->setAltMessage('This is the alternative message');

                如果你发送 HTML 格式的电子邮件，一个可选择的消息字符串会被使用。
		它让你具体指定一个带非 HTML 格式的替代消息，该消息针对不接受 HTML 电子邮件的人来讲会被添加到标题字符串。
		如果你不设定你自己的消息，CodeIgniter 将会从你的 HTML 电子邮件里摘取消息并去掉标签。


	.. php:method:: setHeader($header, $value)

		:param	string	$header: 标题名称
		:param	string	$value: 标题值
		:returns:	CodeIgniter\\Email(电子邮件)\\Email instance[电子邮件接口(锚链方法)]
		:rtype: CodeIgniter\\Email\\Email

		附加额外的标题到电子邮件::

			$email->setHeader('Header1', 'Value1');
			$email->setHeader('Header2', 'Value2');

	.. php:method:: clear($clearAttachments = false)

		:param	bool	$clearAttachments: 是否或者不去清理附件
		:returns:	CodeIgniter\\Email(电子邮件)\\Email instance[电子邮件接口(锚链方法)]
		:rtype: CodeIgniter\\Email\\Email

                初始化所有的电子邮件变量到空值状态。
		如果你在一个循环里运行电子邮件发送方法，对于使用来说这个方法是故意的，在循环周期之间容许数据被重置。
		::

			foreach ($list as $name => $address)
			{
				$email->clear();

				$email->setTo($address);
				$email->setFrom('your@example.com');
				$email->setSubject('Here is your info '.$name);
				$email->setMessage('Hi ' . $name . ' Here is the info you requested.');
				$email->send();
			}

                        如果你设定参数为 TRUE，任何附件会被清理::

			$email->clear(true);

	.. php:method:: send($autoClear = true)

		:param	bool	$autoClear: 是否自动地清理消息数据
		:returns:	成功为 TRUE，失败为 FALSE
		:rtype:	bool
		
		
                电子邮件发送方法。基于成功或者失败返回布尔值为 TRUE 或者 FALSE ，授予它被附有条件地使用::

			if (! $email->send())
			{
				// 导致错误
			}

                如果请求是成功的，这个方法将会自动地清理所有的参数。通过 FALSE 去阻止这个行为::

			if ($email->send(false))
			{
				// 参数将不会被清理
			}



		.. note:: 为了使用 ``printDebugger()`` 方法，你需要避免清理电子邮件参数。

		.. note:: 如果 ``BCCBatchMode`` 是可授予的，并且有更多的 ``BCCBatchSize`` 收件人，这个方法常返回布尔值 ``TRUE`` 。
		

	.. php:method:: attach($filename[, $disposition = ''[, $newname = null[, $mime = '']]])

		:param	string	$filename: 文件名
		:param	string	$disposition: 附件的 'disposition' 。不管怎样大多数电子邮件客户端制定了他们自己的不加理会的 MIME 规格书的决策并使用在这里。                                                                             https://www.iana.org/assignments/cont-disp/cont-disp.xhtml
		:param	string	$newname: 在邮件里使用的定制文件名
		:param	string	$mime: MIME 类型要使用（对缓冲数据有帮助） 
		:returns:	CodeIgniter\\Email(电子邮件)\\Email instance[电子邮件接口(锚链方法)]
		:rtype:	CodeIgniter\\Email\\Email

		授权你去发送附件。在第一参数里放置文件路径（path）/名称（name）。对于多个附件使用多次方法。事例::

			$email->attach('/path/to/photo1.jpg');
			$email->attach('/path/to/photo2.jpg');
			$email->attach('/path/to/photo3.jpg');

                去使用默认处置（附件），让第二参数处在空格状态，否则使用订制的安排::

			$email->attach('image.jpg', 'inline');

		你也能使用URL::

			$email->attach('http://example.com/filename.pdf');

		如果你想要是用定制的文件名称，你要使用第三参数::
	

			$email->attach('filename.pdf', 'attachment', 'report.pdf');

                如果你需要使用缓冲型字符串替代真实 - physical - （物理）文件，你要是用第一参数做缓冲类型，第三参数作为文件名并且第四参数作为 mime 类型::


			$email->attach($buffer, 'attachment', 'report.pdf', 'application/pdf');

	.. php:method:: setAttachmentCID($filename)

		:param	string	$filename: 现存的附件文件名
		:returns:	附件内容标识符，或者，如果找不到为 FALSE
		:rtype:	string

                设定并且返回附件的内容标识符，任何授权你的，在线的（图片）嵌入附件到 HTML。第一参数必须是早已附加的文件名。

		::

			$filename = '/img/photo1.jpg';
			$email->attach($filename);
			foreach ($list as $address)
			{
				$email->setTo($address);
				$cid = $email->setAttachmentCID($filename);
				$email->setMessage('<img src="cid:'. $cid .'" alt="photo1" />');
				$email->send();
			}


		.. note:: 对每个电子邮件内容标识符必须重建为独一无二的形式。

	.. php:method:: printDebugger($include = ['headers', 'subject', 'body'])

		:param	array	$include:  消息的部分要打印输出
		:returns:	格式化调试数据
		:rtype:	string

                返回包含任何服务器消息，电子邮件标题，以及电子邮件消息的字符串。对调试有帮助。

               你能自动地具体指定应该被答应的消息部分。有效的选项是: **headers**, **subject**, **body**。


		事例::

			// 为了邮件数据当发送时你需要通过 FALSE 
			// 如发生了，不会被清理，printDebugger() 将出现 
			// 不输出任何字符
			$email->send(false);

			// 将仅仅打印电子邮件标题，包括消息主题和正文
			$email->printDebugger(['headers']);

		.. note:: 默认情况下，所有的未加工的数据将会被打印。
