robotframework-RanorexLibrary
=============================

Remote Ranorex library to integrate with Robot Framework

Introduction
============
This is basic implementation of Ranorex test tool (www.ranorex.com) to use
with Robot Framework.

Installation
============
To run remote server you need:
- ranorexremoteserver.py (https://github.com/robotframework/PythonRemoteServer)
- ironpython (https://ironpython.codeplex.com/releases/view/90087)

Run
===
To run remote server on machine just type:
ipy.exe/ipy64.exe rxconnector.py [args]
- argument should be :   <ip> <port> to run on
eg.   ipy.exe rxconnector.py 10.1.32.43 8452

In Robot Framework test suite/case just specify
Library    Remote    ip:port
and run keywords that are implemented in here
