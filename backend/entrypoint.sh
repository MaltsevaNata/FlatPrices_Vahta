#!/bin/sh

supervisord -c supervisord.conf
exec "$@"