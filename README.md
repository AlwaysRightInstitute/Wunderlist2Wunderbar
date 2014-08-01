Wunderlist2Wunderbar
====================

Convert a Wunderlist HTML to a proper, standardized, format.

Wunderlist doesn't support accepted Internet standards, namely iCalendar and
CalDAV. Bummer.

There are two components to this:
- public/published lists like the excellent "Must-Read Software Developer Books" (https://www.wunderlist.com/lists/70326287)
- access from CalDAV clients to the personal Wunderlists


The former obviously shouldn't be delivered in a proprietary format but in
nothing else but iCalendar. Just like holiday calendars and such are nowadays
freely available in a standard format (http://icalshare.com/ being one hub),
lists like that should be as well.

Unfortunately Wunderlist doesn't, but the Python script provided here converts
the Wunderlist HTML pages to proper VCALENDAR files containing the respective
VTODO items.
You should be able to import the output of the script into Apple Reminders,
Outlook, Lotus Notes, Mozilla Lightning, and any other 'legacy' todo list app.


External developers can't do much about the second, the Wundercloud is a silo
not supporting Internet standards. Which is why I still recommend to use the
Apple Reminders applications. Despite the excellent user interface they get
one part right - they are proper CalDAV clients. And iCloud is a proper CalDAV
server allowing you to access your data in the standard format.


### Using the Script

Having a Wunderlist URL like:
[https://www.wunderlist.com/lists/70326287](https://www.wunderlist.com/lists/70326287)
![](http://imgur.com/PbVJGZS.png)

Run the script like this:
```Python
./Wunderlist2Wunderbar.py \
  https://www.wunderlist.com/lists/70326287 \
  > ~/Desktop/Booklist.ics
```

And you can drag the Booklist.ics file on top of the Reminders application.
You'll end up with this:
![](http://imgur.com/34FBzhe.png)

As mentioned you should also be able to import this into Outlook or Notes,
or pretty much any non-hipster calendaring/todolist app :-)
