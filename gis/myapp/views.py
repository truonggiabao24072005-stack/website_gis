from django.shortcuts import render, get_object_or_404
from .models import Apartment
from django.http import JsonResponse
from .tool import RoutingTool 


def home(request):
    return render(request, 'home.html')


def map_view(request):
    apartments_db = Apartment.objects.all()
    
    apartments_list = []
    for apt in apartments_db:
        
        if apt.image:
            img_url = apt.image.url
        else:
            img_url = 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267'

        apartments_list.append({
            'id': apt.id,
            'name': apt.name,
            'price': apt.price,
            'address': apt.address,
            'desc': apt.desc,
            'image': img_url,
            'lat': apt.lat,
            'lng': apt.lng
        })
    
    context = {
        'apartments': apartments_list
    }
    return render(request, 'map.html', context)
def apartment_detail(request, apartment_id):
    apartment = get_object_or_404(Apartment, pk=apartment_id)
    return render(request, 'apartment_detail.html', {'apartment': apartment})
def get_route_api(request):
    """
    API trả về dữ liệu đường đi (JSON) cho Javascript gọi
    URL: /api/route/?start_lat=...&start_lng=...&end_lat=...&end_lng=...&mode=driving
    """ 
    start_lat = request.GET.get('start_lat')
    start_lng = request.GET.get('start_lng')
    end_lat = request.GET.get('end_lat')
    end_lng = request.GET.get('end_lng')  
    mode = request.GET.get('mode', 'driving') 
    if not all([start_lat, start_lng, end_lat, end_lng]):
        return JsonResponse({'error': 'Thiếu tọa độ đầu vào'}, status=400)
    try:
        tool = RoutingTool()
        result = tool.get_route(start_lat, start_lng, end_lat, end_lng, mode=mode)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    