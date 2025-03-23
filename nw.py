from re import I
import pandas as pd

# sequence1 = input()
# sequence2 = input()

# sequence1 = "DPLE"
# sequence2 = "DPME"

sequence1 = "CAGCCUCGCUUAG"
sequence2 = "AAUGCCAUUGACGG"

# sequence1 = "FMDTPLNE"
# sequence2 = "FKHMEDPLE"

# sequence1 = "ornot"
# sequence2 = "something"


num_rows = len(sequence1)
num_cols = len(sequence2)

# intializing matricies and inserting gap penalties

row_labels = ['0'] + list(sequence1)
col_labels = ['0'] + list(sequence2)

score_matrix = pd.DataFrame(0, index=row_labels, columns=col_labels)
directional_matrix = pd.DataFrame('', index=row_labels, columns=col_labels)

for i in range(1, num_rows+1):
    score_matrix.iloc[i, 0] = score_matrix.iloc[i-1, 0] - 2
    directional_matrix.iloc[i, 0] = str(score_matrix.iloc[i-1, 0] - 2) # getting the value as an int from scoring matrix so that it can be stored/displayed in the directional matrix and potentially accessed later if needed

for j in range(1, num_cols+1):
    score_matrix.iloc[0, j] = score_matrix.iloc[0, j-1] - 2
    directional_matrix.iloc[0, j] = str(score_matrix.iloc[0, j-1] - 2) 

# filling matricies

for i in range(2, num_rows+2):
    for j in range(2, num_cols+2):

        directions = []

        # match
        if sequence1[i-2] == sequence2[j-2]:

            # diagonal
            if score_matrix.iloc[i-2, j-2] + 1 >= score_matrix.iloc[i-1, j-2] - 2 and score_matrix.iloc[i-2, j-2] + 1 >= score_matrix.iloc[i-2, j-1] - 2:
                score_matrix.iloc[i-1, j-1] = score_matrix.iloc[i-2, j-2] + 1
                directions.append("D")

            # up
            if score_matrix.iloc[i-1, j-2] - 2 >= score_matrix.iloc[i-2, j-2] + 1 and score_matrix.iloc[i-1, j-2] - 2 >= score_matrix.iloc[i-2, j-1] - 2:
                score_matrix.iloc[i-1, j-1] = score_matrix.iloc[i-1, j-2] - 2
                directions.append("L")

            # left
            if score_matrix.iloc[i-2, j-1] - 2 >= score_matrix.iloc[i-1, j-2] - 2 and score_matrix.iloc[i-2, j-1] - 2 >= score_matrix.iloc[i-2, j-2] + 1:
                score_matrix.iloc[i-1, j-1] = score_matrix.iloc[i-2, j-1] - 2
                directions.append("U")

        # mismatch
        else:

            # diagonal
            if score_matrix.iloc[i-2, j-2] - 2 >= score_matrix.iloc[i-1, j-2] - 2 and score_matrix.iloc[i-2, j-2] - 2 >= score_matrix.iloc[i-2, j-1] - 2:
                score_matrix.iloc[i-1, j-1] = score_matrix.iloc[i-2, j-2] - 2
                directions.append("D")

            # up
            if score_matrix.iloc[i-1, j-2] - 2 >= score_matrix.iloc[i-2, j-2] - 2 and score_matrix.iloc[i-1, j-2] - 2 >= score_matrix.iloc[i-2, j-1] - 2:
                score_matrix.iloc[i-1, j-1] = score_matrix.iloc[i-1, j-2] - 2
                directions.append("L")

            # left
            if score_matrix.iloc[i-2, j-1] - 2 >= score_matrix.iloc[i-1, j-2] - 2 and score_matrix.iloc[i-2, j-1] - 2 >= score_matrix.iloc[i-2, j-2] - 2:
                score_matrix.iloc[i-1, j-1] = score_matrix.iloc[i-2, j-1] - 2
                directions.append("U")

        # all three directions were valid (meaning no direction was assigned)
        if not directions:
            # default to diagonal to break ties
            score_matrix.iloc[i-1, j-1] = score_matrix.iloc[i-2, j-2] - 2
            directions.append("D")

        directional_matrix.iloc[i-1, j-1] = directions[0]  # always pick first valid direction, still results in an optimal alignment

print(score_matrix, '\n')
print(directional_matrix, '\n')

# traceback

score = 0
matches = 0
mismatches = 0
gaps = 0
sequence1_aligned_reversed = ""
sequence2_aligned_reversed = ""
i = num_rows
j = num_cols

while i > 0 and j > 0:
    direction = directional_matrix.iloc[i, j]
    
    # match or mismatch
    if direction == 'D':
        if sequence1[i-1] == sequence2[j-1]:
            matches += 1
            score += 1
        else:
            mismatches += 1
            score -= 2
    
        sequence1_aligned_reversed += sequence1[i-1]
        sequence2_aligned_reversed += sequence2[j-1]
        i -= 1
        j -= 1

    # gap in sequence 1
    elif direction == 'L':
        score -= 2
        gaps += 1
        sequence1_aligned_reversed += '-'
        sequence2_aligned_reversed += sequence2[j-1]
        j -= 1

    # gap in sequence 2
    elif direction == 'U':
        score -= 2
        gaps += 1
        sequence1_aligned_reversed += sequence1[i-1]
        sequence2_aligned_reversed += '-'
        i -= 1

# handling when one side reaches an edge before the other
while j > 0:
    sequence1_aligned_reversed += '-'
    sequence2_aligned_reversed += sequence2[j-1]
    score -= 2
    gaps += 1
    j -= 1
    
while i > 0:
    sequence2_aligned_reversed += '-'
    sequence1_aligned_reversed += sequence1[i-1]
    score -= 2
    i -= 1

sequence1_aligned = ''.join(reversed(sequence1_aligned_reversed))
sequence2_aligned = ''.join(reversed(sequence2_aligned_reversed))

print("Sequence 1: ", sequence1_aligned, '\n')
print("Sequence 2: ", sequence2_aligned, '\n')
print("Matches: ", matches, '\n')
print("Mismatches: ", mismatches, '\n')
print("Gaps: ", gaps, '\n')
print("Score: ", score)