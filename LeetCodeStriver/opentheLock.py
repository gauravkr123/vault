class Solution:
    def openLock(self, deadends: List[str], target: str) -> int:
        dead_set = set(deadends)
        if '0000' in dead_set:
            return -1
        if target == '0000':
            return 0
        
        def get_neighbors(combo):
            neighbors = []
            for i in range(4):
                digit = int(combo[i])
                for move in (-1, 1):
                    new_digit = (digit + move) % 10
                    neighbors.append(combo[:i] + str(new_digit) + combo[i+1:])
            return neighbors

        # Two queues for BFS: one from the start, one from the target
        start_queue, end_queue = set(['0000']), set([target])
        visited = set(['0000'])
        steps = 0

        # Bidirectional BFS
        while start_queue and end_queue:
            # Always expand the smaller search front for optimization
            if len(start_queue) > len(end_queue):
                start_queue, end_queue = end_queue, start_queue

            next_level = set()
            for combination in start_queue:
                if combination in end_queue:
                    return steps
                #run bfs to get all the neighbors
                for neighbor in get_neighbors(combination):
                    if neighbor not in visited and neighbor not in dead_set:
                        visited.add(neighbor)
                        next_level.add(neighbor)

            start_queue = next_level
            steps += 1

        return -1

        