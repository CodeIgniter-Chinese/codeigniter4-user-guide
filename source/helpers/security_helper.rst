###############
安全辅助函数
###############

安全辅助函数文件包含与安全相关的函数。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
===================

使用以下代码加载此辅助函数：

.. literalinclude:: security_helper/001.php

可用函数
===================

提供以下函数：

.. php:function:: sanitize_filename($filename[, $relativePath = false])

    :param    string    $filename: 文件名
    :param    bool      $relativePath: 是否接受相对路径（自 v4.6.2 起可用）
    :returns:    经过清理的文件名
    :rtype:    string

    提供针对目录遍历攻击的保护。

    更多信息请参考 :doc:`安全类库 <../libraries/security>` 文档。

.. php:function:: strip_image_tags($str)

    :param    string    $str: 输入字符串
    :returns:    移除图片标签后的输入字符串
    :rtype:    string

    这是一个安全函数，用于从字符串中移除图片标签。
    它会将图片 URL 保留为纯文本。

    示例：

    .. literalinclude:: security_helper/002.php

.. php:function:: encode_php_tags($str)

    :param    string    $str: 输入字符串
    :returns:    安全格式化的字符串
    :rtype:    string

    这是一个安全函数，用于将 PHP 标签转换为实体字符。

    示例：

    .. literalinclude:: security_helper/003.php
