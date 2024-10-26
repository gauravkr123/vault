from collections import deque
class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        #make adj list for the tree

        adj = {k:[] for k in range(numCourses)}
        in_degree = [0]*numCourses
        for dest, src in prerequisites:
            adj[src].append(dest)
            in_degree[dest]+=1
        # print(adj)

        queue = deque([i for i in range(numCourses) if in_degree[i]==0])
        result  = []

        while queue:
            course = queue.popleft()
            result.append(course)
            
            for neighbor in adj[course]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        return result if len(result) == numCourses else []
        