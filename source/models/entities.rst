#####################
运行实体集
#####################

在 CodeIgniter 数据库层里，CodeIgniter 像头等公民般支持实体类，当然要保证它们完整地随意的去使用。它们一般地作为存储库模式的一部分被使用，但如果它们更适合你需要的方式，它们是能与 :doc:`Model </models/model>` 模块直接地被使用。



.. contents::
    :local:
    :depth: 2


实体用法
============

在它的核心内，一个实体类是描述单一的数据库行的简单地类。它有描述数据库列的类属性，并且提供了任意附加的方法为行执行业务逻辑。核心的特点，尽管它不知道关于如何维持自身的任何事情。那应当是模型或者存储类库的职责。以那样的方式，如果任何事情的改变基于你如何需要保存的对象，你不需要怎样改变对象自始自终在应用上的使用。这能尽可能的让实体类使用JSON或者XML文件在快速的原型设计阶段去存储对象，然后当你已经证明工作概念时简单地转换一个数据库。
让我们马马虎虎的演示一个非常简单的用户实体并且我们乐于运行实体类去使事情明朗化。
假定你有一个数据库表格被命名为 ``users`` 并且已经有了以下的模式::

    id          - integer
    username    - string
    email       - string
    password    - string
    created_at  - datetime


创建实体类
-----------------------

现在创建一个新实体类。由于没有默认位置去存储这些类，并且它与确凿的路径结构不适合，要在  **app/Entities** 创建新的路径。在 **app/Entities/User.php** 里创建实体自身。


::

    <?php namespace App\Entities;

    use CodeIgniter\Entity;

    class User extends Entity
    {
        //
    }


在它的最简单的方式里，这就是全部你需要做的，虽然我们要使它立刻更有价值。


创建模型
----------------

首先在 **app/Models/UserModel.php** 路径里创建模型以至于我们能与其相互作用::

    <?php namespace App\Models;

    use CodeIgniter\Model;

    class UserModel extends Model
    {
        protected $table         = 'users';
        protected $allowedFields = [
            'username', 'email', 'password'
        ];
        protected $returnType    = 'App\Entities\User';
        protected $useTimestamps = true;
    }

在数据库里对所有他的行动模型使用 ``users`` 表格。我们已经设置了包括所有我们想要的外部类来改变字段 ``$allowedFields`` 属性。
那 ``id``, ``created_at``, 和 ``updated_at`` 字段是由类或者数据库来自动地被操控，因此我们不要去改变那些字段。最终，我们已经设置了我们的实体类作为 ``$returnType`` .
就像正常情况一般，这可以确保所有模型的方法从数据返回我们用户实体类代替对象或者数组的实例。



运行实体类
-----------------------------

