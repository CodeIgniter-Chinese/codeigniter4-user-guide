############
安装
############

CodeIgniter 支持两种安装方式：手动下载或使用 `Composer <https://getcomposer.org>`_。该如何选择？

- 推荐使用 Composer 安装，由此可以更方便地保持 CodeIgniter 更新。
- 如果倾向于 CodeIgniter 3 那种熟悉的“下载即用”的简便安装方式，请选择手动安装。

无论选择何种方式安装并运行 CodeIgniter4，都可以在线访问最新的 `用户指南 <https://codeigniter.org.cn/user_guide/>`_。如需查看旧版本，可从 `codeigniter4/userguide <https://github.com/codeigniter4/userguide/releases>`_ 仓库下载。

.. note:: 使用 CodeIgniter 4 前，请确保服务器符合 :doc:`服务器要求 </intro/requirements>`，特别是 PHP 版本及所需的 PHP 扩展。例如，可能需要取消 ``php.ini`` 中 “extension” 行的注释，以启用 “curl” 和 “intl”。

.. toctree::
    :titlesonly:

    installing_composer
    installing_manual
    running
    worker_mode
    troubleshooting
    deployment
    ../changelogs/index
    upgrading
    repositories
