############
安装
############

CodeIgniter 支持两种安装方法:手动下载和使用 `Composer <https://getcomposer.org>`_ 。
对你来说哪个是正确的?

- 我们推荐使用 Composer 安装,因为它可以轻松地保持 CodeIgniter 的更新。
- 如果你希望使用 CodeIgniter3 所知的简单“下载并使用”安装,请选择手动安装。

无论你选择以何种方式安装和运行 CodeIgniter4,最新的
`用户指南 <https://codeigniter.com/user_guide/>`_ 都可以在线访问。
如果你想查看之前的版本,可以从
`codeigniter4/userguide <https://github.com/codeigniter4/userguide/releases>`_
存储库下载。

.. note:: 在使用 CodeIgniter 4 之前,请确保你的服务器满足
    :doc:`要求 </intro/requirements>` ,特别是 PHP
    版本和所需的 PHP 扩展。
    例如,你可能需要取消注释 ``php.ini`` 文件的“extension”
    行以启用“curl”和“intl”。

.. toctree::
    :titlesonly:

    installing_composer
    installing_manual
    running
    troubleshooting
    ../changelogs/index
    upgrading
    repositories
