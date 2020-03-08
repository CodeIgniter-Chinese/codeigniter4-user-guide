手动安装
###############################################################################

`CodeIgniter 4 框架 <https://github.com/codeigniter4/framework>`_ 目录保存了所有已发布的框架版本。
这是为那些不想用Composer的开发者准备的。

在 ``app`` 文件夹里开发你的项目，而 ``public`` 文件夹就将成为你的对外根目录。
与此同时，请勿更改 ``system`` 文件夹下面的任何内容！

**Note**: 这是和 `CodeIgniter 3 <https://codeigniter.com/user_guide/installation/index.html>`_ 描述的安装方式最相近的。

安装
============================================================

下载 `最新版本 <https://github.com/CodeIgniter4/framework/releases/latest>`_, 并将其解压到你的项目根目录。

设置
-------------------------------------------------------

无

升级
-------------------------------------------------------

下载一份最新的框架，并根据发布通知或更新日志里的升级教程来将最新版本的内容合并进你的项目。

通常来说，替换掉 ``system`` 目录，并且检查 ``app/Config`` 文件夹下受影响的变更内容即可。

对于专家来说
-------------------------------------------------------

下载-》运行

对于贡献者来说
-------------------------------------------------------

当更新时，你有必要合并冲突

结构
-------------------------------------------------------

在你的项目设置完成后，新建以下文件夹:
app, public, system, writable


安装翻译
============================================================

如果你想充分利用系统信息的翻译，可以类似地把这些翻译加入到项目中。

下载 `最新版本的翻译 <https://github.com/codeigniter4/translations/releases/latest>`_
解压下载的zip文件并将 ``Language`` 文件夹的内容复制到你的 ``PROJECT_ROOT/app/Languages`` 文件夹下。

在进行任何翻译的升级时都需要重复以上步骤。