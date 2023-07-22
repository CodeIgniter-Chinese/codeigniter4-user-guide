##########
视图单元格
##########

许多应用程序都有可以在页面之间重复使用的小视图片段,或者在页面的不同位置重复使用。这些通常是帮助框、导航控件、广告、登录表单等。CodeIgniter 允许你将这些表示块的逻辑封装在视图单元格中。它们基本上是可以在其他视图中包含的迷你视图。它们可以内置逻辑来处理任何单元格特定的显示逻辑。它们可以用于通过将每个单元格的逻辑分隔到自己的类中来使视图更可读和可维护。

CodeIgniter 支持两种类型的视图单元格:简单和受控。简单视图单元格可以从你选择的任何类和方法生成,并不必遵循任何规则,只要它返回一个字符串即可。受控视图单元格必须从扩展 ``Codeigniter\View\Cells\Cell`` 类的类生成,该类提供了额外的功能,使你的视图单元格更灵活、更快速地使用。

.. contents::
    :local:
    :depth: 2

.. _app-cells:

*******************
调用视图单元格
*******************

无论你使用哪种类型的视图单元格,都可以通过在任何视图中使用 ``view_cell()`` 辅助方法来调用它。第一个参数是要调用的类和方法的名称,第二个参数是要传递给该方法的参数数组。该方法必须返回一个字符串,该字符串将插入到调用 ``view_cell()`` 方法的视图中。
::

    <?= view_cell('App\Cells\MyClass::myMethod', ['param1' => 'value1', 'param2' => 'value2']) ?>

如果你没有包含类的完整命名空间,它将假定可以在 ``App\Cells`` 命名空间中找到它。所以,以下示例将尝试在 ``app/Cells/MyClass.php`` 中找到 ``MyClass`` 类。如果没有找到,将扫描所有命名空间,直到找到它,在每个命名空间的 ``Cells`` 子目录中搜索。
::

    <?= view_cell('MyClass::myMethod', ['param1' => 'value1', 'param2' => 'value2']) ?>

.. note:: 从 v4.3.0 和更高版本开始支持省略命名空间。

你也可以以键/值字符串的方式传递参数:
::

    <?= view_cell('MyClass::myMethod', 'param1=value1, param2=value2') ?>

************
简单单元格
************

简单单元格是从选择的方法返回字符串的类。警报消息单元格的一个简单示例如下:
::

    namespace App\Cells;

    class AlertMessage
    {
        public function show(array $params): string
        {
            return "<div class="alert alert-{$params['type']}">{$params['message']}</div>";
        }
    }

你可以在视图内这样调用它:
::

    <?= view_cell('AlertMessage::show', ['type' => 'success', 'message' => 'The user has been updated.']) ?>

另外,你可以使用与方法中的参数变量匹配的参数名称以提高可读性。
以这种方式使用时,在视图单元格调用中必须始终指定所有参数::

    // 在视图中
    <?= view_cell('Blog::recentPosts', 'category=codeigniter, limit=5') ?>

    // 在单元格中
    public function recentPosts(string $category, int $limit)
    {
        $posts = $this->blogModel->where('category', $category)
                                 ->orderBy('published_on', 'desc')
                                 ->limit($limit)
                                 ->get();

        return view('recentPosts', ['posts' => $posts]);
    }

.. _controlled-cells:

****************
受控单元格
****************

.. versionadded:: 4.3.0

受控单元格主要有两个目标:尽可能快速地构建单元格,并在视图需要时为视图提供额外的逻辑和灵活性。该类必须扩展 ``CodeIgniter\View\Cells\Cell``。它们应该在同一文件夹中有一个视图文件。按照惯例,类名应采用 PascalCase 后缀为 ``Cell``,视图应该是类名的 snake_case 版本,没有后缀。例如,如果有一个 ``MyCell`` 类,视图文件应该是 ``my.php``。

.. note:: 在 v4.3.5 之前的版本中,生成的视图文件以 ``_cell.php`` 结尾。尽管 v4.3.5 和更高版本将生成不带 ``_cell`` 后缀的视图文件,但现有的视图文件仍然会被定位和加载。

创建受控单元格
==========================

在最基本的级别上,你需要在类中实现的是公共属性。这些属性将自动供视图文件使用。将上面的 AlertMessage 作为受控单元格实现如下:
::

    // app/Cells/AlertMessageCell.php
    namespace App\Cells;

    use CodeIgniter\View\Cells\Cell;

    class AlertMessageCell extends Cell
    {
        public $type;
        public $message;
    }

    // app/Cells/alert_message.php
    <div class="alert alert-<?= esc($type, 'attr') ?>">
        <?= esc($message) ?>
    </div>

    // 在主视图中调用:
    <?= view_cell('AlertMessageCell', 'type=warning, message=Failed.') ?>

.. _generating-cell-via-command:

通过命令生成单元格
===========================

