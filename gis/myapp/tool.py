import requests
import polyline

class RoutingTool:
    OSRM_URL = "http://router.project-osrm.org/route/v1"
    def __init__(self):
        pass
    def get_route(self, start_lat, start_lng, end_lat, end_lng, mode='driving'):
        try:
            s_lat, s_lng = float(start_lat), float(start_lng)
            e_lat, e_lng = float(end_lat), float(end_lng)
        except ValueError:
            return {'error': 'Tọa độ lỗi.'}
        osrm_mode_map = {
            'driving': 'driving', 
            'cycling': 'bike', 
            'walking': 'foot'
        }
        osrm_profile = osrm_mode_map.get(mode, 'driving')
        coords = f"{s_lng},{s_lat};{e_lng},{e_lat}"
        url = f"{self.OSRM_URL}/{osrm_profile}/{coords}"    
        params = {
            'overview': 'full', 
            'geometries': 'polyline', 
            'steps': 'true',
            'alternatives': 'true' 
        }       
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
