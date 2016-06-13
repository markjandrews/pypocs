input = [1, 6, 3]

input.sort()
index = 0

missing_numbers = []
for number in input:
    while index < number:
        missing_numbers.append(index)
        index += 1

    index = number + 1

print(missing_numbers)