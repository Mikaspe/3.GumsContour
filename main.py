from pathvalidate import is_valid_filename


def extract_triangles_from_stl_file():
    """Extracting all triangle coordinates from stl file."""
    triangles_data = []

    while True:
        filename = input('Enter the name of file in STL ASCII format(eg. \'upperjaw.stl\'): ')
        if not filename.endswith('.stl'):
            print('The file extension must be \'.stl\'.')
            continue
        try:
            with open(filename) as f:
                if 'solid' not in f.readline():
                    print(filename, 'is not in ASCII format.')
                    continue
                for line in f:
                    if 'outer loop' in line:  # That's means the next 3 lines consists 3 vertices of 1 triangle
                        ls = f.readline().split()
                        x1, y1, z1 = map(float, (ls[1], ls[2], ls[3]))  # First vertex of triangle
                        ls = f.readline().split()
                        x2, y2, z2 = map(float, (ls[1], ls[2], ls[3]))  # Second vertex of triangle
                        ls = f.readline().split()
                        x3, y3, z3 = map(float, (ls[1], ls[2], ls[3]))  # Third vertex of triangle
                        triangles_data.append(((x1, y1, z1), (x2, y2, z2), (x3, y3, z3)))
            break
        except FileNotFoundError:
            print('File not found')
        except IndexError:
            print('File error')

    print('Triangles in source:', len(triangles_data))
    print('Vertecies in source:', 3*len(triangles_data))
    return triangles_data


def get_sides_of_triangles(triangles):
    """Determining all triangles sides from triangles coordinates.
    One side is a tuple of two triangle vertieces.
    """
    sides = []  # List with every single side from input triangles
    for triangle in triangles:
        # Point with lower x coordinate is first in tuple, because then it's easier to count the same sides in next step
        if triangle[0] < triangle[1]:
            sides.append((triangle[0], triangle[1]))
        else:
            sides.append((triangle[1], triangle[0]))

        if triangle[0] < triangle[2]:
            sides.append((triangle[0], triangle[2]))
        else:
            sides.append((triangle[2], triangle[0]))

        if triangle[1] < triangle[2]:
            sides.append((triangle[1], triangle[2]))
        else:
            sides.append((triangle[2], triangle[1]))

    return sides


def get_contour(sides):
    """Determing model contour from sides."""
    # Side makes contour if appears only once in sides
    sides_counter = {}
    for side in sides:  # Counting how many times same side appears
        sides_counter[side] = sides_counter.get(side, 0) + 1

    sides_contour = []  # Sides that make model contour
    for side in sides_counter:  # Choosing sides that appears once - model contour
        if sides_counter[side] == 1:
            sides_contour.append(side)

    return sides_contour


def get_gums_contour(all_sides_contours, min_gum_line_length=100, max_gum_line_length=400):
    """Determing gums contour points of whole model contours."""
    gums_contour = []
    while all_sides_contours:  # This loop separates each contour in model and picks contours that makes a gum
        one_of_contours = [all_sides_contours[0][0]]
        while True:  # This loop determine each one of model contours in 'one_of_contours'
            # for loop checks if point of one side is also an point in another side, so it makes same line contour
            for side in all_sides_contours:
                if one_of_contours[-1] == side[0]:
                    one_of_contours.append(side[1])
                    all_sides_contours.remove(side)
                    break
                elif one_of_contours[-1] == side[1]:
                    one_of_contours.append(side[0])
                    all_sides_contours.remove(side)
                    break
            else:  # That's means there's no more points(sides) in 'one_of_contours'
                break

        if min_gum_line_length < len(one_of_contours) < max_gum_line_length:  # Determing all gums in one list
            gums_contour.extend(one_of_contours)

    print('Points in output .obj file:', len(gums_contour))
    return gums_contour


def export_to_file(points, filename):
    """Exporting 3D points as .obj file."""
    try:
        with open(filename + '.obj', "w") as f:
            for point in points:
                f.write('v' + ' ' + str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[2]) + '\n')
    except IOError:
        print('Unable to create file on disk')


def main_function():
    all_triangles = extract_triangles_from_stl_file()
    all_sides = get_sides_of_triangles(all_triangles[:])  # One side is definied by two vertices
    contour = get_contour(all_sides[:])
    gums_contour_points = get_gums_contour(contour[:])

    # UI
    while True:
        ans = input('Print gums contour points in console? (y/n):')
        if ans == 'y' or ans == 'Y':
            for point in gums_contour_points:
                print(*point)
            break
        elif ans == 'n' or ans == 'N':
            break

    while True:
        ans = input('Create .obj file with result? (y/n):')
        if ans == 'y' or ans == 'Y':
            while True:
                filename = input('Name of file to create:')
                if is_valid_filename(filename):
                    export_to_file(gums_contour_points, filename)
                    break
                else:
                    print('Invalid filename')
            break
        elif ans == 'n' or ans == 'N':
            break


if __name__ == '__main__':
    main_function()
