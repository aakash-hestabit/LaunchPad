#!/bin/bash
TIMESTAMP=$(/bin/date +'%Y-%m-%d %H:%M:%S')

/bin/tar -czf "/home/aakash/Desktop/Launchpad/day5/build-${TIMESTAMP}.tgz" /home/aakash/Desktop/Launchpad/day5/*

/usr/bin/sha256sum "/home/aakash/Desktop/Launchpad/day5/build-${TIMESTAMP}.tgz" > "/home/aakash/Desktop/Launchpad/day5/build-${TIMESTAMP}.tgz.sha256"
