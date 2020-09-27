#####################
使用实体类
#####################

CodeIgniter 支持实体类作为数据层的“第一类公民”，同时使它是可选使用的。
它通常作为存储库模式的一部分，但如果更适合你的需要，则也可以直接与 :doc:`Model </models/model>` 一起使用。

.. contents::
    :local:
    :depth: 2

使用实体类
============

实体类的核心只是一个代表单个数据行的类。它具有表示数据列的类属性，并提供额外的方法来实现该行的业务逻辑。
他的核心特征是它无需知道如何持久化，这是模型或者存储类的责任。这样，当你保存对象的方式有任何改变时，
你不必在整个程序中更改该对象的使用方式。这样可以快速的在原型制作阶段使用 JSON 或 XML 文件存储对象，
然后在证明概念有效时，可以轻松的切换到数据库。

让我们来看一个非常简单的实体类，以及如何使用它来帮助我们使事情变得清晰。

假设你有一个数据库表名为 ``users``, 它具有以下结构：
::

    id          - integer
    username    - string
    email       - string
    password    - string
    created_at  - datetime

创建实体类
-----------------------

现在创建一个新的实体类。由于没有默认的位置存储这些类，并且它不适合现有的目录结构，因此创建一个新的目录 **app/Entities** 。
在 **app/Entities/User.php** 创建实体类本身。

::

    <?php namespace App\Entities;

    use CodeIgniter\Entity;

    class User extends Entity
    {
        //
    }

简单来说，这就是你需要做的全部，尽管我们一会会使他更有用。

创建模型
----------------

首先在 **app/Models/UserModel.php** 创建模型，这样我们就可以与它交互：
::

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

该模型将数据库中的 ``users`` 表用于它的所有活动。我们将设置 ``$allowedFields`` 属性设置为包含我们希望外部更改的所有字段。
``id``, ``created_at`` 和 ``updated_at`` 字段由数据库自动处理，因此我们不想更改这些字段。最后，我们设置 ``$returnType``
属性为实体类。这可以确保模型中从数据库返回行的所有方法都返回实体类的实例，而不是像通常那样返回对象或数组。

使用实体类
-----------------------------

