#PYTHON 
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def create_data_model_from_input():
    data = {}

    # Nhập N, M và K từ người dùng
    N, M, K = map(int, input().split())
    data['N'] = N
    data['M'] = M
    data['K'] = K

    # Nhập q[1], q[2], ..., q[M]
    q = list(map(int, input().split()))
    data['weights'] = [0] * (2 * N + 2 * M + 1)
    data['weights'][N:N+M] = q

    # Nhập Q[1], Q[2], ..., Q[K]
    Q = list(map(int, input().split()))
    data['vehicle_capacities'] = Q

    # Nhập ma trận khoảng cách
    distance_matrix = []
    for _ in range(2 * N + 2 * M + 1):
        row = list(map(int, input().split()))
        distance_matrix.append(row)
    data['distance_matrix'] = distance_matrix

    data['num_vehicles'] = data['K']
    data['depot'] = 0

    return data

def print_input():
    data = create_data_model_from_input()
    print("N:", data['N'])
    print("M:", data['M'])
    print("K:", data['K'])
    print("Weights:", data['weights'])
    print("Vehicle Capacities:", data['vehicle_capacities'])
    print("Distance Matrix:")
    for row in data['distance_matrix']:
        print(row)


def add_direct_follow_constraint(routing, manager, i, j):
    index_i = manager.NodeToIndex(i)
    index_j = manager.NodeToIndex(j)
    routing.solver().Add(routing.NextVar(index_i) == index_j)


def add_precedence_constraint(distance_dimension, routing, manager, i, j):
    index_i = manager.NodeToIndex(i)
    index_j = manager.NodeToIndex(j)
    routing.solver().Add(routing.VehicleVar(index_j) == routing.VehicleVar(index_i))
    routing.solver().Add(distance_dimension.CumulVar(index_j) >= distance_dimension.CumulVar(index_i) + 1)


def print_solution(data, manager, routing, solution):
    # In số lượng xe
    print(data['num_vehicles'])
    
    # Duyệt qua tất cả các xe và in các tuyến đường
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))  # Thêm điểm cuối

        # In tổng số điểm và các điểm cụ thể mà xe đó đi qua
        print(len(route))  # In số lượng điểm
        print(" ".join(map(str, route)))  # In các điểm cụ thể

def main():
    # Gọi hàm nhập dữ liệu từ người dùng
    data = create_data_model_from_input()
    
    # Khởi tạo manager và routing model
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )
    routing = pywrapcp.RoutingModel(manager)

    # Hàm tính toán khoảng cách giữa hai điểm
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Hàm tính toán trọng lượng tại mỗi điểm
    def weight_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data["weights"][from_node]
    weight_callback_index = routing.RegisterUnaryTransitCallback(weight_callback)

    # Thêm các constraint về trọng lượng và khoảng cách
    wei_dimension_name = "Weight"
    dis_dimension_name = "Distance"
    routing.AddDimensionWithVehicleCapacity(
        weight_callback_index,
        0,
        data["vehicle_capacities"],
        True,
        wei_dimension_name,
    )
    routing.AddDimension(
        transit_callback_index,
        0,
        1000000,
        True,
        dis_dimension_name,
    )

    distance_dimension = routing.GetDimensionOrDie(dis_dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Thêm các constraint về thứ tự và quan hệ trước sau
    for i in range(1, data["N"] + 1):
        add_direct_follow_constraint(routing, manager, i, i + data["N"] + data["M"])
    for i in range(1, data["M"] + 1):
        add_precedence_constraint(distance_dimension, routing, manager, i + data["N"], i + 2 * data["N"] + data["M"])

    # Cấu hình các tham số tìm kiếm
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.seconds = 20

    # Giải bài toán và in kết quả
    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print("No solution found!")


if __name__ == "__main__":
    main()
