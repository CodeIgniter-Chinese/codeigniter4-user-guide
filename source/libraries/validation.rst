验证类
##################################################

CodeIgniter 提供了全面的数据验证类，最大程度减少你需要编写的代码量。

.. contents::
    :local:
    :depth: 2

概述
************************************************

在解释 CodeIgniter 的数据验证之前，我们先介绍理想的状况：

#. 显示一个表单。
#. 你填写并提交。
#. 如果你提交的表单数据无效，或者丢失了必填项，将重新显示包含了你的数据和错误消息的表单。
#. 这个过长将一直持续到你提交的表单数据有效为止。

在接收端，脚本必须：

#. 检查需要的数据。
#. 验证数据的类型是否正确，并且符合要求的标准。例如，如果提交了用户名，则必须仅包含允许的字符。
   它必须大于最小长度，小于最大长度。用户名不能是系统中已经存在的用户名，甚至是保留的关键词。
   等等。
#. 处理数据以保证安全。
#. 如果有必要，对数据进行格式化 (是否需要裁剪数据 ? HTML 编码? 等等。)
#. 准备要插入数据库的数据。

尽管上述过程没有什么非常复杂的，但是通常需要编写大量的代码，并且显示各种错误消息，在 HTML 表单中
放置各种控制结构。表单验证虽然容易创建，但是通常十分混乱，实现起来很繁琐。

表单验证教程
************************************************

以下是实现 CodeIgniter 表单验证的“动手”教程。

为了实现表单验证，你需要做三件事：

#. 一个包含表单的 :doc:`View </outgoing/views>` 文件。
#. 一个提交成功后显示 "success" 的 View 文件。
#. 一个 :doc:`controller </incoming/controllers>` 方法用来接收和处理提交的数据。

让我们以会员注册表单为例来做这三件事。

表单
================================================

