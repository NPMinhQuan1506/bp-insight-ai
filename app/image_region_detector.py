from collections import deque


def adr_detectRegions(binary_matrix, min_height=5, min_width=2):
    if not binary_matrix or not binary_matrix[0]:
        return []

    height = len(binary_matrix)
    width = len(binary_matrix[0])

    visited = [[False for _ in range(width)] for _ in range(height)]

    all_components = []

    for y in range(height):
        for x in range(width):
            if binary_matrix[y][x] == 1 and not visited[y][x]:
                component = ard_findConnComponent(binary_matrix, visited, x, y)
                all_components.append(component)

    bounding_boxes = []
    for component_pixels in all_components:
        if component_pixels:
            box = ard_calcBoundingBox(component_pixels)
            bounding_boxes.append(box)

    filtered_boxes = []
    for x, y, w, h in bounding_boxes:
        if w >= min_width and h >= min_height:
            filtered_boxes.append((x, y, w, h))

    sorted_boxes = sorted(filtered_boxes, key=lambda box: box[0])

    return sorted_boxes


def ard_findConnComponent(matrix, visited, start_x, start_y):
    height = len(matrix)
    width = len(matrix[0])

    component_pixels = []
    queue = deque([(start_x, start_y)])
    visited[start_y][start_x] = True

    while queue:
        x, y = queue.popleft()
        component_pixels.append((x, y))

        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                nx, ny = x + dx, y + dy

                if 0 <= nx < width and 0 <= ny < height:
                    if matrix[ny][nx] == 1 and not visited[ny][nx]:
                        visited[ny][nx] = True
                        queue.append((nx, ny))

    return component_pixels


def ard_calcBoundingBox(pixels):
    min_x = min(p[0] for p in pixels)
    max_x = max(p[0] for p in pixels)
    min_y = min(p[1] for p in pixels)
    max_y = max(p[1] for p in pixels)

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    return (min_x, min_y, width, height)
