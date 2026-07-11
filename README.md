# Bioinformatics Scripts

Showcase of some bioinformatics and computational biology scripts written for my bioinformatics course. Includes scripts for sequence analysis, genomic data parsing, and applying classic ML models to biological data.

## Setup

```bash
git clone https://github.com/raumsie/bioinformatics-scripts
cd Bioinfo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Tested on Python 3.14.

## Scripts

### `scripts/fasta_parser.py`
Parses a bacterial genome FASTA file with Biopython's `SeqIO` and computes nucleotide (A/C/G/T) composition. Plots the result as a bar chart.

### `scripts/microRNA_detector.py`
Trains a Random Forest and a Logistic Regression classifier to predict microRNA-target binding from human training data, then evaluates on human and mouse test data. Sequences are one-hot encoded (A/C/G/U) with length and GC-content features. 

### `scripts/classifier.py`
Logistic Regression classifier on the Iris dataset. 

### `scripts/seq_backtracking.py`
Global pairwise sequence alignment (Needleman-Wunsch) with a full dynamic programming scoring matrix and traceback to recover the optimal alignment. 

### `scripts/random_algo.py`
Monte Carlo root-finding for a nonlinear equation. Not biology-specific, but the randomized-search approach is the same family of technique used in optimization for molecular structure and parameter estimation problems.

## Data

- `data/Ecoli-bacteria-complete-genome-low-GC.fasta`, `data/thermophile-thermo-microbium-complete-genome-has-high-CGs.fasta` - bacterial genomes used by `fasta_parser.py`. Chosen as a contrasting pair: E. coli (low GC%) vs. a thermophile (high GC%).
- `data/ecoli_percentages.png`, `data/microbium_percentages.png` - nucleotide composition charts produced by `fasta_parser.py` for each genome above.
- `data/human_training_data.csv`, `data/human_test_data.csv`, `data/mouse_test_data.csv` - microRNA/target sequence pairs with binding labels, used by `microRNA_detector.py`.
- `data/iris_training.csv`, `data/iris_test.csv` - the Iris flower dataset, used by `classifier.py`.

## License

MIT