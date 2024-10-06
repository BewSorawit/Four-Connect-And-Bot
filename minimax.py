import math


def minimax(curDepth, nodeIndex, maxTurn, scores, targetDepth):
    # base case: targetDepth reached
    print(curDepth, nodeIndex, targetDepth, maxTurn)
    if curDepth == targetDepth:
        print(
            f"Depth {curDepth}, Node {nodeIndex}: score = {scores[nodeIndex]}")
        return scores[nodeIndex]

    if maxTurn:
        left_value = minimax(curDepth + 1, nodeIndex * 2,
                             False, scores, targetDepth)
        right_value = minimax(curDepth + 1, nodeIndex *
                              2 + 1, False, scores, targetDepth)
        value = max(left_value, right_value)
        print(
            f"Depth {curDepth}, Node {nodeIndex}: max({left_value}, {right_value}) = {value}")
        return value
    else:
        left_value = minimax(curDepth + 1, nodeIndex * 2,
                             True, scores, targetDepth)
        right_value = minimax(curDepth + 1, nodeIndex *
                              2 + 1, True, scores, targetDepth)
        value = min(left_value, right_value)
        print(
            f"Depth {curDepth}, Node {nodeIndex}: min({left_value}, {right_value}) = {value}")
        return value


# Driver code
scores = [3, 5, 2, 9, 12, 5, 23, 23]
# scores = [3, 5, 2, 9, 12, 5, 23, 23,
#           10, 7, 6, 4, 1, 0, 8, 11]
treeDepth = math.log(len(scores), 2)
print("The optimal value is : ")
optimal_value = minimax(0, 0, True, scores, treeDepth)
print(optimal_value)
