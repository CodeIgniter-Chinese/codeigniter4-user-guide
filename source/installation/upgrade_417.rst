#############################
从 4.1.6 升级到 4.1.7
#############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

重大变更
****************

- 当 ``$xssClean`` 为 true 时,``get_cookie()`` 改变了输出。现在使用 ``FILTER_SANITIZE_FULL_SPECIAL_CHARS``,而不是 ``FILTER_SANITIZE_STRING``。确保更改可以接受。请注意,使用 XSS 过滤是一种不好的做法。它不能完美地防止 XSS 攻击。建议在视图中使用正确的 ``$context`` 来 ``esc()``。
