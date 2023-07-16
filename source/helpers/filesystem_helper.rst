#################
文件系统辅助函数
#################

文件系统辅助函数文件包含了帮助处理目录的函数。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
===================

使用以下代码加载此辅助函数:

.. literalinclude:: filesystem_helper/001.php

可用函数
===================

以下函数可用:

.. php:function:: directory_map($sourceDir[, $directoryDepth = 0[, $hidden = false]])

    :param    string  $sourceDir: 源目录路径
    :param    int   $directoryDepth: 遍历的目录深度(0 = 完全递归,1 = 当前目录,等等)
    :param    bool    $hidden: 是否包含隐藏路径
    :returns:    文件数组
    :rtype:    array

    示例:

    .. literalinclude:: filesystem_helper/002.php

    .. note:: 路径几乎总是相对于你的 main index.php 文件。

    包含在目录中的子文件夹也将被映射。如果你希望控制递归深度,可以使用第二个参数(整数)。深度为 1 只会映射顶级目录:

    .. literalinclude:: filesystem_helper/003.php

    默认情况下,返回的数组中不包括隐藏文件,跳过隐藏目录。要覆盖此行为,可以将第三个参数设置为 true(布尔值):

    .. literalinclude:: filesystem_helper/004.php

    每个文件夹名称将是一个数组索引,其包含的文件将以数字索引。这里是一个典型数组的示例::

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

    如果未找到结果,它将返回一个空数组。

.. php:function:: directory_mirror($original, $target[, $overwrite = true])

    :param    string    $original: 原始源目录
    :param    string    $target: 目标目的目录
    :param    bool    $overwrite: 是否在冲突时覆盖单个文件

    递归复制源目录的文件和目录到目标目录,即“镜像”其内容。

    例子:

    .. literalinclude:: filesystem_helper/005.php

    你可以通过第三个参数选择更改覆盖行为。

.. php:function:: write_file($path, $data[, $mode = 'wb'])

    :param    string    $path: 文件路径
    :param    string    $data: 要写入文件的数据
    :param    string    $mode: ``fopen()`` 模式
    :returns:    如果写入成功则为 true,如果有错误则为 false
    :rtype:    bool

    将数据写入路径中指定的文件。如果文件不存在,则该函数将创建它。

    例子:

    .. literalinclude:: filesystem_helper/006.php

    你可以通过第三个参数可选地设置写入模式:

    .. literalinclude:: filesystem_helper/007.php

    默认模式为 'wb'。写入模式选项请参阅 `PHP 用户指南 <https://www.php.net/manual/en/function.fopen.php>`_。

    .. note:: 为了使此函数能够将数据写入文件,必须设置其权限以使其可写。如果文件不存在,则包含它的目录必须可写。

    .. note:: 该路径是相对于你的主站点 index.php 文件,而不是你的控制器或视图文件。CodeIgniter 使用前端控制器,因此路径始终相对于主站点 index。

    .. note:: 此函数在写入文件时对该文件进行排他锁定。

.. php:function:: delete_files($path[, $delDir = false[, $htdocs = false[, $hidden = false]]])

    :param    string    $path: 目录路径
    :param    bool    $delDir: 是否也删除目录
    :param    bool    $htdocs: 是否跳过删除 .htaccess 和索引页面文件
    :param    bool    $hidden: 是否也删除隐藏文件(以句点开头的文件)
    :returns:    成功为 true,错误为 false
    :rtype:    bool

    删除提供的路径中包含的所有文件。

    例子:

    .. literalinclude:: filesystem_helper/008.php

    如果第二个参数设置为 true,则提供的根路径中包含的任何目录也将被删除。

    例子:

    .. literalinclude:: filesystem_helper/009.php

    .. note:: 文件必须可写或由系统拥有才能被删除。

.. php:function:: get_filenames($sourceDir[, $includePath = false[, $hidden = false[, $includeDir = true]]])

    :param    string    $sourceDir: 目录路径
    :param    bool|null    $includePath: 是否将路径作为文件名的一部分包含;false 不包含路径,null 包含相对于 ``$sourceDir`` 的路径,true 包含完整路径
    :param    bool    $hidden: 是否包含隐藏文件(以句点开头的文件)
    :param    bool    $includeDir: 是否在数组输出中包含目录
    :returns:    文件名数组
    :rtype:    array

    获取一个服务器路径作为输入,返回一个包含其中包含的所有文件名的数组。通过将第二个参数设置为 'relative' 获取相对路径,或任何其他非空值以获取完整文件路径,可以选择将文件路径添加到文件名中。

    示例:

    .. literalinclude:: filesystem_helper/010.php

.. php:function:: get_dir_file_info($sourceDir[, $topLevelOnly = true])

    :param    string    $sourceDir: 目录路径
    :param    bool    $topLevelOnly: 是否仅查看指定的目录(不包括子目录)
    :returns:    包含有关提供目录内容信息的数组
    :rtype:    array

    读取指定的目录并构建一个包含文件名、文件大小、日期和权限的数组。仅当通过将第二个参数设置为 false 强制时,才读取指定路径中包含的子文件夹,因为这可能是一个密集操作。

    示例:

    .. literalinclude:: filesystem_helper/011.php

.. php:function:: get_file_info($file[, $returnedValues = ['name', 'server_path', 'size', 'date']])

    :param    string        $file: 文件路径
    :param    array|string  $returnedValues: 要作为数组或逗号分隔字符串返回的信息类型
    :returns:    包含指定文件的信息的数组,失败为 false
    :rtype:    array

    根据文件和路径,返回(可选地)*名称*、*路径*、*大小*和*修改日期*信息属性。第二个参数允许你明确声明你想要返回的信息。

    有效的 ``$returnedValues`` 选项有:``name``、``size``、``date``、``readable``、``writeable``、``executable`` 和 ``fileperms``。

.. php:function:: symbolic_permissions($perms)

    :param    int    $perms: 权限
    :returns:    符号权限字符串
    :rtype:    string

    获取数字权限(例如 ``fileperms()`` 返回的)并返回标准符号表示法的文件权限。

    .. literalinclude:: filesystem_helper/012.php

.. php:function:: octal_permissions($perms)

    :param    int    $perms: 权限
    :returns:    八进制权限字符串
    :rtype:    string

    获取数字权限(例如 ``fileperms()`` 返回的)并返回三字符八进制表示法的文件权限。

    .. literalinclude:: filesystem_helper/013.php

.. php:function:: same_file($file1, $file2)

    :param    string    $file1: 第一个文件的路径
    :param    string    $file2: 第二个文件的路径
    :returns:    两个文件是否具有相同的哈希值并存在
    :rtype:    boolean

    比较两个文件是否相同(基于它们的 MD5 哈希)。

    .. literalinclude:: filesystem_helper/014.php

.. php:function:: set_realpath($path[, $checkExistence = false])

    :param    string    $path: 路径
    :param    bool    $checkExistence: 是否检查路径是否实际存在
    :returns:    绝对路径
    :rtype:    string

    此函数将返回没有符号链接或相对目录结构的服务器路径。可选的第二个参数将在无法解析路径时触发错误。

    示例:

    .. literalinclude:: filesystem_helper/015.php
