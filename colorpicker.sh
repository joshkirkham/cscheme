#!/bin/bash

CHOICE=$(./cscheme.py list | dmenu)

./cscheme.py set $CHOICE
