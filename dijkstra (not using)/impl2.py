from heapq import heappop, heappush

INF = int(1e9)
graph = [[]]

def preprocess(n, costs):
    global graph
    graph = [[] for _ in range(n+1)]

    for c in costs:
        src, dst, cost = c[0], c[1], c[2]
        graph[src].append([dst, cost])
        graph[dst].append([src, cost])

def dijkstra(src, dst):
    global graph
    n = len(graph)
    dist = [INF for _ in range(n)]
    dist[src] = 0
    pq = [[0, src]]

    while pq:
        w, x = heappop(pq)
        if dist[x] < w:
            continue
        for item in graph[x]: 
            nx, ncost = item[0], item[1]
            ncost += w
            if ncost < dist[nx]:
                dist[nx] = ncost
                heappush(pq, [ncost, nx])
    return dist[dst]

def solution():
    n, connections = map(int, input().split())
    fares = [[*map(int, input().split())] for _ in range(connections)]
    a, b = map(int, input().split())

    preprocess(n, fares)
    return dijkstra(a, b)

print(solution())