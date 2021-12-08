import os
import re
from ete3 import Tree, TreeStyle, TextFace, TreeFace, NodeStyle

def get_max_MAE(t_node, max_MAE, max_route):
    mae = 0
    if len(t_node.get_children()) == 0:
        mae = t_node.dist
        if mae > max_MAE:
            max_MAE = mae
            max_route = t_node.name
        return [max_MAE, max_route]
    
    for i in range(len(t_node.get_children())):
        child_name = t_node.get_children()[i].name
        max_MAE, max_route = get_max_MAE(t_node.get_children()[i], max_MAE, max_route)
    
    return [max_MAE, max_route]
    
def get_min_MAE(t_node, min_MAE, min_route):
    mae = 0
    if len(t_node.get_children()) == 0:
        mae = t_node.dist
        if mae < min_MAE:
            min_MAE = mae
            min_route = t_node.name
        return [min_MAE, min_route]
    
    for i in range(len(t_node.get_children())):
        child_name = t_node.get_children()[i].name
        min_MAE, min_route = get_min_MAE(t_node.get_children()[i], min_MAE, min_route)
    
    return [min_MAE, min_route]
    
def get_MAE(line):
    global count, s
    pattern = re.compile(r"\[[\d]+[\.]?[\d]*[Ee]?[+-]?[\d]*\]")
    l = pattern.findall(line)
    if len(l) != 0:
        mae = float(l[0].strip('[').strip(']'))
        count += 1
        s += mae
        mae -= 0.3
    else:
        mae = 0
    return mae

def find_route_line(lines, route):
    for line in lines:
        if route in line:
            return line
    
def get_log_name(path):
    filenames = os.listdir(path)
    pattern = re.compile(r".log")
    log_names_list = []
    
    for filename in filenames:
        if pattern.search(filename) is not None:
            log_names_list.append(filename)
    
    return log_names_list

def get_lines(path):
    with open(path, "r") as f:
        lines = f.readlines()
    return lines
    
def growing(t_node):
    self_name = t_node.name
    if len(self_name) >= 3:
        t_node.add_face(TextFace(t_node.name, fsize = 2), column=0, position = "branch-top")
    if len(self_name) == 1:
        return t_node
        
    for x in self_name:
        child_name = self_name.replace(x, '')
        child = t_node.add_child(name = child_name)
        child = growing(child)
        
    return t_node
    
def new_tree():
    t = Tree(name = 'EGPHS')
    t.add_face(TextFace(t.name, fsize = 2), column=0, position = "aligned")
    t = growing(t)
    # print(t.get_ascii(show_internal=True))
    
    style = NodeStyle()
    style["size"] = 0
    t.set_style(style)
    
    return t

def set_leaves_aver(t_node, route, deep, lines1, lines2, color):
    self_name = t_node.name
    new_route = route + '_' + self_name
    line1 = find_route_line(lines1, new_route)
    line2 = find_route_line(lines2, new_route)
    # print(new_route)
    # print(line)
    mae1 = get_MAE(line1)
    mae2 = get_MAE(line2)
    mae = 0
    if mae1 == 0:
        mae = mae2
    elif mae2 == 0:
        mae = mae1
    else:
        mae = (mae1 + mae2)/2
    # print(mae)
    # print('~~~~~~~~~~~~~~~~~~~~~~')
    t_node.dist = 0.05
    
    style = NodeStyle()
    style["size"] = 0
    style["hz_line_color"] = 'Red'
    '''
    if len(self_name) == 1:
        style["hz_line_color"] = color[self_name]
    else:
        style["hz_line_color"] = 'Maroon'
    '''
    style["hz_line_width"] = 0
    
    if len(self_name) == 1:
        leaf = t_node.add_child(name = new_route[1:])
        leaf.set_style(style)
        leaf.dist = mae
        # leaf.add_face(TextFace(new_route[1:], fsize = 3), column=0, position = "aligned")
        return t_node
        
    for i in range(len(t_node.get_children())):
        child_name = t_node.get_children()[i].name
        t_node.get_children()[i] = set_leaves_aver(t_node.get_children()[i], new_route, deep+1, lines1, lines2, color)
    
    extra_branch = t_node.add_child(name = new_route[1:])
    extra_branch.dist = 0.05 * (5 - deep)
    leaf = extra_branch.add_child(name = new_route[1:])
    leaf.set_style(style)
    leaf.dist = mae
    
    return t_node
        
