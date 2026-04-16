########################
图像处理类
########################

CodeIgniter 的图像处理类支持以下操作：

-  图像缩放
-  缩略图生成
-  图像裁剪
-  图像旋转
-  图像水印

支持以下图像库：GD/GD2 和 ImageMagick。

.. contents::
    :local:
    :depth: 2

**********************
初始化类
**********************

与 CodeIgniter 中的大多数类一样，图像类通过调用全局函数 ``service()`` 在控制器中初始化：

.. literalinclude:: images/001.php

你可以将图像库的别名传递给全局函数 ``service()``：

.. literalinclude:: images/002.php

可用的 Handler 如下：

- ``gd``      GD/GD2 图像库
- ``imagick`` ImageMagick 库

如果使用 ImageMagick 库，必须在 **app/Config/Images.php** 中设置服务器的库路径。

.. note:: ImageMagick handler 需要安装 imagick 扩展。

*******************
处理图像
*******************

无论你想要执行哪种类型的处理（缩放、裁剪、旋转或水印），处理流程基本相同。需要设置一些与预期操作对应的偏好设置，然后调用处理函数。

例如，创建图像缩略图的代码如下：

.. literalinclude:: images/003.php

以上代码告诉库在 **/path/to/image** 文件夹中查找名为 **mypic.jpg** 的图像，然后从中创建一个 100 x 100 像素的新图像，并保存到新文件 **mypic_thumb.jpg**。由于使用了 ``fit()`` 方法，它会根据期望的宽高比尝试找到最佳裁剪区域，然后裁剪并缩放结果。

一个图像可以在保存前按顺序应用多个处理方法。原始图像保持原样，使用新图像并逐个传递给每个方法，在上一次结果的基础上应用新的处理效果：

.. literalinclude:: images/004.php

此示例将获取同一图像，首先修复任何手机方向问题，将图像旋转 90 度，然后将结果裁剪为从左上角开始的 100 x 100 像素图像。最终结果将保存为缩略图。

.. note:: 为允许图像类执行任何处理，包含图像文件的文件夹必须具有写入权限。

.. note:: 某些图像处理操作可能需要占用大量服务器内存。如果在处理图像时遇到内存不足错误，可能需要限制图像的最大尺寸，或调整 PHP 内存限制。

图像质量
=============

``save()`` 可以接受额外的 ``$quality`` 参数来更改生成的图像质量。取值范围为 0 到 100，框架默认值为 90。此参数仅适用于 JPEG 和 WebP 图像，其他格式将被忽略：

.. note:: 自 v4.4.0 起，WebP 的 ``$quality`` 参数可用。

.. literalinclude:: images/005.php

.. note:: 质量越高，文件越大。参见 https://www.php.net/manual/zh/function.imagejpeg.php

如果你只想更改图像质量而不进行其他处理，需要包含图像资源，否则会得到完全相同的副本：

.. literalinclude:: images/006.php

******************
处理方法
******************

共有 8 种可用的处理方法：

-  ``$image->crop()``
-  ``$image->convert()``
-  ``$image->fit()``
-  ``$image->flatten()``
-  ``$image->flip()``
-  ``$image->resize()``
-  ``$image->rotate()``
-  ``$image->text()``

这些方法返回类实例，因此可以链式调用，如上所示。如果失败，会抛出包含错误消息的 ``CodeIgniter\Images\ImageException``。最佳实践是捕获异常，在失败时显示错误，如下所示：

.. literalinclude:: images/007.php

裁剪图像
===============

裁剪图像，只保留原始图像的一部分。这通常用于创建符合特定尺寸/宽高比的缩略图。通过 ``crop()`` 方法实现：

    crop(int $width = null, int $height = null, int $x = null, int $y = null, bool $maintainRatio = false, string $masterDim = 'auto')

- ``$width`` 是结果图像的期望宽度，单位为像素。
- ``$height`` 是结果图像的期望高度，单位为像素。
- ``$x`` 是从图像左侧开始裁剪的像素数。
- ``$y`` 是从图像顶部开始裁剪的像素数。
- ``$maintainRatio`` 如果为 true，将根据需要调整最终尺寸以保持图像原始宽高比。
- ``$masterDim`` 指定当 ``$maintainRatio`` 为 true 时应保持不变的尺寸。可选值：``'width'``、``'height'`` 或 ``'auto'``。

要从图像中心取出 50 x 50 像素的区域，需要首先计算适当的 x 和 y 偏移值：

.. literalinclude:: images/008.php

转换图像
=================

``convert()`` 方法更改库内部对目标文件格式的指示符。这不会触及实际的图像资源，但会向 ``save()`` 指示使用什么格式：

    convert(int $imageType)