现在所有部分都准备就绪，你可以像其他类一样使用实体类：
::

    $user = $userModel->find($id);

    // Display
    echo $user->username;
    echo $user->email;

    // Updating
    unset($user->username);
    if (! isset($user->username)
    {
        $user->username = 'something new';
    }
    $userModel->save($user);

    // Create
    $user = new \App\Entities\User();
    $user->username = 'foo';
    $user->email    = 'foo@example.com';
    $userModel->save($user);

你可能注意到 User 类没有为列设置任何属性，但你仍可以像公共属性那样访问它们。基类 **CodeIgniter\\Entity** 为你解决了这一问题，
并提供使用 **isset()** 和 **unset()** 方法检查属性的能力。以及自创建对象或从数据库中提取对象以来哪些列已经更改。

当 User 传递到模型的 **save()** 方法时，他将自动读取属性并保存模型的 **$allowedFields** 属性列出的列的所有更改。
它还知道是创建新行，还是更新现有行。

快速填充属性
--------------------------

实体类还提供一个方法 ``fill()``， 该方法允许你传递键值对数组并设置为类属性。数组中的任何属性都将在实体类中设置。然而，当通过模型
进行保存时，事实上只有在 $allowedFields 中的字段才会被保存到数据库中，因此你可以在实体类上存储其他数据，不必担心会错误的保存多余的字段。

::

    $data = $this->request->getPost();

    $user = new \App\Entities\User();
    $user->fill($data);
    $userModel->save($user);

你也可以在构造函数中传递数据，数据将在实例化过程中传递给 ``fill()`` 方法。

::

    $data = $this->request->getPost();

    $user = new \App\Entities\User($data);
    $userModel->save($user);

批量访问属性
--------------------------
实体类有两种方法可将所有可用属性提取到数组中：``toArray()`` 和 ``toRawArray()``。使用原始版本将绕过魔术方法 ``getter`` 和强制转换。
两种方法都可以使用布尔值作为第一个参数来设置返回的值是否应该是已经更改的值，如果是实体的嵌套递归，则使用第一个参数布尔值作为参数进行递归调用。

处理业务逻辑
=======================

尽管上面的示例很方便，但它们并不能帮助你实施任何业务逻辑。基础实体类巧妙的实现 ``__get()`` 和 ``__set()`` 方法，这将检查并使用特殊方法
，而不是直接使用属性，从而使你能够执行所需的任何业务逻辑或数据转换。

这是一个更新后的实体类实例，展示了如何使用它：
::

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

首先我们要注意的是我们添加的方法的名称。对于任意类，都希望将列名 ``snake_case`` 转化为 ``PascalCase`` 并以 ``set`` 或 ``get`` 开头
（即，将列名转化为驼峰法描述）。当你直接设置或检索类的属性时（i.e. $user->email），会自动调用这些方法。除非你希望从其他类访问它们，否则
这些方法不需要是公共的。例如，``created_at`` 类属性将通过 ``setCreatedAt`` 和 ``getCreatedAt`` 进行访问。

.. note:: 这仅在类外部访问属性时有效，类内部的任何方法都必须直接调用 ``setX()`` 和 ``getX()`` 方法。

在 ``setPassword()`` 方法中，我们确保始终对密码进行哈希处理。

在 ``setCreatedAt()`` 方法中，我们将从模型接到的字符串转化为 DateTime 对象，确保我们的当前时区是 UTC ，这样就可以轻易的转换查看器的当前时区。

在 ``getCreatedAt()`` 方法中，它将时间转化为应用程序当前时区中的格式化字符串。

这些示例虽然简单，但是表明使用实体类可以提供一种非常灵活的方式来实施业务逻辑并创建易于使用的对象。
::

    // Auto-hash the password - both do the same thing
    $user->password = 'my great password';
    $user->setPassword('my great password');

数据映射
============

在你职业生涯的许多时候，你会遇到下面的情况。应用程序的使用发生了变化，并且数据库中原始的列名不再具有意义。或者发现你的编码样式是 
``camelCase`` 风格，但数据库模式需要 ``snake_case`` 名称风格。使用实体类的数据映射功能可以轻松的处理这些情况。

例如，假设你有在程序中使用的简化用户实体类：
::

    <?php namespace App\Entities;

    use CodeIgniter\Entity;

    class User extends Entity
    {
        protected $attributes = [
            'id' => null,
            'name' => null,        // Represents a username
            'email' => null,
            'password' => null,
            'created_at' => null,
            'updated_at' => null,
        ];
    }

你的老板对你说：“没有人再使用用户名”，所以你更改为仅使用邮箱登录。但是他们确实希望对应用程序进行一些个性化设置，因此他们希望
更改名称字段用来表示用户的全名，而不是像现在这样显示用户名。为了保持整洁并确保数据库中的内容继续有意义，你启动了一次迁移，将
``name`` 字段重命名为 ``full_name`` 字段以便清楚的理解。

忽略这个例子的不自然，我们现在有两个选择来修复 User 类。我们可以将属性 ``$name`` 修改为 ``$full_name`` ，但这需要再整个程序中进行更改。
相反的，我们可以简单的将数据库中的 ``full_name`` 映射到 ``$name`` 属性，然后完成实体类的更改：
::

    <?php namespace App\Entities;

    use CodeIgniter\Entity;

    class User extends Entity
    {
        protected $attributes = [
            'id' => null,
            'name' => null,        // Represents a username
            'email' => null,
            'password' => null,
            'created_at' => null,
            'updated_at' => null,
        ];

        protected $datamap = [
            'full_name' => 'name'
        ],
    }

通过添加新的数据名称到 ``$datamap`` 数组中，我们可以告诉类应该通过哪个类属性来访问数据库列。数组的键是数据库总的列名称，数组中的值
是要映射到的类属性。

在示例中，当模型在 User 类上设置 ``full_name`` 字段时，它实际上将值分配给 ``$name`` 属性，所以可以通过 ``$user->name`` 设置和检索。
仍然可以使用原始的 ``$user->full_name`` 进行访问，因此模型需要使用这个名称获取数据并保存到数据库中。但是，``unset`` 和 ``isset`` 只对
映射的属性 ``$name`` 起作用，并不适用于原始名称 ``full_name`` 。

修改器
========

Date 修改器
-------------

默认情况下，实体类将名为 `created_at`，`updated_at` 和 `deleted_at` 的字段转化为 :doc:`Time </libraries/time>` 的实例。
Time 类以不可变的本地化的方式，提供了大量有用的方法。

你可以通过将名称添加到 **options['dates']** 数组的方式来自定义需要自动转化的属性：
::

    <?php namespace App\Entities;

    use CodeIgniter\Entity;

    class User extends Entity
    {
        protected $dates = ['created_at', 'updated_at', 'deleted_at'];
    }

现在，当这些属性中的任何一个被设置时，它们将使用应用程序的当前时区（在 **app/Config/App.php** 中设置）转化为 Time 实例：
::

    $user = new \App\Entities\User();

    // Converted to Time instance
    $user->created_at = 'April 15, 2017 10:30:00';

    // Can now use any Time methods:
    echo $user->created_at->humanize();
    echo $user->created_at->setTimezone('Europe/London')->toDateString();

属性转换
----------------

你可以指定使用 **casts** 属性将实体类中的属性转换为通用数据类型。此选项应该是一个数组，其中键是类属性的名称，而值是应
强制转换为的数据类型。转换仅在读取值时产生影响，不会发生影响实体类或数据库中永久值的转换。可以将属性强制转换为以下任何
数据类型：**integer**，**float**，**double**，**string**，**boolean**，**object**，**array**，**datetime** 和 **timestamp**。
在类型前添加问号，将属性标记为可为空。即，**?string**，**?integer**。

例如，你可以将 User 实体类的 **is_banned** 属性转化为布尔类型：
::

    <?php namespace App\Entities;

    use CodeIgniter\Entity;

    class User extends Entity
    {
        protected $casts = [
            'is_banned' => 'boolean',
            'is_banned_nullable' => '?boolean'
        ],
    }

Array/Json 转换
------------------
Array/Json 转换对于存储为 **serialized arrays** 或 **json** 的字段特别有用。当转换值为：

* **array** 自动反序列化，
* **json** 自动设置为 ``json_decode($value, false)``，
* **json-array** 自动设置为 ``json_decode($value, true)``，

当设置属性值时。与其它可以强制类型转化的数据类型不同，它们的转化为 ：

* **array** 强制类型转换将序列化，
* **json** 和 **json-array** 强制类型转化将调用 json_encode 函数

设置属性值时：
::

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

检查更改的属性
-------------------------------

你可以检查实体类的属性自创建以来是否被更改。唯一的参数是要检查的属性名称：
::

    $user = new User();
    $user->hasChanged('name');      // false

    $user->name = 'Fred';
    $user->hasChanged('name');      // true

或者要检查整个实体类是否有更改的值，则忽略参数：
::

    $user->hasChanged();            // true