使用编辑器创建一个名为 **Signup.php** 的视图文件，将代码复制到文件中，并保存到 **app/Views/** 文件夹：
::

    <html>
    <head>
        <title>My Form</title>
    </head>
    <body>

        <?= $validation->listErrors() ?>

        <?= form_open('form') ?>

        <h5>Username</h5>
        <input type="text" name="username" value="" size="50" />

        <h5>Password</h5>
        <input type="text" name="password" value="" size="50" />

        <h5>Password Confirm</h5>
        <input type="text" name="passconf" value="" size="50" />

        <h5>Email Address</h5>
        <input type="text" name="email" value="" size="50" />

        <div><input type="submit" value="Submit" /></div>

        </form>

    </body>
    </html>

成功页
================================================

使用编辑器创建一个名为 **Success.php** 的视图文件，将代码复制到文件中，并保存到 **app/Views/** 文件夹：
::

    <html>
    <head>
        <title>My Form</title>
    </head>
    <body>

        <h3>Your form was successfully submitted!</h3>

        <p><?= anchor('form', 'Try it again!') ?></p>

    </body>
    </html>

控制器
================================================

使用编辑器创建一个名为 **Form.php**  的控制器文件，将代码复制到文件中，并保存到 **app/Controllers/** 文件夹：
::

    <?php namespace App\Controllers;

    use CodeIgniter\Controller;

    class Form extends Controller
    {
        public function index()
        {
            helper(['form', 'url']);

            if (! $this->validate([]))
            {
                echo view('Signup', [
                    'validation' => $this->validator
                ]);
            }
            else
            {
                echo view('Success');
            }
        }
    }

试一试!
================================================

要尝试使用表单，请使用与此网址相似的网址访问你的网站
::

    example.com/index.php/form/

如果你提交表单，则应该只看到表单重新加载。那是因为你没有设置任何验证规则。

.. note:: 由于你没有告诉 **Validation 类** 进行任何验证, 它在 **默认情况** 下 **返回 false** (boolean false)。 ``validate()``
    方法仅在验证你设置的 **所有规则** 并且没有 **任何失败** 的情况下返回 true 。

说明
================================================

你会注意到上述页面的几件事情：

表单 (Signup.php) 是一个标准的 web 表单，但有一些例外：

#. 它使用表单辅助类来创建表单。从技术上讲这没必要，你可以使用标准的 HTML 代码来创建表单。
   但是，使用表单辅助类可以根据配置文件中的 URL 来生成表单的 action URL。当你的网址发生
   更改时，则你的程序更容易进行移植。
#. 在表单的顶部，你会注意到调用了以下函数：
   ::

    <?= $validation->listErrors() ?>

   该函数将返回 validator 发送的所有错误消息。如果没有消息，则返回一个空字符串。

控制器 (Form.php) 拥有一个方法： ``index()``。这个方法使用控制器提供的 validate 方法，
并加载表单辅助类和 URL 辅助类。它还运行验证程序，根据验证程序是否验证成功，它将显示表单或成功页。

加载 validation 库
================================================

该库通过名叫 **validation** 的服务进行加载：
::

    $validation =  \Config\Services::validation();

这将自动加载 ``Config\Validation`` 文件，文件中包含了多个规则类，以及便于重用的规则集合。

.. note:: 你可用永远都不会使用该方法，因为 :doc:`Controller </incoming/controllers>` 和
 :doc:`Model </models/model>` 中都提供了更简便的验证方法。

设置验证规则
================================================

CodeIgniter 允许你为给定字段设置多个验证规则，并按顺序执行它们。要设置验证规则，你将使用
``setRule()``，``setRules()`` 方法。

setRule()
---------

该方法设置单个规则，它使用 **字段名称** 作为第一个参数，第二个参数是一个可选的标签，第三个参数是以竖线
分隔的规则列表的字符串：
::

    $validation->setRule('username', 'Username', 'required');

**字段名称** 必须与需要验证的任何数据数组的键匹配。如果直接从 $_POST 获取数组，则它必须与表单的 input name 完全匹配。

setRules()
----------

与 ``setRule()`` 类似，但其接受字段名称与其规则所组成的数组：
::

    $validation->setRules([
        'username' => 'required',
        'password' => 'required|min_length[10]'
    ]);

想设置带标签的错误消息，你可以像这样设置：
::

    $validation->setRules([
        'username' => ['label' => 'Username', 'rules' => 'required'],
        'password' => ['label' => 'Password', 'rules' => 'required|min_length[10]']
    ]);

withRequest()
-------------

使用验证库最常见的场景之一是验证从 HTTP 请求输入的数据。如果需要，你可以传递当前的 Request 对象的实例，
它将接收所有输入数据，并将其设置为待验证的数据：
::

    $validation->withRequest($this->request)
               ->run();

处理 Validation
************************************************

验证数组的键
================================================

如果需要验证的数据在嵌套的关联数组中，则可以使用 “点数组语法” 轻松验证数据：
::

    // The data to test:
    'contacts' => [
        'name' => 'Joe Smith',
        'friends' => [
            [
                'name' => 'Fred Flinstone'
            ],
            [
                'name' => 'Wilma'
            ]
        ]
    ]

    // Joe Smith
    $validation->setRules([
        'contacts.name' => 'required'
    ]);

    // Fred Flintsone & Wilma
    $validation->setRules([
        'contacts.friends.name' => 'required'
    ]);

你可以使用通配符 “*” 来匹配数组的任何一个层级：
::

    // Fred Flintsone & Wilma
    $validation->setRules([
        'contacts.*.name' => 'required'
    ]);

“点数组语法” 也通常用于一维数组。例如，多选下拉列表返回的数据：
::

    // The data to test:
    'user_ids' => [
        1,
        2,
        3
    ]
    // Rule
    $validation->setRules([
        'user_ids.*' => 'required'
    ]);

验证单个值
================================================

根据规则验证单个值：
::

    $validation->check($value, 'required');

将验证规则集合保存到配置文件
=======================================================

Validation 类一个好的功能是，它允许你将整个程序的验证规则存储在配置文件中。将规则组合成一个 “group” 
，可以在运行验证时指定不同的组。

.. _validation-array:

如何保存你的规则
-------------------------------------------------------

要存储你的验证规则，只需在 ``Config\Validation`` 类中使用 group 名创建一个新的公共属性，
该元素将包含你的验证规则数组。验证规则数组的原型如下所示：
::

    class Validation
    {
        public $signup = [
            'username'     => 'required',
            'password'     => 'required',
            'pass_confirm' => 'required|matches[password]',
            'email'        => 'required|valid_email'
        ];
    }

你可以在调用 ``run()`` 方法时指定要使用的组：
::

    $validation->run($data, 'signup');

你也可以将自定义错误消息存储在配置文件中，属性名称与组名相同并添加 ``_errors``。
当使用该组时，默认的错误消息将被替换：
::

    class Validation
    {
        public $signup = [
            'username'     => 'required',
            'password'     => 'required',
            'pass_confirm' => 'required|matches[password]',
            'email'        => 'required|valid_email'
        ];

        public $signup_errors = [
            'username' => [
                'required'    => 'You must choose a username.',
            ],
            'email'    => [
                'valid_email' => 'Please check the Email field. It does not appear to be valid.'
            ]
        ];
    }

或者在组中传递所有的设置：
::

    class Validation
    {
        public $signup = [
            'username' => [
                'rules'  => 'required',
                'errors' => [
                    'required' => 'You must choose a Username.'
                ]
            ],
            'email'    => [
                'rules'  => 'required|valid_email',
                'errors' => [
                    'valid_email' => 'Please check the Email field. It does not appear to be valid.'
                ]
            ],
        ];
    }

有关数组格式的详细信息请查看下文。

获取与设置规则组
-------------------------------------------------------

**获取规则组**

该方法从验证配置中获取规则组：
::

    $validation->getRuleGroup('signup');

**设置规则组**

该方法设置将规则组从验证配置设置到验证服务：
::

    $validation->setRuleGroup('signup');

运行多个 Validation
=======================================================

.. note:: ``run()`` 方法不会重置错误状态。如果上次运行失败，``run()`` 方法将始终返回 false ，
   ``getErrors()`` 方法将始终返回上次的所有错误，直至状态被显式重置。

如果需要运行多个验证，例如在不同的数据集上运行或者一个接一个的运行不同的规则，你应该在每次运行前
调用 ``$validation->reset()`` 清除上次运行产生的错误。需要注意的是 ``reset()`` 将重置之前的所有数据、规则
或是自定义错误消息。所以需要重复 ``setRules()``，``setRuleGroup()`` 等方法：
::

    for ($userAccounts as $user) {
        $validation->reset();
        $validation->setRules($userAccountRules);
        if (!$validation->run($user)) {
            // handle validation errors
        }
    }

Validation 占位符
=======================================================

Validation 类提供了一个简单的方法，可以根据传入的数据替换部分规则。这听起来十分晦涩，但在使用 ``is_unique`` 进行验证时
十分方便。 占位符是字段的名称（或数组的键），该字段名称（或数组的键）将用花括号包起来作为 $data 传入。它将被替换为匹配的
传入字段的 **值**。 以下例子可以解释这些：
::

    $validation->setRules([
        'email' => 'required|valid_email|is_unique[users.email,id,{id}]'
    ]);

在这组规则中，它声明 email 在数据库中是唯一的，除了具有与占位符匹配的 id 信息，
假设表单 POST 数据中有以下内容：
::

    $_POST = [
        'id' => 4,
        'email' => 'foo@example.com'
    ];

那么占位符 ``{id}`` 将被修改为数字 **4**，以下是修改后的规则：
::

    $validation->setRules([
        'email' => 'required|valid_email|is_unique[users.email,id,4]'
    ]);

因此，在验证 email 唯一时，将忽略数据库中 ``id=4`` 的行。

这也可以用于在运行时动态创建更多的规则，只要你确保传入的任何动态键都不会与表单
数据产生冲突。

处理错误
************************************************

Validation 库提供了几种方法帮助你设置错误消息，提供自定义错误消息，以及显示一个
或多个错误消息。

默认情况下，错误消息来自 ``system/Language/en/Validation.php`` 中的语言字符串，
其中每个规则都有一个条目。 

.. _validation-custom-errors:

设置自定义错误消息
=============================

``setRule()`` 和 ``setRules()`` 允许自定义错误消息数据作为最后一个参数传入。每一个错误的
错误消息都是定制的，这将带来愉快的用户体验。如果没有设置自定义错误消息，则提供默认值。

这是两种设置错误消息的方式。

作为最后一个参数：
::

    $validation->setRules([
            'username' => 'required|is_unique[users.username]',
            'password' => 'required|min_length[10]'
        ],
        [   // Errors
            'username' => [
                'required' => 'All accounts must have usernames provided',
            ],
            'password' => [
                'min_length' => 'Your password is too short. You want to get hacked?'
            ]
        ]
    );

或者作为标签样式：
::

    $validation->setRules([
            'username' => [
                'label'  => 'Username',
                'rules'  => 'required|is_unique[users.username]',
                'errors' => [
                    'required' => 'All accounts must have {field} provided'
                ]
            ],
            'password' => [
                'label'  => 'Password',
                'rules'  => 'required|min_length[10]',
                'errors' => [
                    'min_length' => 'Your {field} is too short. You want to get hacked?'
                ]
            ]
        ]
    );

如果你希望包含字段的“human”名称，或者某些规则允许的可选参数 (比如 max_length)，或当前参与验证的值，
则可以分别将 ``{field}``，``{param}``，``{value}`` 标记添加到你的消息中：
::

    'min_length' => 'Supplied value ({value}) for {field} must have at least {param} characters.'

在一个用户名字段为 Username ，验证规则为 min_length[6] ，字段值为 “Pizza” 的验证中，将显示错误消息
“Supplied value (Pizza) for Username must have at least 6 characters”

.. note:: 如果你传递最后一个参数，则标签样式的错误信息将被忽略。

消息和验证标签的翻译
=============================================

要使用语言文件中的翻译字符串，可以简单的使用点语法。假设我们有一个包含翻译的文件位
于 ``app/Languages/en/Rules.php``。我们可以简单的使用定义在文件中的语言行，如下：
::

    $validation->setRules([
            'username' => [
                'label'  => 'Rules.username',
                'rules'  => 'required|is_unique[users.username]',
                'errors' => [
                    'required' => 'Rules.username.required'
                ]
            ],
            'password' => [
                'label'  => 'Rules.password',
                'rules'  => 'required|min_length[10]',
                'errors' => [
                    'min_length' => 'Rules.password.min_length'
                ]
            ]
        ]
    );

获取所有错误
==================

如果你需要检索所有验证失败字段的错误消息，你可以使用 ``getErrors()`` 方法：
::

    $errors = $validation->getErrors();

    // Returns:
    [
        'field1' => 'error message',
        'field2' => 'error message',
    ]

如果没有错误，则返回空数组。

获取单个错误
======================

你可以使用 ``getError()`` 方法检索单个字段的错误消息。参数名是唯一的参数：
::

    $error = $validation->getError('username');

如果没有错误，则返回空字符串。

检查是否存在错误
=====================

你可以使用 ``hasError()`` 方法检查字段是否存在错误。字段名是唯一的参数：
::

    if ($validation->hasError('username'))
    {
        echo $validation->getError('username');
    }

自定义错误显示
************************************************

当你调用 ``$validation->listErrors()`` 或 ``$validation->showError()`` ，它将在后台加载一个视图文件，
该文件确定错误的显示方法。默认情况下，它在经过包装的 div 上显示 ``errors`` 。你可以轻松的创建视图并在整个程序
中使用它。

创建视图
==================

第一步是创建视图文件，它可以放在 ``view()`` 方法可以加载的任何地方。这意味着标准的 View 目录，或者任何命名空间
下的 View 目录都可以正常工作。例如，可以在  **/app/Views/_errors_list.php** 创建新的视图文件：
::

    <div class="alert alert-danger" role="alert">
        <ul>
        <?php foreach ($errors as $error) : ?>
            <li><?= esc($error) ?></li>
        <?php endforeach ?>
        </ul>
    </div>

