#!/bin/bash

# Function to calculate the greatest common divisor (GCD) of two numbers
gcd() {
    a=$1
    b=$2
    while [ $b -ne 0 ]; do
        t=$b
        b=$((a % b))
        a=$t
    done
    echo $a
}

if [ $# -ne 1 ]; then
    echo "Usage: $0 <cif_file>"
    exit 1
fi

cif_file="$1"

# Check if the file exists
if [ ! -f "$cif_file" ]; then
    echo "File not found: $cif_file"
    exit 1
fi

# Extract phase names and counts from CIF file
phase_data=$(grep '_pd_phase_name' "$cif_file" | awk '{print $2}')

# Declare indexed arrays to store elements and counts
elements=()
counts=()

# Loop through each phase data to extract element counts
for phase in $phase_data; do
    # Extract elements and their counts from the phase name
    elements_phase=$(echo "$phase" | grep -o -E '[A-Z][a-z]?[0-9]*')
    for element in $elements_phase; do
        # Extract element symbol and count
        symbol=${element//[0-9]/}
        count=${element//[^0-9]/}
        # symbol=$(echo "$element" | sed 's/[0-9]*//')
        # count=$(echo "$element" | sed 's/[^0-9]*//')

        # Check if the element is already in the array
        found=0
        for ((i = 0; i < ${#elements[@]}; i++)); do
            if [ "${elements[$i]}" == "$symbol" ]; then
                found=1
                break
            fi
        done

        # If the element is not found, add it to the array
        if [ $found -eq 0 ]; then
            elements+=("$symbol")
            counts+=("$count")
        else
            # If the element is found, update its count
            idx=$i
            counts[$idx]=$((counts[$idx] + count))
        fi
    done
done

# Initialize GCD with the first element count
gcd_value=${counts[0]}

# Find the greatest common divisor (GCD) of all element counts
for count in "${counts[@]}"; do
    gcd_value=$(gcd $gcd_value $count)
done

# Build the reduced chemical formula using the GCD
reduced_formula=""
for ((i = 0; i < ${#elements[@]}; i++)); do
    count=$((counts[$i] / gcd_value))
    if [ $count -gt 1 ]; then
        reduced_formula+="${elements[$i]}$count"
    else
        reduced_formula+="${elements[$i]}"
    fi
done

# Print the reduced chemical formula
echo "$reduced_formula"
