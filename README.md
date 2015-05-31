# Lobotomy #

This readme will give you a brief introduction about Lobotomy and us.

## What is Lobotomy? ##

Lobotomy consists of a web front-end and several Python scripts to allow easier analysis of a memory image. It was made to save time, work with multiple researchers on the same data simultaneously and get to easily spot suspicious data using basic filters.

## The 'Lobotomy Workflow' ##

### Yourjob ###
* Create a memory image
* Upload the image to Lobotomy

### Lobotomy's job ###
* Lobotomy automatically detects a new image
* Lobotomy calculates md5 and sha256 hashes for the image
* Lobotomy determines the profile
* Lobotomy starts up volatility plugins, bulk extractor and photorec
* Lobotomy stores all output in a database
* Lobotomy puts all extracted files in a seperate folder and calculates md5 and sha256 hashes

### Yourjob (continued) ###
* Open your webbrowser and start analyzing the data

### Contributors ###

* Wim Venhuizen <wim@lobotomy.nl>
* Jeroen Hagebeek <jeroen@lobotomy.nl>