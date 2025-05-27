import requests
import socket
import platform
import psutil
import wmi  # Necesario: instalar con pip install wmi

# Obtener nombre del equipo
nombre = platform.node()

# Sistema operativo
sistema = platform.system() + " " + platform.release()


# RAM física instalada (en GB)
ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)

c = wmi.WMI()
procesador = c.Win32_Processor()[0]
descripcion_procesador = f"{procesador.Name}, {procesador.MaxClockSpeed} MHz, {procesador.NumberOfCores} núcleos, {procesador.NumberOfLogicalProcessors} hilos"

# Disco principal (unidad C:)
disco = round(psutil.disk_usage('/').total / (1024 ** 3), 2)

# IP actual del equipo
ip = socket.gethostbyname(socket.gethostname())

# Empaquetar datos
datos = {
    "nombre": nombre,
    "sistema": sistema,
    "ram": ram,
    "procesador": descripcion_procesador,
    "disco": disco,
    "ip": ip
}

# Enviar al servidor Flask (ajusta IP si es otro equipo)
url = 'http://127.0.0.1:5050/registrar'

try:
    respuesta = requests.post(url, json=datos)
    print("Respuesta del servidor:", respuesta.json())
except Exception as e:
    print("Error al conectar con el servidor:", e)
