collectr: Keep your S3 static files up to date.
===============================================

More and more, we find ourselves storing our static website files - CSS,
Javascript, images and more - on `Amazon S3 <http://aws.amazon.com/s3/>`_. Some
of us do it because we use services like `Heroku <http://www.heroku.com/>`_ and
don't want to force the static files through our web dynos. Others of us do it
to avoid huge bandwidth costs associated with hosting these on our own servers.
Still others do it to take advantage of the scale and distributed nature of S3.

However, managing our S3 files can be a pain. Each time we change them we have
to minify and reupload them. We also need to set all the metadata we want:
things like Cache-Control headers. This can be boring and error-prone. collectr
aims to help with that.

Using collectr
--------------

collectr is a collection of functions built on top of the
`boto <https://github.com/boto/boto>`_ library. This allows you to plug
collectr into any of your Python code however you see fit. For those who want a
'just works' solution, however, collectr also comes with an example script that
is perfect for using with any Django project.

If you want simple, you can use collectr like this::

    import collectr
    collectr.update('path/to/static/files', 'bucket-name')

collectr will scan the directory, minify anything that can be minified using
whatever tools you have on your system, and upload all your files to the
specified S3 bucket. Anything that already existed on S3 will have all of its
metadata persisted.

Of course, you can have quite a bit more control than that.

::

    import collectr
    statics = collectr.StaticDir('path/to/static/files')
    statics.input_directory = 'path/to/other/dir'
    statics.minifier = 'yuicompressor -o {out_name} {in_name}'
    statics.force_update = True
    statics.ignore = ['*.jpg', '*.json']
    statics.metadata = {'Cache-Control': 'max-age=3600'}
    statics.update('bucket-name')

Before you do anything, though, make sure you have your environment variables
set up. You'll need AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY set to
the correct values.

Features
--------

- Static file minification.
- Ignore filters.
- Multiple directory management.
- Metadata management.
- Fire-and-forget configuration.

Installation
------------

To install collectr::

    $ pip install collectr

If you don't have ``pip`` and can't install it, you should complain to your
sysadmin, and then do::

    $ easy_install collectr

Contributing
------------

collectr welcomes contributions, both bug fixes and new features. Any feature
request should strongly consider the implications for the API. API clarity
is valued above new features, so any feature that complicates the API must add
significant value to the library to be accepted.

If you want to contribute, do the following:

1. Check that your idea hasn't already been proposed. Check both open **and
   closed** issues on GitHub.
2. Fork the repository on GitHub and make your changes.
3. Where possible, write a test that can reproduce the bug, or that will test
   the new feature.
4. Send a Pull Request. Don't forget to add yourself to the AUTHORS file.
