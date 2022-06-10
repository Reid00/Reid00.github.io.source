#!/bin/bash
set -e
POST_SLUG="$1"
if [ -z "$POST_SLUG" ]; then
  read -p "Post Name (e.g. your-new-post): " POST_SLUG
fi
# TIMESTAMP=`date +%Y%m%d%H%M%S`
TIMESTAMP=`date +%Y%m%d`
POST_FILENAME="${TIMESTAMP}-${POST_SLUG}.md"
hugo new "posts/${POST_FILENAME}"
sleep 1