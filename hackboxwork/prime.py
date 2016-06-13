

for i in range(100000):
    prime = True

    var_a = int(i/2)
    while var_a > 1:

        if i == int(i/var_a)*var_a:
            # print('%s is Not Prime, %s is a factor' % (i, var_a))
            prime = False
            break

        var_a -= 1

    if prime is True:
        print('%s is Prime' % i)


