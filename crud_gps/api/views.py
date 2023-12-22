from typing import Any
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse as HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import Posicion
import json
import pandas as pd
from django.http import HttpResponse
from django.views import View
import requests

# Create your views here.
#Creación de Views para el modelo Posicion
class PosicionView(View):
    
    #Def para anular token CSRF (Para autorizar inserciones)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    #Creación de Request GET (Posicion)    
    def get(self, request, posicion_id=None):
        if posicion_id is None:
            #Listar todos los registros
            posiciones = Posicion.objects.all()
        else:
            #Listar un registro específico por ID
            try:
                posiciones = Posicion.objects.filter(id=posicion_id)
            except Posicion.DoesNotExist:
                response_data = {
                    "message": f"No se encontró la posición con ID {posicion_id}",
                    "posiciones": []
                }
                return JsonResponse(response_data, status=404)

        data = []

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
                },
                "fecha_hora": posicion.fecha_hora
            }
            data.append(posicion_data)

        if posicion_id is None:
            #Si no se proporciona un ID, listar todos los registros
            response_data = {
                "message": "Datos listados con éxito",
                "posiciones": data
            }
        else:
            #En caso de proporcionar un ID, listar el registro
            response_data = {
                "message": f"Dato listado con éxito para la posición con ID {posicion_id}",
                "posiciones": data
            }

        return JsonResponse(response_data)
    
    #Creacion de Request POST (Posicion)
    def post(self, request):
        data=json.loads(request.body)
        Posicion.objects.create(
            imei=data['imei'], 
            lat=data['lat'], 
            lon=data['lon'], 
            alt=data['alt'], 
            speed=data['speed'], 
            orientation=data['orientation'], 
            acc=data['acc'], 
            dil=data['dil'], 
            towing=data['towing']
            )
        response_data = {
            "message": "Datos guardados con éxito"
        }
        return JsonResponse(response_data)
    
    #Creacion de Request PUT (Posicion)
    def put(self, request, posicion_id):
        try:
            #Obtener posicion por ID
            posicion = Posicion.objects.get(id=posicion_id)
            data = json.loads(request.body)
            #Actualización de campos
            posicion.imei = data.get('imei', posicion.imei)
            posicion.lat = data.get('lat', posicion.lat)
            posicion.lon = data.get('lon', posicion.lon)
            posicion.alt = data.get('alt', posicion.alt)
            posicion.speed = data.get('speed', posicion.speed)
            posicion.orientation = data.get('orientation', posicion.orientation)
            posicion.acc = data.get('acc', posicion.acc)
            posicion.dil = data.get('dil', posicion.dil)
            posicion.towing = data.get('towing', posicion.towing)
            posicion.save()
            response_data = {
                "message": f"Posición con ID {posicion_id} actualizada con éxito"
            }
            return JsonResponse(response_data)

        except Posicion.DoesNotExist:
            response_data = {
                "message": f"No se encontró la posición con ID {posicion_id}"
            }
            return JsonResponse(response_data, status=404)
    
    #Creacion de Request DELETE (Posicion)
    def delete(self, request, posicion_id):
        posicion = list(Posicion.objects.filter(id=posicion_id).values())
        if len (posicion)>0:
            Posicion.objects.filter(id=posicion_id).delete()
            response_data = {
                "message": f"Posición con ID {posicion_id} eliminada con éxito"
            }
        else:
            response_data = {
                "message": f"No se encontró el registro"
            }
        return JsonResponse(response_data)

class ExportToExcelView(View):
    def get(self, request, *args, **kwargs):
        # Realiza la solicitud GET a la API
        api_url = 'http://127.0.0.1:8000/api/posicion/'
        response = requests.get(api_url)

        # Verifica si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Convierte los datos JSON en una lista de diccionarios
            datos_api = response.json().get("posiciones", [])

            # Desanida los datos antes de crear el DataFrame
            desanidados = []
            for dato in datos_api:
                desanidado = {
                    "imei": dato.get("imei", ""),
                    "lat": dato.get("position", {}).get("lat", ""),
                    "lon": dato.get("position", {}).get("lon", ""),
                    "alt": dato.get("alt", ""),
                    "speed": dato.get("speed", ""),
                    "orientation": dato.get("orientation", ""),
                    "acc": dato.get("sensores", {}).get("acc", ""),
                    "dil": dato.get("sensores", {}).get("dil", ""),
                    "towing": dato.get("sensores", {}).get("towing", ""),
                    "fecha_hora": dato.get("fecha_hora", ""),
                }
                desanidados.append(desanidado)

            # Define las columnas
            columnas = ["imei", "lat", "lon", "alt", "speed", "orientation", "acc", "dil", "towing", "fecha_hora"]

            # Crea el DataFrame directamente desde la lista de diccionarios
            df = pd.DataFrame(desanidados, columns=columnas)

            # Crea la respuesta del archivo Excel
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=datos_api.xlsx'
            df.to_excel(response, index=False)

            return response
        else:
            return HttpResponse(f"Error en la solicitud a la API. Código de estado: {response.status_code}")