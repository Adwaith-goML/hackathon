class Department:
    def __init__(self, name, mgr):
        self.name = name
        self.mgr = mgr
        self.child = []
 
def get_mgrs(tree, dpt_name):
    dpt_lookup = {}
 
    def build_lookup(node):
        if not node:
            return
        dpt_lookup[node.name] = node
        for child in node.child:
            build_lookup(child)
    build_lookup(tree)
    mgrs = []
    curr_dpt = dpt_lookup.get(dpt_name, None)
    while curr_dpt:
        mgrs.append(curr_dpt.mgr)
        found_parent = False
        for dept in dpt_lookup.values():
            if curr_dpt in dept.child:
                curr_dpt = dept
                found_parent = True
                break
        if not found_parent:
            curr_dpt = None
 
    return mgrs#[::-1] 
 
ceo = Department('CEO', 'Alice')
engineering = Department('Engineering', 'Bob')
sales = Department('Sales', 'Charlie')
backend = Department('Backend', 'David')
frontend = Department('Frontend', 'Eve')
domestic = Department('Domestic', 'Fay')
 
ceo.child = [engineering, sales]
engineering.child = [backend, frontend]
sales.child = [domestic]
 

print(get_mgrs(ceo, 'Backend'))
print(get_mgrs(ceo, 'Sales'))
print(get_mgrs(ceo, 'Engineering')) 
print(get_mgrs(ceo, 'Frontend'))
print(get_mgrs(ceo, 'Domestic')) 