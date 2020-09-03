"""
my Rock Paper Scissors v2.0
"""

import random


def human_choice(options):
    return options[int(input('Enter your choice: ')) - 1]


def computer_choice(options):
    return random.choice(options)


def get_components_dict(rules, print_out=0):
    """
    Creates a dictionary with the game components (rock, scissors... )
    from the game rules string
    The components dictionary assigns each component a bit value

    :param rules: string - rules of the game
                  ex: Rock breaks scissors,
                      scissors cuts paper,
                      paper covers rock'
    :param print_out: bool - for debugging
    :return: components_dic: dictionary - {string : binary}
                             ex: {'rock' : 0b1, 'paper' : 0b01, etc.}
    """
    components_dic = {}
    bit_val = 0b1

    rules_list = rules.split(', \n')
    for rule in rules_list:
        strong_component = rule.split(' ')[0].lower()
        weak_component = rule.split(' ')[-1].lower()

        if strong_component not in components_dic.keys():
            components_dic[strong_component] = bit_val
            bit_val <<= 1
        if weak_component not in components_dic.keys():
            components_dic[weak_component] = bit_val
            bit_val <<= 1

    if print_out:
        for k, v in components_dic.items():
            print(k, ' : ', '{0:b}'.format(v))

    return components_dic


def get_win_dic(rules, comp_dic, print_out=0):
    """
    Creates the win dictionary from the game rules string and
    the components dictionary.
    The win dictionary determines in the end the winner of the round

    :param rules: string - rules of the game
                  ex: Rock breaks scissors,
                      scissors cuts paper,
                      paper covers rock'
    :param comp_dic: dictionary - {string : binary}
                     ex: {'rock' : 0b1, 'paper' : 0b01, etc.}
    :param print_out: bool - for debugging
    :return: win_dic: dictionary - {0b1 : [winner, rule]}
                      ex: {101  :  ['paper', 'paper covers rock']}
    """
    win_dic = {}

    rules_list = rules.split(', \n')
    for rule in rules_list:
        strong_component = rule.split(' ')[0].lower()
        strong_component_binary = comp_dic[strong_component]

        weak_component = rule.split(' ')[-1].lower()
        weak_component_binary = comp_dic[weak_component]

        battle_result = strong_component_binary | weak_component_binary

        if battle_result not in win_dic.keys():
            win_dic[battle_result] = [strong_component, rule]

    if print_out:
        for k, v in win_dic.items():
            print('{0:b}'.format(k), ' : ', v)

    return win_dic


def prt_msg(message, border='-'):
    print(border * len(message))
    print(message)
    print(border * len(message))


def determine_winner(comp_dic, win_dic):
    """

    :param comp_dic:
    :param win_dic:
    :return:
    """

    human = human_choice(list(comp_dic.keys()))
    pc = computer_choice(list(comp_dic.keys()))

    print()
    msg_choices = f'You chose: {human} \nComputer chose: {pc}'
    max_msg = max([len(x) for x in msg_choices.split(' \n')])
    print('-' * max_msg)
    print(msg_choices)
    print('-' * max_msg)

    if human == pc:
        prt_msg('Draw!', '=')
    else:
        result = comp_dic[human] | comp_dic[pc]
        winner = win_dic[result][0]

        if human == winner:
            msg = f'You win! {win_dic[result][1]}'
        else:
            msg = f'You lose! {win_dic[result][1]}'
        prt_msg(msg, '=')


def print_rules(rules):
    print()
    print('Game Rules:')

    print(rules)


def print_options(comp_dic):
    """
    Prints the options to choose from.
    ex: rock, paper, scissors
    :param comp_dic: dictionary - {string : binary}
                     ex: {'rock' : 0b1, 'paper' : 0b01, etc.}
    :return: None - prints out options
    """
    count = 0
    for k in comp_dic.keys():
        count += 1
        print(f'({count}) {k}')


def choose_game():
    # available_games = ['RPS-3', 'RPS-5', 'RPS-7', 'RPS-9', 'RPS-11',
    #                    'RPS-15', 'RPS-25', 'RPS-101']

    available_games = ['RPS-3', 'RPS-5', 'RPS-7']

    print()
    print('Available games:')
    for i, g in enumerate(available_games):
        print(f'({i + 1}) {g}')

    game = int(input(f'Choose a game (1 to {len(available_games)}): '))

    if game == 1:
        from Rules.rps_3_rules import rules
    elif game == 2:
        from Rules.rps_5_rules import rules
    elif game == 3:
        from Rules.rps_7_rules import rules

    return rules


def play_round(rules):
    comp_dic = get_components_dict(rules)
    print()
    print_options(comp_dic)
    win_dic = get_win_dic(rules, comp_dic)
    determine_winner(comp_dic, win_dic)


def play():
    rules = choose_game()
    print_rules(rules)

    while True:
        play_round(rules)
        if input('Play another round? Y/N: ').lower() == 'n':
            break


play()
