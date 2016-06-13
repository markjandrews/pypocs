
input = ['t', 'e', 'n']

var_a = input[0]

for var_b in input:

    if var_b < var_a:
        print('FALSE')
        exit(0)

    var_a = var_b

print('TRUE')
