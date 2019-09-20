from pulp import *


def shortestPath(edges_with_cost, start_point, end_point, directed=True):

    prob = LpProblem(
        "Shortest Path between 2 points with Linear Programming", LpMinimize
    )

    flippedEdges = []
    if not directed:

        for s, e, c in edges_with_cost:
            flippedEdges.append([e, s, c])
        edges_with_cost += flippedEdges

    toSumForObjectiveFunction = []
    variablesThatStartWith = {}
    variablesThatEndWith = {}

    all_start_vars = []
    all_end_vars = []

    for s, e, c in edges_with_cost:
        thisVar = LpVariable("BinaryVar_" + str(s) + "_" + str(e), 0, 1, LpInteger)
        toSumForObjectiveFunction.append(thisVar * c)

        if s == start_point:
            all_start_vars.append(thisVar)
        else:
            if s in variablesThatStartWith.keys():
                variablesThatStartWith[s].append(thisVar)
            else:
                variablesThatStartWith[s] = [thisVar]

        if e == end_point:
            all_end_vars.append(thisVar)
        else:
            if e in variablesThatEndWith.keys():
                variablesThatEndWith[e].append(thisVar)
            else:
                variablesThatEndWith[e] = [thisVar]

    prob += lpSum(all_start_vars) == 1
    prob += lpSum(all_end_vars) == 1
    for kk in variablesThatEndWith.keys():
        if kk in variablesThatEndWith.keys():
            endArray = variablesThatEndWith[kk]
        else:
            endArray = []
        if kk in variablesThatStartWith.keys():
            startArray = variablesThatStartWith[kk]
        else:
            startArray = []
        # prob += lpSum(variablesThatEndWith[kk]) == lpSum(variablesThatStartWith[kk])
        prob += lpSum(endArray) == lpSum(startArray)

    prob += lpSum(toSumForObjectiveFunction)

    # solve and print results

    prob.solve()

    if LpStatus[prob.status] == "Optimal":
        goodVars = {}
        for v in prob.variables():
            if v.varValue == 1.0:
                s, e = v.name.split("_")[1:]
                goodVars[s] = e
        solution = []
        cur = start_point
        while True:
            solution.append(cur)
            if cur == end_point:
                break
            cur = goodVars[cur]
        return {"possible": True, "solution": solution, "cost": value(prob.objective)}

    elif LpStatus[prob.status] == "Infeasible":
        return {"possible": False}


if __name__ == "__main__":
    print()
    edges_with_cost = [
        ["1", "2", 5],
        ["2", "3", 5],
        ["3", "4", 1],
        ["1", "3", 300],
        ["1", "4", 1],
    ]

    start_point = "1"
    end_point = "3"

    print(shortestPath(edges_with_cost, start_point, end_point))
    print(shortestPath(edges_with_cost, start_point, end_point, directed=False))