你还可以通过内置命令从 CLI 生成受控单元格。该命令是 ``php spark make:cell``。它接受一个参数,要创建的单元格的名称。名称应采用 PascalCase,类将在 ``app/Cells`` 目录中创建。视图文件也将在 ``app/Cells`` 目录中创建。

::

    > php spark make:cell AlertMessageCell

使用不同的视图
======================

你可以通过在类中设置 ``view`` 属性来指定自定义视图名称。视图的定位与正常视图相同。

::

    namespace App\Cells;

    use CodeIgniter\View\Cells\Cell;

    class AlertMessageCell extends Cell
    {
        public $type;
        public $message;

        protected $view = 'my/custom/view';
    }

自定义渲染
=======================

如果你需要更多地控制 HTML 的渲染,可以实现一个 ``render()`` 方法。此方法允许你执行其他逻辑并在需要时向视图传递额外的数据。 ``render()`` 方法必须返回一个字符串。要利用受控单元格的全部功能,你应该使用 ``$this->view()`` 代替正常的 ``view()`` 辅助函数。
::

    namespace App\Cells;

    use CodeIgniter\View\Cells\Cell;

    class AlertMessageCell extends Cell
    {
        public $type;
        public $message;

        public function render(): string
        {
            return $this->view('my/custom/view', ['extra' => 'data']);
        }
    }

计算属性
===================

如果你需要为一个或多个属性执行其他逻辑,可以使用计算属性。这需要将属性设置为 ``protected`` 或 ``private``,并实现一个由属性名称包围在 ``get`` 和 ``Property`` 之间的公共方法。
::

    // 在视图中初始化受保护的属性
    view_cell('AlertMessageCell', ['type' => 'note', 'message' => 'test']);

    // app/Cells/AlertMessageCell.php
    namespace App\Cells;

    use CodeIgniter\View\Cells\Cell;

    class AlertMessageCell extends Cell
    {
        protected $type;
        protected $message;
        private $computed;

        public function mount()
        {
            $this->computed = sprintf('%s - %s', $this->type, $this->message);
        }

        public function getComputedProperty(): string
        {
            return $this->computed;
        }

        public function getTypeProperty(): string
        {
            return $this->type;
        }

        public function getMessageProperty(): string
        {
            return $this->message;
        }
    }

    // app/Cells/alert_message.php
    <div>
        <p>type - <?= esc($type) ?></p>
        <p>message - <?= esc($message) ?></p>
        <p>computed: <?= esc($computed) ?></p>
    </div>

.. important:: 在单元格初始化期间,你不能设置声明为私有的属性。

呈现方法
====================

有时你需要对视图执行其他逻辑,但你不想将其作为参数传递。你可以实现一个将从单元格的视图本身调用的方法。这可以帮助提高视图的可读性。
::

    // app/Cells/RecentPostsCell.php
    namespace App\Cells;

    use CodeIgniter\View\Cells\Cell;

    class RecentPostsCell extends Cell
    {
        protected $posts;

        public function linkPost($post)
        {
            return anchor('posts/' . $post->id, $post->title);
        }
    }

    // app/Cells/recent_posts.php
    <ul>
        <?php foreach ($posts as $post): ?>
            <li><?= $this->linkPost($post) ?></li>
        <?php endforeach ?>
    </ul>

执行设置逻辑
======================

如果你需要在渲染视图之前执行其他逻辑,可以实现一个 ``mount()`` 方法。在类实例化后立即调用此方法,可用于设置其他属性或执行其他逻辑。

::

    namespace App\Cells;

    use CodeIgniter\View\Cells\Cell;

    class RecentPostsCell extends Cell
    {
        protected $posts;

        public function mount()
        {
            $this->posts = model('PostModel')->getRecent();
        }
    }

你可以通过将它们作为数组传递给 ``view_cell()`` 辅助函数来向 ``mount()`` 方法传递其他参数。传递的与 ``mount`` 方法参数名称匹配的任何参数都将被传递进去。
::

    // app/Cells/RecentPostsCell.php
    namespace App\Cells;

    use CodeIgniter\View\Cells\Cell;

    class RecentPostsCell extends Cell
    {
        protected $posts;

        public function mount(?int $categoryId)
        {
            $this->posts = model('PostModel')
                ->when($categoryId, function ($query, $category) {
                    return $query->where('category_id', $categoryId);
                })
                ->getRecent();
        }
    }

    // 在主视图中调用:
    <?= view_cell('RecentPostsCell', ['categoryId' => 5]) ?>

************
单元格缓存
************

你可以通过将要缓存数据的秒数作为第三个参数传入来缓存视图单元格调用的结果。这将使用当前配置的缓存引擎。
::

    // 缓存视图 5 分钟
    <?= view_cell('App\Cells\Blog::recentPosts', 'limit=5', 300) ?>

如果喜欢,你可以提供一个自定义名称代替自动生成的名称,方法是将新名称作为第四个参数传递::

    // 缓存视图 5 分钟
    <?= view_cell('App\Cells\Blog::recentPosts', 'limit=5', 300, 'newcacheid') ?>
