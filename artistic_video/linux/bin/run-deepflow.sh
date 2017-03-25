#!/usr/bin/env bash

./linux/bin/deepmatching-static $1 $2 -nt 0 | ./linux/bin/deepflow2-static $1 $2 $3 -match