``$errors`` 数组可以在包含错误列表的视图中使用，其中键是发生错误的字段名，值是错误消息，如下所示：
::

    $errors = [
        'username' => 'The username field must be unique.',
        'email'    => 'You must provide a valid email address.'
    ];

实际上可以创建两种类型的视图文件。第一种包含所有错误消息，这就是我们刚才看到的。另一种更简单，只包含一个错误消息变量 ``$error``。
它与指定字段名的 ``showError()`` 方法一起使用。
::

    <span class="help-block"><?= esc($error) ?></span>

配置
=============

创建视图后，需要让 Validation 库知道它们。 打开 ``Config/Validation.php``，在里面找到 ``$templates`` 属性。
你可以在其中列出任意多个自定义视图，并提供一个可以引用他们的短别名。我们将添加上边的示例文件，它看起来像：
::

    public $templates = [
        'list'    => 'CodeIgniter\Validation\Views\list',
        'single'  => 'CodeIgniter\Validation\Views\single',
        'my_list' => '_errors_list'
    ];

指定模板
=======================

通过将别名作为 ``listErrors`` 方法的第一个参数，来指定要使用的模板：
::

    <?= $validation->listErrors('my_list') ?>

当显示特定字段错误时，你可以将别名作为第二个参数传递给 ``showError`` 方法，别名参数应该在字段名称之后：
::

    <?= $validation->showError('username', 'my_single') ?>

