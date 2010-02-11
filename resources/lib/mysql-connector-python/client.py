#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Connector/Python, native MySQL driver written in Python.
Copyright 2009 Sun Microsystems, Inc. All rights reserved. Use is subject to license terms.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

"""
Simple CLI using the Connector/Python. It does not take arguments so
you'll need to set the proper login information manually.

Example output:

$ ./client.py 
Welcome to MySQL Python CLI.
Your MySQL connection ID is 21.
Server version: 5.0.62-enterprise-gpl

Python 2.5.1 (r251:54863, Jan 17 2008, 19:35:17) 
[GCC 4.0.1 (Apple Inc. build 5465)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(MySQLConsole)
>>> show tables;
1046 (3D000): No database selected
>>> use test;
>>> show tables;
>>> create table t1 (id int);
>>> show tables;
[u't1']

"""

import sys
import os
import readline
import code
import atexit
import re

# We're actually just a demo and supposed to run in the source directory.
sys.path.append('.')

import mysql.connector

class MySQLConsole(code.InteractiveConsole):
    mysql = None
    regexp = {}
    
    def __init__(self, mysql, locals=None, filename="<console>",
                 histfile=os.path.expanduser("~/.mysql_history")):
        code.InteractiveConsole.__init__(self)
        self.init_history(histfile)
        self.mysql = mysql

        self.regexp['USE'] = re.compile('USE (\w*)', re.IGNORECASE)

    def init_history(self, histfile):
        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile):
        readline.write_history_file(histfile)
    
    def send_query(self, line):
      rows = ()
      try:
          cursor = self.mysql.cursor()
          cursor.execute(line)
          rows = cursor.fetchall()
      except mysql.connector.errors.InterfaceError, e:
          print e.errmsglong
      else:
          for row in rows:
              print row
    
    def _do_use(db):
      try:
          my.cmd_init_db(db)
      except mysql.connector.errors.InterfaceError, e:
          print e
            
    def push(self, line):
      try:
        res = self.regexp['USE'].findall(line)
        db = res[0]
        self._do_use(db)
      except:
        pass
      self.send_query(line)
      code.InteractiveConsole(self, line)


if __name__ == '__main__':

    print "Welcome to MySQL Python CLI."
    
    try:
        db = mysql.connector.Connect(unix_socket='/tmp/mysql.sock', user='root', password='')
    except mysql.connector.errors.InterfaceError, e:
        print e
        sys.exit(1)
    
    console = MySQLConsole(db)
    
    print "Your MySQL connection ID is %d." % (db.get_server_threadid())
    print "Server version: %s" % (db.get_server_version())
    print
    
    console.interact()


