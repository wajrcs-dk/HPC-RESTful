#!/bin/bash
#
for (( counter=100000; counter>0; counter-- ))
do
	echo -n "$RANDOM "
	echo $RANDOM >> /data/input/SomeRandomNumbers.txt
done

printf "Sorting\n"
sort -r /data/input/SomeRandomNumbers.txt > /data/output/SortedRandomNumbers.txt
printf "\n"