创建自定义规则
************************************************

规则简单的存储在命名空间类中。只要自动加载器能找到它们，你可将他们存储到任何位置。这些文件称作规则集。要添加新的规则集，
请编辑 **Config/Validation.php** 并将新文件添加到 ``$ruleSets`` 数组：
::

    public $ruleSets = [
        \CodeIgniter\Validation\Rules::class,
        \CodeIgniter\Validation\FileRules::class,
        \CodeIgniter\Validation\CreditCardRules::class,
    ];

你可以将其添加为具有完全限定类的简单字符串，或者使用 ``::class`` 后缀进行添加。如上所示，这里的好处是，它在更高级的 IED 
中提供了额外的一些导航功能。

在文件中，每一个方法都是一个规则，它必须接受字符串作为第一个字符串，并且必须返回布尔值 true 或 false 。如果通过测试则返回
true ，否则返回 false 。
::

    class MyRules
    {
        public function even(string $str): bool
        {
            return (int)$str % 2 == 0;
        }
    }

默认情况下，系统将在 ``CodeIgniter\Language\en\Validation.php`` 中查找错误要使用语言字符串。在自定义规则中，你可以通过第二个参数 $error 的引用来
提供错误消息：
::

    public function even(string $str, string &$error = null): bool
    {
        if ((int)$str % 2 != 0)
        {
            $error = lang('myerrors.evenError');
            return false;
        }

        return true;
    }

