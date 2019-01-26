#!/bin/bash
cd `dirname $0`
ls ../DLids/ids/ | xargs -i basename {} .txt > screen_name.txt

