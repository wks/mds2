# mds2

*Just a simpler Maven Document Server re-written in Python*

If you want to read the HTML JavaDocs or ScalaDocs in your local Maven or Ivy
repositories (usually in `~/.m2/repository` or `~/.ivy2/cache`), this program
can run a web server and serve the contents inside those `*-javadoc.jar`
packages.

By the way, you have to configure your Maven or SBT to download JavaDoc
packages. This program will not download them for you.

## How to use?

    python2 mds2.py

And then open a browser.

Make sure you use **python2**. Some Linux distributions (e.g. Arch) aliases
`python` as `python3` instead of `python2`. Be careful.

## Command-line parameters

- Choose the TCP listening port with `-p` or `--port`.
- Customize the repositories (where mds2 looks for `*-javadoc.jar` files)
  with `-e` or `-r`.

Invoke `python2 mds2.py --help` for more information.

## Author

Kunshan Wang <wks1986@gmail.com>

## License

MIT license.

## Related works

There is [an older counterpart](https://github.com/wks/mvn-doc-server) written
in Scala, but it just overkills. You may enjoy the small size of this one and
the fact that Python interpreters are automatically present on almost all
machines (sorry, MS Windows users).

