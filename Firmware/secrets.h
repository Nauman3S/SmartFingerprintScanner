#include <pgmspace.h>
String mac = (WiFi.macAddress());
char __mac[sizeof(mac)];

// const char ssid[]="hotspot2";
// const char password[] ="abc123098a#";

const char *mqtt_server = "18.213.166.207";
const int mqtt_port = 1883;
const char *mqtt_user = "device";
const char *mqtt_pass = "device";
const char *mqtt_client_name = __mac; //"12312312312332212";// any random alphanumeric string