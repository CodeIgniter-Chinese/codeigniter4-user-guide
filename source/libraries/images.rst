########################
图像处理类
########################

CodeIgniter的图像处理类允许你执行以下操作:

-  图像大小调整
-  创建缩略图
-  图像裁剪
-  图像旋转
-  图像水印

图像处理类支持使用以下图像库:GD/GD2和 ImageMagick

.. contents::
    :local:
    :depth: 2

**********************
初始化类
**********************

与CodeIgniter中的大多数其他类一样，你可以通过控制器中调用Services类的初始化图像处理类::

	$image = Config\Services::image();

你可以将要使用的图像库的别名传递给服务功能::

    $image = Config\Services::image('imagick');

可用的图像库处理程序如下:

- gd        对应调用的是GD/GD2图像库。
- imagick   对应调用的是ImageMagick图像库。

如果你要使用ImageMagick图像库，则必须要在 **application/Config/Images.php** 中设置服务器上该库的所在路径。

.. note:: ImageMagick处理程序不需要在服务器上加载imagick扩展。只要你的脚本可以访问该库并且可以使用 ``exec()`` 运行在服务器上，它就可以工作。

处理图像
===================

无论你执行何种图像的处理方法函数（调整大小、裁剪、旋转、使用水印），一般调用过程都是相同的。
你将根据要执行的操作设置一些首选项，然后调用其中一个你需要的使用的可用处理函数::

	$image = Config\Services::image()
		->withFile('/path/to/image/mypic.jpg')
		->fit(100, 100, 'center')
		->save('/path/to/image/mypic_thumb.jpg');

上面的代码告我们它会查找来自image文件夹中的名为*mypic.jpg*的图像，然后使用GD2 image_library图像库来创建一个100 x 100像素的新图像，并将其保存到新文件（the thumb）。
由于它使用fit()方法，它将尝试根据所需的宽高比找到要裁剪的图像的最佳部分，然后裁剪并调整结果大小。

在保存新图像之前，可以根据需求来通过许多可用方法来处理图像。原始图像将保持原样，而新图像会通过每个方法传参，将处理结果应用于直接的结果之上::

	$image = Config\Services::image()
		->withFile('/path/to/image/mypic.jpg')
		->reorient()
		->rotate(90)
		->crop(100, 100, 0, 0)
		->save('/path/to/image/mypic_thumb.jpg');

此示例将采用相同的图像并首先修复任何移动电话的定向问题，图像将旋转90度，然后从左上角开始将结果裁剪为100x100像素图像。结果将保存成缩略图。

.. note:: 为了让图像处理类可以进行任何处理，包含图像文件的文件夹必须具有写入权限。

.. note:: 对于某些操作，图像处理时可能需要相当大量的服务器内存。如果在处理图像时遇到内存不足错误，可能需要限制其图像的最大大小，和/或调整PHP内存限制。

处理方法
==================

有六种可用的处理方法可以调用:

-  $image->crop()
-  $image->fit()
-  $image->flatten()
-  $image->flip()
-  $image->resize()
-  $image->rotate()
-  $image->text()

这些方法将会返回类实例，如上所示，它们可以链接在一起。如果失败，它们将抛出包含错误的消息到 ``CodeIgniter\Images\ImageException`` 。
一个好的做法是捕获异常消息，在失败时显示错误，如下所示::

	try {
        $image = Config\Services::image()
            ->withFile('/path/to/image/mypic.jpg')
            ->fit(100, 100, 'center')
            ->save('/path/to/image/mypic_thumb.jpg');
	}
	catch (CodeIgniter\Images\ImageException $e)
	{
		echo $e->getMessage();
	}

.. note:: 你可以选择通过在函数中提交开始/结束标记来指定要应用于错误的HTML格式，如下所示::

	$this->image_lib->display_errors('<p>', '</p>');

图像裁剪
---------------

图像可以被裁剪，只保留原始图像的一部分。通常用于创建特定大小/纵横比匹配的缩略图图像。这是用 ``crop()`` 方法处理的::

    crop(int $width = null, int $height = null, int $x = null, int $y = null, bool $maintainRatio = false, string $masterDim = 'auto')

- **$width** 是结果图像的所需宽度，以像素为单位。
- **$height** 是结果图像的所需高度，以像素为单位。
- **$x** 是从图像左侧开始裁剪的像素数。
- **$y** 是从图像顶部开始裁剪的像素数。
- **$maintainRatio** 如果为true，将根据需要调整最终尺寸以保持图像的原始高宽比。
- **$masterDim** 可使其保持不变的维度，当$maintainRatio为true时。值可以是：'width'，'height'或'auto'。

要从图像中心取出50x50像素的正方形，你需要首先计算适当的x和y偏移值::

    $info = Services::image('imagick')
		->withFile('/path/to/image/mypic.jpg')
		->getFile()
		->getProperties(true);

    $xOffset = ($info['width'] / 2) - 25;
    $yOffset = ($info['height'] / 2) - 25;

    Services::image('imagick')
		->withFile('/path/to/image/mypic.jpg')
		->crop(50, 50, $xOffset, $yOffset)
		->save('path/to/new/image.jpg');

