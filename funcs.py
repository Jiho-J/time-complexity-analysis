import ast

# 노트 타입 변환
def change_node_type(node, new_type):
    new_node = new_type()
    new_node.__dict__.update(node.__dict__)
    return new_node


def modify_code(code: str):
    setting_code = ast.Assign(
        targets=[ast.Name(id='operate_count', ctx=ast.Store())],
        value=ast.Constant(value=0),
        lineno=0
    ) # operate_count = 0

    global_code = ast.Global(
        names=['operate_count']
    ) # global operate_count

    inserting_node = ast.AugAssign(
        target=ast.Name(id='operate_count', ctx=ast.Store()),
        op=ast.Add(),
        value=ast.Constant(value=1)
    ) # operate_count += 1

    tree = ast.parse(code) # 코드 파싱

    tree.body.insert(0, setting_code) # 정의 삽입
    
    # 자식 값은 내재되어 있지만, 부모 값은 설정되어 있지 않기에, 추가적으로 설정
    cp_connection = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            cp_connection[str(child)] = node
            
    
    # 노드를 추가하는 함수
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
        # 부모가 있는지 판별, 없으면 넘어감
        try:
            _ = cp_connection[str(node)]
        except KeyError:
            continue
            
        # 각 노드 종류에 따라 다르게 판별
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
