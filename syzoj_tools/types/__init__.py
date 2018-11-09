problem_types = None

def load_types():
    global problem_types
    if problem_types == None:
        from .traditional import ProblemTraditional
        problem_types = {
            "traditional": ProblemTraditional
        }

def get_type(name):
    global problem_types
    load_types()
    return problem_types.get(name)
