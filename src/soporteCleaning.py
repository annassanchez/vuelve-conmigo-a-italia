def nivelGeo(columna):
    columna = str(columna)
    if len(columna) == 2 and columna == 'IT':
        return 0
    elif len(columna) == 4 and columna.startswith('IT'):
        return 1
    elif len(columna) == 5 and columna.startswith('IT'):
        return 2
    else:
        return 3

def yearOrMonthlyData(columna):
    columna = str(columna)
    if len(columna) == 4:
        return 'yearly'
    else:
        return 'monthly'