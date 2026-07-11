import matplotlib.pyplot as plt
from Bio import SeqIO

#ecoli_file = "Ecoli-bacteria-complete-genome-low-GC.fasta"
#microbe_file = "thermophile-thermo-microbium-complete-genome-has-high-CGs.fasta"

record = next(SeqIO.parse("Ecoli-bacteria-complete-genome-low-GC.fasta", "fasta"))
sequence = str(record.seq).upper()

# Calculate nucleotide percentages
letters = ['A', 'C', 'G', 'T']
counts = {letter: sequence.count(letter) for letter in letters}
total = len(sequence)
percentages = {letter: (count/total)*100 for letter, count in counts.items()}

# Print results
print(f"Sequence length: {total}")
for letter in letters:
    print(f"{letter}: {counts[letter]} ({percentages[letter]:.2f}%)")

# BAR CHART
fig, ax = plt.subplots(figsize=(8, 6))

bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']
bar_labels = ['A', 'C', 'G', 'T']

bars = ax.bar(letters, percentages.values(), label=bar_labels, color=bar_colors, alpha=0.8)

ax.set_ylabel('Percentage (%)', fontsize=12)
ax.set_xlabel('Letter', fontsize=12)
ax.set_title('Letter Percentages', fontsize=14, pad=20)


# Add grid
ax.grid(axis='y', alpha=0.3)


#plt.savefig('microbium_percentages.png', dpi=300)
plt.show()