现在所有块都在适当的位置里，你要运行实体类就像你使用任何其他类一样::


    $user = $userModel->find($id);

    // 显示
    echo $user->username;
    echo $user->email;

    // 更新
    unset($user->username);
    if (! isset($user->username)
    {
        $user->username = 'something new';
    }
    $userModel->save($user);

    // 创建
    $user = new \App\Entities\User();
    $user->username = 'foo';
    $user->email    = 'foo@example.com';
    $userModel->save($user);

你也许已经通知用户类没有设置对列的任何属性，但是你仍旧能使用他们犹如他们是公共属性。基础类， **CodeIgniter\Entity**,
对于你来说小心处理实体类，和 **isset()** 属性的能力一样，或者 **unset()** 属性，而且以前来自于数据库对象被创建或者被拉取的保持轨迹的列已经被改变。
当用户通过了模型的 **save()** 方法，它可以在模型的 **$allowedFields** 属性里自动地小心读取属性并且保存任何变化的列的目录。无论新行，或者更新的现存行，那应当是熟知的。



快速填充属性
--------------------------

实体类也提供方法，``fill()`` 允许你去使键/值副的数组渐渐变为类和移植类属性。数组里的任何属性将会被设置在实体类上。然而，当通过模型保存时，仅有的 $allowedFields 字段实际上将会被保存到数据库里，因此除了过多担心孤立的字段来获得错误地挽救，你能储存附加的数据在你的实体集里。


::

    $data = $this->request->getPost();

    $user = new \App\Entities\User();
    $user->fill($data);
    $userModel->save($user);

你也能在构造函数里传递数据并且实例化过程中数据将会贯穿 `fill()` 方法。

::

    $data = $this->request->getPost();

    $user = new \App\Entities\User($data);
    $userModel->save($user);


处理业务逻辑
=======================

当上述示例是方便的时候，它们不要助长执行任何业务逻辑。基本的实体类执行一些聪明的 ``__get()`` 和 ``__set()`` 方法，并且那是为了特殊方法而检测，然后使用那些特殊方法代替直接地使用属性，当你需要时允许你执行任何业务逻辑或者数据转换。
下面是更新的用户实体类提供一些示例并演示示例如何运用::


    <?php namespace App\Entities;

    use CodeIgniter\Entity;
    use CodeIgniter\I18n\Time;

    class User extends Entity
    {
        public function setPassword(string $pass)
        {
            $this->attributes['password'] = password_hash($pass, PASSWORD_BCRYPT);

            return $this;
        }

        public function setCreatedAt(string $dateString)
        {
            $this->attributes['created_at'] = new Time($dateString, 'UTC');

            return $this;
        }

        public function getCreatedAt(string $format = 'Y-m-d H:i:s')
        {
            // Convert to CodeIgniter\I18n\Time object
            $this->attributes['created_at'] = $this->mutateDate($this->attributes['created_at']);

            $timezone = $this->timezone ?? app_timezone();

            $this->attributes['created_at']->setTimezone($timezone);

            return $this->attributes['created_at']->format($format);
        }
    }

首要的事情，通知我们已经添加方法的名字。对于每个人，类要求 snake_case （蛇形命名法）列名要被转换到 PascalCase （帕斯卡命名法），并且加 ``set`` 或者 ``get`` 任一个作为字首。
无论何时使用直接语法你设置或者检索类属性这些方法将会自动地被调用(例如： $user->email)。该方法不需要被公开除非你想它们通过其他的类。例如，``created_at`` 类属性将通过 ``setCreatedAt()`` 和 ``getCreatedAt()`` 方法。
当设法从外部类使用属性时这是最佳的工作内容。任何方法的本质对于类来说必须被直接地调用 ``setX()`` 和 ``getX()`` 方法。 
在 ``setPassword()`` 方法里我们确定密码总是混乱的。
在 ``setCreatedAt()`` 方法里我们从模型接收到 DateTime 对象并转换字符类型，确保我们的时区是 UTC ，因此我们能简单地转换显示器最近的时区。
在 ``getCreatedAt()`` 方法里，它在应用最近的时区里转换时区到一种字符串格式。

当清楚简单的时候，这些示例显示使用实体类能提供非常灵活的路线去执行业务逻辑并且创建愉快使用的对象。


::

    // 自动哈希密码 - 两者做相同的事情
    $user->password = 'my great password';
    $user->setPassword('my great password');


数据映射
============

在你的工作里的许多重要时刻，你将会遇到应用的使用已经被改变并且原始列名字在数据库里不再产生判断力的情形。或者你找到你的代码样式提出  camelCase （驼峰命名法）类属性，但是你的数据概要需求 snake_case （蛇形命名法）命名。 这些情形能简单地与实体类的数据映射特征操作。

一个例子，想想你通过你的应用拥有被使用的简化的用户实体::


    <?php namespace App\Entities;

    use CodeIgniter\Entity;

    class User extends Entity
    {
        protected $attributes = [
            'id' => null,
            'name' => null,        // 描绘一个用户名
            'email' => null,
            'password' => null,
            'created_at' => null,
            'updated_at' => null,
        ];
    }

你的老板到你身边并说没有人使用更多的用户名，因此你要转换仅使用邮件登录。
然而他们想把应用拟人化一点，因此现在他们想你要改变命名字段去描绘一个用户的全名，而不是他们想它最近产生的一样的用户名。
你鞭策一个变革重命名 `name` 字段去为了清楚的 `full_name`， 在数据库里要保持事物整洁并且确保事物继续产生判断力。
忽略如何策划事例，我们现有两个选择关于如何调整用户类。我们能从 ``$name`` 到 $full_name`` 更改属性，但是将应用需要彻头彻尾的改变。
取而代之的是，我们能对 ``$name`` 属性在数据库简单地映射 ``$full_name``列，并且完成时被实体类改变::


    <?php namespace App\Entities;

    use CodeIgniter\Entity;

    class User extends Entity
    {
        protected $attributes = [
            'id' => null,
            'name' => null,        // 描绘一个用户名
            'email' => null,
            'password' => null,
            'created_at' => null,
            'updated_at' => null,
        ];

        protected $datamap = [
            'full_name' => 'name'
        ],
    }

由添加我们新的数据库名到 ``$datamap`` 数组，我们能说类属性数据库列应该是自始自终易接近的类。在数据库里数组的键是列的名字，在数组里的数值是映射它的类属性。
在这个例子里，在用户类上当模型设置 ``full_name`` 字段时，它实际分派了到类的值 ``$name`` 属性，因此 它能通过 ``$user->name`` 被设置和检索。通过最初的 ``$user->full_name`` ，值将仍旧是易受影响的，并且，对于模型就像这个值需要去获取数据返还并且保存到数据库里。然而，``unset`` 和 ``isset`` 仅工作在映射的属性上，``$name`` ，不是在原名字上，``full_name``.


赋值函数
========

日期赋值函数
-------------

默认情况下，实体类将会转换字段名字 `created_at`, `updated_at`, 或者 `deleted_at` 到 :doc:`Time </libraries/time>` 实例，无论何时实例会被设置或者被检索。本地化途径的时间类提供有益的方法的大数字。你能定义属性由添加名字到 **options['dates']** 数组自动地被转换 ::


    <?php namespace App\Entities;

    use CodeIgniter\Entity;

    class User extends Entity
    {
        protected $dates = ['created_at', 'updated_at', 'deleted_at'];
    }

现在，当这些属性的任何一些被设置，它们将被转换为时间实例，使用应用最近的时区，就像设置 **app/Config/App.php** 路径::


    $user = new \App\Entities\User();

    // Converted to Time instance
    $user->created_at = 'April 15, 2017 10:30:00';

    // 转换到时间实例
    echo $user->created_at->humanize();
    echo $user->created_at->setTimezone('Europe/London')->toDateString();


属性转换
----------------

在你的实体类里你能具体指定属性应当被转换到带 **casts** 属性的普通数据类型里。选项应当是数组，数组的键位是类属性名字，并且值是数据类型也应当是被转换的。当数值读取时转换仅受影响。在任一实体里或者数据库里，没有转换放生影响固定的值。属性能被转换到任何下面的数据类型:**integer**, **float**, **double**, **string**, **boolean**, **object**, **array**, **datetime**, 和 **timestamp**.
在类型的开始就像可空类型去添加问题去标记属性，例如 **?string**, **?integer**.
示例，如果你有带着 **is_banned** 属性的用户实体，你能转换它为 boolean 类型::


    <?php namespace App\Entities;

    use CodeIgniter\Entity;

    class User extends Entity
    {
        protected $casts = [
            'is_banned' => 'boolean',
            'is_banned_nullable' => '?boolean'
        ],
    }


数组/Json 转换
------------------

带字段的数组 / Json 转换是特别有用的，在它的字段里它可以存储连续数组或者Json。当时转换就像：当你读取属性的值时，
* an **array** ， 它们将会自动地被非序列化，
* a **json**, 它们将会自动地被设置就像 json_decode($value, false),
* a **json-array**, 它们将自动地被设置为 json_decode($value, true),
数据类型不同的剩余部分，你能转换属性到这些:
* **array** 转换类型将会序列化，
* **json** 和 **json-array** 转换将会使用 json_encode 函数
值在无论何时属性要设置::


    <?php namespace App\Entities;

    use CodeIgniter\Entity;

    class User extends Entity
    {
        protected $casts => [
            'options' => 'array',
		    'options_object' => 'json',
		    'options_array' => 'json-array'
        ];
    }

    $user    = $userModel->find(15);
    $options = $user->options;

    $options['foo'] = 'bar';

    $user->options = $options;
    $userModel->save($user);


为了更改的属性检查
-------------------------------

如果实体属性已经改变你能自从它被创建时检查。仅有的参数是属性的名字要检查::


    $user = new User();
    $user->hasChanged('name');      // false

    $user->name = 'Fred';
    $user->hasChanged('name');      // true

或者对于改变的值省略参数去检查整个的实体类::


    $user->hasChanged();            // true
