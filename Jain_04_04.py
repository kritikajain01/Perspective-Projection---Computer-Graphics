# Jain, Kritika
# 1002-093-381
# 2017-10-25
# Assignment_04_04

#This file was provided by professor

# This a sample code for parallel projection clipping
# against the parallel volume bounded by the six planes
# x=1 ; x=-1 ; y=1 ; y=-1 ; z=0 ; and z=1
def assign_parallel_outcode(x, y, z):
    outcode = 0b000000
    if x > 1:
        outcode = 0b100000
    elif x < -1:
        outcode = 0b010000
    if y > 1:
        outcode = outcode | 0b001000
    elif y < -1:
        outcode = outcode | 0b000100
    if z > 1:
        outcode = outcode | 0b000010
    elif z < 0:
        outcode = outcode | 0b000001
    return outcode


def clip_line_parallel(p1, p2):
    # This function returns [] if the line is rejected.
    x1 = p1[0]
    y1 = p1[1]
    z1 = p1[2]
    x2 = p2[0]
    y2 = p2[1]
    z2 = p2[2]
    RIGHT = 0b100000
    LEFT = 0b010000
    TOP = 0b001000
    BOTTOM = 0b000100
    FAR = 0b000010
    NEAR = 0b000001
    input_point_1_outcode = assign_parallel_outcode(x1, y1, z1);
    input_point_2_outcode = assign_parallel_outcode(x2, y2, z2);
    while True:
        if input_point_1_outcode & input_point_2_outcode:
            return []
        if not (input_point_1_outcode | input_point_2_outcode):
            # print 'result' , [[x1,y1,z1],[x2,y2,z2]]
            return [[x1, y1, z1], [x2, y2, z2]]
        if input_point_1_outcode:
            outcode = input_point_1_outcode
        else:
            outcode = input_point_2_outcode
        if outcode & RIGHT:
            # Point is on the right of volume
            x = 1
            y = (y2 - y1) * (1 - x1) / (x2 - x1) + y1
            z = (z2 - z1) * (1 - x1) / (x2 - x1) + z1
        elif outcode & LEFT:
            # Point is on the left of volume
            x = -1
            y = (y2 - y1) * (-1 - x1) / (x2 - x1) + y1
            z = (z2 - z1) * (-1 - x1) / (x2 - x1) + z1
        elif outcode & TOP:
            # Point is on above the volume
            x = (x2 - x1) * (1 - y1) / (y2 - y1) + x1
            y = 1
            z = (z2 - z1) * (1 - y1) / (y2 - y1) + z1
        elif outcode & BOTTOM:
            # Point is below the volume
            x = (x2 - x1) * (-1 - y1) / (y2 - y1) + x1
            y = -1
            z = (z2 - z1) * (-1 - y1) / (y2 - y1) + z1
        elif outcode & FAR:
            x = (x2 - x1) * (1 - z1) / (z2 - z1) + x1
            y = (y2 - y1) * (1 - z1) / (z2 - z1) + y1
            z = 1
        elif outcode & NEAR:
            x = (x2 - x1) * (-z1) / (z2 - z1) + x1
            y = (y2 - y1) * (-z1) / (z2 - z1) + y1
            z = 0
        if outcode == input_point_1_outcode:
            x1 = x
            y1 = y
            z1 = z
            input_point_1_outcode = assign_parallel_outcode(x1, y1, z1)
        else:
            x2 = x
            y2 = y
            z2 = z
            input_point_2_outcode = assign_parallel_outcode(x2, y2, z2)

# Testing the clipping function
if __name__ == '__main__':
    p1=[0.1, 0.1,-0.5]
    p2=[0.2,0.1,1.5]
    print(clip_line_parallel(p1, p2))
