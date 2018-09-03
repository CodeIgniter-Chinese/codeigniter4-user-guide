##############
安全类
##############

安全类包含了一些方法，用于帮助保护你的网站，以免受到跨站请求伪造（CSRF）的攻击。

.. contents:: Page Contents
	:local:

*******************
Loading the Library
*******************

If your only interest in loading the library is to handle CSRF protection, then you will never need to load it,
as it is ran as filter and has no manual interaction.

If you find a case where you do need direct access, though, you may load it through the Services file::

	$security = \Config\Services::security();

*********************************
Cross-site request forgery (CSRF)
*********************************

You can enable CSRF protection by altering your **application/Config/Filters.php**
and enabling the `csrf` filter globally::

	public $globals = [
		'before' => [
			'csrf'
		]
	];

Select URIs can be whitelisted from CSRF protection (for example API
endpoints expecting externally POSTed content). You can add these URIs
by adding them as exceptions in the filter::

	public $globals = [
		'before' => [
			'csrf' => ['except' => ['api/record/save']]
		]
	];

Regular expressions are also supported (case-insensitive)::

    public $globals = [
		'before' => [
			'csrf' => ['except' => ['api/record/[0-9]+']]
		]
	];

If you use the :doc:`form helper <../helpers/form_helper>`, then
:func:`form_open()` will automatically insert a hidden csrf field in
your forms. If not, then you can use the always available ``csrf_token()``
and ``csrf_hash()`` functions
::

	<input type="hidden" name="<?= csrf_token() ?>" value="<?= csrf_hash() ?>" />

Additionally, you can use the ``csrf_field()`` method to generate this 
hidden input field for you::

	// Generates: <input type="hidden" name="{csrf_token}" value="{csrf_hash}" />
	<?= csrf_field() ?>

Tokens may be either regenerated on every submission (default) or
kept the same throughout the life of the CSRF cookie. The default
regeneration of tokens provides stricter security, but may result
in usability concerns as other tokens become invalid (back/forward
navigation, multiple tabs/windows, asynchronous actions, etc). You
may alter this behavior by editing the following config parameter
::

	public $CSRFRegenerate  = true;

*********************
Other Helpful Methods
*********************

You will never need to use most of the methods in the Security class directly. The following are methods that
you might find helpful that are not related to the CSRF protection.

**sanitizeFilename()**

Tries to sanitize filenames in order to prevent directory traversal attempts and other security threats, which is
particularly useful for files that were supplied via user input. The first parameter is the path to sanitize.

If it is acceptable for the user input to include relative paths, e.g. file/in/some/approved/folder.txt, you can set
the second optional parameter, $relative_path to true.
::

	$path = $security->sanitizeFilename($request->getVar('filepath'));
