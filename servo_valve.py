import RPi.GPIO as GPIO # Cargamos la libreria RPi.GPIO
from time import sleep  # cargamo
import MySQLdb

GPIO.setmode(GPIO.BCM)  # Ponemos la Raspberry en modo BCM
GPIO.setup(18, GPIO.OUT)  # Ponemos el pin GPIO como salida

#variables
pause_time = 0.05           # Declaramos un lapso de tiempo para las pausas en segundos
min_value = 15				#min porcentaje de apertura de valvula
max_value = 100				#max porcentaje de apertura de valvula
inact_counter = 0
#PWM setup
valve=GPIO.PWM(18, 250) 	#configuramos la senal pwm a la frecuencia deseada
valve.start(min_value) 		#iniciamos valvula con apertura minima 

try:
	print "reseteando tablas"
	db1 = MySQLdb.connect(host="localhost", user="root", passwd="funtain@tds", db="funtain_db")
        cur1 = db.cursor()
	cur1.execute("delete from single_shake;")
        db1.commit()
        print "shake_single del"
        cur1.execute("delete from group_shake;")
        db1.commit()
        print "shake_group del"
        cur1.execute("delete from user_funtain;")
        db1.commit()
        print "user_reset"
	# close the cursor
        cur1.close()
        # close the connection
        db1.close ()
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
					gshake_val = row_val[2]/q_user
					shake_val = shake_val + gshake_val
					print shake_val
					#update values
					cur.execute("update group_shake set shaked=1 where user_id=" + str(u_id) + " and gshake_id <= " + str(gshake_id) )
					db.commit()
					if shake_val > max_value:
                                		shake_val = max_value

                        		if shake_val < min_value:
                                		shake_val = min_value

                        		valve.ChangeDutyCycle(shake_val)
                        		sleep(pause_time)
				except:
					print "nothing in group"
					sleep(0.5)
		else:
			inact_counter = inact_counter +1
			print "nothing to process"
			valve.ChangeDutyCycle(min_value)
			sleep(2)
			cur.execute("delete from single_shake where shaked = 1;")
			db.commit()
			print "shake_single del"
			cur.execute("delete from group_shake where shaked = 1;")
			db.commit()
			print "shake_group del"
			if inact_counter > 5:
				inact_counter =0
				cur.execute("update user_funtain set online = 0 where online=1;")
        	                db.commit()
				print "user_reset"
			
	else:
		row = cur.fetchone()
		user_id = row[0]
		#print user_id
		

		#execute single shake
		cur.execute("SELECT *  FROM single_shake where shaked = 0 and user_id = " + str(user_id) + " order by sshake_id asc;")
		#Iterate 
		for row in cur.fetchall():
			#data from rows
			sshake_id = row[0] 
			shake_val = row[2]
			cur.execute("update single_shake set shaked=1 where sshake_id = " + str(sshake_id))
			db.commit()

			#print 
			print shake_val
			if shake_val > max_value:
				shake_val = max_value

			if shake_val < min_value:
				shake_val = min_value

			valve.ChangeDutyCycle(shake_val)					
			sleep(pause_time)

	# close the cursor
	cur.close()
	# close the connection
	db.close ()

except KeyboardInterrupt:   # Se ha pulsado CTRL+C!!
    valve.stop()            # Detenemos el objeto 'valve'
    GPIO.cleanup()          # Limpiamos los pines GPIO y salimos
