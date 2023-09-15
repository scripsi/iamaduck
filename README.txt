I am a Duck
===========

This is a display for "quacks", cat pictures and other home comforts. The Information on this memory stick is what makes it work - read on to find out how to change settings and get things working in a new location.

Changing Settings
=================

All the settings are held in a file called "settings.txt" in the same folder as this README file. It is a plain text file that you can open, edit and save using Windows Notepad. You will only need to edit some of the settings, but if you want to find out what all of them do, have a look at "docs\settings-example.txt" which is a fully commented version of the settings file.

IMPORTANT: when editing the settings file, only change the text after the ":" symbol on each line. Make sure that you don't change the spacing at the beginning of a line.
 
WiFi
====

The most important thing is to set up wireless networking for wherever you are. The display will still work without being connected to a network, but it won't be able to download new "quacks" or cat pictures and it won't stay synchronised with other displays.

You will first need to change the country setting to match where you currently are:

  wifi_country: uk

Helpful values are "gb" (United Kingdom); "gr" (Greece); "de" (Germany); "at" (Austria); "ch" (Switzerland). The full list is available at https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2

Then edit the following lines to match your network:

  - network: my_network
    ssid   : my_wifi_name
    key    : my_wifi_password

You can repeat those three lines to add more than one wireless network if you need. You'll see I've already done that for some standard networks like our home network (Avocado).

These settings assume that you are using a standard, domestic wireless network - they won't work for something like EduRoam! If you don't have access to a standard WiFi network, then you could try "tethering" the display to your phone (see below)
