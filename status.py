from db_conn import get_db_connection

def get_status():
    qualities = get_db_connection().execute(
        'SELECT water_quality, dispenser_quality, filter_quality'
        ' FROM quality'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    water = get_db_connection().execute(
        'SELECT temperature, preparation_date'
        ' FROM water'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    dispenser = get_db_connection().execute(
        'SELECT fill_value'
        ' FROM dispenser'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    water_consumption = get_db_connection().execute(
        'SELECT consumption'
        ' FROM water_consumption'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if qualities is None or water is None or dispenser is None or water_consumption is None:
        return {'status': 'Query failed'}
    
    return {
        'data': {
            'qualities': {
                'water_quality' : qualities['water_quality'],
                'dispenser_quality' : qualities['dispenser_quality'],
                'filter_quality' : qualities['filter_quality'],
            },
            'water': {
                'temperature': water['temperature'],
                'preparation_date': water['preparation_date'],
            },
            'dispenser': {
                'fill_value': dispenser['fill_value'],
            },
            'water_consumption': {
                'consumption': water_consumption['consumption'],
            }
        }
    }
    