#########################
从 3.x 升级到 4.x
#########################

CodeIgniter 4 是对框架的全面重写，与旧版本不向后兼容。
因此，更准确的说法是“转换”应用，而不是“升级”应用。
完成转换之后，从某个 CodeIgniter 4 版本升级到下一个版本将会非常简单。

“精简、高效、易用”的理念得以保留，但与 CodeIgniter 3 相比，
其实现方式存在大量差异。

这里并不存在一个 12 步的升级清单。相反，应当从一个全新的
CodeIgniter 4 项目文件夹开始，
:doc:`按照你喜爱的方式安装和使用 </installation/index>`，
然后逐步转换并集成你的应用组件。
我们会在这里指出最重要的注意事项。

在升级项目时，我们总结了两个主要任务。首先是一些对所有项目都适用、
且必须处理的通用调整。其次是构成 CodeIgniter 的各个类，
它们包含了最重要的功能。这些类彼此独立运作，
因此需要逐个检查和处理。

**在开始转换项目前，请务必阅读用户指南！**

.. contents::
    :local:
    :depth: 2

通用调整
*******************

下载
=========

- CI4 仍然提供 :doc:`可直接运行的 zip 或 tarball 包 <../installation/installing_manual>`。
- 也可以通过 :doc:`Composer <../installation/installing_composer>` 进行安装。

命名空间
==========

- CI4 基于 PHP 8.1+ 构建，框架中的所有内容都使用命名空间，
  辅助函数和语言文件除外。

应用程序结构
=====================

.. important::
    **index.php** 已不再位于项目根目录！它已被移动到 **public** 文件夹中，
    以提升安全性并实现组件分离。

    这意味着你需要将 Web 服务器配置为指向项目的 **public** 文件夹，
    而不是项目根目录。

    如果使用共享主机，请参阅 :ref:`deployment-to-shared-hosting-services`。

- **application** 文件夹已重命名为 **app**，框架仍然包含 **system** 文件夹，
  其含义与之前一致。
- 框架现在提供了一个 **public** 文件夹，作为应用的文档根目录。
- ``defined('BASEPATH') OR exit('No direct script access allowed');`` 这一行已不再需要，
  因为在标准配置下，**public** 文件夹之外的文件无法被直接访问。
  同时，CI4 也不再定义 ``BASEPATH`` 常量，因此需要在所有文件中移除该行。
- 还新增了 **writable** 文件夹，用于存放缓存数据、日志和 Session 数据。
- **app** 文件夹在结构上与 CI3 的 **application** 非常相似，
  但有一些名称变更，且部分子目录被移动到了 **writable** 文件夹中。
- 不再存在嵌套的 **application/core** 文件夹，
  因为 CI4 使用了不同的机制来扩展框架组件（见下文）。

路由
=======

- 自动路由默认是禁用的。你需要默认 :ref:`显式定义所有路由
  <defined-route-routing>`。
- 如果希望以与 CI3 相同的方式使用自动路由，需要启用
  :ref:`auto-routing-legacy`。
- CI4 还提供了一个可选的、更安全的 :ref:`auto-routing-improved`。

模型、视图与控制器
==========================

- CodeIgniter 基于 MVC 概念，因此模型、视图和控制器的变更是最重要的部分之一。
- 在 CodeIgniter 4 中，模型位于 **app/Models**，并且需要在 PHP 开始标签之后添加
  ``namespace App\Models;`` 以及 ``use CodeIgniter\Model;``。
  最后一步是将 ``extends CI_Model`` 替换为 ``extends Model``。
- CodeIgniter 4 的视图已移动到 **app/Views**。此外，
  加载视图的语法需要从 ``$this->load->view('directory_name/file_name')``
  改为 ``echo view('directory_name/file_name');``。
- CodeIgniter 4 的控制器需要移动到 **app/Controllers**。
  然后在 PHP 开始标签后添加 ``namespace App\Controllers;``。
  最后，将 ``extends CI_Controller`` 替换为 ``extends BaseController``。
- 有关更多信息，建议参考以下升级指南，
  它们提供了将 CodeIgniter 4 中 MVC 类进行转换的分步说明：

.. toctree::
    :titlesonly:

    upgrade_models
    upgrade_views
    upgrade_controllers

核心类变更
==================

