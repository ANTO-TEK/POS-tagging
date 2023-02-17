"""
Antonio Bove
mat. 0622701898
"""

"""
This function works by using a dynamic programming approach.

The algorithm involves the iterative construction by columns of two matrices:
    - C, containing the probabilities of the best paths crossed
    - D, with the trace of the states crossed

These two matrices will have a number of rows equal to the number of states present 
in tuple R and a number of columns equal to the number of words present in tuple S.

In this comment, I indicate with A and B respectively the transition matrix and the emission matrix.

The first column of the C matrix is initialized by setting 

    C(i,0) = A(0,i) * B(index(s_0),i)

that is the probabilities of emitting the first word s_0 through the transition from the initial state to a first state R_i. 

The first column of the D matrix is initialized by setting 

    D(i,0) = 0 

as we do not yet have previous parts of the path to trace.

The subsequent columns of the C matrix are iteratively calculated as 

    C(i,j) = max_k[C(k,j−1) * A(k+1,i) * B(index(s_j),i)]

choosing in practice to reach the state R_i from the previous state R_k which maximizes the probability of the partial path. 

Consequently in the D matrix we will insert just such k calculated as

    D(i,j) = argmax_k[C(k,j−1) * A(k+1,i) * B(index(s_j),i)]

Finally, the function follows the backpointers iterating over D matrix to recover the optimal path, then returns 
the optimal path as a dictionary mapping words to roles.

The time complexity of this function is O(n*m^2), where n is the length of the sentence and m is the number of possible roles.
"""

def pos_tagging(R, S, T, E):

    # Initialize the arrays for storing the intermediate results of the algorithm
    sentenceLen = len(S)  # length of the sentence
    C = [[0] * sentenceLen for i in range(len(R))] # probabilities matrix
    D = [[-1] * sentenceLen for i in range(len(R))] # backpointer matrix

    # Initialize the first column
    for i, tag in enumerate(R):
        # Set the initial probability for each role to be the transition probability
        # from the start role to this role multiplied by the emission probability of
        # the first word in the sentence for this role
        C[i][0] = T['Start'][tag] * E[S[0]][tag]
        D[i][0] = 0 # set the backpointer for the initial state to 0
    
    # Fill the rest of the matrix
    for i in range(1, sentenceLen):
        for j, current_tag in enumerate(R):
            max_prob = max_arg = -1
            for k, prev_tag in enumerate(R):
                # Compute the probability of the current role being assigned to the current word
                # based on the probability of the previous role being assigned to the previous word,
                # the transition probability between the previous role and the current role,
                # and the emission probability of the current word for the current role
                prob = C[k][i-1] * T[prev_tag][current_tag] * E[S[i]][current_tag]
                # Update the maximum probability and index if necessary
                if prob > max_prob:
                    max_prob = prob
                    max_arg = k
            # Update the probabilities matrix and backpointer matrix for the current role and word
            C[j][i] = max_prob
            D[j][i] = max_arg

    # Find the role with the highest probability at the final step        
    max_prob = max_arg = -1
    for i, tag in enumerate(R):
        # Calculate the probability of the current role being assigned to the final word
        # based on the probability of the current role being assigned to the second-to-last word
        # and the transition probability between the current role and the end role
        prob = C[i][sentenceLen-1] * T[tag]['End']
        # Update the maximum probability and index if necessary
        if prob > max_prob:
            max_prob = prob
            max_arg = i
    
    # Follow the backpointers to recover the optimal path
    optimal_path = []
    
    i = sentenceLen - 1
    while i >= 0:
        # Add the current word and role to the optimal path
        optimal_path.append((S[i], R[max_arg]))
        # Update the index based on the backpointer matrix 
        max_arg = D[max_arg][i]
        i -= 1

    # Reverse the optimal path to get the correct order and return it as a dictionary
    return dict(reversed(optimal_path))