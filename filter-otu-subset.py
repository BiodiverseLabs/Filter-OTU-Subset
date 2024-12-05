import os
import pandas as pd

# Automatically detect files based on extensions
current_dir = os.getcwd()
fasta_file = next((f for f in os.listdir(current_dir) if f.endswith((".fa", ".fasta"))), None)
metadata_file = next((f for f in os.listdir(current_dir) if f.endswith((".xlsx", ".xls"))), None)
otu_table_file = next((f for f in os.listdir(current_dir) if f.endswith(".txt")), None)

if not fasta_file or not metadata_file or not otu_table_file:
    raise FileNotFoundError("Required files not found in the current folder. Ensure a .fa/.fasta, .xlsx/.xls, and .txt file are present.")

# Step 1: Load metadata and extract sample IDs
metadata_df = pd.read_excel(metadata_file)
metadata_sample_ids = set(metadata_df["Sample ID"].tolist())

# Step 2: Load OTU table
otu_table = pd.read_csv(otu_table_file, sep="\t")

# User input for minimum number of reads
try:
    min_reads_threshold = int(input("Enter the minimum number of reads to include OTUs (default is > 0): ") or 0)
except ValueError:
    print("Invalid input. Using default minimum threshold of > 0.")
    min_reads_threshold = 0

# Filter columns to include only those in metadata_sample_ids
filtered_otu_table = otu_table[["SH_name"] + [col for col in otu_table.columns if col in metadata_sample_ids]]

# Identify OTUs with counts greater than the threshold in the filtered OTU table
filtered_otu_names = set(
    filtered_otu_table.loc[(filtered_otu_table.iloc[:, 1:] > min_reads_threshold).any(axis=1), "SH_name"]
)

# Step 3: Filter the FASTA file based on OTU names
filtered_sequences = []
with open(fasta_file, 'r') as infile:
    write_flag = False
    current_sequence = ""
    for line in infile:
        if line.startswith('>'):  # Header line
            if write_flag and current_sequence:
                filtered_sequences.append(current_sequence)
            otu_id = line.split('|')[0][1:]  # Extract OTU ID
            write_flag = otu_id in filtered_otu_names
            if write_flag:
                current_sequence = line  # Start new sequence
        elif write_flag:
            current_sequence += line  # Append sequence
    if write_flag and current_sequence:
        filtered_sequences.append(current_sequence)

# Count the total number of sequences
total_sequences = len(filtered_sequences)

# Construct the output file name dynamically
filtered_fasta_filename = f"{os.path.splitext(fasta_file)[0]}_filtered_{total_sequences}_sequences_min{min_reads_threshold}reads.fa"

# Write the filtered sequences to the output FASTA file
filtered_fasta_filepath = os.path.join(current_dir, filtered_fasta_filename)
with open(filtered_fasta_filepath, 'w') as outfile:
    for sequence in filtered_sequences:
        outfile.write(sequence)

# Summary
print(f"Filtered FASTA file saved as: {filtered_fasta_filepath}")
print(f"Total sequences in the filtered FASTA file: {total_sequences}")
