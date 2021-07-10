def extract_triangles(file_name):
    """Extracting all triangle coordinates from stl file."""
    data = []
    try:
        with open(file_name, encoding='utf-8') as f:
            for line in f:
                if 'outer loop' in line:  # that's means the next 3 lines consists cordinates for 1 triangle
                    ls = f.readline().split()
                    x1, y1, z1 = map(float, (ls[1], ls[2], ls[3]))  # first point of triangle
                    ls = f.readline().split()
                    x2, y2, z2 = map(float, (ls[1], ls[2], ls[3]))  # second point of triangle
                    ls = f.readline().split()
                    x3, y3, z3 = map(float, (ls[1], ls[2], ls[3]))  # third point of triangle

                    data.append(((x1, y1, z1), (x2, y2, z2), (x3, y3, z3)))
        return data

    except FileNotFoundError:
        print('File not found')


def sides_from_triangles(all_triangles):    # extracting all triangle sides
    all_sides = []
    for triangle in all_triangles:
        if triangle[0] < triangle[1]:
            all_sides.append((triangle[0], triangle[1]))
        else:
            all_sides.append((triangle[1], triangle[0]))

        if triangle[0] < triangle[2]:
            all_sides.append((triangle[0], triangle[2]))
        else:
            all_sides.append((triangle[2], triangle[0]))

        if triangle[1] < triangle[2]:
            all_sides.append((triangle[1], triangle[2]))
        else:
            all_sides.append((triangle[2], triangle[1]))

    return all_sides


def sides_only_once(all_sides):     # extracting sides that apeear only once
    dct = {}
    for side in all_sides:
        dct[side] = dct.get(side, 0) + 1

    side_once = []
    for side in dct:
        if dct[side] == 1:
            side_once.append(side)

    return side_once


triangles = extract_triangles('dol.stl')
sides = sides_from_triangles(triangles)
sides_once = sides_only_once(sides)



