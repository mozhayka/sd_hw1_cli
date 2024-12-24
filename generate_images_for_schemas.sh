#!/bin/bash

PLANTUML_CMD="plantuml"

# shellcheck disable=SC2207
CHANGED_FILES=($(ls -l seminar_tasks/ | grep -E -wo "[A-Za-z0-9\-]+\.puml"))

if [ ${#CHANGED_FILES[@]} -eq 0 ]; then
    echo "No .puml files changed."
    exit 0
fi

for file in "${CHANGED_FILES[@]}"
do
    OUTPUT_FILE="$(basename "$file" .puml).svg"
    echo "$OUTPUT_FILE"
    echo "Generating SVG for $file -> seminar_tasks/$OUTPUT_FILE"
    $PLANTUML_CMD -tsvg "./seminar_tasks/$file" -o "./" || exit 1
done

echo "PlantUML schemas are up to date"
exit 0
