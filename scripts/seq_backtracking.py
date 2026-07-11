import numpy as np
'''
Raumsie Gaballa
'''

def seq_alignment(seq1, seq2):

    n1, n2 = len(seq1), len(seq2)

    # Create matrices
    M = [[0] * (n2 + 1) for _ in range(n1 + 1)]
    BT = [[''] * (n2 + 1) for _ in range(n1 + 1)]

    # Initialize
    for i in range(n1 + 1):
        M[i][0] = i * (-6)
        BT[i][0] = 's'
    for j in range(n2 + 1):
        M[0][j] = j * (-6)
        BT[0][j] = 's'

    # Fill matrices
    for i in range(1, n1 + 1):
        for j in range(1, n2 + 1):
            # Implement algorithm
            if seq1[i - 1] == seq2[j - 1]:
                diagonal = M[i - 1][j - 1] + 5
            else:
                diagonal = M[i - 1][j - 1] - 2

            up = M[i - 1][j] - 6
            left = M[i][j - 1] - 6

            # Find max using temporary variable
            tmp_max = max(diagonal, up, left)
            M[i][j] = tmp_max

            # Backtracking
            if tmp_max == up:
                BT[i][j] = 'u'
            elif tmp_max == left:
                BT[i][j] = 'l'
            else:  # tmp_max == diagonal
                BT[i][j] = 'd'

    print("SCORING MATRIX M:")
    print_matrix(M, seq1, seq2, "M")

    print("\nBACKTRACKING MATRIX BT:")
    print_matrix(BT, seq1, seq2, "BT")

    # Backtrack to find alignment
    i, j = n1, n2
    aligned1, aligned2 = [], []

    while i > 0 or j > 0:
        if BT[i][j] == 'd':  # diagonal
            aligned1.append(seq1[i - 1])
            aligned2.append(seq2[j - 1])
            i -= 1
            j -= 1
        elif BT[i][j] == 'u':  # up
            aligned1.append(seq1[i - 1])
            aligned2.append('-')
            i -= 1
        elif BT[i][j] == 'l':  # left
            aligned1.append('-')
            aligned2.append(seq2[j - 1])
            j -= 1
        else:  # stop
            if i > 0:
                aligned1.append(seq1[i - 1])
                aligned2.append('-')
                i -= 1
            elif j > 0:
                aligned1.append('-')
                aligned2.append(seq2[j - 1])
                j -= 1

    aligned1 = ''.join(aligned1[::-1])
    aligned2 = ''.join(aligned2[::-1])

    return aligned1, aligned2, M[n1][n2], M, BT

'''
I couldn't get numpy to print the backtracking matrix
so I made a print method
'''
def print_matrix(matrix, seq1, seq2, matrix_name):

    n1, n2 = len(seq1), len(seq2)

    # Create header offset for S2
    header = ['', '-'] + list(seq2)

    # Print header
    print("     " + "  ".join(f"{cell:>3}" for cell in header))
    print("    " + "---" * (len(header) + 1))

    # Print first row
    row0 = ['-'] + [str(matrix[0][j]) if matrix_name == "M" else matrix[0][j] for j in range(n2 + 1)]
    print(" -  | " + "  ".join(f"{str(cell):>3}" for cell in row0))

    # Print rest of the rows
    for i in range(1, n1 + 1):
        row_label = seq1[i - 1]
        row_data = [row_label] + [str(matrix[i][j]) if matrix_name == "M" else matrix[i][j] for j in range(n2 + 1)]
        print(f" {row_label}  | " + "  ".join(f"{str(cell):>3}" for cell in row_data))


# Example A
print("Example A")
print("S1 = ACGU")
print("S2 = ACU")

S1 = "ACGU"
S2 = "ACU"

aligned1, aligned2, score, M, BT = seq_alignment(S1, S2)

print(f"\nALIGNMENT RESULTS:")
print(f"S1: {aligned1}")
print(f"S2: {aligned2}")
print(f"Alignment score: {score}")

# Example B
print("=" * 20)
print("Example B")
print("S1 = ACGU")
print("S2 = CGAU")

S1 = "ACGU"
S2 = "CGAU"

aligned1, aligned2, score, M, BT = seq_alignment(S1, S2)

print(f"\nALIGNMENT RESULTS:")
print(f"S1: {aligned1}")
print(f"S2: {aligned2}")
print(f"Alignment score: {score}")


# Example C
print("=" * 20)
print("Example C")
print("S1 = UCAU")
print("S2 = UACGU")

S1 = "UCAU"
S2 = "UACGU"

aligned1, aligned2, score, M, BT = seq_alignment(S1, S2)

print(f"\nALIGNMENT RESULTS:")
print(f"S1: {aligned1}")
print(f"S2: {aligned2}")
print(f"Alignment score: {score}")