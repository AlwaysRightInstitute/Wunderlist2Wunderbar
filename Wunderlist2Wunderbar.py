#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, optparse, urllib2
import xml.etree.ElementTree as ET

reload(sys)
sys.setdefaultencoding("UTF-8")

# config
usage = "usage: %s <wunderurl>" % ( sys.argv[0], )
usage += "\n"
usage += "Sample:\n"
usage += "  %s https://www.wunderlist.com/lists/70326287" % ( sys.argv[0], )
optParser = optparse.OptionParser(usage=usage)


# a Wunderlist is not proper XHTML, so we need to patch it up

def cleanupWLCrap(filedata):
  idx = filedata.find("<body")
  filedata = filedata[idx:]
  idx = filedata.find("</body>")
  filedata = filedata[:idx + 7]
  
  # we use the <ol> since we can't easily scan for </div> close tags in invalid
  # XML
  idx = filedata.find('<ol class="tasks')
  filedata = filedata[idx:]
  idx = filedata.find("</ol>")
  filedata = filedata[:idx + 5]
  return filedata


def hasAttr(node, attr, value):
  if not node.attrib.has_key(attr):
    return None
  
  v  = node.attrib[attr]
  vs = v.split(" ")
  return value in vs
  
def iCalEscapeValue(str):
  #  FIXME: properly escape ...
  return str


class MakeWunderlistWunderbar:

  def handleTaskItem(self, node):
    """
    <li class="taskItem" aria-label="Release It: Design and Deploy .. 
               http://www.amazon.com/Release-It-Production-Ready-Pragmatic-Programmers/dp/0978739213">
      <span class="checkBox left"></span>
      <div class="title">
        Release It: Design and Deploy Production-Ready Software - Michael Nygard 
        <a href="http://www.amazon.com/Release-It-Production-Ready-Pragmatic-Programmers/dp/0978739213" target="_blank">www.amazon.com/Release-It-Production-Ready-Pragmatic-Programmers/dp/0978739213</a>
      </div>
    </li>
    """
    title = ""
    url   = ""
    for child in node:
      if hasAttr(child, "class", "title"):
        title =  child.text.strip()
        u = child.find("a")
        if u is not None:
          url = u.attrib["href"]
    
    print "BEGIN:VTODO"
    print "STATUS:NEEDS-ACTION" # this is a template ...
    print "SUMMARY:" + iCalEscapeValue(title)
    print "URL:"     + iCalEscapeValue(url)
    # Lame: OSX reminders doesn't support URL ...
    print "DESCRIPTION:"     + iCalEscapeValue(url)
    print "END:VTODO"

  def handleTaskList(self, node):
    for child in node:
      if hasAttr(child, "class", "taskItem"):
        self.handleTaskItem(child)

  # we could actually import this info, - if, the HTML wouldn't be crap
  """
  <div class="tasks container">
    <h1 class="information">
      <span class="list-name">Must-Read Software Developer Books</span>
      <div class="avatar">
        <img src="https://a.wunderlist.com/api/v1/avatar?user_id=4194452"/>
      </div>
      <span class="sender-name">
        Published by Chad Fowler
      </span>
    </h1>
  """

  def scanHTML(self, root):
    print "BEGIN:VCALENDAR"
    print "VERSION:2.0"
    print "PRODID:-//Always Right Institute//Wunderbar//EN"
    print "CALSCALE:GREGORIAN"
    
    for child in root:
      if hasAttr(child, "class", "tasks"):
        self.handleTaskList(child)
    
    print "END:VCALENDAR"

def main():
  options, args = optParser.parse_args()
  if len(args) < 1:
    print usage
    sys.exit(42)

  # load wunderlist
  if not args[0].startswith("http"):
    filename = args[0]
    f = open(filename, "r")
    filedata = f.read()
    f.close()
  else:
    response = urllib2.urlopen(args[0])
    filedata = response.read()
  
  # parse
  tree = ET.fromstring(cleanupWLCrap(filedata))

  # process
  root = ( tree, )

  w2w = MakeWunderlistWunderbar()
  w2w.scanHTML( root )

if __name__ == "__main__":
  main()
