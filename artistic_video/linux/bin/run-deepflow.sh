#!/usr/bin/env bash

./artistic_video/linux/bin/deepmatching-static $1 $2 -nt 0 | ./artistic_video/linux/bin/deepflow2-static $1 $2 $3 -match