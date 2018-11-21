
def get_julian_day_from_scene_id(scene_id):
  return int(scene_id[13:16])

def criteria(scene_id, start_pos_rain):
    julian_day = get_julian_day_from_scene_id(scene_id)
    key = julian_day - start_pos_rain

    if key < 0:
        key += 150
    return key

def sort(raster_paths):
    return sorted(raster_paths, key=lambda raster: raster['order_id'], reverse=True)