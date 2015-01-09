__author__ = 'roberto'


x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8

c_real, c_imag = -0.62772, -0.42193j


def run_julia_set(desired_width, max_iterations):

    # c = -0.62772 - 0.42193j

    # print(c)

    # f(z) = z^2 + c

    # top left corner: z = -1.8 - 1.8j

    # center: z = 0 + 0j

    # escape function: abs(z) < 2.0

    x_step = float(x2 - x1) / float(desired_width)

    y_step = float(y2 - y1) / float(desired_width)

    x = []

    y = []

    ycoord = y2  # from highest to lowest

    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step

    xcoord = x1

    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step

