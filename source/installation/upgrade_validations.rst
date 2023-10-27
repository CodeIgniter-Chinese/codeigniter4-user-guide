升级验证
###################

.. contents::
    :local:
    :depth: 2

库文档
=========================

- `CodeIgniter 3.X 表单验证文档 <http://codeigniter.com/userguide3/libraries/form_validation.html>`_
- :doc:`CodeIgniter 4.X 验证文档 </libraries/validation>`

变更点
=====================
- 如果要更改验证错误显示,必须设置 CI4 :ref:`验证视图模板 <validation-customizing-error-display>`。
- CI4 验证没有 CI3 的回调和可调用函数。
  请使用 :ref:`规则类 <validation-using-rule-classes>` 或
  :ref:`闭包规则 <validation-using-closure-rule>`
  代替。
- 在 CI3 中，回调/可调用规则具有优先级，但在 CI4 中，闭包规则没有优先级，并且按照它们在列表中的顺序进行检查。
- CI4 验证格式规则不允许为空字符串。
- CI4 验证永远不会改变你的数据。
- 从 v4.3.0 开始,引入了 :php:func:`validation_errors()`,但 API 与 CI3 的不同。

升级指南
=============
1. 在包含表单的视图中进行更改:

    - ``<?php echo validation_errors(); ?>`` 改为 ``<?= validation_list_errors() ?>``

2. 在控制器中进行更改:

    - ``$this->load->helper(array('form', 'url'));`` 改为 ``helper(['form', 'url']);``
    - 移除 ``$this->load->library('form_validation');``
    - ``if ($this->form_validation->run() == FALSE)`` 改为 ``if (! $this->validate([]))``
    - ``$this->load->view('myform');`` 改为 ``return view('myform', ['validation' => $this->validator,]);``

3. 必须更改验证规则。新语法是在控制器中将规则设置为数组:

   .. literalinclude:: upgrade_validations/001.php

代码示例
============

CodeIgniter 3.x 版本
------------------------
路径:**application/views**::

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

路径:**application/controllers**:

.. literalinclude:: upgrade_validations/ci3sample/002.php

CodeIgniter 4.x 版本
-----------------------
路径:**app/Views**::

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

路径:**app/Controllers**:

.. literalinclude:: upgrade_validations/002.php
