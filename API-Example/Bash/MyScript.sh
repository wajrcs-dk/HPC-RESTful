#!/bin/bash
#
for i in {1..100000}; do
echo $RANDOM >> /data/input/SomeRandomNumbers.txt
sort -r /data/input/SomeRandomNumbers.txt > /data/ouput/SortedRandomNumbers.txt