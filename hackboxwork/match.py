input = ['(', '(', ')', '(', ')', ')']

var_a = 0

for var_c in input:
    if var_c == '(':
        var_a += 1
    else:
        var_a -= 1

    if var_a < 0:
        print('FALSE')
        exit(0)

if var_a == 0:
    print('TRUE')
else:
    print('FALSE')