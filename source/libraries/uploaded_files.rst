***************************
使用文件上传类
***************************

在 CodeIgniter 中通过表单使用文件上传功能将会比直接使用 PHP 的 ``$_FILES`` 数组更加简单和安全。其将继承  :doc:`文件类 </libraries/files>` 并获取该类的所有功能。

.. note:: 这和 CodeIgniter 的上一版本的文件上传类不同。这次提供了一个原生接口及一些小功能来上传文件。上传类将在最终版的时提供。

.. contents::
    :local:
    :depth: 2

===============
访问文件
===============

所有文件
----------

当你上传文件时，PHP 可以在本地使用全局数组 ``$_FILES`` 来访问这些文件。当你同时上传多个文件时，这个数组存在一些不可忽视的缺点和很多开发者没有意识到的安全方面的潜在缺陷。CodeIgniter 通过一个公共接口来规范你对文件的使用，从而改善这些问题。


通过当前的 ``IncomingRequest`` 实例来访问文件。使用 ``getFiles()`` 方法来获取本次请求中上传的所有文件。方法将会返回由 ``CodeIgniter\HTTP\Files\UploadedFile`` 实例表示的文件数组::

	$files = $this->request->getFiles();


当然，有很多种方式来为文件 input 标签命名，除了最简外任何其他任何命名方式都可能产生奇怪的结果。数组将会以你期望的方式返回。使用最简方式，一个单文件提交表单可能会是这样::

	<input type="file" name="avatar" />

其将会返回一个简单的数组像是::

	[
		'avatar' => // UploadedFile instance
	]

如果你在标签名称中使用数组表示法，input 标签将看上去像是这样::

	<input type="file" name="my-form[details][avatar]" />

``getFiles()`` 方法返回的数组看上去将像是这样::

	[
		'my-form' => [
			'details' => [
				'avatar' => // UploadedFile instance
			]
		]
	]

在某些情况下，你可以指定一组文件元素来上传::

	Upload an avatar: <input type="file" name="my-form[details][avatars][]" />
	Upload an avatar: <input type="file" name="my-form[details][avatars][]" />

在这种情况下，返回的文件数组将会像是这样::

	[
		'my-form' => [
			'details' => [
				'avatar' => [
					0 => /* UploadedFile instance */,
					1 => /* UploadedFile instance */
			]
		]
	]

单个文件
-----------

如果你只需要访问单个文件，你可以使用 ``getFile()`` 方法来直接获取文件实例。其将会返回一个 ``CodeIgniter\HTTP\Files\UploadedFile`` 实例:


最简使用
^^^^^^^^^^^^^^

使用最简方式，一个单文件提交表单可能会是这样::

	<input type="file" name="userfile" />

其将会返回一个简单的文件实例像是::

	$file = $this->request->getFile('userfile');


数组表示法
^^^^^^^^^^^^^^

如果你在标签名称中使用数组表示法，input 标签将看上去像是这样::

	<input type="file" name="my-form[details][avatar]" />

这样来获取文件实例::

	$file = $this->request->getFile('my-form.details.avatar');


多文件
^^^^^^^^^^^^^^

	<input type="file" name="images[]" multiple />

在控制器中::

	if($imagefile = $this->request->getFiles())
	{
	   foreach($imagefile['images'] as $img)
	   {
	      if ($img->isValid() && ! $img->hasMoved())
	      {
	           $newName = $img->getRandomName();
	           $img->move(WRITEPATH.'uploads', $newName);
	      }
	   }
	}

	循环中的 **images** 是表单中的字段名称

如果多个文件使用相同名称提交，你可以使用 ``getFile()`` 去逐个获取每个文件::
在控制器中::

	$file1 = $this->request->getFile('images.0');
	$file2 = $this->request->getFile('images.1');

另外一个例子::

	Upload an avatar: <input type="file" name="my-form[details][avatars][]" />
	Upload an avatar: <input type="file" name="my-form[details][avatars][]" />

在控制器中::

	$file1 = $this->request->getFile('my-form.details.avatars.0');
	$file2 = $this->request->getFile('my-form.details.avatars.1');

.. note:: 使用  ``getFiles()`` 更合适。

=====================
使用文件
=====================

一旦你获取到了 UploadedFile 实例,你可以以安全的方式检索到文件的信息，还能将文件移动到新的位置。

验证文件
-------------

你可以调用 ``isValid()`` 方法来检查文件是否是通过 HTTP 无误上传的::

	if (! $file->isValid())
	{
		throw new RuntimeException($file->getErrorString().'('.$file->getError().')');
	}

如这个例子所见，如果一个文件产生一个上传错误，你可以通过 ``getError()`` 和 ``getErrorString()`` 方法获取错误码（一个整数）和错误消息。通过此方法可以发现以下错误:

* 文件大小超过了 upload_max_filesize 配置的值。
* 文件大小超过了表单定义的上传限制。
* 文件仅部分被上传。
* 没有文件被上传。
* 无法将文件写入磁盘。
* 无法上传文件：缺少临时目录。
* PHP扩展阻止了文件上传。


文件名称
----------

**getName()**

你可以通过 ``getName()`` 提取到客户端提供的文件的原始名称。其通常是由客户端发送的文件名，不应受信。如果文件已经被移动，将返回移动文件的最终名称::

	$name = $file->getName();

**getClientName()**

总是返回由客户端发送的上传文件的原始名称，即使文件已经被移动了::

  $originalName = $file->getClientName();

**getTempName()**

要获取在上传期间产生的临时文件的全路径，你可以使用 ``getTempName()`` 方法::

	$tempfile = $file->getTempName();


其他文件信息
---------------

**getClientExtension()**

基于上传文件的名称，返回原始文件扩展名。这不是一个值得信赖的来源。对于可信的版本，请使用 ``getExtension()`` 来代替::

	$ext = $file->getClientExtension();

**getClientType()**

返回由客户端提供的文件的媒体类型(mime type)。这不是一个值得信赖的值，对于可信的版本，请使用 ``getType()`` 来代替::

	$type = $file->getClientType();

	echo $type; // image/png

移动文件
------------

每个文件都可以使用恰如其名的 ``move()`` 方法来移动到新的位置。使用第一个参数为目标目录来移动文件::

	$file->move(WRITEPATH.'uploads');

默认的，将使用文件原始名称。你可以指定一个新的文件名称作为第二个参数传递给方法。

	$newName = $file->getRandomName();
	$file->move(WRITEPATH.'uploads', $newName);

一旦文件被移除，将删除临时文件。你可以通过 ``hasMoved()`` 方法来检查文件是否已经被移动了，返回布尔值::

    if ($file->isValid() && ! $file->hasMoved())
    {
        $file->move($path);
    }
