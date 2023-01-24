#!/bin/bash

echo $(xrandr --current)

xrandr --output HDMI-1 --same-as eDP-1

echo "If this did not work, check the port correctly"
