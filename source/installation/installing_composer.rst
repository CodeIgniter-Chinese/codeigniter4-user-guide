通过Composer安装
###############################################################################

.. contents::
    :local:
    :depth: 1

可以通过多种方式在你的系统中来使用Composer安装CodeIgniter。

前两种方法描述了使用CodeIgniter4来创建一个项目的骨架结构，从而让你可以在一个新的webapp中作为基础来使用。
而第三种技术，如下所述，使得你可以将CodeIgniter4加入进一个现存的webapp中。

**注意**: 如果你正使用一个Git仓库来存储代码或与他人写作，那么 ``vendor`` 目录就需要添加到gitignore文件中。在这种情况下，当你克隆仓库到新系统中，就需要执行 ``composer update`` 指令

启动应用
============================================================

`CodeIgniter 4 应用启动 <https://github.com/codeigniter4/appstarter>`_
仓库里通过composer依赖最新版本的框架来维护了一个基础骨架的应用。

以下安装教程适用于每一位希望启动一个新的基于CodeIgniter4的项目的开发者。

安装和设置
-------------------------------------------------------

在你的项目根目录执行以下命令::

    composer create-project codeigniter4/appstarter project-root

该指令将会创建一个 "project-root" 目录。

如果你忽略了"project-root"参数，该命令就会创建一个"appstarter"目录，该目录当需要时可以被重命名。

如果你不需要或不想安装PHPUnit以及跟它相关的任何Composer依赖，请在该命令的尾部增加"--no-dev"选项。
这一操作将只会使用Composer安装框架本体以及三个我们打包过的可信赖的外部依赖包。

下面是一个这样的安装指令的示例，使用默认的项目根目录"APPstarter"::

    composer create-project codeigniter4/appstarter --no-dev

安装完成后你应该根据 "升级" 这节里的步骤继续进行。

升级
-------------------------------------------------------

每当有新的发布时，在你项目的根目录运行以下指令::

    composer update

如果在你创建项目时使用了"--no-dev"选项，那么在这里也一样适合这样做。``composer update --no-dev``

阅读升级指南，并检查指定的 ``app/Config`` 目录是否有内容变更。

优点
-------------------------------------------------------

便于安装，便于升级。

缺点
-------------------------------------------------------

你仍需要在更新后检查 ``app/Config`` 的变更。

结构
-------------------------------------------------------

设置完成后你的项目中会有以下目录:

- app, public, tests, writable
- vendor/codeigniter4/framework/system
- vendor/codeigniter4/framework/app & public (compare with yours after updating)

最新的开发版本
-------------------------------------------------------

App Start仓库里有着 ``builds`` 脚本，在框架当前稳定发布版本和最新的开发版本间进行选择。
对于开发者而言，可以选择使用该脚本来获取最新的变更，不过这些变更可能是不稳定的。

`开发者用户手册 <https://codeigniter4.github.io/CodeIgniter4/>`_ 可以在线访问。请注意与当前发布版本的用户手册
有所不同，并独立维护一个开发的分支。

在你的项目根目录执行以下指令::

    php builds development

以上的指令将会更新 **composer.json** 文件并将当前的工作仓库指向 ``develop`` 分支，并在配置和XML文件中更新对应的路径。
如果要回退以上变更，请执行::

    php builds release

在使用完 ``builds`` 命令后，请确保运行 ``composer update`` 来将你的vendor目录与最新版本的同步。

将CodeIgniter4添加到现存项目中
============================================================

在"手动安装"这章中描述过的 `CodeIgniter 4 framework <https://github.com/codeigniter4/framework>`_
仓库同样也可使用Composer来被添加到现存的项目中。

在 ``app`` 目录下开发你的应用，``public`` 目录作为文档的根目录。

在你的项目根目录下::

    composer require codeigniter4/framework

与前面两个composer安装方式类似，你也可以在"composer require"命令中使用"--no-dev"参数来忽略安装PHPunit。

设置
-------------------------------------------------------

从 ``vendor/codeigniter4/framework`` 中复制app, public, tests 和 writable目录到你的项目根目录下。

从 ``vendor/codeigniter4/framework`` 中复制 ``env``, ``phpunit.xml.dist`` and ``spark`` 文件到你的项目根目录下。

你需要设置指向 ``vendor/codeigniter/framework`` 的目录 —— 通过修改 ``app/Config/Paths.php`` 中的 ``$systemDirectory`` 变量


升级
-------------------------------------------------------

每当有新的发布时，在你项目的根目录运行以下指令::

    composer update

如果在你创建项目时使用了"--no-dev"选项，那么在这里也一样适合这样做。``composer update --no-dev``

阅读升级指南，并检查指定的 ``app/Config`` 目录是否有内容变更。

专业人士
-------------------------------------------------------

相当简单的安装方式；便于升级

贡献者
-------------------------------------------------------

你仍需要在更新后检查 ``app/Config`` 的变更。

结构
-------------------------------------------------------

设置完成后你的项目结构如下:

- app, public, tests, writable
- vendor/codeigniter4/framework/system


安装翻译
============================================================

如果你想充分利用系统信息的翻译，可以类似地把这些翻译加入到项目中。

在项目根目录运行以下指令::

    composer require codeigniter4/translations @rc

当你每次运行 ``composer update`` 时这些翻译文件也同样会被更新。
