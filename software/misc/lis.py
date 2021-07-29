def LIS(book_list):
    # https://stackoverflow.com/questions/27324717/obtaining-the-longest-increasing-subsequence-in-python

    # make a list of lists
    sequences = list()
    for i in range(0, len(book_list)):
        sequences.append(list())

    # the first increasing subsequence is the first element in book_list
    # sequences[0].append(book_list[0])

    for i in range(0, len(book_list)):
        for j in range(0, i):

            # a new larger increasing subsequence found
            if (
                book_list[j].get_internal_code() < book_list[i].get_internal_code()
            ) and (len(sequences[i]) < len(sequences[j])):
                # 'throw the previous list'
                sequences[i] = []
                # 'add all elements of sequences[j] to sequences[i]'
                sequences[i].extend(sequences[j])
        sequences[i].append(book_list[i])

    maxLength = max(len(seq) for seq in sequences)
    return [seq for seq in sequences if len(seq) == maxLength]
