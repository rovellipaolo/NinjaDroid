#!/usr/bin/env bash

case "$1" in
    ninjadroid|ninjadroid.py)
        shift
        exec python3 $NINJADROID_HOME/ninjadroid.py $@
        ;;
    help)
        echo "ninjadroid ninjadroid.py|json|html|version [opts]"
        echo ""
        echo " ninjadroid json <apk>: prints JSON to STDOUT"
        echo " ninjadroid html <apk>: prints HTML to STDOUT"
        echo " ninjadroid ninjadroid.py <...>"
        ;;
    json|html)
        format=$1
        apk_file=$2
        output_dir=$(mktemp -d)
        log_path=/var/log/ninjadroid/output
        python3 $NINJADROID_HOME/ninjadroid.py -e $output_dir $apk_file >$log_path 2>&1
        output_file=$(ls $output_dir | grep "report-.*\.$format$" | head -1)
        if [[ ! -z $output_file ]] ; then
            exec cat $output_dir/$output_file
        else
            cat $log_path >&2 && exit 1
        fi
        ;;
    *)
        # Pass through other commands, like /bin/bash
        exec "$@"
        ;;
esac
