##########
分页
##########

CodeIgniter 提供了一个非常简单但灵活的分页库，该库主题简单，可以在 Model 中使用，并能够在单个页面上支持多个分页器。

*******************
加载库
*******************

与 CodeIgniter 中的所有服务一样，它可以通过 ``Config\Services`` 进行加载，尽管通常它并不需要手动加载： ::

    $pager = \Config\Services::pager();

***************************
分页数据库结果
***************************

通常，可以使用分页器库对从数据库中检索到的结果进行分页。使用 :doc:`Model </models/model>` 类时，可以使用其内置的 ``paginate()``
方法来自动检索当前批次的结果，并设置 Pager 库，以便可以在控制器中使用它。它甚至可以通过 ``page=X`` 变量从当前 URL 读取当前应显示的页面。

在你的应用程序中提供用户的分页列表时，控制器的方法应类似于： ::

    <?php namespace App\Controllers;

    use CodeIgniter\Controller;

    class UserController extends Controller
    {
        public function index()
        {
            $model = new \App\Models\UserModel();

            $data = [
                'users' => $model->paginate(10),
                'pager' => $model->pager
            ];

            echo view('users/index', $data);
        }
    }

在上面的示例中，我们首先创建了 UserModel 的实例。然后，我们对它填充数据来发送到视图。第一个元素是来自数据库 **users** 的结果，
这将针对正确的页面进行检索，每页会返回 10 个用户。发送到视图的第二个必须的项是 Pager 实例本身。为了方便起见，Model 将会保留所使用的实例，
并将其存储在 public 类变量 **$pager** 中。因此，我们将其获取并将其分配给视图中的 $pager 变量。

然后，在视图内，我们需要告诉它应该在哪里显示结果的链接： ::

   <?= $pager->links() ?>

就是这样。Pager 类将为当前页面两侧超过两个页面的任何页面呈现“首页”和“末页”的链接，以及“下一页”和“上一页”的链接。

如果你更喜欢简单的输出，则可以使用 ``simpleLinks()`` 方法，它会输出“较旧”和“较新”链接而不是有着详细信息的分页链接： ::

    <?= $pager->simpleLinks() ?>

在后台中，库加载了一个视图文件，文件确定链接的格式，从而可以轻松地根据需要进行修改。有关如何完全自定义输出的详细信息，请参见下文。

分页多个结果
===========================

如果需要提供来自两个不同的结果集的链接，则可以将组名传递给大多数分页方法，以使数据分开： ::

    // 在控制器文件中：
    public function index()
    {
        $userModel = new \App\Models\UserModel();
        $pageModel = new \App\Models\PageModel();

        $data = [
            'users' => $userModel->paginate(10, 'group1'),
            'pages' => $pageModel->paginate(15, 'group2'),
            'pager' => $userModel->pager
        ];

        echo view('users/index', $data);
    }

    // 在视图文件中：
    <?= $pager->links('group1') ?>
    <?= $pager->simpleLinks('group2') ?>

手动分页
=================

你可能会发现有时候只需要根据已知数据来创建分页。这时你可以使用 ``makeLinks()`` 方法来手动创建链接，这个方法分别将当前页面，
每页的结果数和项目总数作为第一个，第二个和第三个参数： ::

    <?= $pager->makeLinks($page, $perPage, $total) ?>

默认情况下，这将以正常方式将链接显示为一组链接，你还可以通过将模板名称作为第四个参数传入来更改使用的显示模板。在以下各节中可以找到更多详细信息。

::

    <?= $pager->makeLinks($page, $perPage, $total, 'template_name') ?>

也可以使用 URI 字段（segment）而不是用查询参数来表示页码，只需指定字段号即可用作的第五个参数 ``makeLinks()`` 。然后，由分页器生成的 URI 看起来会像
*https://domain.tld/model/『页码』* 而不是 *https://domain.tld/model?page=『页码』* 。
::

<?= $pager->makeLinks($page, $perPage, $total, 'template_name', $segment) ?>

请注意： ``$segment`` 的值不能大于 URI 字段的数量加 1。

如果你需要在一页上显示很多分页器，那么定义组的其他参数可能会有所帮助： ::

	$pager = service('pager');
	$pager->setPath('path/for/my-group', 'my-group'); // 另外，你可以为每个组定义路径
	$pager->makeLinks($page, $perPage, $total, 'template_name', $segment, 'my-group');

仅使用预期查询进行分页
=====================================

默认情况下，所有 GET 查询都显示在分页链接中。

例如，当访问 URL *http://domain.tld?search=foo&order=asc&hello=i+am+here&page=2* 时，可以生成 页面 3 链接以及其他链接，如下所示： ::

    echo $pager->links();
    // 页面 3 链接： http://domain.tld?search=foo&order=asc&hello=i+am+here&page=3

``only()`` 方法还允许你将其限制为仅已预期的查询： ::

    echo $pager->only(['search', 'order'])->links();
    // 页面 3 链接： http://domain.tld?search=foo&order=asc&page=3

*page* 查询默认情况下启用。并 ``only()`` 在所有分页链接中起作用。

