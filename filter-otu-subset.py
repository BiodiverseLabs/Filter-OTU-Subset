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

# Save all extracted sample IDs to a text file
sample_id_filename = f"extracted_sample_ids-{len(metadata_sample_ids)}samples.txt"
sample_id_filepath = os.path.join(current_dir, sample_id_filename)
with open(sample_id_filepath, 'w') as sample_file:
    for sample_id in metadata_sample_ids:
        sample_file.write(f"{sample_id}\n")

# Step 2: Load OTU table
otu_table = pd.read_csv(otu_table_file, sep="\t")

# User input for minimum number of reads
try:
    min_reads_threshold = int(input("Enter the minimum number of reads to include OTUs (default is > 0): ") or 0)
except ValueError:
    print("Invalid input. Using default minimum threshold of > 0.")
    min_reads_threshold = 0

# Filter columns to include only those in metadata_sample_ids
filtered_sample_ids = [col for col in otu_table.columns if col in metadata_sample_ids]
filtered_otu_table = otu_table[["SH_name"] + filtered_sample_ids]

# Remove rows (OTUs) where the sum of the row is 0
filtered_otu_table["Row_Sum"] = filtered_otu_table.iloc[:, 1:].sum(axis=1)
filtered_otu_table = filtered_otu_table[filtered_otu_table["Row_Sum"] > 0]

# Count the number of samples and OTUs
num_samples = len(filtered_sample_ids)
num_otus = filtered_otu_table.shape[0]

# Save the new OTU table
intermediary_otu_filename = f"{os.path.splitext(otu_table_file)[0]}-filtered-{num_samples}samples-{num_otus}otus.txt"
intermediary_otu_filepath = os.path.join(current_dir, intermediary_otu_filename)
filtered_otu_table.drop(columns=["Row_Sum"]).to_csv(intermediary_otu_filepath, sep="\t", index=False)

# Step 3: Create a revised FASTA file
filtered_otu_names = set(filtered_otu_table["SH_name"])
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

# Save the filtered FASTA file
filtered_fasta_filename = f"{os.path.splitext(fasta_file)[0]}_filtered_{total_sequences}_sequences_min{min_reads_threshold}reads.fa"
filtered_fasta_filepath = os.path.join(current_dir, filtered_fasta_filename)
with open(filtered_fasta_filepath, 'w') as outfile:
    for sequence in filtered_sequences:
        outfile.write(sequence)

# Summary
print(f"Sample IDs file saved as: {sample_id_filepath}")
print(f"Intermediary OTU table saved as: {intermediary_otu_filepath}")
print(f"Filtered FASTA file saved as: {filtered_fasta_filepath}")
print(f"Total sequences in the filtered FASTA file: {total_sequences}")
print(f"Number of samples in intermediary OTU table: {num_samples}")
print(f"Number of OTUs in intermediary OTU table: {num_otus}")



