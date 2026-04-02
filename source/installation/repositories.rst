CodeIgniter 仓库
########################

.. contents::
    :local:
    :depth: 2

codeigniter4 组织
=========================

CodeIgniter 4 开源项目拥有自己的
`GitHub 组织 <https://github.com/codeigniter4>`_。

其中包含多个开发仓库，可能会对潜在的贡献者有所帮助：

+------------------+--------------+-----------------------------------------------------------------+
| 仓库             | 受众         | 描述                                                            |
+==================+==============+=================================================================+
| CodeIgniter4_    | 贡献者       | 项目代码库，包括测试与用户指南源码                              |
+------------------+--------------+-----------------------------------------------------------------+
| translations_    | 开发者       | 系统消息翻译                                                    |
+------------------+--------------+-----------------------------------------------------------------+
| coding-standard_ | 贡献者       | 编码风格约定与规则                                              |
+------------------+--------------+-----------------------------------------------------------------+
| devkit_          | 开发者       | 用于 CodeIgniter 类库与项目的开发工具包                         |
+------------------+--------------+-----------------------------------------------------------------+
| settings_        | 开发者       | CodeIgniter 4 的 Settings 类                                    |
+------------------+--------------+-----------------------------------------------------------------+
| shield_          | 开发者       | CodeIgniter 4 的认证与授权类                                    |
+------------------+--------------+-----------------------------------------------------------------+
| tasks_           | 开发者       | CodeIgniter 4 的任务调度器                                      |
+------------------+--------------+-----------------------------------------------------------------+
| cache_           | 开发者       | CodeIgniter 4 的 PSR-6 与 PSR-16 缓存适配器                     |
+------------------+--------------+-----------------------------------------------------------------+
| queue_           | 开发者       | CodeIgniter 4 的任务队列                                        |
+------------------+--------------+-----------------------------------------------------------------+

.. _CodeIgniter4: https://github.com/codeigniter4/CodeIgniter4
.. _translations: https://github.com/codeigniter4/translations
.. _coding-standard: https://github.com/CodeIgniter/coding-standard
.. _devkit: https://github.com/codeigniter4/devkit
.. _settings: https://github.com/codeigniter4/settings
.. _shield: https://codeigniter4.github.io/shield
.. _tasks: https://github.com/codeigniter4/tasks
.. _cache: https://github.com/codeigniter4/cache
.. _queue: https://github.com/codeigniter4/queue

此外，还有若干部署仓库，在安装说明中会引用到。
这些部署仓库会在发布新版本时自动构建，
并不接受直接贡献。

+------------------+--------------+-----------------------------------------------------------------+
| 仓库             | 受众         | 描述                                                            |
+==================+==============+=================================================================+
| framework_       | 开发者       | 框架的已发布版本                                                |
+------------------+--------------+-----------------------------------------------------------------+
| appstarter_      | 开发者       | 启动项目（app/public/writable）。                                |
|                  |              | 依赖于“framework”                                               |
+------------------+--------------+-----------------------------------------------------------------+
| userguide_       | 任何人       | 预构建的用户指南                                                |
+------------------+--------------+-----------------------------------------------------------------+

.. _framework: https://github.com/codeigniter4/framework
.. _appstarter: https://github.com/codeigniter4/appstarter
.. _userguide: https://github.com/codeigniter4/userguide

在上述所有仓库中，
可以通过 GitHub 仓库页面中 "Code" 选项卡内的次级导航栏，
点击 "releases" 链接来下载仓库的最新版本。
每个仓库的当前（开发中）版本，
可以在仓库主页右侧通过 "Clone or download" 下拉按钮进行克隆或下载。

Composer 包
=================

我们还在 `packagist.org <https://packagist.org/search/?query=codeigniter4>`_ 上维护了一系列可通过 Composer 安装的包，
它们与前面提到的仓库相对应：

- `codeigniter4/framework <https://packagist.org/packages/codeigniter4/framework>`_
- `codeigniter4/appstarter <https://packagist.org/packages/codeigniter4/appstarter>`_
- `codeigniter4/translations <https://packagist.org/packages/codeigniter4/translations>`_
- `codeigniter/coding-standard <https://packagist.org/packages/codeigniter/coding-standard>`_
- `codeigniter4/devkit <https://packagist.org/packages/codeigniter4/devkit>`_
- `codeigniter4/settings <https://packagist.org/packages/codeigniter4/settings>`_
- `codeigniter4/shield <https://packagist.org/packages/codeigniter4/shield>`_
- `codeigniter4/cache <https://packagist.org/packages/codeigniter4/cache>`_

更多信息请参阅 :doc:`安装 </installation/index>` 页面。

CodeIgniter 4 项目
======================

我们还在 GitHub 上维护了一个
`codeigniter4projects <https://github.com/codeigniter4projects>`_ 组织，
其中的项目并不属于框架本身，
但用于展示 CodeIgniter 4，或让使用更加便捷。

+------------------+--------------+-----------------------------------------------------------------+
| 仓库             | 受众         | 描述                                                            |
+==================+==============+=================================================================+
| website_         | 开发者       | codeigniter.com 网站，使用 CodeIgniter 4 编写                   |
+------------------+--------------+-----------------------------------------------------------------+
| playground_      | 开发者       | 以项目形式提供的基础代码示例，仍在持续扩展中                    |
+------------------+--------------+-----------------------------------------------------------------+

.. _website: https://github.com/codeigniter4projects/website
.. _playground: https://github.com/codeigniter4projects/playground

这些仓库无法通过 Composer 安装。
