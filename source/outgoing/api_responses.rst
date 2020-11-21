##################
API 响应特性
##################

现代化的 PHP开发都需要构建 API ，不管它只是为了给 javascript 单页应用提供数据还是作为独立的产品。CodeIgniter 提供了一个API响应特性，可用于任何控制器，使公共响应类型简单，无需记住它的 HTTP 状态代码应返回的响应类型。

.. contents::
    :local:
    :depth: 2

*************
使用示例
*************

下面的示例显示了控制器中常见的使用模式。

::

    <?php namespace App\Controllers;

    class Users extends \CodeIgniter\Controller
    {
        use CodeIgniter\API\ResponseTrait;

        public function createUser()
        {
            $model = new UserModel();
            $user = $model->save($this->request->getPost());

            // 响应 201 状态码
            return $this->respondCreated();
        }
    }

在这个例子中，响应了 201 的HTTP状态码，并使用“创建”的通用状态消息返回。方法存在于最常见的用例中 ::

    // 通用响应方式
    respond($data, 200);
    // 通用错误响应
    fail($errors, 400);
    // 项目创建响应
    respondCreated($data);
    // 项目成功删除
    respondDeleted($data);
    // 客户端未授权
    failUnauthorized($description);
    // 禁止动作
    failForbidden($description);
    // 找不到资源
    failNotFound($description);
    // Data 数据没有验证
    failValidationError($description);
    // 资源已存在
    failResourceExists($description);
    // 资源早已被删除
    failResourceGone($description);
    // 客户端请求数过多
    failTooManyRequests($description);

***********************
处理响应类型
***********************

当您通过以下任何一种方法传递数据时，它们将决定基于数据类型来格式化结果:

* 如果 $data 是一个字符串，它将被当作 HTML 发送回客户端。
* 如果 $data 是一个数组，它将尝试请求内容类型与客户端进行协商，默认为 JSON。如果没有在 Config\API.php 中配置内容。默认使用 ``$supportedResponseFormats`` 属性。

需要使用格式化，请修改 **Config/Format.php** 文件配置。``$supportedResponseFormats`` 包含了一个格式化响应类型列表。默认情况下，系统将会自动判断并响应 XML 和 JSON 格式::

        public $supportedResponseFormats = [
            'application/json',
            'application/xml'
        ];

这是在 :doc:`Content Negotiation </libraries/content_negotiation>` 中使用的数组，以确定返回的响应类型。如果在客户端请求的内容和您支持的内容之间没有匹配，则返回第一个该数组中的格式。

接下来，需要定义用于格式化数据数组的类。这必须是一个完全合格的类名，类名必须实现 **CodeIgniter\API\FormatterInterface**。格式化支持 JSON 和 XML ::

    public $formatters = [
        'application/json' => \CodeIgniter\API\JSONFormatter::class,
        'application/xml'  => \CodeIgniter\API\XMLFormatter::class
    ];

因此，如果您的请求在 **Accept** 头中请求 JSON 格式的数据，那么您传递的数据数组就可以通过其中任何一个 ``respond*`` 或 ``fail*`` 方法将由 **CodeIgniter\API\JSONFormatter** 格式化。由此产生的 JSON 数据将被发送回客户端。

===============
引用类
===============
.. php:method:: respond($data[, $statusCode=200[, $message='']])

    :param mixed  $data:  返回客户端的数据。字符串或数组。
    :param int    $statusCode: 返回的HTTP状态码。默认为 200。
    :param string $message: 返回的自定义 "reason" 消息。

    这是该特征中所有其他方法用于将响应返回给客户端的方法。

     ``$data`` 元素可以是字符串或数组。 默认情况下，一个字符串将作为 HTML 返回，而数组将通过 json_encode 运行并返回为 JSON，除非 :doc:`Content Negotiation </libraries/content_negotiation>` 确定它应该以不同的格式返回。

    如果一个 ``$message`` 字符串被传递，它将被用来替代标准的 IANA 标准码回应状态。但不是每个客户端都会遵守自定义代码，并将使用 IANA 标准匹配状态码。

    .. note:: 由于它在活动的响应实例上设置状态码和正文，所以应该一直作为脚本执行中的最终方法。

.. php:method:: fail($messages[, int $status=400[, string $code=null[, string $message='']]])

    :param mixed $messages: 包含遇到错误消息的字符串或字符串数组。
    :param int   $status: 返回的HTTP状态码。 默认为400。
    :param string $code: 一个自定义的API特定的错误代码。
    :param string $message: 返回的自定义“reason”消息。
    :returns: 以客户端的首选格式进行多部分响应。

    这是用于表示失败的响应的通用方法，并被所有其他“fail”方法使用。

    该 ``$messages`` 元素可以是字符串或字符串数​​组。
    该 ``$status`` 参数是应返回的HTTP状态码。

    由于使用自定义错误代码更好地提供了许多 API，因此可以在第三个参数中传递自定义错误代码。如果没有值，它将是一样的 ``$status`` 【状态码】。

    如果一个 ``$message`` 字符串被传递，它将被用于代替响应状态的标准 IANA 码。不是每个客户端都会遵守自定义代码，并且将使用与状态代码相匹配的 IANA 标准。

    这个响应是一个包含两个元素的数组： ``error`` 和 ``messages`` 。 ``error`` 元素包含错误的状态代码。``messages`` 元素包含一组错误消息。它看起来像::

        $response = [
            'status' => 400,
            'code' => '321a',
            'messages' => [
                'Error message 1',
                'Error message 2'
            ]
        ];

