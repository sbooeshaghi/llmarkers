#!/bin/bash

# Script to run mrkr extract on all bioRxiv manuscripts
# Usage: bash run_mrkr_all.sh [N]
#   N = number of parallel jobs (default: 5)

N=${1:-5}

# ============================================
# Configuration
# ============================================

BASE_DIR="/Users/sinabooeshaghi/projects/markergeneextraction/llmarkers/data/biorxiv/meca"
VENV="/Users/sinabooeshaghi/projects/markergeneextraction/llmarkers/.venv/bin/activate"
ENV_FILE="/Users/sinabooeshaghi/projects/markergeneextraction/mrkr/.env"

# ============================================
# Setup
# ============================================

source "$VENV"

if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
fi

# Temp dir for tracking results across subshells
RESULT_DIR=$(mktemp -d)
trap "rm -rf $RESULT_DIR" EXIT

# ============================================
# Single-folder processing function
# ============================================

process_folder() {
    local folder="$1"
    local md_file="$BASE_DIR/$folder/manuscript.md"
    local output_file="$BASE_DIR/$folder/markers.json"
    local metrics_file="$BASE_DIR/$folder/metrics.json"

    if mrkr extract -m "$md_file" -o "$output_file" --metrics "$metrics_file" -v \
        > "$RESULT_DIR/$folder.log" 2>&1; then
        echo "OK" > "$RESULT_DIR/$folder.status"
        echo "OK:   $folder"
    else
        echo "FAIL" > "$RESULT_DIR/$folder.status"
        echo "FAIL: $folder"
    fi
}

# ============================================
# Collect folders to process
# ============================================

cd "$BASE_DIR"

to_process=()
count_skip=0
count_no_md=0

for folder in */; do
    folder="${folder%/}"

    # Skip if already processed (markers.json = success, metrics.json = ran but 0 extractions)
    if [ -f "$BASE_DIR/$folder/markers.json" ] || [ -f "$BASE_DIR/$folder/metrics.json" ]; then
        ((count_skip++))
        continue
    fi

    if [ ! -f "$BASE_DIR/$folder/manuscript.md" ]; then
        ((count_no_md++))
        continue
    fi

    to_process+=("$folder")
done

total=${#to_process[@]}
echo "Papers to process: $total"
echo "Already done:      $count_skip"
echo "No manuscript.md:  $count_no_md"
echo "Parallel jobs:     $N"
echo "========================================"

# ============================================
# Run in parallel
# ============================================

for folder in "${to_process[@]}"; do
    process_folder "$folder" &

    # Wait if we've hit the parallel limit
    while [ "$(jobs -rp | wc -l)" -ge "$N" ]; do
        sleep 0.5
    done
done

# Wait for remaining jobs
wait

# ============================================
# Summary
# ============================================

count_success=0
count_fail=0

for status_file in "$RESULT_DIR"/*.status; do
    [ -f "$status_file" ] || continue
    status=$(cat "$status_file")
    if [ "$status" = "OK" ]; then
        ((count_success++))
    else
        ((count_fail++))
    fi
done

echo ""
echo "========================================"
echo "SUMMARY"
echo "========================================"
echo "  Successful: $count_success"
echo "  Failed:     $count_fail"
echo "  Skipped:    $count_skip (already have markers.json)"
echo "  No markdown: $count_no_md"
echo "========================================"

# List failures if any
if [ "$count_fail" -gt 0 ]; then
    echo ""
    echo "Failed papers:"
    for status_file in "$RESULT_DIR"/*.status; do
        [ -f "$status_file" ] || continue
        if [ "$(cat "$status_file")" = "FAIL" ]; then
            folder=$(basename "$status_file" .status)
            echo "  $folder"
            echo "    Log: $RESULT_DIR/$folder.log"
        fi
    done
fi
