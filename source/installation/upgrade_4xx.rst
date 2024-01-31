#########################
从 3.x 升级到 4.x
#########################

CodeIgniter 4 是框架的重写,并且不向后兼容。将你的应用程序转换更合适,而不是升级它。一旦你完成了转换,从 CodeIgniter 4 的一个版本升级到下一个版本将很简单。

“精简、敏捷、简单”的理念仍然保留,但实现与 CodeIgniter 3 有很多不同。

升级没有 12 步检查表。相反,请在一个新的项目文件夹中使用 CodeIgniter 4 的副本开始,
选择 :doc:`你希望的安装和使用方式 </installation/index>`, 然后转换和集成你的应用组件。
我们将尽量指出这里最重要的注意事项。

为了升级你的项目,我们总结出两项主要工作。首先,有一些对每个项目都很重要的一般调整,必须处理。其次是 CodeIgniter 构建的库,包含一些最重要的函数。这些库可以互相独立工作,所以你必须一一查看它们。

**在启动项目转换之前,请阅读用户指南!**

.. contents::
    :local:
    :depth: 2

一般调整
*******************

下载
=========

- CI4 仍以 :doc:`ready-to-run 压缩包或 tarball <../installation/installing_manual>` 形式提供。
- 它也可以使用 :doc:`Composer <../installation/installing_composer>` 安装。

命名空间
==========

- CI4 是为 PHP 7.4+ 构建的,框架中的所有内容都使用了命名空间,除了 helper 和 lang 文件。

应用程序结构
=====================

- **application** 文件夹重命名为 **app**,框架仍然有 **system** 文件夹,与以前的解释相同。
- 框架现在提供了 **public** 文件夹,旨在作为你的应用程序的文档根目录。
- ``defined('BASEPATH') OR exit('No direct script access allowed');`` 这一行不是必需的,因为在默认配置下, **public** 文件夹之外的文件不可访问。
  并且 CI4 不再定义常量 ``BASEPATH``,所以在所有文件中删除该行。
- 还有一个 **writable** 文件夹,用于保存缓存数据、日志和 session 数据。
- **app** 文件夹与 CI3 的 **application** 非常相似,只是一些名称更改,一些子文件夹移到了 **writable** 文件夹。
- 不再有嵌套的 **application/core** 文件夹,因为我们有一个不同的机制来扩展框架组件(见下文)。

路由
=======

- 默认情况下自动路由被禁用。你需要 :ref:`定义所有路由 <defined-route-routing>`。
- 如果你希望以与 CI3 相同的方式使用自动路由,则需要启用 :ref:`auto-routing-legacy`。
- CI4 还具有可选的新的更安全的 :ref:`auto-routing-improved`。

模型、视图和控制器
==========================

- CodeIgniter 基于 MVC 概念。因此,模型、视图和控制器的更改是你必须处理的最重要的事项之一。
- 在 CodeIgniter 4 中,模型现在位于 **app/Models** 中,在打开的 php 标记之后,你必须添加 ``namespace App\Models;`` 以及 ``use CodeIgniter\Model;``。最后一步是将 ``extends CI_Model`` 替换为 ``extends Model``。
- CodeIgniter 4 的视图已移至 **app/Views**。此外,你必须将加载视图的语法从 ``$this->load->view('directory_name/file_name')`` 更改为 ``echo view('directory_name/file_name');``。
- CodeIgniter 4 的控制器必须移至 **app/Controllers**。之后,在打开的 php 标记后添加 ``namespace App\Controllers;``。最后,将 ``extends CI_Controller`` 替换为 ``extends BaseController``。
- 有关更多信息,我们推荐你参考以下升级指南,这些指南将为你提供一些分步说明,以在 CodeIgniter4 中转换 MVC 类:

.. toctree::
    :titlesonly:

    upgrade_models
    upgrade_views
    upgrade_controllers

类加载
=============

