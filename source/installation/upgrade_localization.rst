升级本地化
####################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.X 语言文档 <http://codeigniter.com/userguide3/libraries/language.html>`_
- :doc:`CodeIgniter 4.X 本地化文档 </outgoing/localization>`

变更点
=====================
- 在 CI4 中,语言文件以数组形式返回语言线。

升级指南
=============
1. 在 **Config/App.php** 中指定默认语言:

   .. literalinclude:: upgrade_localization/001.php

2. 现在将语言文件移到 **app/Language/<locale>**。
3. 之后需要更改语言文件中的语法。下面的代码示例中可以看到文件中的语言数组应该如何表示。
4. 从每个文件中删除语言加载器 ``$this->lang->load($file, $lang);``。
5. 用 ``echo lang('Errors.errorEmailMissing');`` 替换加载语言行的方法 ``$this->lang->line('error_email_missing')``。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_localization/ci3sample/002.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_localization/002.php
