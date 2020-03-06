######################################
从CodeIgniter 3系列版本升级到4系列版本
######################################

CodeIgniter 4是对该框架的重写，并且不向前兼容（对以前的版本不兼容）。
比起升级你的应用，更为合适的是转换和重写它。当你做完了这一步（即已经升级到CodeIgniter4）之后，在CodeIgniter4的不同版本间进行升级就会轻而易举。

The "lean, mean and simple" philosophy has been retained, but the
implementation has a lot of differences, compared to CodeIgniter 3.

升级过程中并没有12步检查列表之类的东西。取而代之的是，在一个新的项目文件夹里开始CodeIgniter 4的重新部署 :doc:`开始与使用本框架 </installation/index>` ，
并开始转换和整合你的应用部件。下面我们会试着指出最需要注意的点。

CI4中我们并没有完全迁移和重写全部的CI3库！参考 `CodeIgniter 4 路线图 <https://forum.codeigniter.com/forum-33.html>`_ 中的最新列表！

在项目转换之前 **请务必阅读用户指南** !

**下载**

- CI4同样可以通过解压-运行的zip或tarball压缩文件的格式进行使用，其中包含有用户指南（在 `docs` 子目录中）
- 它也可以通过Composer进行安装

**命名空间**

- CI4构建基于PHP7.2+的版本，框架中除了辅助函数的所有部分都进行了命名空间标注。

**应用结构**

- ``application`` 目录被重命名为 ``app`` ，而框架中仍旧存在着 ``system`` 文件夹，有着与以往版本一样的功能。
- 本框架现在提供了一个 ``public`` 目录，希望你可以将其用于项目的根目录
- There is also a ``writable`` folder, to hold cache data, logs, and session data
- ``app`` 目录与CI3中的 ``application`` 目录类似，不过有着一些命名的变更，以及将一些子目录移动到 ``writable`` 目录下。
- 如今已经没有一个嵌套的 ``application/core`` 目录了，由于我们已经提供了一套不同的机制来扩展框架核心（如下所示）。

**加载类文件**

- 由于对框架组件的引用如今已作为属性动态注入到你的控制器中，现在已经不存在一个CodeIgniter的"超级对象"了。
- 类如今已经按需加载了，并且组件也是通过 ``Services`` 进行维护（服务）
- 类加载器自动处理PSR4风格的类文件定位，对于那些以 ``App``（application目录）和 ``CodeIgniter`` system目录） 为顶级命名空间的类。而通过对composer自动加载的支持与智能假设机制，框架甚至可以定位你的那些并未命名空间声明的模型和库文件。
- 你可以配置类的自动加载来支持任何你喜欢的应用结构，包括"HMVC"风格的（译者注：按等级划分的MVC模式，简单的解释就是把MVC又细分成了多个子MVC，每个模块就分成一个MVC）

**控制器**

- 控制器继承了 ``\\CodeIgniter\\Controller`` 类，而非 ``CI_Controller`` 类
- 控制器不再需要一个构造函数了（用于调用CI魔术方法），除非这是你自己定义的基类控制器的一部分
- CI 提供了 ``Request`` （请求）and ``Response`` （响应）对象供你使用，比起CI3的风格来说更为强大
- 如果你需要一个基类控制器（比如CI3中的MY_Controller），那么请在你需要的地方使用就行。比如 ``BaseController extends Controller`` ，并使用你自己的类来继承 ``BaseController``

**模型**

- 模型继承了 ``\\CodeIgniter\\Model`` 而非 ``CI_Model``
- CI4的模型拥有更多的功能，包括动态数据库连接，基础的CRUD（增删改查），模型内验证和自动分页功能。
- CI4 同样拥有可供你构建的 ``Entity`` （实体）类，用于实现更为丰富的数据表映射功能
- 取消使用CI3的 ``$this->load->model(x);`` ，而是使用模型的命名空间模式来调用 ``$this->x = new X();``。

**视图**

- 你的视图看起来与从前类似，但是却是以完全不同的方式调用……取消使用 ``$this->load->view(x);`` ，而是通过 ``echo view(x);``。
- CI4支持视图单元，以构建分片响应
- 模板处理器一如过往，但是在功能上有了显著的提升

**库**

- 你的应用类仍旧可以深入访问 ``app/Libraries``，但这不是必须的。
- 取消使用CI3的 ``$this->load->library(x);`` 调用方式，如今你可以使用组件的命名空间模式来调用 ``$this->x = new X();``

**辅助函数**

- 辅助函数与以往大致相似，不过有一部分被简化了

**事件**

- Hooks（钩子）如今已经被Events（事件）所取代
- 取消使用CI3的 ``$hook['post_controller_constructor']`` 调用方式，如今你可以使用命名空间 ``CodeIgniter\Events\Events;`` 下的 ``Events::on('post_controller_constructor', ['MyClass', 'MyFunction']);`` 。
- 事件保持启用状态并全局可用。

**扩展框架**

- 你不需要一个 ``core`` 目录来保存类似 ``MY_...`` 的框架组件扩展或替代品。
- 在库目录下，你不需要类似 ``MY_x`` 之类的类来继承或取代CI4的框架部分。
- 你可以在任何地方创建这样的类，并加入适当的自定义组件来代替默认的那些组件。
