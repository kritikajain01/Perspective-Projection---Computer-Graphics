# Jain, Kritika
# 1002-093-381
# 2017-10-25
# Assignment_04_03

import numpy
import math
import copy
import Jain_04_04


class cl_world:
    def __init__(self, objects=[], canvases=[]):
        self.objects = objects
        self.canvases = canvases
        # variables are initialized
        self.vertexes = []
        self.faces = []
        self.current_camera_array = [self.Camera()] # this hold data about all cameras, the first cam is created as default
        self.read_camera_file()
        self.current_camera = self.current_camera_array[0]  # this hold data about the current cam
        self.viewport = self.current_camera.camera_viewport
        self.window = [-1,-1,1,1]


    class Camera: # camera class with the default values
        camera_name = ""
        camera_type = "parallel"
        VRP = [0, 0, 0]
        VPN = [0, 0, 1]
        VUP = [0, 1, 0]
        PRP = [0, 0, 1]
        VRC = [-1, 1, -1, 1, -1, 1]
        camera_viewport = [0.1, 0.1, 0.4, 0.4]



    def add_canvas(self, canvas):
        self.canvases.append(canvas)
        canvas.world = self


    def map_to_viewport(self,point,viewport,window):
        if point != []:
            for i in range(0,2):
                point[i] = (point[i]*(viewport[i+2] - viewport[i])/(window[i+2]-window[i])+ (viewport[i+2]+viewport[i])/2)
        return point

    def map_to_volume(self, vertexes, volume):
        vertexes = copy.deepcopy(vertexes)
        for point in vertexes:
            for i in range(0, 3):
                point[i] = (point[i] / (volume[i + 1] - volume[i])) # + ( volume[i + 1] + volume[i]) / 2)
        return vertexes

    def map_XY(self, point):
        result =[]
        if point!= []:
            result=[point[0],point[1]] # projecting to xy
        else:
            result.append(None)

        return result


    def map_to_window(self, point, window, canvas):
        if point != []:
            point[0] = int(int(canvas.cget("width"))*((point[0]*(window[2]-window[0]) +(window[2]+window[0])/2)/(window[2]-window[0])))
            point[1] = int(int(canvas.cget("height")) * (((point[1])*(window[3]-window[1])+(window[3]+window[1])/2)/(window[3]-window[1]))) ##cget("height"))-
        return point

    def project_parralel(self,vertexes):
        # vertexes = copy.deepcopy(vertexes)
        o = numpy.asarray(self.current_camera.VRP)
        n = numpy.asarray(self.current_camera.VPN)
        u = numpy.asarray(self.current_camera.VUP)
        new_vertexes = []
        p = numpy.asarray(self.current_camera.PRP)
        matrix = [-numpy.cross(u, n), u, n] / numpy.sqrt(
            numpy.dot(numpy.cross(u, n), numpy.cross(u, n)))
        matrix1 = [numpy.cross(u, -(p - o)) / numpy.sqrt(
            numpy.dot(numpy.cross(u, p - o),
                      numpy.cross(u, p - o))), u,
                   -(p - o)]
        matrix2 = [[-2, 0, 0], [0, 2, 0], [0, 0, 0]]
        for point in vertexes:
            if point != []:
                numpy.asarray(point)
                point = numpy.dot(numpy.dot(numpy.dot(point - o, matrix), matrix1), matrix2) + o
                new_vertexes.append(point)
        return new_vertexes








    def prepare_port_view(self, polynom , canvas, window):
        polynom1 = [0,0,0,0]
        polynom1[0] = int(int(canvas.cget("width"))* polynom[0] )
        polynom1[1] = int(int(canvas.cget("height"))*polynom[1] )
        polynom1[2] = int(int(canvas.cget("width")) * polynom[2] )
        polynom1[3] = int(int(canvas.cget("height")) * polynom[3] )
        result = [polynom1[0],polynom1[1],polynom1[2],polynom1[1],polynom1[2],polynom1[3],polynom1[0],polynom1[3]]
        return result


    def create_graphic_objects(self, canvas):
        vertexes = copy.deepcopy(self.vertexes)
        vertexes = self.project_parralel(vertexes)  # data is projected and mapped to volume
        vertexes = self.map_to_volume(vertexes,self.current_camera.VRC)
        viewport_frame = self.prepare_port_view(self.viewport, canvas,self.window)
        self.objects = []
        self.objects.append(canvas.create_polygon(viewport_frame, fill="white", outline='black'))
        canvas.itemconfigure(self.objects[0], state='normal')
        if True:
            for face in self.faces:
                # all the polys are constructed
                self.objects.append(canvas.create_polygon([vertexes[face[0] - 1][0],vertexes[face[0] - 1][1],
                                                           vertexes[face[1] - 1][0],vertexes[face[1] - 1][1],
                                                           vertexes[face[2] - 1][0],vertexes[face[2] - 1][1]],
                                                           fill="red", outline='black'))
                
                # if at least 2 point of the poly is in the volume then the poly is drawn
                k = 0
                if Jain_04_04.clip_line_parallel(vertexes[face[0] - 1], vertexes[face[1] - 1]) != [] :
                    k=k+1
                if Jain_04_04.clip_line_parallel(vertexes[face[1] - 1],vertexes[face[2] - 1]) != [] :
                    k = k+1
                if Jain_04_04.clip_line_parallel(vertexes[face[2] - 1],vertexes[face[0] - 1]) != []:
                    k = k+1
                if k> 1:
                    if Jain_04_04.clip_line_parallel(vertexes[face[0] - 1], vertexes[face[1] - 1]) != []:
                        point1, point2 = Jain_04_04.clip_line_parallel(vertexes[face[0] - 1], vertexes[face[1] - 1])
                    if Jain_04_04.clip_line_parallel(vertexes[face[1] - 1],vertexes[face[2] - 1]) != []:
                        point2, point3 = Jain_04_04.clip_line_parallel(vertexes[face[1] - 1], vertexes[face[2] - 1])
                    if Jain_04_04.clip_line_parallel(vertexes[face[2] - 1],
                                                                      vertexes[face[0] - 1]) != []:
                        point3, point1 = Jain_04_04.clip_line_parallel(vertexes[face[2] - 1], vertexes[face[0] - 1])
                    # print(point1)
                    point1 = self.map_to_viewport(point1, self.viewport, self.window)
                    point3 = self.map_to_viewport(point3, self.viewport, self.window)
                    point2 = self.map_to_viewport(point2, self.viewport, self.window)
                    point1 = self.map_to_window(point1,self.window, canvas)
                    point3 = self.map_to_window(point3,self.window, canvas)
                    point2 = self.map_to_window(point2,self.window, canvas)
                    point1 = self.map_XY(point1)
                    point3 = self.map_XY(point3)
                    point2 = self.map_XY(point2)
                    new_coords = [point1[0], point1[1],
                                  point3[0], point3[1],
                                  point2[0], point2[1]]

                    canvas.coords(self.objects[self.faces.index(face)+1], new_coords)
                    canvas.itemconfigure(self.objects[self.faces.index(face)+1],  state='normal')
                else:
                    canvas.itemconfigure(self.objects[self.faces.index(face)+1], state='hidden')

    def redisplay(self, canvas, ):
            if self.objects !=[]:
                viewport_frame = self.prepare_port_view(self.viewport, canvas, self.window)
                canvas.coords(self.objects[0], viewport_frame )
            vertexes = copy.deepcopy(self.vertexes)
            vertexes = self.project_parralel(vertexes)
            vertexes = self.map_to_volume(vertexes, self.current_camera.VRC)
            for face in self.faces:
                # if the points are in the volume space (cliping)
                # if atleast 2 point of the poly is in the volume then the poly is drawn
                k = 0
                if Jain_04_04.clip_line_parallel(vertexes[face[0] - 1], vertexes[face[1] - 1]) != []:
                    k = k + 1
                if Jain_04_04.clip_line_parallel(vertexes[face[1] - 1], vertexes[face[2] - 1]) != []:
                    k = k + 1
                if Jain_04_04.clip_line_parallel(vertexes[face[2] - 1], vertexes[face[0] - 1]) != []:
                    k = k + 1
                if k > 1:
                    if Jain_04_04.clip_line_parallel(vertexes[face[0] - 1], vertexes[face[1] - 1]) != []:
                        point1, point2 = Jain_04_04.clip_line_parallel(vertexes[face[0] - 1],
                                                                               vertexes[face[1] - 1])
                    if Jain_04_04.clip_line_parallel(vertexes[face[1] - 1], vertexes[face[2] - 1]) != []:
                        point2, point3 = Jain_04_04.clip_line_parallel(vertexes[face[1] - 1],
                                                                               vertexes[face[2] - 1])
                    if Jain_04_04.clip_line_parallel(vertexes[face[2] - 1],
                                                             vertexes[face[0] - 1]) != []:
                        point3, point1 = Jain_04_04.clip_line_parallel(vertexes[face[2] - 1],
                                                                               vertexes[face[0] - 1])
                    point1 = self.map_to_viewport(point1, self.viewport, self.window)  # if the poly should be drawn it
                    point3 = self.map_to_viewport(point3, self.viewport, self.window)  # is projected to the viewport
                    point2 = self.map_to_viewport(point2, self.viewport, self.window)  # and then projected to XY
                    point1 = self.map_to_window(point1, self.window, canvas)
                    point3 = self.map_to_window(point3, self.window, canvas)
                    point2 = self.map_to_window(point2, self.window, canvas)
                    point1 = self.map_XY(point1)
                    point3 = self.map_XY(point3)
                    point2 = self.map_XY(point2)
                    new_coords = [point1[0], point1[1],
                                  point3[0], point3[1],
                                  point2[0], point2[1]]

                    canvas.coords(self.objects[self.faces.index(face) + 1], new_coords)
                    canvas.itemconfigure(self.objects[self.faces.index(face) + 1], state='normal')
                else:  # else it is hidden
                    canvas.itemconfigure(self.objects[self.faces.index(face) + 1], state='hidden')

    def rotate(self, angle, start_point, end_point, vertexes_original):

        def rotation_matrix(vector, theta):  # rotation matrix constructed here
            vector = numpy.asarray(vector)
            vector = vector / math.sqrt(numpy.dot(vector, vector))
            a = math.cos(theta / 2.0)
            b, c, d = -vector * math.sin(theta / 2.0)
            aa, bb, cc, dd = a * a, b * b, c * c, d * d
            bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
            return numpy.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                                 [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                                 [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

        vertexes = copy.deepcopy(vertexes_original[:])
        vector = [0, 0, 0]
        for i in range(3):
            vector[i] = float(end_point[i]) - float(start_point[i]) # vector for rotation constructed
        vectro_length = (vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2) ** (0.5) # vector length
        for i in range(3):  # vector normalized
            vector[i] = vector[i] / (vectro_length)
        vertexes1 =[]
        angle = angle * math.pi/180
        for vertex in vertexes:  # rotation is made as multiplication of matrices
            vertex1 = numpy.dot(rotation_matrix(vector, angle),vertex)
            vertexes1.append(vertex1)
        return vertexes1

    def translate_vector(self, translate, vertexes_original :list):
        vertexes = copy.deepcopy(vertexes_original[:])
        for vertex in vertexes:
            for i in range(3):  # translation
                vertex[i] = vertex[i] + translate[i]
        return vertexes

    def scale(self, vector, scale, vertexes_original): 
        vertexes = copy.deepcopy(vertexes_original[:])
        for vertex in vertexes:  # and shift
            for i in range(3):  # first we subtract the point
                vertex[i] = vertex[i] - vector[i]
        scale_matrix = [[scale[0], 0, 0], [0, scale[1], 0], [0, 0, scale[2]]]  # scaling matrix
        vertexes1 = []
        for vertex in vertexes:
            vertex1 = numpy.dot(scale_matrix, vertex)
            vertexes1.append(vertex1)
        for vertex in vertexes1:
            for i in range(3):  # and then we add it (after scale)
                vertex[i] = vertex[i] + vector[i]
        return vertexes1

    def read_camera_file(self): # reads camera file on start
        number_of_cameras = -1
        with open("cameras.txt") as f:
            file_lines = f.readlines()
        file_lines = [x.strip() for x in file_lines]
        for line in file_lines:
            if line[0] == "c":
                number_of_cameras += 1
                self.current_camera_array[number_of_cameras] = self.Camera()
            if line[0] == "i":
                self.current_camera_array[number_of_cameras].camera_name = prepare_data(line, type="str")
            if line[0] == "t":
                self.current_camera_array[number_of_cameras].camera_type = prepare_data(line,type="str")
            if line[0] == "r":
                self.current_camera_array[number_of_cameras].VRP = prepare_data(line,type="float")
            if line[0] == "n":
                self.current_camera_array[number_of_cameras].VPN = prepare_data(line,type="float")
            if line[0] == "u":
                self.current_camera_array[number_of_cameras].VUP = prepare_data(line,type="float")
            if line[0] == "p":
                self.current_camera_array[number_of_cameras].PRP = prepare_data(line,type="float")
            if line[0] == "s":

                self.current_camera_array[number_of_cameras].camera_viewport = prepare_data(line,type="float")

            if line[0] == "w":
                self.current_camera_array[number_of_cameras].VRC = prepare_data(line, type="float")

        # viewport_frame = self.prepare_port_view(self.viewport, self.canvas, self.window)

        # self.objects = []
        # self.objects.append(self.canvas.create_polygon(viewport_frame, fill="white", outline='black'))
        # self.canvas.itemconfigure(self.objects[0], state='normal')


def prepare_data(str, type="int"):  #unnecessary parts of string are removed
    a_list = str.split()
    a_list.pop(0)
    for i in a_list:
        if type == "int":
            a_list[a_list.index(i)] = int(a_list[a_list.index(i)])
        if type == "float":
            a_list[a_list.index(i)] = float(a_list[a_list.index(i)])
        if type =="str":
            pass
    return a_list


# Referred to this video (https://www.youtube.com/watch?v=I8o4kK9QRL4) for rotational matrix and parallel projection