- 输入类
    - CI3 的 `输入类 <https://codeigniter.org.cn/userguide3/libraries/input.html>`_
      对应于 CI4 的 :doc:`IncomingRequest </incoming/incomingrequest>`。
    - 由于历史原因，CI3 和 CI4 曾使用不正确的 HTTP 方法名称，如
      “get”和“post”。自 v4.5.0 起，CI4 使用正确的 HTTP 方法名称，
      如 “GET”和“POST”。
- 输出类
    - CI3 的 `输出类 <https://codeigniter.org.cn/userguide3/libraries/output.html>`_
      对应于 CI4 的 :doc:`HTTP 响应 </outgoing/response>`。

类加载
=============

- 不再存在 CodeIgniter 的“超级对象”，
  即框架组件不会再自动作为属性注入到控制器中。
- 类会在需要时实例化，框架组件由
  :doc:`../concepts/services` 进行管理。
- :doc:`自动加载器 <../concepts/autoloader>` 会自动处理
  PSR-4 风格的类定位，适用于 ``App`` （即 **app** 文件夹）
  和 ``CodeIgniter`` （即 **system** 文件夹）这两个顶级命名空间，
  并支持 Composer 自动加载。
- 你可以配置类加载方式，以支持任何你习惯的应用结构，
  包括 “HMVC” 风格。
- CI4 提供了 :doc:`../concepts/factories`，
  可像 CI3 中的 ``$this->load`` 一样加载类并共享实例。

类库
=========

- 应用类库仍然可以放在 **app/Libraries** 中，但并非强制要求。
- 不再使用 CI3 的 ``$this->load->library('x');``，
  而是可以按照命名空间的约定使用
  ``$this->x = new \App\Libraries\X();``。
  或者，也可以使用 :doc:`../concepts/factories`：
  ``$this->x = \CodeIgniter\Config\Factories::libraries('X');``。

辅助函数
========

- :doc:`辅助函数 <../general/helpers>` 与之前基本一致，
  但部分已被简化。
- 自 v4.3.0 起，可以像 CI3 一样，通过 **app/Config/Autoload.php**
  自动加载辅助函数。
- CodeIgniter 3 中的一些辅助函数在 4.x 中已不再存在。
  对于这些辅助函数，需要寻找新的实现方式。
  包括：`验证码辅助函数 <https://codeigniter.org.cn/userguide3/helpers/captcha_helper.html>`_、
  `Email 辅助函数 <https://codeigniter.org.cn/userguide3/helpers/email_helper.html>`_、
  `路径辅助函数 <https://codeigniter.org.cn/userguide3/helpers/path_helper.html>`_、
  `表情辅助函数 <https://codeigniter.org.cn/userguide3/helpers/smiley_helper.html>`_。
- CI3 中的 `下载辅助函数 <https://codeigniter.org.cn/userguide3/helpers/download_helper.html>`_
  已被移除。在使用 ``force_download()`` 的地方，需要改用 Response 对象。
  参见 :ref:`force-file-download`。
- CI3 中的 `语言辅助函数 <https://codeigniter.org.cn/userguide3/helpers/language_helper.html>`_
  已被移除，但 ``lang()`` 在 CI4 中始终可用。参见 :php:func:`lang()`。
- CI3 中的 `排版辅助函数 <https://codeigniter.org.cn/userguide3/helpers/typography_helper.html>`_
  在 CI4 中变为 :doc:`Typography 类 <../libraries/typography>`。
- CI3 中的 `目录辅助函数 <https://codeigniter.org.cn/userguide3/helpers/directory_helper.html>`_
  和 `文件辅助函数 <https://codeigniter.org.cn/userguide3/helpers/file_helper.html>`_
  在 CI4 中合并为 :doc:`../helpers/filesystem_helper`。
- CI3 中 `字符串辅助函数 <https://codeigniter.org.cn/userguide3/helpers/string_helper.html>`_
  的函数在 CI4 中包含于 :doc:`../helpers/text_helper`。
- 在 CI4 中，``redirect()`` 与 CI3 有完全不同的行为：
    - `redirect() 文档 CodeIgniter 3.x <https://codeigniter.org.cn/userguide3/helpers/url_helper.html#redirect>`_
    - `redirect() 文档 CodeIgniter 4.x <../general/common_functions.html#redirect>`_
    - 在 CI4 中，:php:func:`redirect()` 返回一个 ``RedirectResponse`` 实例，
      而不是直接重定向并终止脚本执行。
      必须在控制器或控制器过滤器中返回该实例。
    - 在调用 ``redirect()`` 之前设置的 Cookie 和 HTTP 标头
      不会自动携带到 ``RedirectResponse`` 中。
      如果需要发送它们，必须手动调用 ``withCookies()``
      或 ``withHeaders()``。
    - 需要将 CI3 的 ``redirect('login/form')`` 修改为
      ``return redirect()->to('login/form')``。

