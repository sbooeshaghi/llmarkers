#!/bin/bash

# Activate jats virtual environment
source /Users/sinabooeshaghi/projects/claim-validation/jats/.venv/bin/activate

# Base directory
BASE_DIR="/Users/sinabooeshaghi/projects/llmarkers/data/biorxiv/meca"

cd "$BASE_DIR"

count_success=0
count_fail=0
count_skip=0

# Process each folder
for folder in */; do
  folder="${folder%/}"

  # Find XML file in content folder
  xml_file=$(find "$BASE_DIR/$folder/content" -name "*.xml" -type f 2>/dev/null | head -1)
  manifest_file="$BASE_DIR/$folder/manifest.xml"

  if [ -f "$xml_file" ] && [ -f "$manifest_file" ]; then
    base_name=$(basename "$xml_file" .xml)
    output_file="$BASE_DIR/$folder/content/${base_name}.md"

    echo "Converting: $folder"

    if jats convert "$xml_file" -m "$manifest_file" --no-refs -o "$output_file" 2>&1; then
      echo "✓ Created: ${base_name}.md"
      ((count_success++))
    else
      echo "✗ Failed: $folder"
      ((count_fail++))
    fi
    echo ""
  else
    if [ ! -f "$xml_file" ]; then
      echo "⚠ Skipping $folder (no XML file)"
    elif [ ! -f "$manifest_file" ]; then
      echo "⚠ Skipping $folder (no manifest)"
    fi
    ((count_skip++))
  fi
done

echo "============================================"
echo "Summary:"
echo "  Successful: $count_success"
echo "  Failed: $count_fail"
echo "  Skipped: $count_skip"
echo "============================================"
