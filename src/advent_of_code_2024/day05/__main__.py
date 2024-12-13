from functools import cmp_to_key
from os import path

from .. import DATA_PATH

def part1(filename: str) -> int:
    file_path = path.join(DATA_PATH, filename)
    with open(file_path, "r") as fh:
        top, bottom = fh.read().strip().split("\n\n")
    
    rules = frozenset(top.split("\n"))
    
    middle_page_sum = 0
    for update in bottom.split("\n"):
        pages = list(map(int, update.split(",")))
        sorted_pages = sorted(pages, key=cmp_to_key(lambda p1, p2: -1 if f"{p1}|{p2}" in rules else 1))

        if pages == sorted_pages:
            middle_page_sum += sorted_pages[len(sorted_pages) // 2]

    return middle_page_sum


def part2(filename: str) -> int:
    file_path = path.join(DATA_PATH, filename)
    with open(file_path, "r") as fh:
        top, bottom = fh.read().strip().split("\n\n")
    
    rules = frozenset(top.split("\n"))
    
    middle_page_sum = 0
    for update in bottom.split("\n"):
        pages = list(map(int, update.split(",")))
        sorted_pages = sorted(pages, key=cmp_to_key(lambda p1, p2: -1 if f"{p1}|{p2}" in rules else 1))

        if pages != sorted_pages:
            middle_page_sum += sorted_pages[len(sorted_pages) // 2]

    return middle_page_sum


assert part1("day05-sample.txt") == 143
assert part1("day05.txt") == 4959

assert part2("day05-sample.txt") == 123
assert part2("day05.txt") == 4655


#
# i did all this without realizing that the list of sorting rules was "complete",
# so i just determined the order myself
#
# but for part 2, the dependencies form a loop, so i just rotated the loop such that the first element 
# of the ordered list matched the first update... but this caused some rules to be violated
#
"""
if:
    A preceeds B and B preceeds C
    then A preceeds C
then:
    we can delete the rule A|C if provided
"""
# def add_following(ordered_nodes: list[int], preceeds: dict[int, int]) -> list[int]:
#     while True:
#         last_node = ordered_nodes[-1]
#         try:
#             next_node = preceeds[last_node]
#             if next_node in ordered_nodes:
#                 break
#         except KeyError:
#             break

#         ordered_nodes.append(next_node)

#     return ordered_nodes


# def add_preceeding(ordered_nodes: list[int], preceeds: dict[int, int]) -> list[int]:
#     follows = {v: k for k, v in preceeds.items()}

#     while True:
#         first_node = ordered_nodes[0]
#         try:
#             first_node = follows[first_node]
#             if first_node in ordered_nodes:
#                 break
#         except KeyError:
#             break

#         ordered_nodes.insert(0, first_node)

#     return ordered_nodes


# def get_preceeds(top: str) -> dict[int, int]:
#     node_sets: dict[int, set[int]] = {}
#     for item in top.split("\n"):
#         from_node, to_node = map(int, item.split("|"))
#         if from_node not in node_sets:
#             node_sets[from_node] = {to_node}
#         else:
#             node_sets[from_node].add(to_node)

#     for node1, post_node1 in node_sets.items():
#         to_remove = set()
#         for node2 in post_node1:
#             try:
#                 post_node2 = node_sets[node2]
#             except KeyError:
#                 continue

#             to_remove |= {node3 for node3 in post_node2 if node3 in post_node1}

#         post_node1.difference_update(to_remove)

#     assert all(len(v) == 1 for v in node_sets.values())

#     return {k: v.pop() for k, v in node_sets.items()}


# def get_ordered_nodes(top: str) -> list[int]:
#     preceeds = get_preceeds(top)

#     # just pick a node that's in both the sample and actual data
#     assert 47 in preceeds

#     ordered_nodes = [47]
#     ordered_nodes = add_following(ordered_nodes, preceeds)
#     ordered_nodes = add_preceeding(ordered_nodes, preceeds)

#     return ordered_nodes


# def valid_ordering(pages: list[int], ordered_nodes: list[int]) -> int:
#     op = ordered_nodes[:]
#     for page in pages:
#         try:
#             while page != op[0]:
#                 op.pop(0)
#         except IndexError:
#             return 0

#     return pages[len(pages) // 2]

# def sort_pages(pages: list[int], ordered_nodes: list[int]) -> list[int]:
#     sorted_pages = []
#     for page in ordered_nodes:
#         if page in pages:
#             sorted_pages.append(page)

#     return sorted_pages


# def part1(filename: str) -> int:
#     file_path = path.join(DATA_PATH, filename)
#     with open(file_path, "r") as fh:
#         top, bottom = fh.read().strip().split("\n\n")

#     ordered_nodes = get_ordered_nodes(top)

#     middle_page_sum = 0
#     for row in bottom.split("\n"):
#         pages = list(map(int, row.strip().split(",")))
#         assert len(pages) % 2 == 1

#         if "sample" in filename:
#             middle_page_sum += valid_ordering(pages, ordered_nodes)
#         else:
#             assert pages[0] in ordered_nodes
#             while ordered_nodes[0] != pages[0]:
#                 ordered_nodes = ordered_nodes[-1:] + ordered_nodes[:-1]
#             middle_page_sum += valid_ordering(pages, ordered_nodes)


#     return middle_page_sum


# def part2(filename: str) -> int:
#     file_path = path.join(DATA_PATH, filename)
#     with open(file_path, "r") as fh:
#         top, bottom = fh.read().strip().split("\n\n")

#     ordered_nodes = get_ordered_nodes(top)

#     middle_page_sum = 0
#     for row in bottom.split("\n"):
#         pages = list(map(int, row.strip().split(",")))
#         assert len(pages) % 2 == 1

#         if "sample" in filename:
#             if valid_ordering(pages, ordered_nodes) == 0:
#                 pages = sort_pages(pages, ordered_nodes)
#                 middle_page_sum += pages[len(pages) // 2]
#         else:
#             assert pages[0] in ordered_nodes
#             while ordered_nodes[0] != pages[0]:
#                 ordered_nodes = ordered_nodes[-1:] + ordered_nodes[:-1]
#             if valid_ordering(pages, ordered_nodes) == 0:
#                 pages = sort_pages(pages, ordered_nodes)
#                 middle_page_sum += pages[len(pages) // 2]

#     return middle_page_sum

# assert part1("day05-sample.txt") == 143
# assert part1("day05.txt") == 4959

# assert part2("day05-sample.txt") == 123
# print(part2("day05.txt"))
