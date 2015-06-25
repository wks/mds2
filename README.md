# mds2

*Just a simpler Maven Document Server re-written in Python*

`mds2` is a simple HTTP server. It will serve all files with the suffix
"-javadoc.jar" in the following directories:

* `~/.m2/repository`
* `~/.ivy2/cache`
* `~/.mds2/jars`

## How to use?

If you use Maven, SBT or other tools that download jar packages for you, you
need to configure them to also download the JavaDoc packages.

To start the HTTP server, invoke:

    python3 mds2.py

And then open a browser.

Make sure you use **python3**. Some systems (e.g. OSX) provides Python 2 and
the `python` command is aliased to `python2`.

## Command-line parameters

- Choose the TCP listening port with `-p` or `--port`.
- Customize the repositories (where mds2 looks for `*-javadoc.jar` files)
  with `-e` or `-r`.

Invoke `python3 mds2.py --help` for more information.

## Author

Kunshan Wang <wks1986@gmail.com>

## License

MIT license.

## Related works

There is [an older counterpart](https://github.com/wks/mvn-doc-server) written
in Scala, but it just overkills. You may enjoy the small size of this one and
the fact that Python interpreters are automatically present on almost all
machines (sorry, MS Windows users).