钩子
=====

- CI3 的 `钩子 <https://codeigniter.org.cn/userguide3/general/hooks.html>`_
  已被 :doc:`../extending/events` 所取代。
- 不再使用 CI3 的 ``$hook['post_controller_constructor']``，
  而是使用
  ``Events::on('post_controller_constructor', ['MyClass', 'MyFunction']);``，
  并使用命名空间 ``CodeIgniter\Events\Events;``。
- 事件始终处于启用状态，并在全局范围内可用。
- ``pre_controller`` 和 ``post_controller`` 挂钩点已被移除，
  请改用 :doc:`../incoming/filters`。
- ``display_override`` 和 ``cache_override`` 挂钩点已被移除，
  因为相应的基础方法已不存在。
- ``post_system`` 挂钩点被移动到最终渲染页面发送之前。

错误处理
==============

- CI4 中的错误处理行为略有变化。

  - 在 CI3 中，相关行为在 **index.php** 文件中设置：

      - 由 ``error_reporting()`` 设置的错误级别的错误会被记录
        （但是否写入日志文件取决于 ``log_threshold`` 设置）。
      - 错误级别为
        ``E_ERROR | E_PARSE | E_COMPILE_ERROR | E_CORE_ERROR | E_USER_ERROR``
        的错误会停止框架执行，
        不受 ``error_reporting()`` 设置的影响。
  - 在 CI4 中，相关行为在 **app/Config/Boot/{environment}.php**
    文件中设置：

      - 由 ``error_reporting()`` 设置的错误级别的错误会被记录
        （但是否写入日志文件取决于 ``Config\Logger::$threshold`` 设置）。
      - 所有未被 ``error_reporting()`` 忽略的错误
        都会停止框架执行。

扩展框架
=======================

- 不再需要 **core** 文件夹来存放 ``MY_...`` 形式的
  框架组件扩展或替换。
- 不再需要在 libraries 文件夹中使用 ``MY_X`` 类
  来扩展或替换 CI4 的组件。
- 可以在任意位置创建这些类，并在 **app/Config/Services.php**
  中添加相应的服务方法，
  以加载你的组件来替代默认组件。
- 详情请参阅 :doc:`../extending/core_classes`。

升级类库
*******************

- 应用类仍然可以放在 **app/Libraries** 中，但并非强制要求。
- 不再使用 CI3 的 ``$this->load->library('x');``，
  而是可以使用
  ``$this->x = new \App\Libraries\X();``，
  遵循命名空间的约定来组织组件。
  或者，也可以使用 :doc:`../concepts/factories`：
  ``$this->x = \CodeIgniter\Config\Factories::libraries('X');``。
- CodeIgniter 3 中的一些类在 4.x 中已不再存在。
  对于这些类，需要寻找新的实现方式。
  包括：
  `日历类 <https://codeigniter.org.cn/userguide3/libraries/calendar.html>`_、
  `FTP 类 <https://codeigniter.org.cn/userguide3/libraries/ftp.html>`_、
  `Javascript 类 <https://codeigniter.org.cn/userguide3/libraries/javascript.html>`_、
  `购物车类 <https://codeigniter.org.cn/userguide3/libraries/cart.html>`_、
  `引用通告类 <https://codeigniter.org.cn/userguide3/libraries/trackback.html>`_、
  `XML-RPC 与 XML-RPC 服务器类 <https://codeigniter.org.cn/userguide3/libraries/xmlrpc.html>`_，
  以及 `Zip 编码类 <https://codeigniter.org.cn/userguide3/libraries/zip.html>`_。
- 其余在两个 CodeIgniter 版本中都存在的类，
  可以通过一些调整完成升级。
  最重要、最常用的类都提供了升级指南，
  可通过简单的步骤和示例帮助你调整代码。

.. toctree::
    :titlesonly:

    upgrade_configuration
    upgrade_database
    upgrade_emails
    upgrade_encryption
    upgrade_file_upload
    upgrade_html_tables
    upgrade_images
    upgrade_localization
    upgrade_migrations
    upgrade_responses
    upgrade_pagination
    upgrade_routing
    upgrade_security
    upgrade_sessions
    upgrade_validations
    upgrade_view_parser
