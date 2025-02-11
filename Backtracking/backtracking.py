#PYTHON 
def read_input():
    n, m, k = map(int, input().split())
    q = list(map(int, input().split()))
    Q = list(map(int, input().split()))
    distance_matrix = [list(map(int, input().split())) for _ in range(2 * n + 2 * m + 1)]
    return n, m, k, q, Q, distance_matrix

def compute_route_distance(route, distance_matrix):
    return sum(distance_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))

def check_capacity(route, q, n, m, taxi_capacity):
    capacity = 0
    picked_up = set()
    
    pickup_start = n + 1
    pickup_end = m + n
    dropoff_start = m + 2*n + 1
    dropoff_end = 2*m + 2*n
    
    for node in route:
        if pickup_start <= node <= pickup_end:
            capacity += q[node - n - 1]
            picked_up.add(node)
        elif dropoff_start <= node <= dropoff_end:
            parcel_id = node - m - 2*n
            if parcel_id in picked_up:
                capacity -= q[parcel_id - 1]
                picked_up.remove(parcel_id)
        
        if capacity > taxi_capacity:
            return False
    return True

def is_valid_next_stop(pickup, route, dropoff, n):
    if 1 <= pickup <= n: 
        return True  
    else:  
        return dropoff not in route  

def estimate_cost(route, pickup, dropoff, distance_matrix):
    if not route:
        return distance_matrix[0][pickup] + distance_matrix[pickup][dropoff] + distance_matrix[dropoff][0]
    last = route[-1]
    return distance_matrix[last][pickup] + distance_matrix[pickup][dropoff]

def backtrack(taxi_routes, remaining_requests, current_distances, best_max_distance, n, m, k, q, Q, distance_matrix):
    if not remaining_requests:
        max_distance = max(current_distances)
        if max_distance < best_max_distance[0]:
            best_max_distance[0] = max_distance
            best_max_distance[1] = [route[:] for route in taxi_routes]
        return

    taxi_order = sorted(range(k), key=lambda x: current_distances[x])
    
    for taxi in taxi_order:
        route = taxi_routes[taxi]
        
        sorted_requests = sorted(
            remaining_requests,
            key=lambda req: estimate_cost(route, req[0], req[1], distance_matrix)
        )
        
        for req in sorted_requests:
            pickup, dropoff = req
            
            if pickup not in route and is_valid_next_stop(pickup, route, dropoff, n):
                # Handle passenger requests
                if 1 <= pickup <= n:
                    new_route = route + [pickup, dropoff]
                    if check_capacity(new_route, q, n, m, Q[taxi]):
                        distance = compute_route_distance([0] + new_route + [0], distance_matrix)
                        
                    
                        if distance >= best_max_distance[0]:
                            continue
                            
                        taxi_routes[taxi] = new_route
                        current_distances[taxi] = distance
                        new_remaining = remaining_requests - {req}
                        
                        backtrack(taxi_routes, new_remaining, current_distances, 
                                best_max_distance, n, m, k, q, Q, distance_matrix)
                        
                        taxi_routes[taxi] = route
                        current_distances[taxi] = compute_route_distance([0] + route + [0], distance_matrix)
                
                # Handle parcel requests
                else:
                    new_route = route + [pickup]
                    if check_capacity(new_route, q, n, m, Q[taxi]):
                        distance = compute_route_distance([0] + new_route + [0], distance_matrix)
                        
                        if distance >= best_max_distance[0]:
                            continue
                            
                        taxi_routes[taxi] = new_route
                        current_distances[taxi] = distance
                        new_remaining = remaining_requests - {req} | {(pickup, dropoff)}
                        
                        backtrack(taxi_routes, new_remaining, current_distances,
                                best_max_distance, n, m, k, q, Q, distance_matrix)
                        
                        taxi_routes[taxi] = route
                        current_distances[taxi] = compute_route_distance([0] + route + [0], distance_matrix)
            
            # Handle dropoff for already picked up requests
            elif pickup in route and dropoff not in route:
                new_route = route + [dropoff]
                if check_capacity(new_route, q, n, m, Q[taxi]):
                    distance = compute_route_distance([0] + new_route + [0], distance_matrix)
                    
                    if distance >= best_max_distance[0]:
                        continue
                        
                    taxi_routes[taxi] = new_route
                    current_distances[taxi] = distance
                    new_remaining = remaining_requests - {req}
                    
                    backtrack(taxi_routes, new_remaining, current_distances,
                            best_max_distance, n, m, k, q, Q, distance_matrix)
                    
                    taxi_routes[taxi] = route
                    current_distances[taxi] = compute_route_distance([0] + route + [0], distance_matrix)

def solve():
    n, m, k, q, Q, distance_matrix = read_input()

    # Generate all requests
    passenger_requests = {(i, i + n + m) for i in range(1, n + 1)}
    parcel_requests = {(i + n, i + 2*n + m) for i in range(1, m + 1)}
    all_requests = passenger_requests | parcel_requests

    taxi_routes = [[] for _ in range(k)]
    current_distances = [0] * k
    best_max_distance = [float('inf'), None] 

    backtrack(taxi_routes, all_requests, current_distances, best_max_distance, n, m, k, q, Q, distance_matrix)

    print(k)
    for route in best_max_distance[1]:
        print(len(route) + 2)
        print(0, *route, 0)


solve()