拟合图像
--------------

使用 ``fit()`` 方法旨在通过执行以下步骤帮助简化以“智能”方式裁剪图像的一部分:

- 确定要裁剪的原始图像的正确部分，以保持所需的宽高比。
- 裁剪原始图像。
- 调整大小到最终尺寸。

::

    fit(int $width, int $height = null, string $position = 'center')

- **$width** 是图像的最终宽度。
- **$height** 是图像所需的最终高度。
- **$position** 确定要裁剪的图像部分。允许的位置: 'top-left', 'top', 'top-right', 'left', 'center', 'right', 'bottom-left', 'bottom', 'bottom-right'。

这里提供一种更简单的裁剪方式，可以始终保持纵横比::

	Services::image('imagick')
		->withFile('/path/to/image/mypic.jpg')
		->fit(100, 150, 'left')
		->save('path/to/new/image.jpg');

展平图像
-----------------

使用 ``flatten()`` 方法旨在在透明图像（PNG）后面添加背景颜色并将RGBA像素转换为RGB像素

- 从透明图像转换为jpgs格式时指定背景颜色。

::

    flatten(int $red = 255, int $green = 255, int $blue = 255)

- **$red** 是背景的红色值。
- **$green** 是背景的绿色值。
- **$blue** 是背景的蓝色值。

::

	Services::image('imagick')
		->withFile('/path/to/image/mypic.png')
		->flatten()
		->save('path/to/new/image.jpg');

	Services::image('imagick')
		->withFile('/path/to/image/mypic.png')
		->flatten(25,25,112)
		->save('path/to/new/image.jpg');

翻转图像
---------------

图像可以沿水平轴或垂直轴翻转::

    flip(string $dir)

- **$dir** 指定要翻转的轴。可以是“垂直”或“水平”。

::

	Services::image('imagick')
		->withFile('/path/to/image/mypic.jpg')
		->flip('horizontal')
		->save('path/to/new/image.jpg');

调整图像大小
---------------

可以使用resize()方法调整图像大小以适合你需要的任何维度::

	resize(int $width, int $height, bool $maintainRatio = false, string $masterDim = 'auto')

- **$width** 是新图像的所需宽度（以像素为单位）
- **$height** 是新图像的所需高度（以像素为单位）
- **$maintainRatio** 确定图像是否被拉伸以适应新尺寸，或者是否保持原始宽高比。
- **$masterDim** 指定在保持比率时哪个轴应该具有其维度。'宽度'，'高度'。

调整图像大小时，你可以选择是保持原始图像的比例，还是拉伸/压缩新图像以适合所需的尺寸。
如果$maintainRatio为true，则$masterDim指定的尺寸将保持不变，而另一个尺寸将更改为与原始图像的纵横比相匹配。

::

	Services::image('imagick')
		->withFile('/path/to/image/mypic.jpg')
		->resize(200, 100, true, 'height')
		->save('path/to/new/image.jpg');

旋转图像
---------------

使用 rotate() 方法允许你以90度的增量旋转图像::

	rotate(float $angle)

- **$angle** 是要旋转的度数。'90'，'180'，'270'之一。

.. note:: 虽然$angle参数接受float，但它会在进程中将其转换为整数。
		如果该值不是上面列出的三个值， 他会抛出一个自CodeIgniter\Images\ImageException的图像异常错误.

添加文本水印
-----------------------

你可以使用text()方法非常简单地将文本水印叠加到图像上。
这对于放置版权声明，摄影师名称或简单地将图像标记为预览非常有用，这会使它们最终不会用于其他人的产品上。

::

	text(string $text, array $options = [])

第一个参数是你要显示的文本字符串。第二个参数是一个选项数组，允许你指定文本的显示方式::

	Services::image('imagick')
		->withFile('/path/to/image/mypic.jpg')
		->text('Copyright 2017 My Photo Co', [
		    'color'      => '#fff',
		    'opacity'    => 0.5,
		    'withShadow' => true,
		    'hAlign'     => 'center',
		    'vAlign'     => 'bottom',
		    'fontSize'   => 20
		])
		->save('path/to/new/image.jpg');

可识别的选项如下:

- color         文本颜色 (十六进制数字), 即＃ff0000
- opacity		设置一个介于0到1之间的数字，表示文本的不透明度。
- withShadow	以布尔值是否来显示阴影。
- shadowColor   设定阴影的颜色（十六进制数）。
- shadowOffset	偏移阴影的像素数。适用于垂直和水平值。
- hAlign        水平对齐：左，中，右
- vAlign        垂直对齐：顶部，中间，底部
- hOffset		指定x轴上的附加偏移，以像素为单位
- vOffset		指定y轴上的附加偏移，以像素为单位
- fontPath		要使用的TTF字体的完整服务器路径。如果没有给出系统字体，将使用系统字体。
- fontSize		要使用的字体大小。将GD处理程序与系统字体一起使用时，有效值介于1-5之间。

.. note:: ImageMagick驱动程序无法识别fontPath的完整服务器路径。相反，需要你提供希望使用的已安装系统字体之一的名称，即如Calibri。