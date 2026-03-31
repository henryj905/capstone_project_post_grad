import Gathers
import Algorithm


def team_season(team, year):
    stat_list = []
    num_list = []
    passing = Gathers.passing_gather_season(team, year)
    rushing = Gathers.rushing_gather_season(team, year)
    receiving = Gathers.receiving_gather_season(team, year)
    sacks = Gathers.sacks_gather_season(team, year)
    special = Gathers.special_gather_season(team, year)

    combine_1 = Algorithm.combine(passing)
    combine_2 = Algorithm.combine(rushing)
    combine_3 = Algorithm.combine(receiving)
    combine_4 = Algorithm.combine(sacks)
    combine_5 = Algorithm.combine(special)

    stats_1 = []
    stats_2 = []
    stats_3 = []
    stats_4 = []
    stats_5 = []

    for x in combine_1:
        stats_1.append(x)
    for stat in stats_1:
        num_list.append(combine_1[f"{stat}"])

    for x in combine_2:
        stats_2.append(x)
    for stat in stats_2:
        num_list.append(combine_2[f"{stat}"])

    for x in combine_3:
        stats_3.append(x)
    for stat in stats_3:
        num_list.append(combine_3[f"{stat}"])

    for x in combine_4:
        stats_4.append(x)
    for stat in stats_4:
        num_list.append(combine_4[f"{stat}"])

    for x in combine_5:
        stats_5.append(x)
    for stat in stats_5:
        num_list.append(combine_5[f"{stat}"])

    for stat in stats_1:
        stat_list.append(stat)

    for stat in stats_2:
        stat_list.append(stat)

    for stat in stats_3:
        stat_list.append(stat)

    for stat in stats_4:
        stat_list.append(stat)

    for stat in stats_5:
        stat_list.append(stat)

    return stat_list, num_list

# stats, num  = (team_season('WAS', 2024))

# data = [f"{s:<25}: {n}" for s, n in zip(stats, num)]
# print(num)
# for i in data:
#     print(i)
# a, b = team_passing_season('WAS', 2024)
#
# for i in range(0,len(passing)):
#     print(a[i], b[i])
#
# a, b = team_rushing_season('WAS', 2024)
#
# for i in range(0,len(rushing)):
#     print(a[i], b[i])
#
# a, b = team_receiving_season('WAS', 2024)
#
# for i in range(0,len(receiving)):
#     print(a[i], b[i])
#
# a, b = team_sacks_season('WAS', 2024)
#
# for i in range(0,len(sacks)):
#     print(a[i], b[i])
#
# a, b = team_special_tds_season('WAS', 2024)
#
# for i in range(0,len(special)):
#     print(a[i], b[i])