.. php:method:: respondCreated($data[, string $message = ''])

    :param mixed  $data: 返回给客户端的数据。字符串或数组。
    :param string $message: 返回的自定义“reason”消息。
    :returns: Response 对象的 send()方法的值。

    设置创建新资源时使用的相应状态代码，通常为201::

        $user = $userModel->insert($data);
        return $this->respondCreated($user);

.. php:method:: respondDeleted($data[, string $message = ''])

    :param mixed  $data: 返回给客户端的数据。字符串或数组
    :param string $message: 自定义的“原因”消息返回。
    :returns: Response 对象的 send()方法的值。

    设置当通过此API调用的结果删除新资源时使用的相应状态代码（通常为200）。
    ::

        $user = $userModel->delete($id);
        return $this->respondDeleted(['id' => $id]);

.. php:method:: failUnauthorized(string $description[, string $code=null[, string $message = '']])

    :param mixed  $description: 显示用户的错误信息。
    :param string $code: 一个自定义的API特定的错误代码。
    :param string $message: 返回的自定义“reason”消息。
    :returns:  Response 对象的 send()方法的值。

    设置当用户未被授权或授权不正确时使用的相应状态代码。状态码为401。
    ::

        return $this->failUnauthorized('Invalid Auth token');

.. php:method:: failForbidden(string $description[, string $code=null[, string $message = '']])

    :param mixed  $description: 显示用户的错误信息。
    :param string $code: 一个自定义的API特定的错误代码。
    :param string $message: 返回的自定义“reason”消息。
    :returns: Response 对象的 send()方法的值。

    不像 ``failUnauthorized``，当请求 API 路径决不允许采用这种方法。未经授权意味着客户端被鼓励再次尝试使用不同的凭据。禁止意味着客户端不应该再次尝试，因为它不会有帮助。状态码为403。

    ::

        return $this->failForbidden('Invalid API endpoint.');

.. php:method:: failNotFound(string $description[, string $code=null[, string $message = '']])

    :param mixed  $description: 显示用户的错误信息。
    :param string $code: 一个自定义的API特定的错误代码。
    :param string $message: 返回的自定义“reason”消息。
    :returns: Response 对象的 send()方法的值。

    设置于在找不到请求的资源时使用的状态码。状态码为404。
    ::

        return $this->failNotFound('User 13 cannot be found.');

.. php:method:: failValidationError(string $description[, string $code=null[, string $message = '']])

    :param mixed  $description: 显示用户的错误信息。
    :param string $code: 一个自定义的API特定的错误代码。
    :param string $message: 返回的自定义“reason”消息。
    :returns: Response 对象的 send()方法的值。

    设置于客户端发送的数据未通过验证规则时使用的状态码。状态码通常为400。

    ::

        return $this->failValidationError($validation->getErrors());

.. php:method:: failResourceExists(string $description[, string $code=null[, string $message = '']])

    :param mixed  $description: 显示用户的错误信息。
    :param string $code: 一个自定义的API特定的错误代码。
    :param string $message: 返回的自定义“reason”消息。
    :returns: Response 对象的 send()方法的值。

    设置于当客户端尝试创建的资源已经存在时使用的状态码。状态码通常为409。

    ::

        return $this->failResourceExists('A user already exists with that email.');

.. php:method:: failResourceGone(string $description[, string $code=null[, string $message = '']])

    :param mixed  $description: 显示用户的错误信息。
    :param string $code: 一个自定义的API特定的错误代码。
    :param string $message: 返回的自定义“reason”消息。
    :returns: Response 对象的 send()方法的值。

    设置于当请求的资源先前被删除并且不再使用时使用的状态码。状态码通常为410。

    ::

        return $this->failResourceGone('That user has been previously deleted.');

.. php:method:: failTooManyRequests(string $description[, string $code=null[, string $message = '']])

    :param mixed  $description: 显示用户的错误信息。
    :param string $code: 一个自定义的API特定的错误代码。
    :param string $message: 返回的自定义“reason”消息。
    :returns: Response 对象的 send()方法的值。

    设置于当客户端调用 API路径次数过多时使用的状态码。这可能是由于某种形式的节流或速率限制。状态码通常为400。
    ::

        return $this->failTooManyRequests('You must wait 15 seconds before making another request.');

.. php:method:: failServerError(string $description[, string $code = null[, string $message = '']])

    :param mixed  $description: 显示用户的错误信息。
    :param string $code: 一个自定义的API特定的错误代码。
    :param string $message: 返回的自定义“reason”消息。
    :returns: Response 对象的 send()方法的值。

    设置于当存在服务器错误时使用的状态码。

    ::

        return $this->failServerError('Server error.');