def set_leaves(t_node, route, deep, lines, color):
    self_name = t_node.name
    new_route = route + '_' + self_name
    line = find_route_line(lines, new_route)
    # print(new_route)
    # print(line)
    mae = get_MAE(line)
    # print(mae)
    # print('~~~~~~~~~~~~~~~~~~~~~~')
    t_node.dist = 0.05
    
    style = NodeStyle()
    style["size"] = 0
    style["hz_line_color"] = 'Red'
    '''
    if len(self_name) == 1:
        style["hz_line_color"] = color[self_name]
    else:
        style["hz_line_color"] = 'Maroon'
    '''
    style["hz_line_width"] = 0
    
    if len(self_name) == 1:
        leaf = t_node.add_child(name = new_route[1:])
        leaf.set_style(style)
        leaf.dist = mae
        # leaf.add_face(TextFace(new_route[1:], fsize = 3), column=0, position = "aligned")
        return t_node
        
    for i in range(len(t_node.get_children())):
        child_name = t_node.get_children()[i].name
        t_node.get_children()[i] = set_leaves(t_node.get_children()[i], new_route, deep+1, lines, color)
    
    extra_branch = t_node.add_child(name = new_route[1:])
    extra_branch.dist = 0.05 * (5 - deep)
    leaf = extra_branch.add_child(name = new_route[1:])
    leaf.set_style(style)
    leaf.dist = mae
    
    return t_node
    
def main():
    global count, s
    
    filenames1 = ["02923e5_1_123.log", "02923e5_0_123.log"]
    filenames2 = ["cd43447_0_123.log", "cd43447_1_123.log"]
    filenames3 = ["ff14c38_0_123.log", "ff14c38_1_123.log"]
    filenames4 = ["ff4e437_0_123.log", "ff4e437_1_123.log"]
    data_path = '../data/log/'
    
    color = {'P':'Crimson', 'E':'Orange', 'G':'Violet', 'S':'RoyalBlue', 'H':'PaleGreen'}
    
    count = 0
    s = 0
    lines1 = get_lines(data_path + filenames4[0])
    lines2 = get_lines(data_path + filenames4[1])
    
    root = new_tree()
    root = set_leaves_aver(root, '', 1, lines1, lines2, color)
    aver = print(s/count)
    
    print('max: ', get_max_MAE(root, 0, ''))
    print('min: ', get_min_MAE(root, 1, ''))
    
    width = get_max_MAE(root, 0, '')[0] + 0.25
    
    ts = TreeStyle()
    # ts.mode = 'c'
    ts.show_leaf_name = False
    ts.allow_face_overlap = True
    ts.show_scale = False
    
    root.show(tree_style = ts)
    root.render(filenames4[0][:7]+'_merge_onion.pdf', w=width*200, h=160, units='mm',tree_style=ts)
    # root.render(log_name[:7]+'_onion_color_r.pdf', w=width*200, h=width*200, units='mm',tree_style=ts)
        
'''    
def main():
    global count, s
    data_path = '../data/log/'
    log_names = get_log_name(data_path)
    
    color = {'P':'Crimson', 'E':'Orange', 'G':'Violet', 'S':'RoyalBlue', 'H':'PaleGreen'}
    for i, log_name in enumerate(log_names):
        count = 0
        s = 0
        lines = get_lines(data_path + log_name)
        print(log_name)
        root = new_tree()
        root = set_leaves(root, '', 1, lines, color)
        print(s/count)
        
        width = get_max_MAE(root, 0) + 0.25
        
        ts = TreeStyle()
        # ts.mode = 'c'
        ts.show_leaf_name = False
        ts.allow_face_overlap = True
        ts.show_scale = False
        
        root.show(tree_style = ts)
        root.render(log_name[:9]+'_onion.pdf', w=width*200, h=160, units='mm',tree_style=ts)
        # root.render(log_name[:7]+'_onion_color_r.pdf', w=width*200, h=width*200, units='mm',tree_style=ts)
'''
if __name__ == '__main__':
    main()