*********************
自定义链接
*********************

查看配置
==================

当链接呈现到页面时，它们使用视图文件来渲染 HTML。你可以通过编辑 **app/Config/Pager.php** 来轻松地更改使用的视图： ::

    public $templates = [
        'default_full'   => 'CodeIgniter\Pager\Views\default_full',
        'default_simple' => 'CodeIgniter\Pager\Views\default_simple'
    ];

设置存储应使用的视图的别名和 :doc:`命名空间的视图路径 </outgoing/views>` 。 *default_full* 和 *default_simple*
视图会分别被用于 ``links()`` 和 ``simpleLinks()`` 方法。要更改在整个应用程序范围内显示的方式，你可以在处分配一个新视图。

例如，假设你创建一个与 Foundation CSS 框架一起使用的新视图文件，然后将文件放在 **app/Views/Pagers/foundation_full.php** 中。
由于 **application** 目录的命名空间为 ``App`` ，并且其下的所有目录都直接映射到命名空间的各个部分，因此你可以通过其命名空间找到视图文件： ::

    'default_full'   => 'App\Views\Pagers\foundation_full',

但是，由于它位于标准的 **app/Views** 目录下，因此不需要命名空间，因为``view()`` 方法可以按文件名定位它。在这种情况下，你只需提供子目录和文件名： ::

    'default_full'   => 'Pagers/foundation_full',

创建视图并将其配置好后，将会自动使用它。你不必替换现有模板。你也可以在配置文件中根据需要创建的任意数量的其他模板。常见的情况是你的应用程序的前端和后端需要不同的样式。

::

    public $templates = [
        'default_full'   => 'CodeIgniter\Pager\Views\default_full',
        'default_simple' => 'CodeIgniter\Pager\Views\default_simple',
        'front_full'     => 'App\Views\Pagers\foundation_full',
    ];

配置完成后，你可以指定它作为 ``links()`` 、 ``simpleLinks()`` 以及 ``makeLinks()`` 方法的最后的一个参数： ::

    <?= $pager->links('group1', 'front_full') ?>
    <?= $pager->simpleLinks('group2', 'front_full') ?>
    <?= $pager->makeLinks($page, $perPage, $total, 'front_full') ?>

创建视图
=================

创建新视图时，只需要创建生成分页链接本身所需的代码。你不应该创建不必要的包装 div，因为它可能会在多个地方使用，并且这会限制它们的用途。这里通过向你展示现有的 default_full 模板，来演示创建新视图： ::

    <?php $pager->setSurroundCount(2) ?>

    <nav aria-label="Page navigation">
        <ul class="pagination">
        <?php if ($pager->hasPrevious()) : ?>
            <li>
                <a href="<?= $pager->getFirst() ?>" aria-label="First">
                    <span aria-hidden="true">First</span>
                </a>
            </li>
            <li>
                <a href="<?= $pager->getPrevious() ?>" aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                </a>
            </li>
        <?php endif ?>

        <?php foreach ($pager->links() as $link) : ?>
            <li <?= $link['active'] ? 'class="active"' : '' ?>>
                <a href="<?= $link['uri'] ?>">
                    <?= $link['title'] ?>
                </a>
            </li>
        <?php endforeach ?>

        <?php if ($pager->hasNext()) : ?>
            <li>
                <a href="<?= $pager->getNext() ?>" aria-label="Previous">
                    <span aria-hidden="true">&raquo;</span>
                </a>
            </li>
            <li>
                <a href="<?= $pager->getLast() ?>" aria-label="Last">
                    <span aria-hidden="true">Last</span>
                </a>
            </li>
        <?php endif ?>
        </ul>
    </nav>

**setSurroundCount()**

在第一行中，``setSurroundCount()`` 方法指定了我们要显示到当前页面链接两侧的两个链接。它接受的唯一参数是要显示的链接数。

**hasPrevious()** & **hasNext()**

如果根据传递给 ``setSurroundCount`` 的值，如果当前页面的任何一侧上可以显示更多链接，则这些方法将返回布尔值 true。例如，假设我们有 20 页数据，当前页面是第 3 页，如果周围的计数是 2，则以下链接将显示在列表中：1、2、3、4 和 5。由于要显示的第一个链接是第 1 页，但是页面 0 并不存在，因此 ``hasPrevious()`` 会返回 **false** 。但是， ``hasNext()`` 将返回 **true** ，因为在第 5 页之后还有 15 个额外的结果页。

**getPrevious()** & **getNext()**

这两个方法返回编号链接两侧上一页或下一页结果的 URL。有关完整说明，请参见上一段。

**getFirst()** & **getLast()**

与 ``getPrevious()`` 和 ``getNext()`` 类似，这两个方法返回指向结果集中第一页和最后一页的链接。

**links()**

返回所有有关编号链接的数据数组。每个链接的数组都包含链接的 uri，标题（只是数字）和一个布尔值，布尔值表示链接为当前链接还是活动链接： ::

	$link = [
		'active' => false,
		'uri'    => 'http://example.com/foo?page=2',
		'title'  => 1
	];
