<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
require_once("link_funtain.php");

if ($_SERVER["REQUEST_METHOD"] == "POST")
{
    $Req_Met = $_REQUEST['metodo'] or die('No existe ese metodo');
    if($Req_Met == "registrar")
    {
        $mac_adrs = $_POST['mac'];
        $ip_adrs = $_POST['ip'];
        $single = $_POST['single'];
        $ob_link_fun = new link_funtain();
    	$response = $ob_link_fun->createUser($ip_adrs, $mac_adrs, $single);
        print $response;
    }
}
else
{
    $Req_Met = $_REQUEST['metodo'] or die('No existe ese metodo');
    if($Req_Met == "sendvalue")
    {
        $req_value = $_REQUEST['value'];
        $req_user = $_REQUEST['user'];
        if(!isset($req_value) or !isset($req_user))
        {
            return "Falta valor.";
        }
        else
        {
            $ob_link_fun = new link_funtain();
            $response = $ob_link_fun->insertShakeValue($req_user,$req_value);
            print $response;
        }
    }
}
?>
