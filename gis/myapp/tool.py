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
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            data = response.json()
            if response.status_code == 200 and data.get('code') == 'Ok':
                routes_result = []                
                speeds = {
                    'walking': 5, 
                    'cycling': 30, 
                    'driving': 40  
                }
                speed_kmh = speeds.get(mode, 40)
                for index, route in enumerate(data['routes']):
                    distance_km = route['distance'] / 1000              
                    duration_min = round((distance_km / speed_kmh) * 60)
                    if duration_min < 1: duration_min = 1
                    summary_name = ""
                    if route.get('legs') and len(route['legs']) > 0:
                         summary_name = route['legs'][0].get('summary', '')             
                    if not summary_name:
                        summary_name = f"Tuyến đường {index + 1}"
                    routes_result.append({
                        'id': index,
                        'summary': summary_name,
                        'distance_km': round(distance_km, 2),
                        'duration_min': duration_min,
                        'route_points': polyline.decode(route['geometry'])
                    })
                return {
                    'routes': routes_result, 
                    'mode': mode
                }
            else:
                return {'error': 'Không tìm thấy đường đi nào.'}
        except Exception as e:
            return {'error': f'Lỗi hệ thống: {str(e)}'}
