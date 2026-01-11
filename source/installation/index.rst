############
安装
############

CodeIgniter 提供两种受支持的安装方式：手动下载，
或使用 `Composer <https://getcomposer.org>`_。
哪一种更适合你？

- 推荐使用 Composer 安装，因为它可以更轻松地让 CodeIgniter 保持最新状态。
- 如果你希望使用 CodeIgniter 3 广为人知的那种简单“下载即用”的安装方式，请选择手动安装。

无论选择哪种方式来安装和运行 CodeIgniter 4，最新的
`用户指南 <https://codeigniter.org.cn/user_guide/>`_ 都可以在线访问。
如果需要查看之前的版本，可以从
`codeigniter4/userguide <https://github.com/codeigniter4/userguide/releases>`_
仓库下载。

.. note:: 在使用 CodeIgniter 4 之前，请确保服务器满足
    :doc:`服务器要求 </intro/requirements>`，尤其是 PHP
    版本以及所需的 PHP 扩展。
    例如，你可能需要在 ``php.ini`` 中取消注释“extension”
    相关行，以启用“curl”和“intl”。

.. toctree::
    :titlesonly:

    installing_composer
    installing_manual
    running
    troubleshooting
    deployment
    ../changelogs/index
    upgrading
    repositories
