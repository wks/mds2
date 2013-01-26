#!/usr/bin/python2

# Copyright (C) 2013 Kunshan Wang
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
mds2 : Maven Document Server
"""

import SocketServer as ss
import BaseHTTPServer as bhs
import os
import os.path
import sys
import zipfile
import cgi
import shutil

repos = []

common_header = """<!DOCTYPE html>
<html>
     <head>
         <title>Maven Document Server</title>
     </head>
     <body>
     <h1>Maven Document Server</h1>
"""

common_footer = """    </body>
</html>"""

mimetypes = {
        ".html": "text/html",
        ".htm": "text/html",
        ".css": "text/css",
        ".js": "text/javascript",
        ".txt": "text/plain",
        ".gif": "image/gif",
        ".png": "image/png",
        ".mf": "text/plain",
        }
def infer_mimetype(name):
    name_lc = name.lower()
    for k,v in mimetypes.iteritems():
        if name_lc.endswith(k):
            return v
    return None

class MyHandler(bhs.BaseHTTPRequestHandler):
    def do_GET(self):
        p = self.path

        if p == '/':
            self.serve_index()
        else:
            self.serve_content(p)

    def serve_index(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        self.wfile.write(common_header)
    
        for repo in repos:
            self.wfile.write("<h2>%s</h2>\n<ul>\n" % cgi.escape(repo))

            in_repo_files = []

            for root, dirs, files in os.walk(repo):
                for name in files:
                    if name.endswith("-javadoc.jar"):
                        fullpath = os.path.join(root, name)
                        in_repo_files.append((name, fullpath))

            for name, fullpath in sorted(in_repo_files):
                self.wfile.write(
                        '<li><a href="%s//">%s</a></li>\n' % (
                            cgi.escape(fullpath, True),
                            cgi.escape(name)))

            self.wfile.write("</ul>\n")

        self.wfile.write(common_footer)

    def serve_content(self, p):
        try:
            jar_path, content_path = p.split(r"//")
            if content_path == "":
                content_path = "index.html"
        except:
            self.send_error(400, "Illegal path: %s"%p)
            return

        try:
            zf = zipfile.ZipFile(jar_path, "r")
        except Exception,e:
            self.send_error(400, "Cannot open jar %s:\n%s"%(jar_path,e))
            return
        else:
            with zf:
                try:
                    f = zf.open(content_path, "r")
                except Exception,e:
                    self.send_error(400, "Cannot open %s in jar %s:\n%s"%(
                        content_path,jar_path, e))
                    return
                else:
                    with f:
                        self.send_response(200)
                        mt = infer_mimetype(content_path)
                        if mt != None:
                            self.send_header("Content-Type", mt)
                        self.end_headers()
                        shutil.copyfileobj(f, self.wfile)

class ThreadedTCPServer(ss.ThreadingMixIn, ss.TCPServer):
    allow_reuse_address = True

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Maven Document Server. Help you read JavaDocs and ScalaDocs in ~/.m2 or ~/.ivy2 or wherever you like.')
    parser.add_argument('-p', '--port', dest='port', type=int, default=63787,
            help='TCP listening port (default: 63787)')
    parser.add_argument('-r', '--user-repos', dest='repos', default=None,
            help='Repositories. Paths separated by colons ":". Will replace default repositories.')
    parser.add_argument('-e', '--user-repos-extra', dest='repos_e', default=None,
            help='Extra repositories. Paths separated by colons ":". Will append after default repositories.')

    args = parser.parse_args()

    global repos
    port = args.port
    homedir = os.getenv("HOME")
    default_repos = [
            os.path.join(homedir, ".m2", "repository"),
            os.path.join(homedir, ".ivy2", "cache"),
            ]
    if args.repos != None:
        repos = args.repos.split(":")
    else:
        repos = default_repos

    if args.repos_e != None:
        repos.extend(args.repos_e.split(":"))

    handler = MyHandler
    httpd = ThreadedTCPServer(("127.0.0.1", port), handler)

    print "Maven Document Server"
    print "Address: http://localhost:%d/" % port
    print
    print "Repositories:"
    for repo in repos:
        print "    ", repo

    httpd.serve_forever()

if __name__=="__main__":
    main()

