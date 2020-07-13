#!/bin/bash
#
for (( counter=100000; counter>0; counter-- ))
do
	echo -n "$RANDOM "
	cho $RANDOM >> /data/input/SomeRandomNumbers.txt
done

printf "Sorting\n"
sort -r /data/input/SomeRandomNumbers.txt > /data/ouput/SortedRandomNumbers.txt
printf "\n"