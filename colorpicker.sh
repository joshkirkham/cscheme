#!/bin/bash


CHOICE=$(/home/swood/scripts/cscheme/cscheme.py list | dmenu)

echo $CHOICE >> /home/sood/scripts/cscheme/who.txt

/home/swood/scripts/cscheme/cscheme.py set $CHOICE
