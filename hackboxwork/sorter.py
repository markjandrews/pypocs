
input = ['a', 'd', 'b', 'c']

var_b = []

for var_a in input:
    var_c = []
    var_d = 0
    while var_d < len(var_b) and var_b[var_d] < var_a:
        var_c.append(var_b[var_d])
        var_d += 1

    var_c.append(var_a)

    while var_d < len(var_b):
        var_c.append(var_b[var_d])
        var_d += 1

    var_b = var_c

print(input)
print(var_b)