- 不再有 CodeIgniter “超级对象”,其中框架组件引用以属性的形式神奇地注入到你的控制器中。
- 类根据需要进行实例化,框架组件通过 :doc:`../concepts/services` 进行管理。
- :doc:`自动加载程序 <../concepts/autoloader>` 自动使用 PSR-4 风格定位类,在 ``App`` (**app** 文件夹)和 ``CodeIgniter`` (即 **system** 文件夹)顶级命名空间内;具有 Composer 自动加载支持。
- 你可以配置类加载以支持你最习惯的任何应用程序结构,包括“HMVC”风格。
- CI4 提供可以像 CI3 中的 ``$this->load`` 一样加载类和共享实例的 :doc:`../concepts/factories`。

库
=========

- 你的应用类仍然可以放在 **app/Libraries** 中,但不必这样做。
- 不再使用 CI3 的 ``$this->load->library('x');`` ,现在可以使用 ``$this->x = new \App\Libraries\X();``,遵循你组件的命名空间约定。或者,你可以使用 :doc:`../concepts/factories`:``$this->x = \CodeIgniter\Config\Factories::libraries('X');``。

辅助函数
===========

- :doc:`辅助函数 <../general/helpers>` 与以前基本相同,尽管有些进行了简化。
- 从 v4.3.0 开始,你可以通过 **app/Config/Autoload.php** 自动加载辅助函数,就像 CI3 一样。
- CodeIgniter 3 中的一些辅助函数在版本 4 中不再存在。对于所有这些辅助函数,你必须找到一种新的方法来实现你的函数。这些辅助函数是 `CAPTCHA Helper <https://www.codeigniter.com/userguide3/helpers/captcha_helper.html>`_,
  `Email Helper <https://www.codeigniter.com/userguide3/helpers/email_helper.html>`_,
  `Path Helper <https://www.codeigniter.com/userguide3/helpers/path_helper.html>`_ 和
  `Smiley Helper <https://www.codeigniter.com/userguide3/helpers/smiley_helper.html>`_。
- CI3 的 `Download Helper <https://www.codeigniter.com/userguide3/helpers/download_helper.html>`_
  已移除。你需要在使用 ``force_download()`` 的地方使用 Response 对象。
  请参阅 :ref:`force-file-download`。
- CI3 的 `Language Helper <https://www.codeigniter.com/userguide3/helpers/language_helper.html>`_
  已移除。但在 CI4 中 ``lang()`` 始终可用。请参阅 :php:func:`lang()`。
- CI3 的 `Typography Helper <https://www.codeigniter.com/userguide3/helpers/typography_helper.html>`_
  在 CI4 中将是 :doc:`排版库 <../libraries/typography>`。
- CI3 的 `Directory Helper <https://www.codeigniter.com/userguide3/helpers/directory_helper.html>`_
  和 `File Helper <https://www.codeigniter.com/userguide3/helpers/file_helper.html>`_ 在 CI4 中将是 :doc:`../helpers/filesystem_helper`。
- CI3 的 `String Helper <https://www.codeigniter.com/userguide3/helpers/string_helper.html>`_ 函数
  在 CI4 的 :doc:`../helpers/text_helper` 中。
- 在 CI4 中, ``redirect()`` 与 CI3 中的完全不同。
    - `redirect() 文档 CodeIgniter 3.X <https://codeigniter.com/userguide3/helpers/url_helper.html#redirect>`_
    - `redirect() 文档 CodeIgniter 4.X <../general/common_functions.html#redirect>`_
    - 在 CI4 中，:php:func:`redirect()` 返回一个 ``RedirectResponse`` 实例，而不是重定向并终止脚本执行。你必须从控制器或控制器过滤器中返回它。
    - 在调用 ``redirect()`` 之前设置的 Cookie 和 Header 不会自动携带到 ``RedirectResponse``。如果你想发送它们，你需要手动调用 ``withCookies()`` 或 ``withHeaders()``。
    - 你需要将 CI3 的 ``redirect('login/form')`` 改为 ``return redirect()->to('login/form')``。

钩子
=====

- `钩子 <https://www.codeigniter.com/userguide3/general/hooks.html>`_ 已被 :doc:`../extending/events` 替换。
- 不再使用 CI3 的 ``$hook['post_controller_constructor']``,现在使用
  ``Events::on('post_controller_constructor', ['MyClass', 'MyFunction']);``,命名空间为 ``CodeIgniter\Events\Events;``。
