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

- CI4 is still available as a ready-to-run zip or tarball, which
  includes the user guide (though in the `docs` subfolder
- It can also be installed using Composer

**命名空间**

- CI4 is built for PHP7.2+, and everything in the framework is namespaced, except for the helpers.

**应用结构**

- The ``application`` folder is renamed as ``app`` and
  the framework still has ``system`` folders, with the same
  interpretation as before
- The framework now provides for a ``public`` folder, intended as the document
  root for your app
- There is also a ``writable`` folder, to hold cache data, logs, and session data
- The ``app`` folder looks very similar to ``application`` for CI3, with some
  name changes, and some subfolders
  moved to the ``writable`` folder
- There is no longer a nested ``application/core`` folder, as we have
  a different mechanism for extending framework components (see below)

**加载类文件**

- There is no longer a CodeIgniter "superobject", with framework component
  references magically injected as properties of your controller
- Classes are instantiated where needed, and components are managed
  by ``Services``
- The class loader automatically handles PSR4 style class locating,
  within the ``App`` (application) and ``CodeIgniter`` (i.e. system) top level
  namespaces; with composer autoloading support, and even using educated
  guessing to find your models and libraries if they are in the right
  folder even though not namespaced
- You can configure the class loading to support whatever application structure
  you are most comfortable with, including the "HMVC" style

**控制器**

- Controllers extend \\CodeIgniter\\Controller instead of CI_Controller
- They don't use a constructor any more (to invoke CI "magic") unless
  that is part of a base controller you make
- CI provides ``Request`` and ``Response`` objects for you to work with -
  more powerful than the CI3-way
- If you want a base controller (MY_Controller in CI3), make it
  where you like, e.g. BaseController extends Controller, and then
  have your controllers extend it

**模型**

- Models extend \\CodeIgniter\\Model instead of CI_Model
- The CI4 model has much more functionality, including automatic
  database connection, basic CRUD, in-model validation, and
  automatic pagination
- CI4 also has the ``Entity`` class you can build on, for
  richer data mapping to your database tables
- Instead of CI3's ``$this->load->model(x);``, you would now use
  ``$this->x = new X();``, following namespaced conventions for your component

**视图**

- Your views look much like before, but they are invoked differently ...
  instead of CI3's ``$this->load->view(x);`` you can use ``echo view(x);``
- CI4 supports view "cells", to build your response in pieces
- The template parser is still there, but substantially
  enhanced

**库**

- Your app classes can still go inside ``app/Libraries``, but they
  don't have to
- Instead of CI3's ``$this->load->library(x);`` you can now use
  ``$this->x = new X();``, following namespaced conventions for your
  component

**辅助函数**

- Helpers are pretty much the same as before, though some have been simplified

**事件**

- Hooks have been replaced by Events
- Instead of CI3's ``$hook['post_controller_constructor']`` you now use ``Events::on('post_controller_constructor', ['MyClass', 'MyFunction']);``, with the namespace ``CodeIgniter\Events\Events;``
- Events are always enabled, and are available globally

**扩展框架**

- You don't need a ``core`` folder to hold ``MY_...`` framework
  component extensions or replacements
- You don't need ``MY_x`` classes inside your libraries folder
  to extend or replace CI4 pieces
- Make any such classes where you like, and add appropriate
  service methods in ``app/Config/Services.php`` to load
  your components instead of the default ones
