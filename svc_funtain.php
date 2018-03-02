<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
require_once("link_funtain.php");

if ($_SERVER["REQUEST_METHOD"] == "POST")
{
    //metodos de seteo
    $Req_Met = $_REQUEST['metodo'] or die('Falta metodo');
    if($Req_Met == "registrar")
    {
        $mac_adrs = $_POST['mac'];
        $ip_adrs = $_POST['ip'];
        $ob_link_fun = new link_funtain();
    	$response = $ob_link_fun->create_user_ws($ip_adrs, $mac_adrs);
        print $response;
    }
    else if ($Req_Met == "interaction")
    {
        //si single =1, juego solitario, valida si existe alguien mas conectado
        //retorna parametro y empieza o no juego
        $user_id = $_POST['user_id'];
        $single = $_POST['single'];
        $ob_link_fun = new link_funtain();
    	$response = $ob_link_fun->interaction_type_ws($user_id, $single);
        print $response;
    }
    else if ($Req_Met == "desconectar")
    {
        $user_id = $_POST['user_id'];
        $ob_link_fun = new link_funtain();
    	$response = $ob_link_fun->setOffline($user_id);
        print $response;
    }
    else
    {
        die ('no existe ese metodo');
    }
}
else
{
    //metodos de envio de data
    $Req_Met = $_REQUEST['metodo'] or die('No existe ese metodo');
    if($Req_Met == "shakeSingle")
    {
        $req_value = $_REQUEST['value'];
        $req_user = $_REQUEST['user_id'];
        if(!isset($req_value) or !isset($req_user))
        {
            return "Falta valor.";
        }
        else
        {
            $ob_link_fun = new link_funtain();
            $response = $ob_link_fun->insert_single_ws($req_user,$req_value);
            print $response;
        }
    }
    else if ($Req_Met == "shakeMulti")
    {
        $req_value = $_REQUEST['value'];
        $req_user = $_REQUEST['user_id'];
        if(!isset($req_value) or !isset($req_user))
        {
            return "Falta valor.";
        }
        else
        {
            $ob_link_fun = new link_funtain();
            $response = $ob_link_fun->insert_multi_ws($req_user,$req_value);
            print $response;
        }
    }
    else if ($Req_Met == "desconectar")
    {
	$user_id = $_REQUEST['user_id'];
        $ob_link_fun = new link_funtain();
    	$response = $ob_link_fun->setOffline($user_id);
        print $response;
    }
    else
    {
        die ('no existe ese metodo');
    }
}
?>
