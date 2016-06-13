import csv
import itertools
import json
import random
import requests
import sys


def download(url, outptufile):
    response = requests.get(url)

    with open(outptufile, 'wb') as outf:
        outf.write(response.text.encode('latin-1'))


def parse_results(inputfile):
    draws = {}
    comb_numbers = [{}, {}, {}, {}]

    with open(inputfile, 'r') as inf:
        parser = csv.reader(inf, delimiter=',', quotechar='"')
        next(parser)

        for row in parser:
            # Record draw
            draw_number = row[0]
            draws[int(draw_number)] = row

            for i, draw_combs in enumerate(comb_numbers):
                comb_range = 7 - i
                for draw_comb in itertools.combinations(row[2:11], comb_range):
                    draw_comb = [int(x) for x in draw_comb]
                    draw_list = draw_combs.setdefault(tuple(sorted(draw_comb)), [])
                    draw_list.append(draw_number)

    comb_numbers[7 - 7] = {key: value for key, value in comb_numbers[7 - 7].items() if len(value) > 0}
    comb_numbers[7 - 6] = {key: value for key, value in comb_numbers[7 - 6].items() if len(value) > 1}
    comb_numbers[7 - 5] = {key: value for key, value in comb_numbers[7 - 5].items() if len(value) > 2}
    comb_numbers[7 - 4] = {key: value for key, value in comb_numbers[7 - 4].items() if len(value) > 3}

    with open('filtered_combs.txt', 'w') as outf:
        outf.write('Combs 7:\n')
        outf.write('--------\n')
        for comb_number in sorted(comb_numbers[7 - 7]):
            outf.write('%s\n' % str(comb_number))
        outf.write('--------\n')
        outf.write('Combs 6:\n')
        outf.write('--------\n')
        for comb_number in sorted(comb_numbers[7 - 6]):
            outf.write('%s\n' % str(comb_number))
        outf.write('--------\n')
        outf.write('Combs 5:\n')
        outf.write('--------\n')
        for comb_number in sorted(comb_numbers[7 - 5]):
            outf.write('%s\n' % str(comb_number))
        outf.write('--------\n')
        outf.write('Combs 4:\n')
        outf.write('--------\n')
        for comb_number in sorted(comb_numbers[7 - 4]):
            outf.write('%s\n' % str(comb_number))
        outf.write('--------\n')

    return draws, comb_numbers


def is_comb_in_sequence(comb):
    comb = sorted(comb)
    start_sequence = comb[0]
    sequence_len = comb[1] - start_sequence

    if sequence_len > 3:
        return False  # Only interested in low value sequences

    for i, value in enumerate(comb):
        if value != (i * sequence_len) + start_sequence:
            return False

    return True


def is_comb_available(comb, comb_numbers):
    comb_range = len(comb)

    comb = tuple(sorted(comb))

    if comb_range < 4 or comb_range > 7:
        return False

    combs = comb_numbers[7 - comb_range]

    if comb in combs:
        return False

    return True


search_result = {1, 15, 4, 32, 11, 9, 37}


def generate_numbers(comb_numbers):
    num_results = 83
    results = []

    num_attempts = 1

    while len(results) < num_results:
        draw_candidate = set()

        while True:
            while len(draw_candidate) < 7:
                draw_candidate.update(random.sample(range(1, 46), 7 - len(draw_candidate)))
                while len(draw_candidate) > 0 and min(draw_candidate) > 18:
                    print('- %s' % min(draw_candidate))
                    draw_candidate.remove(min(draw_candidate))

                while len(draw_candidate) > 0 and max(draw_candidate) < 20:
                    print('+ %s' % max(draw_candidate))
                    draw_candidate.remove(max(draw_candidate))

                # draw_candidate = search_result

            for i, draw_combs in enumerate(comb_numbers):
                comb_range = 7 - i
                for draw_comb in itertools.combinations(draw_candidate, comb_range):
                    if is_comb_in_sequence(draw_comb):
                        print('###### %s' % str(draw_comb))
                        draw_candidate -= set(draw_comb)
                        break

                    if not is_comb_available(draw_comb, comb_numbers):
                        print('****** %s' % str(draw_comb))
                        draw_candidate -= set(draw_comb)
                        break

                    if len(draw_candidate) < 7:
                        break

            if len(draw_candidate) == 7:
                break

        results.append(sorted(draw_candidate))

        # if draw_candidate == search_result:
        #     results.append(draw_candidate)
        #     break
        # else:
        #     diff = draw_candidate & search_result
        #     if len(diff) > 3:
        #         print(diff, num_attempts)
        #
        # num_attempts += 1

    return results


def main(argv):
    url = 'https://tatts.com/DownloadFile.ashx?product=OzLotto'
    results_file = 'results.csv'

    # download(url, results_file)

    draws, comb_numbers = parse_results(results_file)
    results = generate_numbers(comb_numbers)

    with open('picked_results.txt', 'w') as outf:
        for result in sorted(results):
            print(result)
            outf.write('%s\n' % str(result))

        # largest_min = 1
        # smallest_max = 45
        # for draw, results in draws.items():
        #     results = sorted([int(x) for x in results[2:11]])
        #     if largest_min < results[0]:
        #         largest_min = results[0]
        #
        #     if smallest_max > results[-1]:
        #         smallest_max = results[-1]
        #
        #     print(draw, results)
        #
        # print(largest_min)
        # print(smallest_max)


if __name__ == '__main__':
    main(sys.argv[1:])
