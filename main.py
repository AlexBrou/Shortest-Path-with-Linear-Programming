from pulp import LpProblem, lpSum, LpMinimize, LpVariable, LpInteger, LpStatus, value


def shortestPath(edges_with_cost, start_point, end_point, directed=True):

    prob = LpProblem(
        "Shortest Path between 2 points with Linear Programming", LpMinimize
    )

    # this section transforms the directed graph into undirected by duplicating the edges and giving the doubled ones the opposite direction
    if not directed:
        flippedEdges = []
        for s, e, c in edges_with_cost:
            flippedEdges.append([e, s, c])
        edges_with_cost += flippedEdges
    # end of section

    # arrays of variables
    # each variable is binary and is respective to an edge (either if it is part of the solution or not)

    # this array will have all the variables multiplied by the cost
    toSumForObjectiveFunction = []
    # this dictionary will have arrays of all the variables, categorized by their starting point, except the starting point of the path
    variablesThatStartWith = {}
    # same as the one above, but categorized by the ending point, excluding the ending point of the path
    variablesThatEndWith = {}

    # all the variables for the edges that have starting point equal to the starting point of the path
    all_start_vars = []
    # same as above, but for the endings
    all_end_vars = []

    for s, e, c in edges_with_cost:
        # binary variable declared
        thisVar = LpVariable("BinaryVar_" + str(s) + "_" + str(e), 0, 1, LpInteger)

        # now, we place the variable in the respective arrays and dictionaries
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

    # CONSTRAINTS

    # there must be only 1 edge coming from the starting point of the path
    prob += lpSum(all_start_vars) == 1

    # there must be only 1 edge entering the end point of the path
    prob += lpSum(all_end_vars) == 1

    for kk in variablesThatEndWith.keys():
        # this section makes sure that the program works if the input graph has more than 1 connected component
        if kk in variablesThatEndWith.keys():
            endArray = variablesThatEndWith[kk]
        else:
            endArray = []
        if kk in variablesThatStartWith.keys():
            startArray = variablesThatStartWith[kk]
        else:
            startArray = []
        # end of section

        # if there is an edge entering a point, there must be an edge exiting it ( except for the ending point)
        prob += lpSum(endArray) == lpSum(startArray)

    # OBJECTIVE FUNCTION

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

