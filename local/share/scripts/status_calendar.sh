#!/bin/sh 
notify-send  "Calendar" "$(cal --color=always | sed "s/..7m/<b><span color=\"#ff0000\">/;s/..27m/<\/span><\/b>/" | sed "s/^/     /")"
# TODO: Fix text output
