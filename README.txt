I am a Duck
===========

This is a display for "quacks", cat pictures and other home comforts. The Information on this memory stick is what makes it work - read on to find out how to change settings and get things working in a new location.

Changing Settings
=================

All the settings are held in .INI files in the same folder as this README file. They are plain text files that you can open, edit and save using Windows Notepad. You will only need to edit some of the settings.

IMPORTANT: when editing the settings file, only change the text after the "=" symbol on each line, and make sure that you keep any quotes ("") when editing.
 
WiFi
====

The most important thing is to set up wireless networking for wherever you are. The display will still work without being connected to a network, but it won't be able to download new "quacks" or cat pictures and it won't stay synchronised with other displays.

Edit the file called "wifi.ini".

You will first need to change the country setting to match where you currently are:

  country=gb

Helpful values are "gb" (United Kingdom); "gr" (Greece); "de" (Germany); "at" (Austria); "ch" (Switzerland). The full list is available at https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2

Then edit the [network1] section to match your network:

  [network1]
    ssid="my_wifi_network_name"
    key="my_wifi_network_password"
  
You can add another network in the [network2] section if you need to. You'll see I've already added details for some other networks like our home network (Avocado).

These settings assume that you are using a standard, domestic wireless network - they won't work for something like EduRoam! If you don't have access to a standard WiFi network, then you could try "tethering" the display to your phone (see below)
