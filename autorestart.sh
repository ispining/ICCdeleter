#!/bin/bash

PYTHON="C:\Users\user1\AppData\Local\Programs\Python\Python38-32\python.exe"

function myprocess {


$PYTHON main.py start 

}
NOW=$(date +"%b-%d-%y")

until myprocess; do
     echo "$NOW Prog crashed. Restarting..." >> error.txt
     sleep 1
done