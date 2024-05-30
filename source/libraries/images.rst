########################
图像处理类
########################

CodeIgniter 的图像处理类允许你执行以下操作:

- 图像缩放
- 缩略图创建
- 图像裁剪
- 图像旋转
- 图像添加水印

支持以下图像库:GD/GD2 和 ImageMagick。

.. contents::
    :local:
    :depth: 2

**********************
初始化类
**********************

与 CodeIgniter 中的其他大多数类一样,在控制器中通过调用 Services 类来初始化图像类:

.. literalinclude:: images/001.php

你可以将要使用的图像库的别名传递给服务函数:

.. literalinclude:: images/002.php

可用的处理程序如下:

- ``gd``      GD/GD2 图像库
- ``imagick`` ImageMagick 库。

如果使用 ImageMagick 库,必须在 **app/Config/Images.php** 中设置库的路径。

.. note:: ImageMagick 处理程序需要 imagick 扩展。

*******************
处理图像
*******************

无论你想执行的处理类型(调整大小、裁剪、旋转或添加水印),过程都是相同的。你将设置与你计划执行的操作相对应的一些首选项,然后调用可用的处理函数之一。

例如,要创建图像缩略图,你将执行以下操作:

.. literalinclude:: images/003.php

上面的代码告诉库去寻找一个名为 **mypic.jpg** 的图像，该图像位于 **/path/to/image** 文件夹中，然后从中创建一个 100 x 100 像素的新图像，并将其保存到一个新文件 **mypic_thumb.jpg** 中。由于它使用了 ``fit()`` 方法，它将尝试根据所需的纵横比找到图像的最佳部分进行裁剪，然后裁剪并调整结果的大小。

在保存之前,可以通过尽可能多的可用方法对图像进行处理。原始图像保持不变,使用新的图像并通过每个方法传递,在之前的结果上叠加结果:

.. literalinclude:: images/004.php

这个示例首先会修复任何移动手机方向问题,然后将图像旋转 90 度,然后从左上角开始裁剪结果为 100 x 100 像素的图像。结果将保存为缩略图。

.. note:: 为了允许图像类执行任何处理,包含图像文件的文件夹必须具有写入权限。

.. note:: 对于某些操作,图像处理可能需要相当多的服务器内存。如果在处理图像时遇到内存溢出错误,则可能需要限制它们的最大大小和/或调整 PHP 内存限制。

图像质量
=============

``save()`` 可以接受额外的参数 ``$quality`` 来更改结果图像的质量。值的范围从 0 到 100,默认值为 90。此参数仅适用于 JPEG 和 WebP 图像,否则将被忽略:

.. note:: 自 v4.4.0 起，WebP 格式可以使用 ``$quality`` 参数。

.. literalinclude:: images/005.php

.. note:: 更高的质量会导致文件大小更大。另请参阅 https://www.php.net/manual/en/function.imagejpeg.php

如果你只对更改图像质量而不做任何处理感兴趣。你需要包含图像资源,否则最终会得到一个完全相同的副本:

.. literalinclude:: images/006.php

******************
处理方法
******************

有 8 种可用的处理方法:

-  ``$image->crop()``
-  ``$image->convert()``
-  ``$image->fit()``
-  ``$image->flatten()``
-  ``$image->flip()``
-  ``$image->resize()``
-  ``$image->rotate()``
-  ``$image->text()``

这些方法返回类实例,所以它们可以链式调用,如上所示。如果它们失败,它们将抛出一个包含错误消息的 ``CodeIgniter\Images\ImageException``。一个好的做法是捕获异常,在失败时显示错误,像这样:

.. literalinclude:: images/007.php

裁剪图像
===============

可以裁剪图像,使只保留原始图像的一部分。这通常用于在必须与某个大小/纵横比匹配时创建缩略图图像。这是通过 ``crop()`` 方法处理的::

    crop(int $width = null, int $height = null, int $x = null, int $y = null, bool $maintainRatio = false, string $masterDim = 'auto')

- ``$width`` 是所需的结果图像的宽度,以像素为单位。
- ``$height`` 是所需的结果图像的高度,以像素为单位。
- ``$x`` 是从图像左侧开始裁剪的像素数。
- ``$y`` 是从图像顶部开始裁剪的像素数。
- ``$maintainRatio`` 如果为 true,将根据需要调整最终尺寸以维持图像的原始纵横比。
- ``$masterDim`` 指定在 ``$maintainRatio`` 为 true 时应保持不变的维度。值可以是: ``'width'``、 ``'height'`` 或 ``'auto'``。

要从图像中心取一个 50 x 50 像素的正方形,你需要首先计算适当的 x 和 y 偏移值:

.. literalinclude:: images/008.php

转换图像
=================

``convert()`` 方法更改库的内部指示器,以获得所需的文件格式。这不会触及实际的图像资源,而是向 ``save()`` 指示要使用的格式::

    convert(int $imageType)

