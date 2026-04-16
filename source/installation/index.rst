############
安装
############

CodeIgniter 支持两种安装方式：手动下载，
或使用 `Composer <https://getcomposer.org>`_。
哪一种更适合你？

- 推荐使用 Composer 安装方式，因为它可以更轻松地保持 CodeIgniter 为最新版本。
- 如果更偏好 CodeIgniter 3 所熟悉的那种简单“下载即用”方式，请选择手动安装。

无论选择哪种方式来安装和运行 CodeIgniter 4，
最新的
`用户指南 <https://codeigniter.org.cn/user_guide/>`_
都可以在线访问。
如果需要查看之前的版本，可以从
`codeigniter4/userguide <https://github.com/codeigniter4/userguide/releases>`_
仓库下载。

.. note:: 在使用 CodeIgniter 4 之前，请确保你的服务器满足
    :doc:`服务器要求 </intro/requirements>`，尤其是 PHP
    版本以及所需的 PHP 扩展。
    例如，你可能需要在 ``php.ini`` 中取消注释“extension”
    行，以启用“curl”和“intl”。

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
