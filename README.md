# Automatic Filtering of FASTA Sequences Using Metadata and OTU Tables

This repository contains a Python script that automates the filtering of a FASTA file based on metadata and an OTU (Operational Taxonomic Unit) table. The script dynamically detects input files in its working directory and allows the user to specify a minimum read threshold for filtering OTUs.

The primary use case is for users that have datasets with a large number of various samples, and they need to quickly isolate the sequences from a subset of those samples. 

## Features

- **Automatic File Detection**:
  - Detects `.fa` or `.fasta` files (FASTA sequences).
  - Detects `.xlsx` or `.xls` files (Metadata input).
  - Detects `.txt` files (OTU table).
- **Metadata Integration**:
  - Extracts all sample IDs from a metadata Excel file.
  - Reports all extracted sample IDs in a text file.
  - Filters the OTU table to retain only columns corresponding to sample IDs.
- **User-Defined Threshold**:
  - Prompts the user to enter a minimum number of reads for filtering OTUs.
  - Defaults to a threshold of `> 0` if no value is entered.
- **Dynamic Filtering**:
  - Filters OTUs based on metadata sample IDs and the specified read threshold.
  - Matches sequences in the FASTA file to the filtered OTUs.

## Output Files

1. **Extracted Sample IDs**:
   - A text file listing all sample IDs from the metadata file.
   - Filename: `extracted_sample_ids-XXXsamples.txt`.

2. **Filtered OTU Table**:
   - A text file containing the filtered OTU table with retained OTUs and sample columns.
   - Filename: `otu_table-filtered-XXXsamples-XXXotus.txt`.

3. **Filtered and Annotated FASTA File**:
   - A FASTA file with sequences sorted by total reads.
   - Header format: `>OTU_ID-totalsamplesXXX-totalreadsYYY`.
   - Filename: `example_filtered_XXX_sequences_minYreads.fa`.

## Requirements

- Python 3.x
- Required libraries:
  - `pandas`
  - `openpyxl` (for `.xlsx` file handling)

Install the necessary libraries using:
```bash
pip install pandas openpyxl
```
## Usage
1. Clone or download the repository:

```bash
git clone https://github.com/BiodiverseLabs/Filter-OTU-Subset.git
```
Replace your-username and repository-name with your GitHub details.

2. Place the following files in the same directory as the script:

- A .fa or .fasta file (FASTA sequences).
- A .xlsx or .xls file (Metadata containing Sample ID column).
- A .txt file (OTU table linking Sample ID and SH_name or OTU names).

3. Run the script:

```bash
python script_name.py
```
4. When prompted, enter the minimum number of reads for OTU filtering:

- Example: Enter 5 to filter for OTUs with more than 5 reads.
- Press Enter to use the default threshold (> 0).

5. The script will generate a filtered FASTA file in the same directory with a name like:
```
original_filename_filtered_XX_sequences_minYreads.fa
```
where XX is the number of sequences in the filtered file and Y is the minimum read threshold.

## Example<br>

### Input Files
1. Metadata (example_metadata.xlsx):

|Sample ID|
| --- |
|GF05032062S|
|GF04011577S|

2. OTU Table (example_otu_table.txt):

|SH_name  |  GF05032062S | GF04011577S |
|---|---|---|
|OTU0001  |  5        |      2|
|OTU0002  |  0       |       1|
|OTU0003  |  10      |       0|

3. FASTA (example_sequences.fa):
```
shell
>OTU0001
ATCGATCGATCG
>OTU0002
CGATCGTAGCTA
>OTU0003
TACGATGCTAGC
```
### Run Command:
```
python script_name.py
```
User enters 5 as the minimum threshold.

### Output:
Filtered FASTA File (example_sequences_filtered_2_sequences_min5reads.fa):
```
shell
>OTU0001
ATCGATCGATCG
>OTU0003
TACGATGCTAGC
```
## Troubleshooting
1. File Not Found Error: Ensure all required files are in the same directory as the script.

2. Invalid Threshold: If you enter a non-numeric value, the script will default to a threshold of > 0.

3. Missing Dependencies: Install required libraries with:
```
pip install pandas openpyxl
```
### Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.

### License
This project is licensed under the MIT License.
