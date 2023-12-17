import time, ast
from functools import cmp_to_key

def compare_packets(left_packet, right_packet):
    left_packet_copy = list(left_packet)
    right_packet_copy = list(right_packet)
    for i in range(len(right_packet)):
        if i >= len(left_packet): return True # Left side ran out of items
        if type(left_packet[i]) is int and type(right_packet[i]) is int:
            if left_packet[i] < right_packet[i]: return True
            elif left_packet[i] > right_packet[i]: return False
            else: continue
        elif type(left_packet[i]) is int and type(right_packet[i]) is list:
            left_packet_copy[i] = [ left_packet[i] ]
        elif type(left_packet[i]) is list and type(right_packet[i]) is int:
            right_packet_copy[i] = [ right_packet[i] ]
        sub_result = compare_packets(left_packet_copy[i], right_packet_copy[i])
        if sub_result is not None: return sub_result

    if len(left_packet) > len(right_packet): return False # Right side ran out of items
    return None # Equal comparison

def compare_packets_wrapper(left_packet, right_packet):
    result = compare_packets(left_packet, right_packet)
    if result == True: return -1
    elif result == False: return 1
    else: return 0

#
# Process input
#
with open('day 13/input.txt', 'r') as file:
    list_pairs = file.read().split('\n\n')

#
# Puzzle 1
#
acc = 0
all_packets = []
for i, list_pair in enumerate(list_pairs):
    left_packet, right_packet = tuple(map(ast.literal_eval, list_pair.splitlines()))
    all_packets += [left_packet, right_packet] # Required for Puzzle 2
    if compare_packets(left_packet, right_packet): acc += (i+1)
print(f'Puzzle 1 solution is: {acc}')

#
# Puzzle 2
#
all_packets += [[[2]], [[6]]]
all_packets.sort(key=cmp_to_key(compare_packets_wrapper))
acc = 1
for i, packet in enumerate(all_packets):
    if packet == [[2]] or packet == [[6]]: acc *= (i+1)
print(f'Puzzle 2 solution is: {acc}')