现在你可像其他规则一样使用新的自定义规则：
::

    $this->validate($request, [
        'foo' => 'required|even'
    ]);

允许参数
===================

如果你的方法需要使用参数，则该函数至少需要三个参数：要验证的字符串、参数字符串以及包含提交表单所有数据的数组。
$data 数组对于像 require_with 这样需要检查另一个提交字段的值作为其结果基础的规则来说十分方便：
::

    public function required_with($str, string $fields, array $data): bool
    {
        $fields = explode(',', $fields);

        // If the field is present we can safely assume that
        // the field is here, no matter whether the corresponding
        // search field is present or not.
        $present = $this->required($str ?? '');

        if ($present)
        {
            return true;
        }

        // Still here? Then we fail this test if
        // any of the fields are present in $data
        // as $fields is the lis
        $requiredFields = [];

        foreach ($fields as $field)
        {
            if (array_key_exists($field, $data))
            {
                $requiredFields[] = $field;
            }
        }

        // Remove any keys with empty values since, that means they
        // weren't truly there, as far as this is concerned.
        $requiredFields = array_filter($requiredFields, function ($item) use ($data) {
            return ! empty($data[$item]);
        });

        return empty($requiredFields);
    }

自定义错误可以通过第四个参数传递，如上所述。

可用规则
***************

