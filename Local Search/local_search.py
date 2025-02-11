#PYTHON 
import os
import sys
import time

import random
import copy

def import_data():
    N, M, K = map(int, input().split())
    q = list(map(int, input().split()))
    Q = list(map(int, input().split()))
    distance = []
    for _ in range(2 * N + 2 * M + 1):
        distance.append(list(map(int, input().split())))
    return N,M,K,q,Q,distance

def initialize_solution(N, M, K,q, Q):
    solution = [[] for _ in range(K)]
    parcels = list(range(N+1, N + M+1))  # Các yêu cầu chở hàng (4,5,6)
    passengers = list(range(1, N + 1))  # Các yêu cầu chở hành khách
    weight = [0 for i in range(K)] # weight là danh sách chứa khối lượng từng xe

# Phân bổ yêu cầu hàng vào taxi

    for parcel in parcels:
        taxi = random.randint(0, K - 1) # index của xe được chọn
        pickup = parcel # index của hàng được chọn
        dropoff = parcel + M + N

        # Tìm vị trí hợp lệ để chèn
        route = solution[taxi]
        id_pickup = random.randint(0, len(route))

        # nếu khối lượng ít hơn trọng tải thì nhận thêm hàng
        if weight[taxi] + q[pickup-N-1] <= Q[taxi]:
            route.insert(id_pickup, pickup)
            # mỗi khi đón hàng, cập nhật khối lượng hiện tại
            weight[taxi] += q[pickup-N-1]



        # Đảm bảo điểm dropoff được chèn sau điểm pickup
        id_dropoff = random.randint(id_pickup + 1, len(route))
        route.insert(id_dropoff, dropoff)
        weight[taxi] -= q[dropoff-N-M-N-1]


# Phân bổ yêu cầu chở người

    for passenger in passengers:
        taxi = random.randint(0, K - 1)
        pickup = passenger
        dropoff = passenger + M + N

        # Tìm vị trí hợp lệ để chèn pickup
        route = solution[taxi]
        while True:
            insert_pickup = random.randint(0, len(route))  # Chọn vị trí ngẫu nhiên
            # Đảm bảo không trùng với vị trí dropoff của hành khách khác
            if insert_pickup not in [route.index(x) for x in route if x > N + M]:
                break
        route.insert(insert_pickup, pickup)

        # Đảm bảo điểm dropoff được chèn ngay sau điểm pickup
        insert_dropoff = insert_pickup + 1
        route.insert(insert_dropoff, dropoff)

    # Thêm điểm depot vào đầu và cuối mỗi route
    for taxi in range(K):
        solution[taxi] = [0] + solution[taxi] + [0]

    return solution


def calculate_distance(route, distance):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance[route[i]][route[i + 1]]
    return total_distance


def two_opt(route, distance):
    """
    Cải thiện lộ trình bằng cách đảo thứ tự của các điểm giữa hai chỉ số i và j.
    """
    best_route = route
    best_cost = calculate_distance(route, distance)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                # Tạo lộ trình mới bằng cách đảo ngược đoạn i:j
                new_route = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
                new_cost = calculate_distance(new_route, distance)
                # Nếu chi phí giảm, cập nhật lộ trình tốt nhất
                if new_cost < best_cost:
                    best_route = new_route
                    best_cost = new_cost
                    improved = True
    return best_route


def local_search_two_opt(routes, distance, max_iterations=1000):
    for _ in range(max_iterations):
        improved = False
        for taxi in range(len(routes)):
            new_route = two_opt(routes[taxi], distance)
            if check_valid_single(new_route, N, M, Q[taxi], q):
                if new_route != routes[taxi]:  # Kiểm tra xem lộ trình có cải thiện không
                    routes[taxi] = new_route
                    improved = True
        if not improved:
            break
    return routes


def check_valid_single(route, N, M, Q, q):
    """
    Kiểm tra xem lộ trình có hợp lệ không.
    """
    passenger_pick_ups = [i for i in range(1, N + 1)]
    passenger_drop_offs = [i + N + M for i in range(1, N + 1)]
    parcel_pick_ups = [i + N for i in range(1, M + 1)]
    parcel_drop_offs = [i + 2 * N + M for i in range(1, M + 1)]

    load = 0
    visited = set()

    for i, node in enumerate(route):
        if node == 0:
            load = 0
            continue
        if node in visited:
            return False
        visited.add(node)
        if node in passenger_drop_offs:
            pickup_node = passenger_pick_ups[passenger_drop_offs.index(node)]
            if pickup_node not in visited:
                return False
        if node in passenger_pick_ups:
            drop_off_node = passenger_drop_offs[passenger_pick_ups.index(node)]
            if i + 1 >= len(route) or route[i + 1] != drop_off_node:
                return False
        if node in parcel_pick_ups:
            parcel_weight = q[parcel_pick_ups.index(node)]
            load += parcel_weight
            if load > Q:
                return False
        elif node in parcel_drop_offs:
            pickup_node = parcel_pick_ups[parcel_drop_offs.index(node)]
            if pickup_node not in visited:
                return False
            load -= q[parcel_pick_ups.index(pickup_node)]
    return True


# Ví dụ dữ liệu đầu vào
if __name__ == "__main__":

    N,M,K,q,Q,distance = import_data()
    routes = initialize_solution(N, M, K, q, Q)
    optimized_routes = local_search_two_opt(routes, distance)
    # In kết quả
    print(K)
    for route in optimized_routes:
      print(len(route))  # Print the number of stops
      print(" ".join(map(str, route)))  # Print the route as a space-separated string
