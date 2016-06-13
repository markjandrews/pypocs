input = [['d', 'a', 'd'], ['a', 'd', 'd']]


var_a = input[0]
var_a.sort()
for var_b in input:
    var_b.sort()
    if var_a != var_b:
        print(False)
        exit(0)

print(True)
