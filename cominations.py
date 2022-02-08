array = ['A','B','C','D','E']
combination_length = 2

def combination(arr, comb_length):
    output = []
    if (comb_length <= 1):
        return arr

    for index in range(0, len(arr)-1):
        others_list = arr[index+1:]
        smaller_combo=combination(others_list, comb_length-1)
        for combo in smaller_combo:
            output.append([arr[index], combo])
    return output

print(combination(array, combination_length))
    