- ``$imageType`` 是 PHP 的图像类型常量之一(参见例如 https://www.php.net/manual/en/function.image-type-to-mime-type.php):

  .. literalinclude:: images/009.php

.. note:: ImageMagick 已经以扩展名指示的类型保存文件,忽略 ``$imageType``。

调整图像大小
==============

``fit()`` 方法旨在帮助以“智能”的方式裁剪图像的一部分,执行以下步骤:

- 确定应裁剪原始图像的正确部分,以维持所需的纵横比。
- 裁剪原始图像。
- 调整到最终尺寸。

::

    fit(int $width, int $height = null, string $position = 'center')

- ``$width`` 是图像的所需最终宽度。
- ``$height`` 是图像的所需最终高度。
- ``$position`` 确定要裁剪的图像部分。允许的位置: ``'top-left'``、 ``'top'``、 ``'top-right'``、 ``'left'``、 ``'center'``、 ``'right'``、 ``'bottom-left'``、 ``'bottom'``、 ``'bottom-right'``。

这提供了一种更简单的裁剪方式,将始终保持纵横比:

.. literalinclude:: images/010.php

扁平化图像
=================

``flatten()`` 方法旨在为透明图像(PNG)添加背景色,并将 RGBA 像素转换为 RGB 像素

- 将透明图像转换为 jpg 时指定背景色。

::

    flatten(int $red = 255, int $green = 255, int $blue = 255)

- ``$red`` 是背景的红色值。
- ``$green`` 是背景的绿色值。
- ``$blue`` 是背景的蓝色值。

.. literalinclude:: images/011.php

翻转图像
===============

可以沿着水平或垂直轴翻转图像::

    flip(string $dir)

- ``$dir`` 指定要翻转的轴。可以是 ``'vertical'`` 或 ``'horizontal'``。

.. literalinclude:: images/012.php

调整图像大小
===============

可以使用 ``resize()`` 方法将图像调整到任何所需尺寸::

    resize(int $width, int $height, bool $maintainRatio = false, string $masterDim = 'auto')

- ``$width`` 是新图像的所需宽度,以像素为单位
- ``$height`` 是新图像的所需高度,以像素为单位
- ``$maintainRatio`` 确定图像是拉伸以适应新尺寸,还是保持原始纵横比。
- ``$masterDim`` 指定在保持比例时应遵守哪个轴的尺寸。可以是 ``'width'``、 ``'height'``。

在调整图像大小时,你可以选择是保持原始图像的比例,还是拉伸/挤压新图像以适应所需尺寸。如果 ``$maintainRatio`` 为 true, ``$masterDim`` 指定的维度将保持不变,而另一维度将改变以匹配原始图像的纵横比。

.. literalinclude:: images/013.php

旋转图像
===============

``rotate()`` 方法允许你以 90 度为增量旋转图像::

    rotate(float $angle)

- ``$angle`` 是要旋转的角度数。 ``90``、 ``180``、 ``270`` 之一。

.. note:: 尽管 ``$angle`` 参数接受浮点数,但在处理过程中它会将其转换为整数。如果值与上面列出的三个值之一不同,它将抛出一个 CodeIgniter\Images\ImageException。

添加文本水印
=======================

你可以使用 ``text()`` 方法非常简单地在图像上覆盖文本水印。这对于放置版权声明、摄影师姓名或简单地将图像标记为预览很有用,这样它们就不会在其他人的最终产品中使用。

::

    text(string $text, array $options = [])

第一个参数是你希望显示的文本字符串。第二个参数是一个选项数组,允许你指定文本的显示方式:

.. literalinclude:: images/014.php

识别的可能选项如下:

- ``color``         文本颜色(十六进制编号),例如 ``#ff0000``
- ``opacity``        介于 ``0`` 和 ``1`` 之间表示文本不透明度的数字。
- ``withShadow``    布尔值,决定是否显示阴影。
- ``shadowColor``   阴影的颜色(十六进制编号)
- ``shadowOffset``    阴影偏移多少像素。同时适用于垂直和水平值。
- ``hAlign``        水平对齐: ``'left'``, ``'center'``, ``'right'``
- ``vAlign``        垂直对齐: ``'top'``, ``'middle'``, ``'bottom'``
- ``hOffset``        x 轴上的额外偏移,以像素为单位
- ``vOffset``        y 轴上的额外偏移,以像素为单位
- ``fontPath``        你要使用的 TTF 字体的完整服务器路径。如果没有给出,则使用系统字体。
- ``fontSize``        要使用的字体大小。对于使用系统字体的 GD 处理程序,有效值为 ``1`` 到 ``5`` 之间。

.. note:: ImageMagick 驱动程序不识别字体路径的完整服务器路径。相反,只提供你希望使用的已安装系统字体的名称,例如 Calibri。
