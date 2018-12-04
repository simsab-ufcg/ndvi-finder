
def get_julian_day_from_scene_id(scene_id):
    '''
    Get julian day in scene id.
    '''
    return int(scene_id[13:16])

def get_year_from_scene_id(scene_id):
    '''
    Get year in scene id.
    '''
    return int(scene_id[9:13])

def criteria(scene_id):
    '''
    Take the julian day and return a priority of this scene
    according to the beginning of the post rainy period.
    '''
    return get_year_from_scene_id(scene_id)**2 + get_julian_day_from_scene_id(scene_id)

def sort(raster_paths, cond_reverse = False):
    '''
    Sorts raster paths according to priority.
    '''
    return sorted(raster_paths, key=lambda raster: raster['order_id'], reverse = cond_reverse)