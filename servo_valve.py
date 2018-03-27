import RPi.GPIO as GPIO # Cargamos la libreria RPi.GPIO
from time import sleep  # cargamo
import MySQLdb
import serial

GPIO.setmode(GPIO.BCM)  # Ponemos la Raspberry en modo BCM
GPIO.setup(18, GPIO.OUT)  # Ponemos el pin GPIO como salida

#variables
pause_time = 0.2           # Declaramos un lapso de tiempo para las pausas en segundos
min_value = 10				#min porcentaje de apertura de valvula
max_value = 175				#max porcentaje de apertura de valvula
inact_counter = 0
#PWM setup
#valve=GPIO.PWM(18, 250) 	#configuramos la senal pwm a la frecuencia deseada
#valve.start(min_value) 		#iniciamos valvula con apertura minima 
#ser = serial.Serial('/dev/ttyACM0',9600)

ser = serial.Serial(
                      port='/dev/ttyAMA0',
                      baudrate = 9600,
                      parity=serial.PARITY_NONE,
                      stopbits=serial.STOPBITS_ONE,
                      bytesize=serial.EIGHTBITS,
                      timeout=1
                  )
ser.flush()
sleep(1)

try:
	print "reseteando tablas"
	db = MySQLdb.connect(host="localhost", user="root", passwd="funtain@tds", db="funtain_db")
        cur = db.cursor()
	cur.execute("delete from single_shake;")
        db.commit()
        print "shake_single del"
        cur.execute("delete from group_shake;")
        db.commit()
        print "shake_group del"
        cur.execute("delete from user_funtain;")
        db.commit()
        print "user_reset"
	# close the cursor
        cur.close()
        # close the connection
        db.close ()
except:
	print "something happened"


try:                        # Abrimos un bloque 'Try...except KeyboardInterrupt'
    while True:             # Iniciamos un bucle 'while true'
	shake_val = 0
	user_id = 0 

	#connect to DB
        db = MySQLdb.connect(host="localhost", user="root", passwd="funtain@tds", db="funtain_db")

	#create a cursor for the select
	cur = db.cursor()

	#execute single user shake
	cur.execute("SELECT *  FROM user_funtain where single = 1 and online = 1 order by user_id desc;")

	if cur.rowcount==0:
		#execute group shake
		cur.execute("SELECT *  FROM user_funtain where single = 0 and online = 1;")
		q_user = cur.rowcount
	
		if q_user > 0:
			#multi connected
			users = [0] * q_user
			index = 0
			cur.execute("SELECT *  FROM user_funtain where single = 0 and online = 1;")
			for urow in cur.fetchall():
				#data from users
				users[index] = urow[0]
				index = index + 1
				print index
			
			for u_id in users:
				cur.execute("SELECT *  FROM group_shake where shaked = 0 and user_id = " + str(u_id) + " order by gshake_id desc;")
				row_val = cur.fetchone()
				try:
					gshake_id = row_val[0]
					gshake_val = 2*row_val[2]/q_user
					shake_val = shake_val + gshake_val
					#print shake_val
					#update values
					cur.execute("update group_shake set shaked=1 where user_id=" + str(u_id) + " and gshake_id <= " + str(gshake_id) + ";")
					db.commit()
				except:
					print "nothing in group shake"
					sleep(0.5)
			print shake_val

			if shake_val > max_value:
                          	shake_val = max_value

                       	if shake_val < min_value:
                       		shake_val = min_value
        		
			ser.write(str(shake_val))
			ser.write("\n")	
			#valve.ChangeDutyCycle(shake_val)
               		sleep(pause_time)

		else:
			inact_counter = inact_counter +1
			print "nothing to process"
			#valve.ChangeDutyCycle(min_value)
			ser.write("0")
			ser.write("\n")
			sleep(2)
			cur.execute("delete from single_shake where shaked = 1;")
			db.commit()
			print "shake_single del"
			cur.execute("delete from group_shake where shaked = 1;")
			db.commit()
			print "shake_group del"
			if inact_counter > 7:
				inact_counter =0
				cur.execute("update user_funtain set online = 0 where online=1;")
        	                db.commit()
				print "user_reset"
			
	else:
		row = cur.fetchone()
		user_id = row[0]
		#print user_id

		#execute single shake
		cur.execute("SELECT *  FROM single_shake where shaked = 0 and user_id = " + str(user_id) + " order by sshake_id desc;")
		#Iterate 
		try:
			row = cur.fetchone()
			#data from rows
			sshake_id = row[0] 
			shake_val = row[2]*2
			cur.execute("update single_shake set shaked=1 where user_id = " + str(user_id) + " and sshake_id <= " + str(sshake_id) + ";")
			db.commit()

			#print 
			print "single_shake"
			print shake_val

			if shake_val > max_value:
				shake_val = max_value

			if shake_val < min_value:
				shake_val = min_value

			ser.write(str(shake_val))
			ser.write("\n")
			#valve.ChangeDutyCycle(shake_val)					
			sleep(pause_time)
		except:
			print "no val single"
			sleep(pause_time)

	# close the cursor
	cur.close()
	# close the connection
	db.close ()

except KeyboardInterrupt:   # Se ha pulsado CTRL+C!!
    #valve.stop()            # Detenemos el objeto 'valve'
    GPIO.cleanup()          # Limpiamos los pines GPIO y salimos
