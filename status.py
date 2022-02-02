from db_conn import get_db_connection

def get_status():
    qualities = get_db_connection().execute(
        'SELECT water_quality, dispenser_quality, filter_quality'
        ' FROM quality'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    if qualities is None:
        return {'status': 'Query failed'}
    
    return {
        'data': {
            'qualities': {
                'water_quality' : qualities['water_quality'],
                'dispenser_quality' : qualities['dispenser_quality'],
                'filter_quality' : qualities['dispenser_quality']
            }
        }
    }
    