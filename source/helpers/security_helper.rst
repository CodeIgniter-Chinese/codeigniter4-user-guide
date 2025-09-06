###############
安全辅助函数
###############

安全辅助函数文件包含安全相关函数。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
===================

使用以下代码加载此辅助函数:

.. literalinclude:: security_helper/001.php

可用函数
===================

以下函数可用:

.. php:function:: sanitize_filename($filename[, $relativePath = false])

    :param    string    $filename: 文件名
    :param    bool      $relativePath: 是否接受相对路径（自 v4.6.2 起可用）
    :returns:    安全的文件名
    :rtype:    string

    提供对目录遍历的保护。

    更多信息，请参阅 :doc:`安全 <../libraries/security>` 文档。

.. php:function:: strip_image_tags($str)

    :param    string    $str: 输入字符串
    :returns:    不包含图像标签的输入字符串
    :rtype:    string

    这是一个安全函数,用于从字符串中剥离图像标签。
    它将图像 URL 作为纯文本保留。

    例子:

    .. literalinclude:: security_helper/002.php

.. php:function:: encode_php_tags($str)

    :param    string    $str: 输入字符串
    :returns:    安全格式化的字符串
    :rtype:    string

    这是一个安全函数,用于将 PHP 标签转换为实体。

    例子:

    .. literalinclude:: security_helper/003.php
