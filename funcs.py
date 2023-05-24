import ast


def change_node_type(node, new_type):
    new_node = new_type()
    new_node.__dict__.update(node.__dict__)
    return new_node


def modify_code(code: str):
    setting_code = ast.Assign(
        targets=[ast.Name(id='operate_count', ctx=ast.Store())],
        value=ast.Constant(value=0),
        lineno=0
    )

    global_code = ast.Global(
        names=['operate_count']
    )

    inserting_node = ast.AugAssign(
        target=ast.Name(id='operate_count', ctx=ast.Store()),
        op=ast.Add(),
        value=ast.Constant(value=1)
    )

    tree = ast.parse(code)

    tree.body.insert(0, setting_code)

    cp_connection = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            cp_connection[str(child)] = node

    def add_node(nod):
        p = cp_connection[str(nod)]
        if not p:
            return -1
        if isinstance(p, ast.If):
            if nod in p.body:
                p.body.insert(p.body.index(nod), inserting_node)
            elif nod in p.orelse:
                p.orelse.insert(p.orelse.index(nod), inserting_node)
        else:
            p.body.insert(p.body.index(nod), inserting_node)

    for node in ast.walk(tree):
        try:
            _ = cp_connection[str(node)]
        except KeyError:
            continue

        if isinstance(node, ast.FunctionDef):
            node.body.insert(0, global_code)
        if isinstance(node, ast.Return) or isinstance(node, ast.If) or isinstance(node, ast.Expr):
            add_node(node)
        if isinstance(node, ast.Assign):
            if isinstance(node.targets[0], ast.Name) and not node.targets[0].id == 'operate_count':
                add_node(node)
        if isinstance(node, ast.AugAssign):
            if not (node.target.id == 'operate_count'):
                add_node(node)

    modified_code = ast.unparse(tree)
    return modified_code
