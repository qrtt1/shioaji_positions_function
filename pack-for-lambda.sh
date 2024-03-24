#!/usr/bin/env bash

rm -rf output output.zip
pip install . --target output
cd output
zip -r ../output.zip .