以下是可供使用的所有本地规则的列表：

.. note:: 规则是一个字符串；参数之间 **不能有空格**，尤其是 ``is_unique`` 规则。
   ``ignore_value`` 前后不能有空格。

::

    // is_unique[table.field,ignore_field,ignore_value]

    $validation->setRules([
        'name' => "is_unique[supplier.name,uuid, $uuid]",  // is not ok
        'name' => "is_unique[supplier.name,uuid,$uuid ]",  // is not ok
        'name' => "is_unique[supplier.name,uuid,$uuid]",   // is ok
        'name' => "is_unique[supplier.name,uuid,{uuid}]",  // is ok - see "Validation Placeholders"
    ]);


======================= =========== =============================================================================================== ===================================================
Rule                    Parameter   Description                                                                                     Example
======================= =========== =============================================================================================== ===================================================
alpha                   No          Fails if field has anything other than alphabetic characters.
alpha_space             No          Fails if field contains anything other than alphabetic characters or spaces.
alpha_dash              No          Fails if field contains anything other than alphanumeric characters, underscores or dashes.
alpha_numeric           No          Fails if field contains anything other than alphanumeric characters.
alpha_numeric_space     No          Fails if field contains anything other than alphanumeric or space characters.
alpha_numeric_punct     No          Fails if field contains anything other than alphanumeric, space, or this limited set of
                                    punctuation characters: ~ (tilde), ! (exclamation), # (number), $ (dollar), % (percent),
                                    & (ampersand), * (asterisk), - (dash), _ (underscore), + (plus), = (equals),
                                    | (vertical bar), : (colon), . (period).
decimal                 No          Fails if field contains anything other than a decimal number.
                                    Also accepts a + or  - sign for the number.
differs                 Yes         Fails if field does not differ from the one in the parameter.                                   differs[field_name]
exact_length            Yes         Fails if field is not exactly the parameter value. One or more comma-separated values.          exact_length[5] or exact_length[5,8,12]
greater_than            Yes         Fails if field is less than or equal to the parameter value or not numeric.                     greater_than[8]
greater_than_equal_to   Yes         Fails if field is less than the parameter value, or not numeric.                                greater_than_equal_to[5]
hex                     No          Fails if field contains anything other than hexadecimal characters.
if_exist                No          If this rule is present, validation will only return possible errors if the field key exists,
                                    regardless of its value.
in_list                 Yes         Fails if field is not within a predetermined list.                                              in_list[red,blue,green]
integer                 No          Fails if field contains anything other than an integer.
is_natural              No          Fails if field contains anything other than a natural number: 0, 1, 2, 3, etc.
is_natural_no_zero      No          Fails if field contains anything other than a natural number, except zero: 1, 2, 3, etc.
is_not_unique           Yes         Checks the database to see if the given value exist. Can ignore records by field/value to            is_not_unique[table.field,where_field,where_value]
                                    filter (currently accept only one filter).
is_unique               Yes         Checks if this field value exists in the database. Optionally set a                             is_unique[table.field,ignore_field,ignore_value]
                                    column and value to ignore, useful when updating records to ignore itself.
