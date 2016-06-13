
input = [0, 1, 10, 15, 20]

var_b = 0
for var_a in input:
    var_c = var_a

    while var_a > var_b:
        input.insert(var_b, var_a - 1)
        var_a -= 1

    var_b = var_c + 1


print(input)