#!/bin/bash

IFS=$'\n'

DIR=$1
for file in `ls "$DIR" | grep '\.pdf$'`; do
  mv "$DIR/$file" "$DIR/${file//,/_}"
done;
