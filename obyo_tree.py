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
        if mae < min_MAE and mae != 0:
            min_MAE = mae
            min_route = t_node.name
        return [min_MAE, min_route]
    
    for i in range(len(t_node.get_children())):
        child_name = t_node.get_children()[i].name
        min_MAE, min_route = get_min_MAE(t_node.get_children()[i], min_MAE, min_route)
    
    return [min_MAE, min_route]
    
def get_MAE(line):
    pattern = re.compile(r"\[[\d]+[\.]?[\d]*[Ee]?[+-]?[\d]*\]")
    l = pattern.findall(line)
    if len(l) != 0:
        mae = float(l[0].strip('[').strip(']'))
    else:
        mae = 0
    return mae

def find_route_line(lines, route):
    st = '1by1_init_randomly'+route+' '
    for line in lines:
        if st in line:
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
    
def growing(t_node, route, deep):
    global dataset
    if deep == 5:
        return t_node
        
    for x in dataset:
        if x not in route:
            child = t_node.add_child(name = x)
            if deep < 1:
                child.add_face(TextFace(child.name, fsize = 2), column=0, position = "branch-top")
            child = growing(child, route+'_'+x, deep+1)
        
    return t_node
    
def new_tree():
    t = Tree(name = 'root')
    # t.add_face(TextFace(t.name, fsize = 2), column=0, position = "aligned")
    t = growing(t, '', 0)
    # print(t.get_ascii(show_internal=True))
    
    style = NodeStyle()
    style["size"] = 0
    t.set_style(style)
    
    return t

def set_leaves_aver(t_node, route, deep):
    global count, s
    global lines1, lines2
    self_name = t_node.name
    if self_name != 'root':
        new_route = route + '_' + self_name
        line1 = find_route_line(lines1, new_route)
        line2 = find_route_line(lines2, new_route)
        if line1 != None:
            mae1 = get_MAE(line1)
        else:
            mae1 = 0
        if line2 != None:
            mae2 = get_MAE(line2)
        else:
            mae2 = 0
            
        mae = 0
        if mae1 == 0:
            mae = mae2
        elif mae2 == 0:
            mae = mae1
        else:
            mae = (mae1 + mae2)/2
        if mae != 0:
            mae -= 0.3
        # print(mae)
        # print('~~~~~~~~~~~~~~~~~~~~~~')
        t_node.dist = 0.05
        
        style = NodeStyle()
        style["size"] = 0
        style["hz_line_color"] = 'Red'
        style["hz_line_width"] = 0
        
        if deep == 6:
            leaf = t_node.add_child(name = new_route[1:])
            leaf.set_style(style)
            if mae != 0:
                count += 1
                s['all'] += mae
                c[new_route[1]] += 1
            leaf.dist = mae
            s[new_route[1]] += mae
            # leaf.add_face(TextFace(new_route[1:], fsize = 3), column=0, position = "aligned")
            return t_node
            
        for i in range(len(t_node.get_children())):
            child_name = t_node.get_children()[i].name
            t_node.get_children()[i] = set_leaves_aver(t_node.get_children()[i], new_route, deep+1)
        '''
        extra_branch = t_node.add_child(name = new_route[1:])
        extra_branch.dist = 0.05 * (6 - deep)
        leaf = extra_branch.add_child(name = new_route[1:])
        leaf.set_style(style)
        leaf.dist = mae
        '''
    else:
        style = NodeStyle()
        style["hz_line_color"] = '#ffffff'
        style["vt_line_color"] = '#ffffff'
        t_node.dist = 0.05
        for i in range(len(t_node.get_children())):
            child_name = t_node.get_children()[i].name
            t_node.get_children()[i] = set_leaves_aver(t_node.get_children()[i], '', deep+1)
        t_node.set_style(style)
    
    return t_node
    
def set_empty_leaves(t_node, aver):
    if t_node.dist == 0:
        style = NodeStyle()
        style["size"] = 0
        style["hz_line_color"] = 'Red'
        style["hz_line_width"] = 0
        t_node.set_style(style)
        t_node.dist = aver
        return t_node
    else:
        for i in range(len(t_node.get_children())):
            t_node.get_children()[i] = set_empty_leaves(t_node.get_children()[i], aver)
    return t_node
    
def main():
    global count, s, c, dataset, lines1, lines2
    
    filenames = ["a367e11_0_123.log", "a367e11_1_123.log"]
    data_path = '../data/log/'
    
    dataset = ['E', 'G', 'P', 'H', 'S']
    color = {'P':'Crimson', 'E':'Orange', 'G':'Violet', 'S':'RoyalBlue', 'H':'PaleGreen'}
    
    count = 0
    s = {'all': 0, 'E': 0, 'G': 0, 'P': 0, 'H': 0, 'S': 0}
    c = {'all': 0, 'E': 0, 'G': 0, 'P': 0, 'H': 0, 'S': 0}
    lines1 = get_lines(data_path + filenames[0])
    lines2 = get_lines(data_path + filenames[1])
    
    root = new_tree()
    root = set_leaves_aver(root, '', 1)
    
    aver = s['all'] / count
    print(count)
    print(s)
    print(c)
    for key in dataset:
        aver_each = s[key] / c[key]
        print(f"{key}'s aver: {aver_each}")
    
    print('aver: ', aver)
    print('max: ', get_max_MAE(root, 0, ''))
    print('min: ', get_min_MAE(root, 2, ''))
    
    root = set_empty_leaves(root, aver)
    
    width = get_max_MAE(root, 0, '')[0] + 0.25
    
    ts = TreeStyle()
    ts.show_leaf_name = False
    ts.allow_face_overlap = True
    ts.show_scale = False
    
    root.show(tree_style = ts)
    root.render(filenames[0][:7]+'_merge_onion.pdf', w=width*200, units='mm',tree_style=ts)
    # root.render(log_name[:7]+'_onion_color_r.pdf', w=width*200, h=width*200, units='mm',tree_style=ts)
   
if __name__ == '__main__':
    main()
