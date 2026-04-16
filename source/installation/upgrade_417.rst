#############################
从 4.1.6 升级到 4.1.7
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

破坏性变更
****************

- 当 ``$xssClean`` 为 true 时，``get_cookie()`` 的输出结果已发生变化。
  现在它使用 ``FILTER_SANITIZE_FULL_SPECIAL_CHARS``，而不是 ``FILTER_SANITIZE_STRING``。
  请确认该变更是否可以接受。
  请注意，使用 XSS 过滤本身是一种不良实践，它无法完全防止 XSS 攻击。
  建议在视图中结合正确的 ``$context`` 使用 ``esc()``。
