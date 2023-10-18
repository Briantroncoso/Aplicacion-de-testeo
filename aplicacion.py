import subprocess
import socket
import speedtest
import requests
import tkinter as tk
from ping3 import ping

def medir_ping(ip):
    resultado = subprocess.run(['ping', '-c', '4', ip], stdout=subprocess.PIPE, text=True)
    return resultado.stdout

def realizar_traceroute(ip):
    resultado = subprocess.run(['traceroute', ip], stdout=subprocess.PIPE, text=True)
    return resultado.stdout

def comprobar_puertos(ip, puertos):
    resultado_puertos = ""
    for puerto in puertos:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        resultado = sock.connect_ex((ip, puerto))
        if resultado == 0:
            resultado_puertos += f'Puerto {puerto} está abierto\n'
        else:
            resultado_puertos += f'Puerto {puerto} está cerrado\n'
        sock.close()
    return resultado_puertos

def check_internet_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000
    upload_speed = st.upload() / 1_000_000
    return f"Velocidad de descarga: {download_speed:.2f} Mbps\nVelocidad de carga: {upload_speed:.2f} Mbps"

def get_public_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        if response.status_code == 200:
            data = response.json()
            return data['ip']
        else:
            return "No se pudo obtener la IP pública."
    except requests.RequestException as e:
        return "Error al obtener la IP pública: " + str(e)

def check_voip_status(target_host, extencion, clave):
    try:
        response = requests.get(f"{target_host}?ext={extencion}&clave={clave}")
        if response.status_code == 200:
            return "Servicio de VoIP/SIP en línea."
        else:
            return "No se pudo conectar al servicio de VoIP/SIP."
    except requests.RequestException as e:
        return f"Error al conectar con el servicio de VoIP/SIP: {e}"

# Crear la interfaz gráfica
app = tk.Tk()
app.title("Comprobación de Red")

def check_ping():
    target_host = entry_ping.get()
    response_time = ping(target_host)
    if response_time is not None:
        ping_result.set(f"Ping exitoso a {target_host}. Tiempo de respuesta: {response_time * 1000:.2f} ms")
    else:
        ping_result.set(f"Fallo en el ping a {target_host}.")

def check_ports():
    target_host = entry_ip.get()
    ports = [21, 22, 25, 80, 110, 111, 143, 443, 993, 1812, 1813, 3128, 3306, 4118, 8006, 8080, 8088, 8089, 8443, 10443, 20005, 50000, 50001, 50002, 50003, 50004]
    result_text = comprobar_puertos(target_host, ports)
    port_result.set(result_text)

def check_voip():
    target_host = entry_voip.get()
    extencion = entry_extencion.get()
    clave = entry_clave.get()
    voip_result.set(check_voip_status(target_host, extencion, clave))

ping_result = tk.StringVar()
port_result = tk.StringVar()
speed_result = tk.StringVar()
public_ip_result = tk.StringVar()
voip_result = tk.StringVar()

label_ping = tk.Label(app, text="Ingresa el destino para comprobar el Ping:")
label_ping.pack()
entry_ping = tk.Entry(app)
entry_ping.pack()
button_check_ping = tk.Button(app, text="Comprobar Ping", command=check_ping)
button_check_ping.pack()
label_ping_result = tk.Label(app, textvariable=ping_result)
label_ping_result.pack()

label_ip = tk.Label(app, text="Ingresa la dirección IP para verificar los puertos:")
label_ip.pack()
entry_ip = tk.Entry(app)
entry_ip.pack()
button_check_ports = tk.Button(app, text="Comprobar Puertos", command=check_ports)
button_check_ports.pack()
label_port_result = tk.Label(app, textvariable=port_result)
label_port_result.pack()

button_check_speed = tk.Button(app, text="Comprobar Velocidad de Internet", command=lambda: speed_result.set(check_internet_speed()))
button_check_speed.pack()
label_speed_result = tk.Label(app, textvariable=speed_result)
label_speed_result.pack()

button_check_ip = tk.Button(app, text="IP Pública", command=lambda: public_ip_result.set(get_public_ip()))
button_check_ip.pack()
label_public_ip_result = tk.Label(app, textvariable=public_ip_result)
label_public_ip_result.pack()

label_voip = tk.Label(app, text="Ingresa el destino, extensión y clave para comprobar el estado del servicio VoIP/SIP:")
label_voip.pack()
entry_voip = tk.Entry(app)
entry_voip.pack()
entry_extencion = tk.Entry(app)
entry_extencion.pack()
entry_clave = tk.Entry(app, show="*")  # Para ocultar la clave
entry_clave.pack()
button_check_voip = tk.Button(app, text="Comprobar Estado de VoIP/SIP", command=check_voip)
button_check_voip.pack()
label_voip_result = tk.Label(app, textvariable=voip_result)
label_voip_result.pack()

app.mainloop()
