from typing import Any
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse as HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import Posicion
import json

# Create your views here.
#Creación de Views para el modelo Posicion
class PosicionView(View):
    
    #Def para anular token CSRF (Para autorizar inserciones)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    #Creación de Request GET (Posicion)
    def get(self, request):
        posiciones = Posicion.objects.all()
        data=[]
        
        for posicion in posiciones:
            posicion_data = {
                "imei": posicion.imei,
                "position": {
                    "lat": posicion.lat,
                    "lon": posicion.lon
                },
                "alt": posicion.alt,
                "speed": posicion.speed,
                "orientation": posicion.orientation,
                "sensores": {
                    "acc": posicion.acc,
                    "dil": posicion.dil,
                    "towing": posicion.towing
                    
                }
            }
            data.append(posicion_data)
            
        response_data = {
            "message": "Datos listados con éxito",
            "posiciones": data
        }
        
        return JsonResponse(response_data)
    
    #Creacion de Request POST (Posicion)
    def post(self, request):
        data=json.loads(request.body)
        Posicion.objects.create(imei=data['imei'], lat=data['lat'], lon=data['lon'], alt=data['alt'], speed=data['speed'], orientation=data['orientation'], acc=data['acc'], dil=data['dil'], towing=data['towing'])
        response_data = {
            "message": "Datos guardados con éxito"
        }
        return JsonResponse(response_data)
