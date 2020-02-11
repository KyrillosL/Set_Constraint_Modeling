import numpy as np
import os

g = 5   # groups
p = 3   # place in a group
w = 6  # weeks
q = g * p  # players

G = np.arange(1, p * g * q * w + 1).reshape((q, p, g, w))

content = ""

# 1 a player must plays at least one tme per week
for q_1 in range(q):
    for w_1 in range(w):
        for p_1 in range(p):
            for g_1 in range(g):
                content += f"{G[q_1, p_1, g_1, w_1]} "
        content += f"0\n"

# 2 a player play at most one time per week
for q_1 in range(q):
    for w_1 in range(w):
        for p_1 in range(p):
            for g_1 in range(g):
                for p_2 in range(p_1 + 1, p):
                    content += f"-{G[q_1, p_1, g_1, w_1]} -{G[q_1, p_2, g_1, w_1]} 0\n"

# 3 a player can plays only once a week
for q_1 in range(q):
    for w_1 in range(w):
        for p_1 in range(p):
            for g_1 in range(g):
                for g_2 in range(g_1 + 1, g):
                    for p_2 in range(p_1 + 1, p):
                        content += f"-{G[q_1, p_1, g_1, w_1]} -{G[q_1, p_2, g_2, w_1]} 0\n"

# 4 at least one player plays at a position in a group in a week
for w_1 in range(w):
    for p_1 in range(p):
        for g_1 in range(g):
            for q_1 in range(q):
                content += f"{G[q_1, p_1, g_1, w_1]} "
            content += f"0\n"

# 5 at most one player plays at a position in a group in a week
for w_1 in range(w):
    for p_1 in range(p):
        for g_1 in range(g):
            for q_1 in range(q):
                for q_2 in range(q_1 + 1, q):
                    content += f"-{G[q_1, p_1, g_1, w_1]} -{G[q_2, p_1, g_1, w_1]} 0\n"

# #
# # COMMON
# #

# sociability constraint

#w, g, x, x, g, w

for w_1 in range(w):
    for g_1 in range(g):
        for w_2 in range(w_1 + 1, w):
            for g_2 in range(g):

                for q_1 in range(q):
                    for p_11 in range(p):
                        for p_12 in range(p):

                            for q_2 in range(q_1 + 1, q):
                                for p_21 in range(p):
                                    for p_22 in range(p):
                                        content += f"-{G[q_1, p_11, g_1, w_1]} -{G[q_2, p_21, g_1, w_1]} -{G[q_1, p_12, g_2, w_2]} -{G[q_2, p_22, g_2, w_2]} 0\n"

# symétries
# for q_1 in range(q):
#     for p_1 in range(p-1):
#         for g_1 in range(g):
#             for w_1 in range(w):
#                 for q_2 in range(q_1):
#                     content += f"-{G[q_1, p_1, g_1, w_1]} -{G[q_2, p_1+1, g_1, w_1]} 0\n"
#
# for q_1 in range(q):
#     for g_1 in range(g-1):
#         for w_1 in range(w):
#             for q_2 in range(q_1-1):
#                 content += f"-{G[q_1, 0, g_1, w_1]} -{G[q_2, 0, g_1+1, w_1]} 0\n"
#
# for q_1 in range(q):
#     for w_1 in range(w-1):
#         for q_2 in range(q_1):
#             content += f"-{G[q_1, 1, 0, w_1]} -{G[q_2, 1, 0, w_1+1]} 0\n"

print(G)
print(content)

with open("sgp_model_sat", "w") as file:
    file.write(content)

os.system("minisat sgp_model_sat solution.out")

# solution = np.zeros((q, p, g, w)).reshape((q * p * g * w))
#
# with open("solution.out", "r") as file:
#     line = file.readline()
#     if line[:3] == "SAT":
#         result = file.readline().split(" ")
#         print(result)
#         for r in result:
#             if r[0] == "-":
#                 solution[int(r[0:])] = False
#             else:
#                 solution[int(r)] = True

# solution = solution.reshape((q, p, g, w))
#
# print(solution)
#
# for q_1 in range(q):
#     for w_1 in range(w):
#         print(solution[q_1, :, :, w_1])
