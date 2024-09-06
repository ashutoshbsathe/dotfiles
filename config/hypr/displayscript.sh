#!/usr/bin/bash

main() {
    MONITORS=$(hyprctl monitors all -j)
    MONITOR_COUNT=$(jq 'length' <<<"$MONITORS")
    INTERNAL=$(jq '.[] | select(.name | startswith("eDP-"))' <<<"$MONITORS")
    INTERNAL_NAME=$(jq -r '.name' <<<$INTERNAL)
    INTERNAL_DISABLED=$(jq '.disabled' <<<"$INTERNAL")
    EXTERNALS=$(jq "map(select(.id!=$(jq '.id' <<<"$INTERNAL")))" <<<"$MONITORS")
    EXTERNAL_COUNT=$(jq 'length' <<<"$EXTERNALS")

    enable_internal() {
        hyprctl keyword monitor "$INTERNAL_NAME,enable" >/dev/null 2>&1
    }
    disable_internal() {
        hyprctl keyword monitor "$INTERNAL_NAME,disable" >/dev/null 2>&1
    }

    if [[ $EXTERNAL_COUNT > 0 ]]; then
        if [[ $INTERNAL_DISABLED = "false" ]]; then
            disable_internal
        fi
    else
        if [[ $INTERNAL_DISABLED = "true" ]]; then
            enable_internal
        fi
    fi
}

main

handle_hyprland_event() {
    case "$1" in
    monitor*)
        main
        ;;
    esac
}

for var in "$@"; do
    if [[ $var = "daemon" ]]; then
        socat -U - UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock | while read -r line; do handle_hyprland_event "$line"; done
        exit 1
    fi
done
