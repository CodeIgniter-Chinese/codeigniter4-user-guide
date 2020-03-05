通过Composer安装
###############################################################################

.. contents::
    :local:
    :depth: 1

可以通过多种方式在你的系统中来使用Composer安装CodeIgniter。

前两种方法描述了使用CodeIgniter4来创建一个项目的骨架结构，从而让你可以在一个新的webapp中作为基础来使用。
而第三种技术，如下所述，使得你可以将CodeIgniter4加入进一个现存的webapp中。

**Note**: 如果你正使用一个Git仓库来存储代码或与他人写作，那么 ``vendor`` 目录就需要添加到gitignore文件中。在这种情况下，当你克隆仓库到新系统中，就需要执行 ``composer update``指令

App Starter
============================================================

The `CodeIgniter 4 app starter <https://github.com/codeigniter4/appstarter>`_ 
repository holds a skeleton application, with a composer dependency on
the latest released version of the framework.

This installation technique would suit a developer who wishes to start
a new CodeIgniter4 based project.

Installation & Set Up
-------------------------------------------------------

In the folder above your project root::

    composer create-project codeigniter4/appstarter project-root

The command above will create a "project-root" folder.

If you omit the "project-root" argument, the command will create an
"appstarter" folder, which can be renamed as appropriate.

If you don't need or want phpunit installed, and all of its composer
dependencies, then add the "--no-dev" option to the end of the above
command line. That will result in only the framework, and the three
trusted dependencies that we bundle, being composer-installed.

A sample such installation command, using the default project-root "appstarter"::

    composer create-project codeigniter4/appstarter --no-dev

After installation you should follow the steps in the "Upgrading" section.

Upgrading
-------------------------------------------------------

Whenever there is a new release, then from the command line in your project root::

    composer update 

If you used the "--no-dev" option when you created the project, it
would be appropriate to do so here too, i.e. ``composer update --no-dev``.

Read the upgrade instructions, and check designated  ``app/Config`` folders for affected changes.

Pros
-------------------------------------------------------

Simple installation; easy to update

Cons
-------------------------------------------------------

You still need to check for ``app/Config`` changes after updating

Structure
-------------------------------------------------------

Folders in your project after set up:

- app, public, tests, writable 
- vendor/codeigniter4/framework/system
- vendor/codeigniter4/framework/app & public (compare with yours after updating)

Latest Dev
-------------------------------------------------------

The App Starter repo comes with a ``builds`` scripts to switch Composer sources between the
current stable release and the latest development branch of the framework. Use this script
for a developer who is willing to live with the latest unreleased changes, which may be unstable.

The `development user guide <https://codeigniter4.github.io/CodeIgniter4/>`_ is accessible online.
Note that this differs from the released user guide, and will pertain to the
develop branch explicitly.

In your project root::

    php builds development

The command above will update **composer.json** to point to the ``develop`` branch of the
working repository, and update the corresponding paths in config and XML files. To revert
these changes run::

    php builds release

After using the ``builds`` command be sure to run ``composer update`` to sync your vendor
folder with the latest target build.

Adding CodeIgniter4 to an Existing Project
============================================================

The same `CodeIgniter 4 framework <https://github.com/codeigniter4/framework>`_ 
repository described in "Manual Installation" can also be added to an
existing project using Composer.

Develop your app inside the ``app`` folder, and the ``public`` folder 
will be your document root. 

In your project root::

    composer require codeigniter4/framework

As with the earlier two composer install methods, you can omit installing
phpunit and its dependencies by adding the "--no-dev" argument to the "composer require" command.

Set Up
-------------------------------------------------------

Copy the app, public, tests and writable folders from ``vendor/codeigniter4/framework`` 
to your project root

Copy the ``env``, ``phpunit.xml.dist`` and ``spark`` files, from
``vendor/codeigniter4/framework`` to your project root

You will have to adjust paths to refer to vendor/codeigniter/framework``, 
- the $systemDirectory variable in ``app/Config/Paths.php``

Upgrading
-------------------------------------------------------

Whenever there is a new release, then from the command line in your project root::

    composer update 

Read the upgrade instructions, and check designated 
``app/Config`` folders for affected changes.

Pros
-------------------------------------------------------

Relatively simple installation; easy to update

Cons
-------------------------------------------------------

You still need to check for ``app/Config`` changes after updating

Structure
-------------------------------------------------------

Folders in your project after set up:

- app, public, tests, writable 
- vendor/codeigniter4/framework/system


Translations Installation
============================================================

If you want to take advantage of the system message translations,
they can be added to your project in a similar fashion. 

From the command line inside your project root::

    composer require codeigniter4/translations @rc

These will be updated along with the framework whenever you do a ``composer update``.