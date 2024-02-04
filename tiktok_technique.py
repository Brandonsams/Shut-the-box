from tqdm import tqdm


from shut_the_box import Box

if __name__ == "__main__":
    num_dice = 2
    num_sides_per_die = 6
    success_count = 0
    total_trial_count = 1_000_000

    roll_counts = []
    roll_count_frequency_success = {}
    roll_count_frequency_failure = {}
    # for roll_count in range(1, num_dice * num_sides_per_die + 1):
    #     roll_count_frequency_success[roll_count] = 0
    #     roll_count_frequency_failure[roll_count] = 0

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
                box.add_number(dice_total)
                continue
            box.remove_numbers(first_subset)
        else:
            # print(repr(box))
            roll_count = box.get_roll_count()
            roll_count_frequency_success[roll_count] = roll_count_frequency_success.get(
                roll_count, 0) + 1
            roll_counts.append(roll_count)
            success_count += 1

    print(f"({num_dice},{num_sides_per_die}): {(1.0 *sum(roll_counts)) / len(roll_counts)}")
