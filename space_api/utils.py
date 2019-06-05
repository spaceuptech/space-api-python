def generate_find(condition: dict) -> dict:
    if condition.get('type') == 'and':
        d = {}
        for clause in condition.get('clauses'):
            generated = generate_find(clause)
            if clause.get('type') == 'cond':
                if clause.get('f1') not in d:
                    d.update(generated)
                else:
                    d[clause.get('f1')].update(generated[clause.get('f1')])
            else:
                d.update(generated)
        return d
    elif condition.get('type') == 'or':
        new_conditions = []
        for clause in condition.get('clauses'):
            new_conditions.append(generate_find(clause))
        return {'$or': new_conditions}
    elif condition.get('type') == 'cond':
        if condition.get('op') == "==":
            return {condition.get('f1'): condition.get('f2')}
        elif condition.get('op') == ">":
            return {condition.get('f1'): {"$gt": condition.get('f2')}}
        elif condition.get('op') == "<":
            return {condition.get('f1'): {"$lt": condition.get('f2')}}
        elif condition.get('op') == ">=":
            return {condition.get('f1'): {"$gte": condition.get('f2')}}
        elif condition.get('op') == "<=":
            return {condition.get('f1'): {"$lte": condition.get('f2')}}
        elif condition.get('op') == "!=":
            return {condition.get('f1'): {"$ne": condition.get('f2')}}
        elif condition.get('op') == "in":
            return {condition.get('f1'): {"$in": condition.get('f2')}}
        elif condition.get('op') == "notIn":
            return {condition.get('f1'): {"$nin": condition.get('f2')}}


def AND(*conditions) -> dict:
    return {'type': 'and', 'clauses': conditions}


def COND(f1: str, op: str, f2: str) -> dict:
    return {'type': 'cond', 'f1': f1, 'op': op, 'f2': f2}


def OR(*conditions) -> dict:
    return {'type': 'or', 'clauses': conditions}
