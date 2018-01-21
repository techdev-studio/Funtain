<?php
Class link_funtain
{
    public function createUser($ip,$mac,$single)
    {
        $online = 0;
        $query_get_connected_user = "select user_id from user_funtain where online = 1;";
        $user_online = $this->setConnection($query_get_connected_user);
        $r1=mysqli_fetch_array($user_online,MYSQLI_NUM);
        if($r1[0]==1)
        {
            //someone connected
            //create but not online
            $online =0;
        }
        else
        {
            //no one connected
            //create online
            $online =1;
        }
        $query_cu="INSERT INTO user_funtain (mac_adr, ip_adr, online, single) VALUES('$mac','$ip',$online,$single);";
        $user_created = $this->setConnection($query_cu);
        //$r1=mysql_fetch_array($user_created,MYSQLI_NUM);
        $query_last = "Select user_id from user_funtain where mac_adr = '$mac';";
        $new_user = $this->setConnection($query_last);
        $r_new_user=mysqli_fetch_array($new_user,MYSQLI_NUM);
        if($r_new_user[0]>0)
        {
            return $r_new_user[0];
        }
        else
        {
            return 0;
        }
    }

    public function setOffline($user)
    {
        $query_offline = "update user_id set online = 0 where user_id = '$user';";
        $this->setConnection($query_offline);
    }

    private function getOnline($user)
    {
        $query = "select online, single from user_funtain where user_id = '$user';";
        $online = setConnection($query);
        $result=mysqli_fetch_array($online,MYSQLI_NUM);
        $rows = array();
		while($r = mysqli_fetch_assoc($result))
		{
    			$rows[] = $r;
		}
		$response= json_encode($rows);
		return $response;
    }

    public function insertShakeValue($user,$value,$single)
    {
        $online_users = json_decode( getOnline($user));
        if($single )
        {
            $query_shake = "INSERT INTO single_shake (user_id, shake_val) VALUES($user,$value);";
            $resp_shake = setConnection($query_shake);            
        }
        else
        {
            $query_shake = "INSERT INTO group_shake (user_id, shake_val) VALUES($user,$value);";
            $resp_shake = setConnection($query_shake);
        }
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
}
?>
