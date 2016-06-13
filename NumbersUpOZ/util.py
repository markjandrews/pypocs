import random
import statistics
from functools import reduce
import operator as op

import math
from scipy.stats import norm


def nCr(n, r):
    r = min(r, n - r)
    if r == 0: return 1
    numer = reduce(op.mul, range(n, n - r, -1))
    denom = reduce(op.mul, range(1, r + 1))
    return numer // denom


def is_number_sequence(s):
    if len(s) <= 2:
        return None  # tuple of <= 2 elements can't be in sequence

    sorted_s = sorted(s)
    diff = sorted_s[1] - sorted_s[0]

    for i, item in enumerate(sorted_s[2:]):
        if (sorted_s[i + 2] - sorted_s[i + 1]) != diff:
            return None

    return diff


def odd_even_ratio(s):
    even = 0
    odd = 0

    for item in s:
        if item % 2 == 0:
            even += 1
        else:
            odd += 1

    return odd, even


def high_low_ratio(s):
    high = 0
    low = 0

    for item in s:
        if item <= 20:
            low += 1
        else:
            high += 1

    return high, low


def draw_sum(s):
    return sum(s)


def hot_ratio(s, ball_stats):
    hot_count = 0

    for item in s:
        ball_stat = ball_stats[tuple([item])]
        if ball_stat.weeks_since_drawn <= 10:
            hot_count += 1

    return hot_count


def streak_balls_ratio(ball_stats, ratio):

    single_balls = [y for x, y in ball_stats.items() if len(x) == 1]

    hot_balls = sorted(single_balls, key=lambda x: x.total_draws, reverse=True)
    due_balls = sorted(single_balls, key=lambda x: x.weeks_since_drawn, reverse=True)
    real_balls = []

    for hot_index, hot_draw in enumerate(hot_balls):
        recent_index = next(
            (x for x, item in enumerate(due_balls) if item.ball_comb[0] == hot_draw.ball_comb[0]))

        real_index = int(math.floor((hot_index + recent_index)/2))
        real_balls.append((real_index, hot_draw))

    real_balls.sort(key=lambda x: x[1].total_draws, reverse=True)
    real_balls.sort(key=lambda x: x[0])

    # print(hot_balls)
    # print(due_balls)
    # print(real_balls)

    real_balls = [x[1].ball_comb[0] for x in real_balls[:int(math.ceil(len(real_balls) * ratio / 100))]]
    return real_balls


def min_max_ratio(ball_stats, ratio):
    ratio /= 100
    single_ball_count = {}
    for ball in [x for x in ball_stats.keys() if len(x) == 1]:
        single_ball_count[ball[0]] = len(ball_stats[ball].draws)

    min_ball = 1
    max_ball = max(single_ball_count.keys())
    total_balls_drawn = sum(single_ball_count.values())

    while True:
        min_ball += 1
        current_balls_drawn = sum([y for x, y in single_ball_count.items() if min_ball <= x <= max_ball])
        current_ratio = current_balls_drawn / total_balls_drawn
        if current_ratio <= ratio:
            min_ball -= 1
            break

        max_ball -= 1
        current_balls_drawn = sum([y for x, y in single_ball_count.items() if min_ball <= x <= max_ball])
        current_ratio = current_balls_drawn / total_balls_drawn
        if current_ratio <= ratio:
            max_ball += 1
            break

        if min_ball >= max_ball:
            return sorted((min_ball, max_ball))

    return min_ball, max_ball


def sum_ratio(ball_stats, ratio):
    ratio /= 100
    num_balls_per_draw = max([len(x) for x in ball_stats.keys()])
    draw_balls_list = [x for x in ball_stats if len(x) == num_balls_per_draw]

    if len(draw_balls_list) < 2:
        return None

    draw_sums = []
    for draw_balls_item in draw_balls_list:
        draw_sums.append(draw_sum(draw_balls_item))

    mean = statistics.mean(draw_sums)
    standard_dev = statistics.stdev(draw_sums)
    low_z = norm.ppf(0.5 - (ratio / 2))
    high_z = norm.ppf(0.5 + (ratio / 2))
    min_value = low_z * standard_dev + mean
    max_value = high_z * standard_dev + mean

    max_sum = math.ceil(max_value)
    min_sum = math.floor(min_value)

    return min_sum, max_sum


def prompt(desc, default=None):
    print(desc, end='')

    if default is not None:
        print(' (%s)' % default, end='')

    print(':> ', end='')


def random_combination(n, r):
    pool = tuple(range(1, n + 1))
    indicies = sorted(random.sample(range(n), r))
    return tuple(pool[i] for i in indicies)
