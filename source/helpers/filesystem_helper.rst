#################
文件系统辅助函数
#################

文件系统辅助函数文件包含用于处理文件和目录的函数。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
===================

使用以下代码加载此辅助函数：

.. literalinclude:: filesystem_helper/001.php

可用函数
===================

提供以下函数：

.. php:function:: directory_map($sourceDir[, $directoryDepth = 0[, $hidden = false]])

    :param    string  $sourceDir: 源目录路径
    :param    int   $directoryDepth: 需遍历的目录深度（``0`` = 完全递归，``1`` = 仅当前目录，以此类推）
    :param    bool    $hidden: 是否包含隐藏路径
    :returns:    文件数组
    :rtype:    array

    示例：

    .. literalinclude:: filesystem_helper/002.php

    .. note:: 路径几乎总是相对于你的主 **index.php** 文件。

    目录中包含的子文件夹也会被映射。如果要控制递归深度，
    可以使用第二个参数（整数）来实现。深度为 ``1`` 时只映射顶级目录：

    .. literalinclude:: filesystem_helper/003.php

    默认情况下，返回的数组中不会包含隐藏文件，并且会跳过隐藏目录。
    要覆盖此行为，可以将第三个参数设置为 ``true``（布尔值）：

    .. literalinclude:: filesystem_helper/004.php

    每个文件夹名称将作为数组索引，而其包含的文件将进行数字索引。
    这是一个典型数组的示例::

        Array (
            [libraries] => Array
                (
                    [0] => benchmark.html
                    [1] => config.html
                    ["database/"] => Array
                        (
                            [0] => query_builder.html
                            [1] => binds.html
                            [2] => configuration.html
                            [3] => connecting.html
                            [4] => examples.html
                            [5] => fields.html
                            [6] => index.html
                            [7] => queries.html
                        )
                    [2] => email.html
                    [3] => file_uploading.html
                    [4] => image_lib.html
                    [5] => input.html
                    [6] => language.html
                    [7] => loader.html
                    [8] => pagination.html
                    [9] => uri.html
                )
        )

    如果未找到结果，将返回一个空数组。

.. php:function:: directory_mirror($original, $target[, $overwrite = true])

    :param    string    $original: 源目录
    :param    string    $target: 目标目录
    :param    bool    $overwrite: 冲突时是否覆盖单个文件

    递归地将源目录的文件和目录复制到目标目录中，即"镜像"其内容。

    示例：

    .. literalinclude:: filesystem_helper/005.php

    可以选择通过第三个参数更改覆盖行为。

.. php:function:: write_file($path, $data[, $mode = 'wb'])

    :param    string    $path: 文件路径
    :param    string    $data: 要写入文件的数据
    :param    string    $mode: ``fopen()`` 模式
    :returns:    写入成功时返回 ``true``，出错时返回 ``false``
    :rtype:    bool

    将数据写入路径中指定的文件。如果文件不存在，函数将创建它。

    示例：

    .. literalinclude:: filesystem_helper/006.php

    可以选择通过第三个参数设置写入模式：

    .. literalinclude:: filesystem_helper/007.php

    默认模式是 ``'wb'``。有关模式选项，请参阅 PHP 手册中的 `fopen() <https://www.php.net/manual/zh/function.fopen.php>`_。

    .. note:: 为使此函数能够将数据写入文件，其权限必须设置为可写。
        如果文件尚不存在，则包含它的目录必须可写。

    .. note:: 路径是相对于主站点的 **index.php** 文件，而不是相对于
        控制器或视图文件。CodeIgniter 使用前端控制器，因此路径
        始终是相对于主站点索引的。

    .. note:: 此函数在写入文件时会获取文件的独占锁。

.. php:function:: delete_files($path[, $delDir = false[, $htdocs = false[, $hidden = false]]])

    :param    string    $path: 目录路径
    :param    bool    $delDir: 是否同时删除目录
    :param    bool    $htdocs: 是否跳过删除 .htaccess 和索引页面文件
    :param  bool    $hidden: 是否同时删除隐藏文件（以点开头的文件）
    :returns:    成功时返回 ``true``，出错时返回 ``false``
    :rtype:    bool

    删除所提供路径中包含的所有文件。

    示例：

    .. literalinclude:: filesystem_helper/008.php

    如果第二个参数设置为 ``true``，所提供根路径中包含的任何目录也将被删除。

    示例：

    .. literalinclude:: filesystem_helper/009.php

    .. note:: 文件必须可写或属于系统所有才能被删除。

