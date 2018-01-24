import RPi.GPIO as GPIO # Cargamos la libreria RPi.GPIO
from time import sleep  # cargamo

GPIO.setmode(GPIO.BCM)  # Ponemos la Raspberry en modo BCM

GPIO.setup(18, GPIO.OUT)  # Ponemos el pin GPIO como salida

valve=GPIO.PWM(18, 100)

vale.start(0)

pause_time = 0.02           # Declaramos un lapso de tiempo para las pausas

try:                        # Abrimos un bloque 'Try...except KeyboardInterrupt'
    while True:             # Iniciamos un bucle 'while true'
        for i in range(0,101):            # De i=0 hasta i=101 (101 porque el script se detiene al 100%)
            valve.ChangeDutyCycle(i)      # LED #1 = i
            sleep(pause_time)             # Pequena pausa para no saturar el procesador
        for i in range(100,-1,-1):        # Desde i=100 a i=0 en pasos de -1
            valve.ChangeDutyCycle(i)      # LED #1 = i
            sleep(pause_time)             # Pequena pausa para no saturar el procesador

except KeyboardInterrupt:   # Se ha pulsado CTRL+C!!
    valve.stop()            # Detenemos el objeto 'valve'
    GPIO.cleanup()          # Limpiamos los pines GPIO y salimos
