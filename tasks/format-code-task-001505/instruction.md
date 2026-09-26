Option to expire sensor values that did not receive an updates
This option is only usefull for push-style sensors like mqtt. If the sender looses connection, the last value will be displayed forever. With this feature, the value would switch to UNKNOWN after a certain time.

Use case:
I have several temperature sensors, based on ESP8266 using MQTT. From time to time a sensor looses connection (due to wifi maximum range, some are behind multiple walls and have poor wifi signal). When this happens, home assistant still shows the old temperature).

I'll create a pull request for this feature.
