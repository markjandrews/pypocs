input = [1, 0, 1]

var_a = 0
var_c = 0
while var_a < len(input):
    lsb_index = len(input) - var_a - 1
    lsb = input[lsb_index]

    if lsb != 0:
        if var_a == 0:
            var_c += 1
        else:
            var_d = 1
            var_e = 2
            while var_d < var_a:
                var_e = var_e * 2
                var_d += 1

            var_c += var_e

    var_a += 1

print(var_c)