less_than               Yes         Fails if field is greater than or equal to the parameter value or not numeric.                  less_than[8]
less_than_equal_to      Yes         Fails if field is greater than the parameter value or not numeric.                              less_than_equal_to[8]
matches                 Yes         The value must match the value of the field in the parameter.                                   matches[field]
max_length              Yes         Fails if field is longer than the parameter value.                                              max_length[8]
min_length              Yes         Fails if field is shorter than the parameter value.                                             min_length[3]
numeric                 No          Fails if field contains anything other than numeric characters.
regex_match             Yes         Fails if field does not match the regular expression.                                           regex_match[/regex/]
permit_empty            No          Allows the field to receive an empty array, empty string, null or false.
required                No          Fails if the field is an empty array, empty string, null or false.
required_with           Yes         The field is required when any of the other required fields are present in the data.            required_with[field1,field2]
required_without        Yes         The field is required when all of the other fields are present in the data but not required.    required_without[field1,field2]
string                  No          A generic alternative to the alpha* rules that confirms the element is a string
timezone                No          Fails if field does match a timezone per ``timezone_identifiers_list``
valid_base64            No          Fails if field contains anything other than valid Base64 characters.
valid_json              No          Fails if field does not contain a valid JSON string.
valid_email             No          Fails if field does not contain a valid email address.
valid_emails            No          Fails if any value provided in a comma separated list is not a valid email.
valid_ip                No          Fails if the supplied IP is not valid. Accepts an optional parameter of ‘ipv4’ or                valid_ip[ipv6]
                                    ‘ipv6’ to specify an IP format.
valid_url               No          Fails if field does not contain a valid URL.
valid_date              No          Fails if field does not contain a valid date. Accepts an optional parameter                      valid_date[d/m/Y]
                                    to matches a date format.
valid_cc_number         Yes         Verifies that the credit card number matches the format used by the specified provider.          valid_cc_number[amex]
                                    Current supported providers are: American Express (amex), China Unionpay (unionpay),
                                    Diners Club CarteBlance (carteblanche), Diners Club (dinersclub), Discover Card (discover),
                                    Interpayment (interpayment), JCB (jcb), Maestro (maestro), Dankort (dankort), NSPK MIR (mir),
                                    Troy (troy), MasterCard (mastercard), Visa (visa), UATP (uatp), Verve (verve),
                                    CIBC Convenience Card (cibc), Royal Bank of Canada Client Card (rbc),
                                    TD Canada Trust Access Card (tdtrust), Scotiabank Scotia Card (scotia), BMO ABM Card (bmoabm),
                                    HSBC Canada Card (hsbc)
======================= =========== =============================================================================================== ===================================================

文件上传规则
======================

这些验证规则可以让你进行基本的检查，验证上传的文件是否满足你的业务需求。
由于文件上传字段在 HTML 字段中不存在，并且存储在 $_FILES 全局变量中，
因此字段名需要输入两次，第一个用于指定验证的字段，像其他规则一样，第二次
作为所有文件上传规则的第一个参数：
::

    // In the HTML
    <input type="file" name="avatar">

    // In the controller
    $this->validate([
        'avatar' => 'uploaded[avatar]|max_size[avatar,1024]'
    ]);

======================= =========== =============================================================================================== ========================================
Rule                    Parameter   Description                                                                                     Example
======================= =========== =============================================================================================== ========================================
uploaded                Yes         Fails if the name of the parameter does not match the name of any uploaded files.               uploaded[field_name]
max_size                Yes         Fails if the uploaded file named in the parameter is larger than the second parameter in        max_size[field_name,2048]
                                    kilobytes (kb).
max_dims                Yes         Fails if the maximum width and height of an uploaded image exceed values. The first parameter   max_dims[field_name,300,150]
                                    is the field name. The second is the width, and the third is the height. Will also fail if
                                    the file cannot be determined to be an image.
mime_in                 Yes         Fails if the file's mime type is not one listed in the parameters.                              mime_in[field_name,image/png,image/jpg]
ext_in                  Yes         Fails if the file's extension is not one listed in the parameters.                              ext_in[field_name,png,jpg,gif]
is_image                Yes         Fails if the file cannot be determined to be an image based on the mime type.                   is_image[field_name]
======================= =========== =============================================================================================== ========================================

文件验证规则适用于单个和多个文件上传。

.. note:: 你也可以使用任何最多允许两个参数的本地 PHP 函数，
    其中至少需要一个参数（传递字段数据）。
