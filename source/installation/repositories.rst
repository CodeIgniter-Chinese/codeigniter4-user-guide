CodeIgniter 仓库
########################

.. contents::
    :local:
    :depth: 2

codeigniter4 组织
=========================

CodeIgniter 4 开源项目有自己的
`GitHub 组织 <https://github.com/codeigniter4>`_。

有几个开发仓库,对潜在贡献者感兴趣:

+------------------+--------------+-----------------------------------------------------------------+
| 仓库             | 受众         | 描述                                                            |
+==================+==============+=================================================================+
| CodeIgniter4_    | 贡献者       | 项目代码库,包括测试和用户指南源码                               |
+------------------+--------------+-----------------------------------------------------------------+
| translations_    | 开发者       | 系统消息翻译                                                    |
+------------------+--------------+-----------------------------------------------------------------+
| coding-standard_ | 贡献者       | 编码风格约定和规则                                              |
+------------------+--------------+-----------------------------------------------------------------+
| devkit_          | 开发者       | CodeIgniter 库和项目的开发工具包                                |
+------------------+--------------+-----------------------------------------------------------------+
| settings_        | 开发者       | CodeIgniter 4 的设置库                                          |
+------------------+--------------+-----------------------------------------------------------------+
| shield_          | 开发者       | CodeIgniter 4 的身份验证和授权库                                |
+------------------+--------------+-----------------------------------------------------------------+
| tasks_           | 开发者       | CodeIgniter 4 的任务调度程序                                    |
+------------------+--------------+-----------------------------------------------------------------+
| cache_           | 开发者       | CodeIgniter 4 的 PSR-6 和 PSR-16 缓存适配器                     |
+------------------+--------------+-----------------------------------------------------------------+
| queue_           | 开发者       | CodeIgniter 4 的队列                                            |
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

还有几个部署仓库,在安装说明中引用。
部署仓库在发布新版本时会自动构建,不直接贡献。

+------------------+--------------+-----------------------------------------------------------------+
| 仓库             | 受众         | 描述                                                            |
+==================+==============+=================================================================+
| framework_       | 开发者       | 框架的已发布版本                                                |
+------------------+--------------+-----------------------------------------------------------------+
| appstarter_      | 开发者       | 启动项目(app/public/writable)。                                 |
|                  |              | 依赖于“framework”                                               |
+------------------+--------------+-----------------------------------------------------------------+
| userguide_       | 任何人       | 预构建用户指南                                                  |
+------------------+--------------+-----------------------------------------------------------------+

.. _framework: https://github.com/codeigniter4/framework
.. _appstarter: https://github.com/codeigniter4/appstarter
.. _userguide: https://github.com/codeigniter4/userguide

在上述所有仓库中,可以通过在其 GitHub 仓库页面的“Code”选项卡中的二级导航栏中选择“releases”链接来下载仓库的最新版本。
可以通过选择仓库主页右侧的“克隆或下载”下拉按钮来克隆或下载每个仓库的当前(开发中)版本。

Composer 包
=================

我们在 `packagist.org <https://packagist.org/search/?query=codeigniter4>`_ 上也维护 composer 可安装包。
这些与上面提到的仓库对应:

- `codeigniter4/framework <https://packagist.org/packages/codeigniter4/framework>`_
- `codeigniter4/appstarter <https://packagist.org/packages/codeigniter4/appstarter>`_
- `codeigniter4/translations <https://packagist.org/packages/codeigniter4/translations>`_
- `codeigniter/coding-standard <https://packagist.org/packages/codeigniter/coding-standard>`_
- `codeigniter4/devkit <https://packagist.org/packages/codeigniter4/devkit>`_
- `codeigniter4/settings <https://packagist.org/packages/codeigniter4/settings>`_
- `codeigniter4/shield <https://packagist.org/packages/codeigniter4/shield>`_
- `codeigniter4/cache <https://packagist.org/packages/codeigniter4/cache>`_

有关更多信息,请参阅 :doc:`安装 </installation/index>` 页面。

CodeIgniter 4 项目
======================

我们在 GitHub 上也维护一个 `codeigniter4projects <https://github.com/codeigniter4projects>`_ 组织,
其中包含不属于框架本身的项目,但展示了它或使它更易于使用!

+------------------+--------------+-----------------------------------------------------------------+
| 仓库             | 受众         | 描述                                                            |
+==================+==============+=================================================================+
| website_         | 开发者       | 使用 CodeIgniter 4 编写的 codeigniter.com 网站                  |
+------------------+--------------+-----------------------------------------------------------------+
| playground_      | 开发者       | 以项目形式的基本代码示例。仍在增长。                            |
+------------------+--------------+-----------------------------------------------------------------+

.. _website: https://github.com/codeigniter4projects/website
.. _playground: https://github.com/codeigniter4projects/playground

这些不是 composer 可安装的仓库。
