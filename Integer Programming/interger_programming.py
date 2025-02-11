from ortools.linear_solver import pywraplp
import os
import sys
import time

def input_data():

    data = {}

    N, M, K = map(int, input().split())
    q = list(map(int, input().split()))

    data["parcel_number"] = [0 for i in range(2*N + 2*M + 2)]
    for i in range(N + 1, M + N + 1):
        data["parcel_number"][i] = q[i - N - 1]
        data["parcel_number"][i + N + M] = - q[i - N - 1]

    data["capacity"] = [0]
    data["capacity"].extend([int(Q) for Q in list(map(int, input().split()))])

    data["distance"] = []
    for i in range(2*N + 2*M + 1):
        data["distance"].append([int(d) for d in list(map(int, input().split()))])
        point_0 = data["distance"][i][0]
        data["distance"][i].append(point_0)
    data["distance"].append(data["distance"][0])

    return N, M, K, data

if __name__ == "__main__":


    N, M, K, data = input_data()

    solver = pywraplp.Solver.CreateSolver("SCIP")

    alpha = 1000000

    X = [[[0 for k in range(K + 1)] for j in  range(2*M + 2*N + 2)] for i in range(2*M + 2*N + 2)]

    for i in range(2*N + 2*M + 2):
        for j in range(2*N + 2*M + 2):
            if i != j:
                for k in range(1, K + 1):
                    X[i][j][k] = solver.IntVar(0, 1, 'X[%d][%d][%d]' % (i, j, k))

    #Y[k][j]: the number of parcels in the k-th taxi after it leaves j-th point

    Y = [[0 for i in range(2*N + 2*M + 2)] for i in range(K + 1)]

    for k in range(1, K + 1):
        for j in range(2*N + 2*M + 1):
            Y[k][j] = solver.IntVar(0, data["capacity"][k], 'Y[%d][%d]' % (k, j))

    #Z[k][j]: The order of j-th point in the route of k-th taxi
    Z = [[0 for i in range(2*N + 2*M + 2)] for k in range(K + 1)]

    for k in range(1, K + 1):
        for j in range(2*N + 2*M + 2):
            Z[k][j] = solver.IntVar(0, 2*N + 2*M + 1, 'Z[%d][%d]' % (k, j))

    #Add constraints

    #In_degree and out_degree of each point from 1 to 2*N + 2*M are equal to 1
    for i in range(1, 2*N + 2*M + 1):
        in_deg_i = []
        out_deg_i = []
        for j in range(2*N + 2*M + 2):
            if i != j:
                for k in range(1, K + 1):
                    in_deg_i.append(X[j][i][k])
                    out_deg_i.append(X[i][j][k])
        solver.Add(sum(in_deg_i) == 1)
        solver.Add(sum(out_deg_i) == 1)

    #For each taxi, in_degree and out_degree of each point from 1 to 2*N + 2*M are equal
    for k in range(1, K + 1):
        for i in range(1, 2*N + 2*M + 1):
            in_deg_i = []
            out_deg_i = []
            for j in range(2*N + 2*M + 2):
                if i != j:
                    in_deg_i.append(X[j][i][k])
                    out_deg_i.append(X[i][j][k])
            solver.Add(sum(in_deg_i) == sum(out_deg_i))

    #For each taxi, out_degree of start point and in_degree of end point are equal to 1
    for k in range(1, K + 1):
        out_deg_start = []
        in_deg_end = []
        for i in range(1, N + M + 1):
            out_deg_start.append(X[0][i][k])
        for i in range(N + M + 1, 2*N + 2*M + 1):
            in_deg_end.append(X[i][2*N + 2*M + 1][k])
        solver.Add(sum(out_deg_start) == 1)
        solver.Add(sum(in_deg_end) == 1)

    #For each taxi, in_degree  of start point and out_degree of end point are equal to 0
    for k in range(1, K + 1):
        in_deg_start = []
        out_deg_end = []
        for i in range(2*N + 2*M + 2):
            in_deg_start.append(X[i][0][k])
            out_deg_end.append(X[2*N + 2*M + 1][i][k])
        solver.Add(sum(in_deg_start) == 0)
        solver.Add(sum(out_deg_end) == 0)

    #For each taxi, out_degree of i-th point and in_degree of i+N+M-th point are equal
    for k in range(1, K + 1):
        for i in range(N + 1, N+M+1):
            out_deg_i = []
            in_deg_iNM = []
            for j in range(1, 2*N + 2*M + 1):
                if i != j:
                    out_deg_i.append(X[i][j][k])
                if j != i + N + M:
                    in_deg_iNM.append(X[j][i+N+M][k])

            solver.Add(sum(out_deg_i) == sum(in_deg_iNM))

    #If the k-th taxi picks up a passenger at i-th point, it must travel to i+N+M-th point instantly
    #(No stopping point between i-th point and i+N+M-th point)
    for k in range (1, K + 1):
        for i in range(0, 2*N + 2*M + 1):
            for j in range(1, N+1):
                if i != j:
                    solver.Add(alpha*(1 - X[i][j][k]) + 1 >= X[j][j+N+M][k])
                    solver.Add(alpha*(1 - X[i][j][k]) + X[j][j+N+M][k] >= 1)

    #If the k-th taxi travels from i-th point to j-th point then Y[k][j] = Y[k][i] + data["parcel_number"][j]
    for k in range(1, K + 1):
        for i in range(0, 2*N + 2*M + 1):
            for j in range(0, 2*N + 2*M + 2):
                if i != j:
                    solver.Add(alpha*(1 - X[i][j][k]) + Y[k][j] >= Y[k][i] + data["parcel_number"][j])
                    solver.Add(alpha*(1 - X[i][j][k]) + Y[k][i] + data["parcel_number"][j] >= Y[k][j])

    #If the k-th taxi travels from i-th point to j-th point then Z[k][j] = Z[k][i] + 1
    for k in range(1, K + 1):
        for i in range(2*N + 2*N + 1):
            for j in range(1, 2*N + 2*N + 2):
                solver.Add(alpha * (1 - X[i][j][k]) + Z[k][j] >= Z[k][i] + 1)
                solver.Add(alpha * (1 - X[i][j][k]) + Z[k][i] + 1 >= Z[k][j])

    #For each taxi, the number of parcel after it leaves the start point is 0
    for k in range(1, K + 1):
        solver.Add(Y[k][0] == 0)

    #For each taxi, the order of start point is 0
    for k in range(1, K + 1):
        solver.Add(Z[k][0] == 0)

    #Constraint Y[k][i] <= Q[k] is solved by domain of variable Y[k][i]

    #For each taxi, the order of i-th point always less than or equal the order of (i + N + M)-th point
    for k in range(1, K + 1):
        for i in range(1, N + M + 1):
            solver.Add(Z[k][i] <= Z[k][i + N + M])

    #Set the first route is the longest route
    lengthOfRoute = [0]
    for k in range(1, K + 1):
        constrain_expr = []
        for i in range(2*N + 2*M + 2):
            for j in range(2*N + 2*M + 2):
                if i != j:
                    constrain_expr.append(X[i][j][k] * data["distance"][i][j])
        lengthOfRoute.append(sum(constrain_expr))

    for k in range(2, K + 1):
        solver.Add(lengthOfRoute[1] >= lengthOfRoute[k])

    #Minimize the length of first route
    solver.Minimize(lengthOfRoute[1])
    status = solver.Solve()

    #Print output
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(K)
        for k in range(1, K + 1):
            path = [0]
            length = 0
            while path[-1] != 2*N + 2*M + 1:
                for i in range(2*N + 2*M + 2):
                    if i != path[-1]:
                        if X[path[-1]][i][k].solution_value() == 1:
                            path.append(i)
                            length += data["distance"][path[-2]][i]
                            break
            path[-1]=0                
            print(len(path))                
            print(" ".join(map(str, path)))
