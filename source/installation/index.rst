############
安装
############

CodeIgniter4 可以通过多种不同的方式安装：手动，使用 `Composer <https://getcomposer.org>`_ 或使用 `Git <https://git-scm.com/>`_。你喜欢哪个？

- 如果你希望像 CodeIgniter3 那样简单的“下载并使用”，那么你应该选择手动安装。
- 如果你打算在项目中添加其他软件包，我们建议你使用 Composer 方式安装。
- 如果你想为框架添砖加瓦，那么你应该选择 Git 方式安装。

.. toctree::
    :titlesonly:

    installing_manual
    installing_composer
    installing_git
    running
    upgrading
    troubleshooting
    repositories

不论你选择何种方式安装并运行 CodeIgniter4，你都可以随时访问我们的在线 `用户指南 <https://codeigniter-chinese.github.io/codeigniter4-user-guide/>`_。

.. note:: 在使用 CodeIgniter 4 之前，请确保你的服务器满足 :doc:`要求 </intro/requirements>`，尤其是所需的 PHP 版本和 PHP 扩展。例如，你可能会发现必须取消注释 ``php.ini`` 的 “extension” 部分才能启用 “curl” 和 “intl”。
