#!/bin/bash

function find_files(){
  files=$(git diff --name-only --diff-filter=AM HEAD~1..HEAD /github/workspace)
}

find_files
python3 /analyze.py --files $files --repoloc /github/workspace