.. php:function:: get_filenames($sourceDir[, $includePath = false[, $hidden = false[, $includeDir = true]]])

    :param    string    $sourceDir: 目录路径
    :param    bool|null    $includePath: 是否将路径作为文件名的一部分；false 表示不包含路径，null 表示相对于 ``$sourceDir`` 的路径，true 表示完整路径
    :param    bool    $hidden: 是否包含隐藏文件（以点开头的文件）
    :param    bool    $includeDir: 是否在数组输出中包含目录
    :returns:    文件名数组
    :rtype:    array

    接收服务器路径作为输入，并返回包含其中所有文件名称的数组。
    可以选择将文件路径添加到文件名中，方法是将第二个参数设置为 'relative'
    以获取相对路径，或设置为任何其他非空值以获取完整文件路径。

    .. note:: 在 v4.4.4 版本之前，由于一个 bug，此函数不会跟随符号链接文件夹。

    示例：

    .. literalinclude:: filesystem_helper/010.php

.. php:function:: get_dir_file_info($sourceDir[, $topLevelOnly = true])

    :param    string    $sourceDir: 目录路径
    :param    bool    $topLevelOnly: 是否仅查看指定目录（排除子目录）
    :returns:    包含所提供目录内容信息的数组
    :rtype:    array

    读取指定目录并构建包含文件名、文件大小、日期和权限的数组。
    只有通过将第二个参数发送为 false 来强制读取指定路径中包含的子文件夹，
    因为这可能是一个密集的操作。

    示例：

    .. literalinclude:: filesystem_helper/011.php

.. php:function:: get_file_info($file[, $returnedValues = ['name', 'server_path', 'size', 'date']])

    :param    string        $file: 文件路径
    :param    array|string  $returnedValues: 要返回的信息类型（可作为数组或逗号分隔的字符串传递）
    :returns:    包含指定文件信息的数组，失败时返回 false
    :rtype:    array

    给定文件和路径，返回（可选）文件的 *名称*、*路径*、*大小* 和 *修改日期*
    信息属性。第二个参数允许明确声明要返回的信息。

    有效的 ``$returnedValues`` 选项是：``name``、``size``、``date``、``readable``、``writeable``、
    ``executable`` 和 ``fileperms``。

.. php:function:: symbolic_permissions($perms)

    :param    int    $perms: 权限
    :returns:    符号权限字符串
    :rtype:    string

    获取数值形式的权限（例如 `fileperms() <https://www.php.net/manual/zh/function.fileperms.php>`_ 返回的值），并返回文件权限的标准符号表示法。

    .. literalinclude:: filesystem_helper/012.php

.. php:function:: octal_permissions($perms)

    :param    int    $perms: 权限
    :returns:    八进制权限字符串
    :rtype:    string

    获取数值形式的权限（例如 `fileperms() <https://www.php.net/manual/zh/function.fileperms.php>`_ 返回的值），并返回文件权限的三位八进制表示法（字符串）。

    .. literalinclude:: filesystem_helper/013.php

.. php:function:: same_file($file1, $file2)

    :param    string    $file1: 第一个文件的路径
    :param    string    $file2: 第二个文件的路径
    :returns:    两个文件是否都存在且哈希值相同
    :rtype:    boolean

    比较两个文件以查看它们是否相同（基于其 MD5 哈希值）。

    .. literalinclude:: filesystem_helper/014.php

.. php:function:: set_realpath($path[, $checkExistence = false])

    :param    string    $path: 路径
    :param    bool    $checkExistence: 是否检查路径是否实际存在
    :returns:    绝对路径
    :rtype:    string

    此函数将返回一个不含符号链接或相对目录结构的服务器路径。
    可选的第二个参数将在路径无法解析时触发错误。

    示例：

    .. literalinclude:: filesystem_helper/015.php
