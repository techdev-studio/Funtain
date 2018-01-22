<?php
Class link_funtain
{
    public function create_user_ws($ip,$mac)
    {
        $user_created = $this->getExistUser($mac);
        if($user_created>0)
        {
            return $user_created;            
        }
        else
        {
            $query_insert_user="INSERT INTO user_funtain (mac_adr, ip_adr, single, online) VALUES('$mac','$ip',0,0);";
            $user_created = $this->setConnection($query_insert_user);  
            return $this->getExistUser($mac);          
        }
    }

    private function getExistUser($mac)
    {
        $query_user = "Select user_id from user_funtain where mac_adr = '$mac';";
        $exist_user = $this->setConnection($query_user);
        $r_exist_user=mysqli_fetch_array($exist_user,MYSQLI_NUM);
        if(sizeof($r_exist_user)>0)
        {
            return $r_exist_user[0];
        }
        else
        {
            return 0;
        }
    }

    public function interaction_type_ws($user_id, $single)
    {
        $success = false;
        $message = "";
        if ($single == 1)
        {
            $connected_single =$this->get_single_connected_fn();
            if($connected_single==0)
            {
                $success=false;
                $message="Single Player Already Online";
            }
            else
            {
                $query_online_single = "UPDATE user_funtain SET online =1, single=1 where user_id = '$user_id';";
                $new_online = $this->setConnection($query_online_single);
                $online = get_connected_by_id($user_id);       
            }
        }
        else
        {
            $connected_multi = $this->get_multi_connected_fn();
            if ($connected_multi == 0)
            {
                $success=false;
                $message="Multiplayer FULL";
            }
            else
            {
                $query_online_multi = "UPDATE user_funtain SET online =1, single=0 where user_id = '$user_id';";
                $new_online = $this->setConnection($query_online_multi);
                $online = get_connected_by_id($user_id);           
            }
        }

        if($online ==1)//
        {
            $success=true;
            $message = "Connected!";
        }
        else
        {
            $success=false;
            $message="Connection Error.";
        }
        return $this->setJsonResponse($sucess,$message);
    }

    private function get_single_connected_fn()
    {
        $online = 0;
        $query_get_connected_single = "select user_id from user_funtain where online = 1 and single = 1;";
        $single_online = $this->setConnection($query_get_connected_single);
        $r1=mysqli_fetch_array($single_online,MYSQLI_NUM);
        if (sizeof($r1) > 0)
        {
            //hay un single conectado
            return 0;
        }
        else
        {
            //no hay single conectado
            return 1;
        }
    }

    private function get_multi_connected_fn()
    {
        //validar maximo 5 conectados
        $query_get_connected_multi = "select user_id from user_funtain where online = 1 and single = 0;";
        $multi_online = $this->setConnection($query_get_connected_multi);
        $r1=mysqli_fetch_array($single_online,MYSQLI_NUM);
        if(sizeof($r1)<5)
        {
            //multi todavia hay espacio
            return 1;
        }
        else
        {
            //multi completado
            return 0;
        }
    }

    private function get_connected_by_id($user_id)
    {
        $query_get_connected = "select online from user_funtain where user_id = $user_id;";
        $r_get_connected = $this->setConnection($query_get_connected);
        $rc=mysqli_fetch_array($r_get_connected,MYSQLI_NUM);
        if(sizeof($rc)>0)
        {
            //connected success
            return 1;
        }
        else
        {
            //not connected error
            return 0;
        }
    }

    public function setOffline($user)
    {
        $query_offline = "update user_funtain set online = 0 where user_id = '$user';";
        $this->setConnection($query_offline);
    }

    private function getOnline($user)
    {
        $query = "select online, single from user_funtain where user_id = '$user';";
        $online = $this->setConnection($query);
        $result=mysqli_fetch_array($online,MYSQLI_NUM);
        $rows = array();
		while($r = mysqli_fetch_assoc($result))
		{
    			$rows[] = $r;
		}
		$response= $this->json_encode($rows);
		return $response;
    }

    public function insert_single_ws($user_id, $value)
    {
        $online = $this->get_connected_by_id($user_id);
        if($online ==1)//user connected
        {
            $message = $this->insertShakeValue($user_id,$value,1);
            $success=true;
            //$message = "Inserted Value!";
        }
        else
        {
            $success=false;
            $message="User not Online";
        }
        return $this->setJsonResponse($sucess,$message);
    }

    public function insert_multi_ws($user_id, $value)
    {
        $online = $this->get_connected_by_id($user_id);
        if($online ==1)//user connected
        {
            $message=$this->insertShakeValue($user_id,$value,0);
            $success=true;
            //$message = "Inserted Value!";
        }
        else
        {
            $success=false;
            $message="User not Online";
        }
        return $this->setJsonResponse($sucess,$message);
    }

    private function insertShakeValue($user,$value,$single)
    {
        if($single )
        {
            $query_shake = "INSERT INTO single_shake (user_id, shake_val) VALUES($user,$value);";            
        }
        else
        {
            $query_shake = "INSERT INTO group_shake (user_id, shake_val) VALUES($user,$value);";
        }
        return $this->setConnection($query_shake);
    }

    private function setConnection($con_query)
	{
		//echo $con_query;
		$config = parse_ini_file('../private/config.ini');
		$con = mysqli_connect($config['hostname'],$config['username'],$config['password']) or die("ERROR no se puede conectar");
		mysqli_select_db($con,$config['dbname']) or die("ERROR no existe esa bd");
		$result=mysqli_query($con,$con_query) or die ("request error" );
		mysqli_close($con);
		return $result;
    }

    private function setJsonResponse($success, $message)
    {
        $myObj->success = $success;
        $myObj->message = $message;
        
        $myJSON = json_encode($myObj);
        
        return $myJSON;
    }
}
?>
