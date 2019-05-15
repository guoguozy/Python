# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx


def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    result_list = []  # 结果列表
    sequence_list = list(sequence)
    if len(sequence) == 1:  # 长度为1直接返回该字母
        result_list.append(sequence)
    else:
        for i in range(0, len(sequence)):
            sequence_list[i], sequence_list[0] = sequence_list[0], sequence_list[i]
            sequence = ''.join(sequence_list)  # 将固定字母置于首位并转换字符串
            for j in get_permutations(sequence[1:len(sequence)]):
                result_list.append(sequence[0]+j)
            sequence_list[i], sequence_list[0] = sequence_list[0], sequence_list[i]
            sequence = ''.join(sequence_list)
    return result_list


if __name__ == '__main__':
    # EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))

    example_input = 'bust'
    print('Input:', example_input)
    print('Expected Output:', ['bust', 'buts', 'bsut', 'bstu', 'btsu', 'btus', 'ubst', 'ubts', 'usbt', 'ustb',
                               'utsb', 'utbs', 'subt', 'sutb', 'sbut', 'sbtu', 'stbu', 'stub', 'tusb', 'tubs', 'tsub', 'tsbu', 'tbsu', 'tbus'])
    print('Actual Output:', get_permutations(example_input))

    example_input = 'ab'
    print('Input:', example_input)
    print('Expected Output:', ['ba', 'ab'])
    print('Actual Output:', get_permutations(example_input))
    #    # Put three example test cases here (for your sanity, limit your inputs
    #    to be three characters or fewer as you will have n! permutations for a
    #    sequence of length n)
