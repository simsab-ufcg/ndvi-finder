#!/bin/bash

curl https://landsat-pds.s3.amazonaws.com/c1/L8/scene_list.gz --output scene_list.gz
gunzip scene_list.gz