#!/usr/bin/env bash

set -e

DEFAULT_MODULE_NAME=src.main

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME"}

exec python -m $APP_MODULE