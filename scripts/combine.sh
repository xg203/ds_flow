#!/bin/bash

# Usage: ./combine.sh <output_file> <input_file1> <input_file2> ...

OUTPUT_FILE="$1"
shift

if [ -z "$OUTPUT_FILE" ]; then
    echo "Error: Output file not specified"
    exit 1
fi

if [ "$#" -eq 0 ]; then
    echo "Error: No input files specified"
    exit 1
fi

echo "Combining $# files into $OUTPUT_FILE"

# Create/Overwrite output file with the header from the first input file
head -n 1 "$1" > "$OUTPUT_FILE"

# Append content from all files, skipping the header (line 1)
for f in "$@"; do
    tail -n +2 "$f" >> "$OUTPUT_FILE"
done

echo "Done. Preview:"
head -n 5 "$OUTPUT_FILE"
