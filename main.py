from random import randint
from itertools import combinations
from tqdm import tqdm


class Die:
    def __init__(self, num_sides=6):
        self.num_sides = num_sides

    def roll(self):
        rv = randint(1, self.num_sides)
        return rv


class Box:
    def __init__(self, num_dice=2, num_sides_per_die=6):
        self.max_number = num_dice*num_sides_per_die
        self.dice = []
        for i in range(num_dice):
            self.dice.append(Die(num_sides=num_sides_per_die))
        self.numbers = list(range(1, self.max_number+1))
        self.is_shut = False
        self.roll_history = []
        self.box_state_history = []

    def roll_dice(self):
        rv = 0
        for die in self.dice:
            rv += die.roll()
        self.roll_history.append(rv)
        return rv

    def get_valid_subsets(self, dice_total):
        rv = []
        for subset_len in range(1, len(self.numbers)+1):
            for subset in combinations(self.numbers, subset_len):
                if sum(subset) == dice_total:
                    rv.append(subset)
        return rv

    def get_first_valid_subset(self, dice_total):
        for subset_len in range(1, len(self.numbers)+1):
            for subset in combinations(self.numbers, subset_len):
                if sum(subset) == dice_total:
                    return subset
        return None

    def remove_numbers(self, subset):
        self.numbers = list(
            filter(lambda num: num not in subset, self.numbers))
        self.is_shut = len(self.numbers) == 0
        self.box_state_history.append(f"{self}")

    def __str__(self):
        rv = "|"
        width = len(str(self.max_number))
        for number in range(1, self.max_number+1):
            if number in self.numbers:
                rv += f"{number}".zfill(width)
            else:
                rv += "  "
            rv += "|"
        return rv

    def __repr__(self):
        rv = ""
        for roll, box_state in zip(self.roll_history, self.box_state_history):
            rv += f"{box_state} --- {roll}\n"
        return rv


num_dice = 2
num_sides_per_die = 6
success_count = 0
total_trial_count = 100_000

for i in tqdm(range(total_trial_count)):
    box = Box(num_dice=num_dice, num_sides_per_die=num_sides_per_die)
    while not box.is_shut:
        dice_total = box.roll_dice()
        # print(box, dice_total)
        # subsets = box.get_valid_subsets(dice_total=dice_total)
        # if len(subsets) == 0:
        #     break
        first_subset = box.get_first_valid_subset(dice_total=dice_total)
        if first_subset is None:
            break
        box.remove_numbers(first_subset)
    else:
        # print(repr(box))
        success_count += 1

print(f"({num_dice},{num_sides_per_die}): {success_count} / {total_trial_count} = {100*(1.0 *success_count/total_trial_count):.4f}%")
