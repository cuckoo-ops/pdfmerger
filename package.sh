#!/bin/bash

set -e

self_dir=`cd $(dirname $0); pwd`
release_dir=${self_dir}/release

if [ -d ${release_dir} ]; then
    echo "Remove existing release directory: ${release_dir}"
    rm -r ${release_dir}
fi
mkdir -pv ${release_dir}

rm -rvf ${self_dir}/dist ${self_dir}/build ${self_dir}/*.egg-info
#python3 ${self_dir}/setup.py clean --all
python ${self_dir}/setup.py  bdist_wheel -d ${release_dir}

#python3 ${self_dir}/setup.py sdist -d ${release_dir}

echo "Succeeded to create release package."
