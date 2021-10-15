import sys
import timeit

class Face:
    def __init__(self,v1_,v2_,v3_):
        self.v1 = v1_
        self.v2 = v2_
        self.v3 = v3_
    def __eq__(other):
        return (self.v1 == other.v1 and self.v2 == other.v2 and self.v3 == other.v3)
    def get_vertex_list(self,all_vertices):
        ans = "f " + str(all_vertices[self.v1.format_vertex()]) + " " + str(all_vertices[self.v2.format_vertex()]) + " " + str(all_vertices[self.v3.format_vertex()])
        return (ans)
class Vertex:
    def __init__(self, p1_,p2_,p3_):
        self.p1 = p1_
        self.p2 = p2_
        self.p3 = p3_
    def __eq__(other):
        return (float(self.p1) == float(other.p1) and float(self.p2) == float(other.p2) and float(self.p3) == float(other.p3))
    def format_vertex(self):
        return str(self.p1) + " " + str(self.p2) + " " + str(self.p3)
def main():
    file1 = open("stl_file.stl",'r')
    outfile = open("obj_file.obj",'w')
    lines = file1.readlines()
    all_faces = []
    this_face = []
    all_vertices = {}
    vertex_num = 1
    look_for_vertex = False
    for line in lines:
        #print(line)
        if "endloop" in line:
            all_faces.append(Face(this_face[0],this_face[1],this_face[2]))
            this_face = []
            look_for_vertex = False
        if look_for_vertex:
            new_vertex = process_line(line)
            this_face.append(new_vertex)
            vertex_string = new_vertex.format_vertex()
            in_dict = False
            for current in all_vertices:
                if current == vertex_string:
                    in_dict = True
                    break
            if not in_dict:
                all_vertices[vertex_string] = vertex_num
                vertex_num+=1
        if "outer loop" in line:
            look_for_vertex = True
    print(vertex_num-1)
    for current in all_vertices:
        #print (all_vertices[current])
        #print (current)
        outfile.write("v " + current + "\n")
    new_line = ""
    for face in all_faces:
        #print(face.v1.format_vertex() + " | " + face.v2.format_vertex() + " | " + face.v3.format_vertex())
        outfile.write(new_line+face.get_vertex_list(all_vertices))
        new_line = "\n"
    return (vertex_num+len(all_faces))
def simplify_sn(sn_val):
    sn_val_split = sn_val.split("e")
    mantissa = float(sn_val_split[0])
    exp = int(sn_val_split[1])
    real_val = round(mantissa**exp,6)
    return real_val
def process_line(full_line):
    split_line = full_line.split(" ")
    point_list = []
    for val in split_line:
        if "vertex" == val or len(val) == 0:
            continue
        real_val = -1.0
        if "e" in val:
            real_val = str(simplify_sn(val))
        else:
            real_val = str(float(val))
        point_list.append(real_val)
    this_vertex = Vertex(point_list[0],point_list[1],point_list[2])
    return this_vertex

start = timeit.default_timer()
things_written = main()
stop = timeit.default_timer()
execution_time = stop - start
print("Time/(Vertices+Faces): "+str(execution_time/things_written))
