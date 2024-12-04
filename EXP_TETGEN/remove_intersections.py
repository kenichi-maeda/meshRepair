import re

def parse_tetgen_log(log_file):
    """
    Parse the TetGen log to extract vertices from grouped warnings about self-intersections.
    """
    vertices_to_remove = set()
    
    with open(log_file, 'r', encoding='utf-16') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Case 1: A segment and a facet intersect
        if "Warning:  A segment and a facet intersect." in line:
            segment_match = re.search(r"segment: \[(\d+),(\d+)\]", lines[i + 1])
            facet_match = re.search(r"facet triangle: \[(\d+),(\d+),(\d+)\]", lines[i + 2])
            
            if segment_match:
                vertices_to_remove.update(map(int, segment_match.groups()))
            if facet_match:
                vertices_to_remove.update(map(int, facet_match.groups()))
            
            i += 3  # Skip the next two lines (segment and facet)
        
        # Case 2: Two facets exactly intersect
        elif "Warning:  Two facets exactly intersect." in line:
            facet1_match = re.search(r"1st facet triangle: \[(\d+),(\d+),(\d+)\]", lines[i + 1])
            facet2_match = re.search(r"2nd facet triangle: \[(\d+),(\d+),(\d+)\]", lines[i + 2])
            
            if facet1_match:
                vertices_to_remove.update(map(int, facet1_match.groups()))
            if facet2_match:
                vertices_to_remove.update(map(int, facet2_match.groups()))
            
            i += 3  # Skip the next two lines (1st facet and 2nd facet)
        
        else:
            i += 1  # Move to the next line if no match"""

    return vertices_to_remove


def process_ply_file(ply_file, output_ply_file, vertices_to_remove):
    """
    Process the PLY file to remove vertices and update faces.
    """
    vertices = []
    faces = []
    vertex_indices_map = {}

    with open(ply_file, 'r') as f:
        lines = f.readlines()

    # Identify the vertex and face sections in the PLY file
    header = []
    vertex_count = 0
    face_count = 0
    in_vertex_section = False
    in_face_section = False
    for line in lines:
        if line.startswith("element vertex"):
            vertex_count = int(line.split()[-1])
            header.append(line)
        elif line.startswith("element face"):
            face_count = int(line.split()[-1])
            header.append(line)
        elif line.strip() == "end_header":
            header.append(line)
            break
        else:
            header.append(line)

    # Read vertices
    vertex_start_index = len(header)
    for i in range(vertex_start_index, vertex_start_index + vertex_count):
        vertex_line = lines[i].strip()
        vertices.append(vertex_line)

    # Read faces
    face_start_index = vertex_start_index + vertex_count
    for i in range(face_start_index, face_start_index + face_count):
        face_line = lines[i].strip()
        faces.append(face_line)

    # Remove problematic vertices and remap indices
    new_vertices = []
    for i, vertex in enumerate(vertices):
        if i not in vertices_to_remove:
            vertex_indices_map[i] = len(new_vertices)
            new_vertices.append(vertex)

    # Update faces to exclude references to removed vertices
    new_faces = []
    for face in faces:
        parts = list(map(int, face.split()))
        vertex_indices = parts[1:]
        if all(v in vertex_indices_map for v in vertex_indices):
            remapped_face = [len(vertex_indices)] + [vertex_indices_map[v] for v in vertex_indices]
            new_faces.append(" ".join(map(str, remapped_face)))

    # Write the new PLY file
    with open(output_ply_file, 'w') as f:
        f.writelines(header)
        f.writelines(f"{vertex}\n" for vertex in new_vertices)
        f.writelines(f"{face}\n" for face in new_faces)


# Example Usage
log_file = "log.txt"
input_ply_file = "before.ply"
output_ply_file = "tetgen_removal.ply"

vertices_to_remove = parse_tetgen_log(log_file)
process_ply_file(input_ply_file, output_ply_file, vertices_to_remove)
