## Omeobot

Es un bot diseñado para entregar alertas del clúster Ometéotl del CCA-UNAM, fue desarrollado utilizando una API de Python: [Telebot](https://github.com/eternnoir/pyTelegramBotAPI), y las alertas son recibidas por medio de la aplicación de mensajeria [Telegram](https://es.wikipedia.org/wiki/Telegram_Messenger)

Se implementó utilizando el lenguaje de programación [Python](https://www.python.org/), la versión 3.6.
Se utiliza [IPMI](https://en.wikipedia.org/wiki/Intelligent_Platform_Management_Interface) para recabar información de los nodos del clúster.

### Objetivos 

Omeobot es una herramienta que ayuda con el monitoreo del clúster Ometéotl cuyas notificaciones son útiles para llevar a cabo una revisión a detalle en el clúster y así obtener un diagnóstico con el fin de prevenir situaciones de riesgo en él.

### Funcionalidad

Por el momento el bot esta desarrollado para que realice el monitoreo de la temperatura de cada uno de los nodos y envía una alerta en caso de que la temperatura sea mayor a una temperatura considerada de _precaución_, las consultas están programadas para que se realicen cada 5 minutos.
Aún no se implementan comandos para realizar consultas al bot.