- 事件始终启用,并全局可用。
- 挂钩点 ``pre_controller`` 和 ``post_controller`` 已被移除。使用 :doc:`../incoming/filters` 代替。
- 挂钩点 ``display_override`` 和 ``cache_override`` 已被移除。因为基础方法已被移除。
- 挂钩点 ``post_system`` 已经移动到在发送最终渲染页面之前。

错误处理
==============

- CI4 中的行为已经稍有更改。

  - 在 CI3 中，行为在 **index.php** 文件中设置：

      - 错误级别由 ``error_reporting()`` 设置的错误将被记录（但根据 ``log_threshold`` 设置，它们可能不会被写入日志文件）。
      - 错误级别为 ``E_ERROR | E_PARSE | E_COMPILE_ERROR | E_CORE_ERROR | E_USER_ERROR`` 的错误将停止框架处理，无论在 ``error_reporting()`` 中设置的错误级别如何。
  - 在 CI4 中，行为在 **app/Config/Boot/{environment}.php** 文件中设置：

      - 错误级别由 ``error_reporting()`` 设置的错误将被记录（但根据 ``Config\Logger::$threshold`` 设置，它们可能不会被写入日志文件）。
      - 所有不被 ``error_reporting()`` 忽略的错误都将停止框架处理。

扩展框架
=======================

- 你不需要 **core** 文件夹来保存 ``MY_...`` 框架组件扩展或替换文件。
- 你不需要在 libraries 文件夹中使用 ``MY_X`` 类来扩展或替换 CI4 组件。
- 将这些类放在任何地方,并在 **app/Config/Services.php** 中添加适当的服务方法来加载你的组件,而不是默认组件。
- 详细信息请参见 :doc:`../extending/core_classes`。

升级库
*******************

- 你的应用类仍然可以放在 **app/Libraries** 中,但不必这样做。
- 不再使用 CI3 的 ``$this->load->library('x');``,现在可以使用 ``$this->x = new \App\Libraries\X();``,遵循你组件的命名空间约定。或者,你可以使用 :doc:`../concepts/factories`:``$this->x = \CodeIgniter\Config\Factories::libraries('X');``。
- CodeIgniter 3 中的一些库在版本 4 中不再存在。对于所有这些库,你必须找到一种新的方法来实现你的函数。这些库是 `日历 <http://codeigniter.com/userguide3/libraries/calendar.html>`_,
  `FTP <http://codeigniter.com/userguide3/libraries/ftp.html>`_,
  `Javascript <http://codeigniter.com/userguide3/libraries/javascript.html>`_,
  `购物车 <http://codeigniter.com/userguide3/libraries/cart.html>`_,
  `引用通告 <http://codeigniter.com/userguide3/libraries/trackback.html>`_,
  `XML-RPC /服务器 <http://codeigniter.com/userguide3/libraries/xmlrpc.html>`_ 和
  `Zip 编码 <http://codeigniter.com/userguide3/libraries/zip.html>`_。
- CI3 的 `Input <http://codeigniter.com/userguide3/libraries/input.html>`_ 对应于 CI4 的 :doc:`传入请求 </incoming/incomingrequest>`。
- CI3 的 `Output <http://codeigniter.com/userguide3/libraries/output.html>`_ 对应于 CI4 的 :doc:`响应 </outgoing/response>`。
- 存在于两个 CodeIgniter 版本中的所有其他库都可以通过一些调整来升级。
  最重要和使用最广泛的库都有一个升级指南,它将通过简单的步骤和示例帮助你调整代码。

.. toctree::
    :titlesonly:

    upgrade_configuration
    upgrade_database
    upgrade_emails
    upgrade_encryption
    upgrade_file_upload
    upgrade_html_tables
    upgrade_localization
    upgrade_migrations
    upgrade_pagination
    upgrade_responses
    upgrade_routing
    upgrade_security
    upgrade_sessions
    upgrade_validations
    upgrade_view_parser
