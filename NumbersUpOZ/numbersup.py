import json
import os
import shutil
import sys

import remote
from results import OZDraw, BallStat, is_numberset_valid, games_out, calibrate, check_results
from util import random_combination, min_max_ratio


def main(argv):
    ballstats_dict = {}
    last_draw = None
    # last_draw = OZDraw.Parse(
    #     ["1146", "20160202", "5", "7", "9", "44", "22", "2", "19", "36", "28", "$30,000,000.00", "$25,435.25",
    #      "$2,869.40", "$260.85", "$35.30", "$19.80", "$13.60"])
    candidate_list = set()

    if '-d' in argv:
        if os.path.exists('OZ'):
            shutil.rmtree('OZ')

        argv.append('-f')

    if '-f' in argv:
        if os.path.exists('results.csv'):
            os.unlink('results.csv')

    if not os.path.exists('OZ'):
        os.makedirs('OZ')

    # url = 'https://tatts.com/DownloadFile.ashx?product=OzLotto'
    url = argv[0]
    draw_results = []
    print('==============================\nGenerating Draw Statistics\n==============================\n')
    results = remote.pull_results(url)
    for i, result in enumerate(results):
        if result is None or len(result) == 0:
            continue

        draw = OZDraw.Parse(result)
        # Check if last draw "could have" one
        if i == (len(results) - 1):  # Last draw
            print('\n==============================\nChecking Validity of Last Draw\n==============================')
            print('Draw: %s' % draw)
            print('  Could have won: %s' % is_numberset_valid(draw.winning_numbers, ballstats_dict, None))

        draw_results.append(draw)
        for draw_comb_set in [draw.comb_set(x + 1) for x in range(len(draw.winning_numbers))]:
            for draw_comb in draw_comb_set:
                ballstat = ballstats_dict.setdefault(tuple(sorted(draw_comb)), BallStat(draw_comb))
                ballstat.new_draw(draw.date, draw)

    if last_draw is None:
        last_draw = draw_results[-1]

    # Calibrate draw settings
    if '-c' in argv or not os.path.exists('settings.json'):
        calibrate(ballstats_dict)

    games_out_dict = games_out(draw_results, ballstats_dict)

    if os.path.exists('ozcandidate.json'):
        with open('ozcandidate.json', 'r') as inf:
            data = json.load(inf)

        # Look for winning combinations from candidates
        print('\n==============================\nChecking Candidates Against Last Draw\n==============================')
        for item in sorted(data):
            candidate_list.add(tuple(sorted(item)))

        print('Last Draw: %s' % last_draw)
        check_results(last_draw, candidate_list)

        print('\n==============================\nChecking Existing Candidates for Invalid Entries\n'
              '==============================')

        candidate_list = set()
        for item in sorted(data):
            if is_numberset_valid(item, ballstats_dict, games_out_dict) is True:
                # print('%s - Valid' % str(item))
                candidate_list.add(tuple(sorted(item)))
            else:
                print('%s - Invalid' % str(item))

        print()

    num_entries = 100
    if len(candidate_list) < num_entries:
        print('==============================\nAdding new candidates to candidate list\n==============================')
    while len(candidate_list) < num_entries:
        candidate = random_combination(OZDraw.MAX_BALL, OZDraw.NUM_BALLS)
        if is_numberset_valid(candidate, ballstats_dict, games_out_dict) is True:
            print('Adding %s' % str(candidate))
            candidate_list.add(tuple(sorted(candidate)))
        else:
            print('Skipping %s' % str(candidate))

    if '-s' not in sys.argv:
        return

    print('==============================\nSaving Candiate List to File(s)\n==============================')
    with open('ozcandidate.json', 'w') as outf:
        json.dump(list(candidate_list), outf)

    num_entries_per_ticket = 50

    num_files = len(candidate_list) // num_entries_per_ticket
    if (num_files * num_entries_per_ticket) < len(candidate_list):
        num_files += 1

    for i in range(num_files):
        with open('ozcandidate_%s.txt' % str(i + 1), 'w') as outf:
            print('ozcandidate_%s.txt' % str(i + 1))
            for candidate in sorted(candidate_list)[
                             i * num_entries_per_ticket:i * num_entries_per_ticket + num_entries_per_ticket]:
                outf.write('%s\n' % ', '.join([str(i) for i in candidate]))


if __name__ == '__main__':
    main(sys.argv[1:])
