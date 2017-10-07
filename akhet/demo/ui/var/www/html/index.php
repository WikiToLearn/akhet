<?php
try {
    require_once './libs/AkhetInstance.php';
    require_once './libs/AkhetInstanceManager.php';

    $config_txt = file_get_contents("/etc/akhet-demo-ui.yml");
    $config = yaml_parse($config_txt);

    $akhet_api_base = $config['api_protocol'];
    $akhet_api_base .= "://";
    $akhet_api_base .= $config['api_username'];
    $akhet_api_base .= ":";
    $akhet_api_base .= $config['api_password'];
    $akhet_api_base .= "@";
    $akhet_api_base .= $config['api_host'];
    $akhet_api_base .= ":";
    $akhet_api_base .= $config['api_port'];

    $akhet_instance_manager = new AkhetInstanceManager($akhet_api_base);

    function getNoVNCLink($instance)
    {
        $novnc_link = null;
        if ($instance->get_is_running() && count($instance->proxies_hostnames)>0) {
            $novnc_link = "/noVNC/vnc.html#";
            $novnc_link .= "host=".$instance->proxies_hostnames[0];
            $novnc_link .= "&";
            $novnc_link .= "password=".$instance->vnc_password;
            $novnc_link .= "&";
            $novnc_link .= "true_color=1";
            $novnc_link .= "&";
            $novnc_link .= "autoconnect=1";
            $novnc_link .= "&";
            $novnc_link .= "path=portvnc/".$instance->agent_hostname."/".$instance->port_ws_vnc;
            $novnc_link .= "&";
            $novnc_link .= "encrypt=". ((int) isset($_SERVER['HTTPS']));
            $novnc_link .= "&";
            $novnc_link .= "port=".$_SERVER['SERVER_PORT'];
        }
        return $novnc_link;
    }

    if (isset($_GET['instance_id'])) {
        header("Content-Type: text/plain");
        $data = new AkhetInstance($akhet_api_base, $_GET['instance_id']);

        $novnc_link = getNoVNCLink($data);
        if ($novnc_link!=null) {
            header("Location: " . $novnc_link);
        } else {
            header("Refresh: 1");
            echo "Waiting for " . $data->get_instance_id();
        }
    } else {
        if (isset($_POST['instance_image'])) {
            header("Content-Type: text/plain");

            $length = 8;
            $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
            $charactersLength = strlen($characters);
            $randomString = '';
            for ($i = 0; $i < $length; $i++) {
                $randomString .= $characters[rand(0, $charactersLength - 1)];
            }

            $data = array();
            $data['image'] = $_POST['instance_image'];
            $data['vnc_password'] = $randomString;
            $data['shared'] = true;
            $data['user'] = array();
            $data['user']["username"] = "demouser";
            $data['user']["user_label"] = "Demo User";
            $instance_id = $akhet_instance_manager->CreateInstance($data);
            header("Location: /?instance_id=" . $instance_id);
        } else {
            $raw = file_get_contents($akhet_api_base . "/api/v1/agent");
            $api_agents_data = json_decode($raw)->_items;
            $images = array();
            foreach ($api_agents_data as $agent) {
                foreach ($agent->images as $image) {
                    $images[] = $image;
                }
            }

            asort($images);

            $instances = $akhet_instance_manager->GetInstances();
            $shared_instances = array();
            foreach ($instances as $instance) {
                if ($instance->shared) {
                    $novnc_link = getNoVNCLink($instance);
                    if ($novnc_link!= null) {
                        $shared_instances[$instance->get_instance_id()] = $novnc_link;
                    }
                }
            }
            include "tpl/index.php";
        }
    }
} catch (Exception $exception) {
    header("HTTP/1.1 500 Internal Server Error");
    include "tpl/exception.php";
}