- ``$imageType`` 是 PHP 的图像类型常量之一（参见 https://www.php.net/manual/zh/function.image-type-to-mime-type.php）：

  .. literalinclude:: images/009.php

.. note:: ImageMagick 已根据文件扩展名指示的类型保存文件，忽略 ``$imageType``。

适配图像
==============

``fit()`` 方法旨在通过以下步骤帮助简化"智能"裁剪图像的某个部分：

- 确定原始图像的正确裁剪区域以保持期望的宽高比。
- 裁剪原始图像。
- 缩放到最终尺寸。

::

    fit(int $width, int $height = null, string $position = 'center')

- ``$width`` 是图像的期望最终宽度。
- ``$height`` 是图像的期望最终高度。
- ``$position`` 确定要裁剪出图像的哪个部分。允许的位置：``'top-left'``、``'top'``、``'top-right'``、``'left'``、``'center'``、``'right'``、``'bottom-left'``、``'bottom'``、``'bottom-right'``。

这提供了一种更简单的裁剪方式，始终能保持宽高比：

.. literalinclude:: images/010.php

扁平化图像
=================

``flatten()`` 方法旨在为透明图像（PNG）添加背景色，并将 RGBA 像素转换为 RGB 像素

- 在将透明图像转换为 jpg 时指定背景色。

::

    flatten(int $red = 255, int $green = 255, int $blue = 255)

- ``$red`` 是背景的红色值。
- ``$green`` 是背景的绿色值。
- ``$blue`` 是背景的蓝色值。

.. literalinclude:: images/011.php

翻转图像
===============

图像可以沿水平轴或垂直轴翻转：

    flip(string $dir)

- ``$dir`` 指定翻转的轴。可以是 ``'vertical'`` （垂直）或 ``'horizontal'`` （水平）。

.. literalinclude:: images/012.php

缩放图像
===============

可以使用 ``resize()`` 方法将图像缩放到任何需要的尺寸：

    resize(int $width, int $height, bool $maintainRatio = false, string $masterDim = 'auto')

- ``$width`` 是新图像的期望宽度，单位为像素
- ``$height`` 是新图像的期望高度，单位为像素
- ``$maintainRatio`` 决定图像是拉伸以适应新尺寸，还是保持原始宽高比。
- ``$masterDim`` 指定在保持比例时应保留哪个轴的尺寸。可选 ``'width'`` 或 ``'height'``。

缩放图像时，你可以选择是否保持原始图像的比例，或将新图像拉伸/压缩以适应期望的尺寸。如果 ``$maintainRatio`` 为 true，``$masterDim`` 指定的尺寸将保持不变，而另一个尺寸将根据原始图像的宽高比进行更改。

.. literalinclude:: images/013.php

旋转图像
===============

``rotate()`` 方法允许以 90 度为增量旋转图像：

    rotate(float $angle)

- ``$angle`` 是旋转的度数。可选 ``90``、``180``、``270``。

.. note:: 虽然 ``$angle`` 参数接受 float 类型，但在处理过程中会转换为整数。如果值不是上述三个值之一，会抛出 ``CodeIgniter\Images\ImageException``。

添加文字水印
=======================

可以使用 ``text()`` 方法非常简单地在图像上叠加文字水印。适用于放置版权声明、摄影师姓名，或简单地将图像标记为预览版，防止被用于他人的最终产品。

::

    text(string $text, array $options = [])

第一个参数是要显示的文本字符串。第二个参数是选项数组，允许指定文本的显示方式：

.. literalinclude:: images/014.php

可识别的选项如下：

- ``color``         文本颜色（十六进制数字），如 ``'#ff0000'``
- ``opacity``        表示文本不透明度的数字，范围 ``0`` 到 ``1``。
- ``withShadow``    布尔值，是否显示阴影。
- ``shadowColor``   阴影颜色（十六进制数字）
- ``shadowOffset``    阴影偏移的像素数。同时应用于垂直和水平值。
- ``hAlign``        水平对齐：``'left'``、``'center'``、``'right'``
- ``vAlign``        垂直对齐：``'top'``、``'middle'``、``'bottom'``
- ``hOffset``        x 轴上的额外偏移，单位为像素
- ``vOffset``        y 轴上的额外偏移，单位为像素
- ``fontPath``        要使用的 TTF 字体的完整服务器路径。如未提供，将使用系统字体。
- ``fontSize``        要使用的字体大小。使用 GD handler 和系统字体时，有效值为 ``1`` 到 ``5``。

.. note:: ImageMagick 驱动程序不识别 fontPath 的完整服务器路径。相反，只需提供要使用的已安装系统字体名称，如 Calibri。
