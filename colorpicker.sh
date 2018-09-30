#!/bin/bash

who=$(whoami)
echo $who > /home/swood/scripts/cscheme/who.txt

CHOICE=$(/home/swood/scripts//cscheme/cscheme.py list | dmenu)

echo $CHOICE >> /home/sood/scripts/cscheme/who.txt

/home/swood/scripts/cscheme/cscheme.py set $CHOICE
