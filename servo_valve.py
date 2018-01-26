import RPi.GPIO as GPIO # Cargamos la libreria RPi.GPIO
from time import sleep  # cargamo
import MySQLdb

GPIO.setmode(GPIO.BCM)  # Ponemos la Raspberry en modo BCM

GPIO.setup(18, GPIO.OUT)  # Ponemos el pin GPIO como salida

valve=GPIO.PWM(18, 50)

valve.start(0)
pause_time = 0.2           # Declaramos un lapso de tiempo para las pausas

max_value = 1000

try:                        # Abrimos un bloque 'Try...except KeyboardInterrupt'
    while True:             # Iniciamos un bucle 'while true'
        db = MySQLdb.connect(host="localhost", user="root", passwd="funtain@tds", db="funtain_db")

	#create a cursor for the select
	cur = db.cursor()

	#execute an sql query
	cur.execute("SELECT *  FROM single_shake where shaked = 0 order by sshake_id asc;")
	#cur.execute("select * from single_shake order by sshake_id asc;")
	if cur.rowcount==0:
		#print 0
		valve.ChangeDutyCycle(100)
		sleep(pause_time)
		cur.execute("delete from single_shake where shaked = 1;")
		db.commit()
	else:
		##Iterate 
		for row in cur.fetchall() :
      			#data from rows
        		sshake_id = row[0] 
        		shake_val = row[2]/2
        		cur.execute("update single_shake set shaked=1 where sshake_id = " + str(sshake_id))
			db.commit()
      			#print 
        		print shake_val
			if shake_val > 100:
				shake_val = 100            
        		valve.ChangeDutyCycle(100-shake_val)
        		sleep(pause_time)

	# close the cursor
	cur.close()

	# close the connection
	db.close ()

except KeyboardInterrupt:   # Se ha pulsado CTRL+C!!
    valve.stop()            # Detenemos el objeto 'valve'
    GPIO.cleanup()          # Limpiamos los pines GPIO y salimos
