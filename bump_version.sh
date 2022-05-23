#!/bin/bash


TAG=$(git tag | tail -n1)
echo $TAG
version=$(cut -c 1- <<< $TAG)
echo $version

sed -i "s/$TAG/v$1/"  package.json
sed -i "s/$version/$1/" pyproject.toml
