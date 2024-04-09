#!/bin/bash

# Function to calculate the greatest common divisor (GCD) of two numbers
gcd() {
    if [ $2 -eq 0 ]; then
        echo $1
    else
        gcd $2 $(($1 % $2))
    fi
}

# Ensure a POSCAR file is provided as an argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <POSCAR_FILE>"
    exit 1
fi

# Check if the provided file exists
if [ ! -f "$1" ]; then
    echo "Error: File $1 not found!"
    exit 1
fi

# Extract the chemical symbols and counts from the POSCAR file
chemical_symbols=$(sed -n '6p' "$1")
atom_counts=$(sed -n '7p' "$1")

# Convert the chemical symbols and counts into arrays
IFS=' ' read -r -a symbols_array <<< "$chemical_symbols"
IFS=' ' read -r -a counts_array <<< "$atom_counts"

# Create arrays to store symbols and counts
symbols=()
counts=()

# Iterate over the arrays to store counts for each symbol
for ((i=0; i<${#symbols_array[@]}; i++)); do
    symbol="${symbols_array[$i]}"
    count="${counts_array[$i]}"
    if [[ " ${symbols[@]} " =~ " $symbol " ]]; then
        index=$(printf "%d\n" $(echo "${symbols[@]}" | grep -nw "$symbol" | cut -d: -f1))
        counts[$index-1]=$(( counts[$index-1] + count ))
    else
        symbols+=("$symbol")
        counts+=("$count")
    fi
done

# Calculate the greatest common divisor (GCD) for each element's count
gcd_result=${counts[0]}
for count in "${counts[@]}"; do
    gcd_result=$(gcd $gcd_result $count)
done

# Print the chemical formula in the most reduced form
for ((i=0; i<${#symbols[@]}; i++)); do
    reduced_count=$(( counts[$i] / gcd_result ))
    if [ "$reduced_count" -gt 1 ]; then
        echo -n "${symbols[$i]}$reduced_count"
    else
        echo -n "${symbols[$i]}"
    fi
done

echo ""  # Newline
