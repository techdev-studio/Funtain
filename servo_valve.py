import RPi.GPIO as GPIO # Cargamos la libreria RPi.GPIO
from time import sleep  # cargamo
import MySQLdb

GPIO.setmode(GPIO.BCM)  # Ponemos la Raspberry en modo BCM

GPIO.setup(18, GPIO.OUT)  # Ponemos el pin GPIO como salida

valve=GPIO.PWM(18, 100)

valve.start(0)
pause_time = 0.5           # Declaramos un lapso de tiempo para las pausas

max_value = 1000

try:                        # Abrimos un bloque 'Try...except KeyboardInterrupt'
    while True:             # Iniciamos un bucle 'while true'
        db = MySQLdb.connect(host="localhost", user="root", passwd="funtain@tds", db="funtain_db")

	#create a cursor for the select
	cur = db.cursor()

	#execute an sql query
	cur.execute("SELECT *  FROM single_shake where shaked = 0 order by sshake_id asc;")

	##Iterate 
	for row in cur.fetchall() :
      		#data from rows
        	sshake_id = row[0] 
        	shake_val = row[2]
        	cur.execute("update single_shake set shaked=1 where sshake_id = " + str(sshake_id))
		db.commit()
      		#print 
        	print shake_val            
        	valve.ChangeDutyCycle(100*(max_value-shake_val)/max_value)
        	sleep(pause_time)

	# close the cursor
	cur.close()

	# close the connection
	db.close ()

except KeyboardInterrupt:   # Se ha pulsado CTRL+C!!
    valve.stop()            # Detenemos el objeto 'valve'
    GPIO.cleanup()          # Limpiamos los pines GPIO y salimos
