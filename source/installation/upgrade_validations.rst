升级表单验证
###################

.. contents::
    :local:
    :depth: 2

类文档
=========================

- `CodeIgniter 3.x 表单验证文档 <https://codeigniter.org.cn/userguide3/libraries/form_validation.html>`_
- :doc:`CodeIgniter 4.x 验证文档 </libraries/validation>`

变更内容
=====================
- 如果要更改验证错误的显示方式，必须在 CI4 中设置 :ref:`validation View templates <validation-customizing-error-display>`。
- CI4 的验证功能不包含 CI3 中的 `回调 <https://codeigniter.org.cn/userguide3/libraries/form_validation.html#id13>`_。
  请改用 :ref:`Callable 规则 <validation-using-callable-rule>` （自 v4.5.0 起）、
  :ref:`Closure 规则 <validation-using-closure-rule>` （自 v4.3.0 起）或
  :ref:`Rule Classes <validation-using-rule-classes>`。
- 在 CI3 中，Callbacks/Callable 规则具有更高优先级；但在 CI4 中，Closure/Callable 规则没有优先级之分，而是按列出的顺序进行检查。
- 自 v4.5.0 起，引入了 :ref:`Callable 规则 <validation-using-callable-rule>`，但它与 CI3 的 `Callable <https://codeigniter.org.cn/userguide3/libraries/form_validation.html#id14>`_ 略有不同。
- CI4 的格式验证规则不允许空字符串。
- CI4 的验证过程绝不会更改你的数据。
- 自 v4.3.0 起，引入了 :php:func:`validation_errors()`，但其 API 与 CI3 不同。

升级指南
=============
1. 在包含表单的视图中，需要做以下修改：

    - 将 ``<?php echo validation_errors(); ?>`` 改为 ``<?= validation_list_errors() ?>``

2. 在控制器中，需要做以下修改：

    - 将 ``$this->load->helper(array('form', 'url'));`` 改为 ``helper('form');``
    - 删除 ``$this->load->library('form_validation');`` 这一行
    - 将 ``if ($this->form_validation->run() == FALSE)`` 改为 ``if (! $this->validateData($data, $rules))``
      其中，``$data`` 是要验证的数据，通常为 POST 数据 ``$this->request->getPost()``。
    - 将 ``$this->load->view('myform');`` 改为 ``return view('myform', ['validation' => $this->validator,]);``

3. 还需要修改验证规则。新语法是在控制器中将规则设置为数组：

   .. literalinclude:: upgrade_validations/001.php

代码示例
============

CodeIgniter 3.x 版本
------------------------
路径：**application/views**::

    <html>
    <head>
        <title>My Form</title>
    </head>
    <body>

        <?php echo validation_errors(); ?>

        <?php echo form_open('form'); ?>

        <h5>Username</h5>
        <input type="text" name="username" value="" size="50" />

        <h5>Password</h5>
        <input type="text" name="password" value="" size="50" />

        <h5>Password Confirm</h5>
        <input type="text" name="passconf" value="" size="50" />

        <h5>Email Address</h5>
        <input type="text" name="email" value="" size="50" />

        <div><input type="submit" value="Submit" /></div>

        </form>

    </body>
    </html>

路径：**application/controllers**：

.. literalinclude:: upgrade_validations/ci3sample/002.php

CodeIgniter 4.x 版本
-----------------------
路径：**app/Views**::

    <html>
    <head>
        <title>My Form</title>
    </head>
    <body>

        <?= validation_list_errors() ?>

        <?= form_open('form') ?>

        <h5>Username</h5>
        <input type="text" name="username" value="" size="50" />

        <h5>Password</h5>
        <input type="text" name="password" value="" size="50" />

        <h5>Password Confirm</h5>
        <input type="text" name="passconf" value="" size="50" />

        <h5>Email Address</h5>
        <input type="text" name="email" value="" size="50" />

        <div><input type="submit" value="Submit" /></div>

        </form>

    </body>
    </html>

路径：**app/Controllers**：

.. literalinclude:: upgrade_validations/002.php
