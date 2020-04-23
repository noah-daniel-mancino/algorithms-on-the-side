"""
You can characterize each line by the m and b in y = mx + b. Do this for each
pair of lines, and see which ones pops up the most.
"""

def max_points(points):
    lines = set()
    lines_frequency = {}
    for index, point in enumerate(points):
        other_points = points[index + 1:]
        print(other_points)
        for other_point in other_points:
            slope = (point[1] - other_point[1])/(point[0] - other_point[0])
            y_intercept = point[1] - (slope * point[0])
            if (slope, y_intercept) in lines:
                lines_frequency[(slope, y_intercept)] += 1
            else:
                lines_frequency[(slope, y_intercept)] = 1
            lines.add((slope, y_intercept))
    return max(lines_frequency.values())

print(max_points([[1,1],[2,2],[3,3],[7,2]]))
