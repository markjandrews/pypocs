import json
import os
import shutil
import sys

import remote
from results import S4LDraw, BallStat, is_numberset_valid, games_out, calibrate, check_results
from util import random_combination


def main(argv):
    ballstats_dict = {}
    last_draw = None
    # last_draw = S4LDraw.Parse(
    #         ["164", "20160117", "12", "4", "24", "13", "21", "36", "10", "23", "22", "16", "Set for Life", "$0.00",
    #          "$1,016.90", "$111.50", "$32.70", "$20.70", "$13.85", "$10.45"])
    candidate_list = set()

    if '-d' in argv:
        if os.path.exists('S4L'):
            shutil.rmtree('S4L')

        if os.path.exists('results.csv'):
            os.unlink('results.csv')

    if '-f' in argv:
        if os.path.exists('results.csv'):
            os.unlink('results.csv')

    if not os.path.exists('S4L'):
        os.makedirs('S4L')

    # url = 'https://tatts.com/DownloadFile.ashx?product=SetForLife'
    url = argv[0]
    draw_results = []
    print('==============================\nGenerating Draw Statistics\n==============================\n')
    for result in remote.pull_results(url):
        if len(result) == 0:
            continue

        draw = S4LDraw.Parse(result)
        draw_results.append(draw)
        for draw_comb_set in [draw.comb_set(x + 1) for x in range(len(draw.winning_numbers))]:
            for draw_comb in draw_comb_set:
                ballstat = ballstats_dict.setdefault(tuple(sorted(draw_comb)), BallStat(draw_comb))
                ballstat.new_draw(draw.date, draw)

    # Calibrate draw settings
    if '-c' in argv or not os.path.exists('settings.json'):
        calibrate(ballstats_dict)

    games_out_dict = games_out(draw_results, ballstats_dict)

    if os.path.exists('s4lcandidate.json'):
        print('==============================\nChecking Existing Candidates for Invalid Entries\n'
              '==============================')
        with open('s4lcandidate.json', 'r') as inf:
            data = json.load(inf)
            for item in sorted(data):
                if is_numberset_valid(item, ballstats_dict, games_out_dict) is True:
                    # print('%s - Valid' % str(item))
                    candidate_list.add(tuple(sorted(item)))
                else:
                    print('%s - Invalid' % str(item))

        print()

    if len(candidate_list) < 100:
        print('==============================\nAdding new candidates to candidate list\n==============================')
    while len(candidate_list) < 100:
        candidate = random_combination(S4LDraw.MAX_BALL, S4LDraw.NUM_BALLS)
        if is_numberset_valid(candidate, ballstats_dict, games_out_dict) is True:
            print('Adding %s' % str(candidate))
            candidate_list.add(tuple(sorted(candidate)))
        else:
            print('Skipping %s' % str(candidate))

    print('==============================\nSaving Candiate List to File(s)\n==============================')
    with open('s4lcandidate.json', 'w') as outf:
        json.dump(list(candidate_list), outf)

    num_entries_per_ticket = 50
    num_files = len(candidate_list) // num_entries_per_ticket
    if (num_files * num_entries_per_ticket) < len(candidate_list):
        num_files += 1

    for i in range(num_files):
        with open('s4lcandidate_%s.txt' % str(i + 1), 'w') as outf:
            print('s4lcandidate_%s.txt' % str(i + 1))
            for candidate in sorted(candidate_list)[
                             i * num_entries_per_ticket:i * num_entries_per_ticket + num_entries_per_ticket]:
                outf.write('%s\n' % ', '.join([str(i) for i in candidate]))

    if last_draw is None:
        last_draw = draw_results[-1]

    # Check if last draw "could have" one
    print('\n==============================\nChecking Validity of Last Draw\n==============================')
    print('Last Draw: %s' % last_draw)
    print('Could have won: %s' % is_numberset_valid(last_draw.winning_numbers, ballstats_dict, games_out_dict))

    # Look for winning combinations from candidates against last draw
    print('\n==============================\nChecking Candidates Against Last Draw\n==============================')
    print('Last Draw: %s' % last_draw)
    check_results(last_draw, candidate_list)

    # print('\n==============================\nChecking Candidates Against All Previous Draws\n==============================')
    # for draw in draw_results:
    #     print('Draw: %s' % draw)
    #     check_results(draw, candidate_list)
    #     print()


if __name__ == '__main__':
    main(sys.argv[1:])
