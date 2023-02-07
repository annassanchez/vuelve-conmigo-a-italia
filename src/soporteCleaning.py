def nivelGeo(columna):
    if len(columna) == 2:
        return 0
    elif len(columna) == 4:
        return 1
    elif len(columna) == 5:
        return 2

def yearOrMonthlyData(columna):
    if len(columna) == 4:
        return 'yearly'
    else:
        return 'monthly'