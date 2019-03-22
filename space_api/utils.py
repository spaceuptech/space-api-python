def generate_find(condition):
    if condition.type == 'and':
        d = {}
        for clause in condition.clauses:
            d.update(generate_find(clause))
        return d
    elif condition.type == 'or':
        new_conditions = map(generate_find, condition.clauses)
        return {'$or': new_conditions}
    elif condition.type == 'cond':
        if condition.op == "==":
            return {condition.f1: condition.f2}
        elif condition.op == ">":
            return {condition.f1: {"$gt": condition.f2}}
        elif condition.op == "<":
            return {condition.f1: {"$lt": condition.f2}}
        elif condition.op == ">=":
            return {condition.f1: {"$gte": condition.f2}}
        elif condition.op == "<=":
            return {condition.f1: {"$lte": condition.f2}}
        elif condition.op == "!=":
            return {condition.f1: {"$ne": condition.f2}}
        elif condition.op == "in":
            return {condition.f1: {"$in": condition.f2}}
        elif condition.op == "notIn":
            return {condition.f1: {"$nin": condition.f2}}


def AND(*conditions):
    return {'type': 'and', 'clauses': conditions}


def COND(f1, op, f2):
    return {'type': 'cond', 'f1': f1, 'op': op, 'f2': f2}


def OR(*conditions):
    return {'type': 'or', 'clauses': conditions}
