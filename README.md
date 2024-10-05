# SmartBatterySystem

The smart battery uses low-cost electricity to charge the battery.
This electricity can then be used when elekctricity is expensive.
The key to it's succes should be based on simplicity, sustainability and low-impact.
All the system that rely on the battery should be able to function without any alterations.

# Physical system

The physical part consists of four items:

1. Batteries
2. Converter -> battery to grid voltage
3. Control system (see below)
4. Converter -> grid to battery voltage

It would be more efficient if a 2-way convert would be used but they don't seem to exist.
An integrated system would be even more efficient and solve previous problem. But this initially makes it less simple.

The components used in the system are:
- Raspberry PI 4, with the follow compontents:
    - A relay: https://www.bitsandparts.nl/Relais-board-1-kanaals-5V-optocoupled-p101104
    - A voltmeter: https://www.bitsandparts.nl/Spanningsmeter-spanningsdeler-tot-25V-p1096274
    - Wiring
    - Indicator LED's
- An inverter: https://www.bol.com/nl/nl/p/ecoline-omvormer-12v-naar-220v-230v-300w-600w-vermogen-gemodificeerde-sinus-auto-omvormer/9300000134186311/?s2a=
- A charger: https://www.bol.com/nl/nl/p/tecmate-optimate-4-dual-can-bus-0-8a-12v-acculader-druppellader-voor-scooter-motor/9200000090601966/?

# Control system

The control system is responsible for making sure the systems that rely on the battery get low-cost electricity.
This means that it should use several datasources to get low-cost electricity and save it for later.
Datasources that could be beneficial:

- Battery charge (voltage)
- Solarpanel charge
- Day/Night electricity (when having 2 two tariff's)
- Electricity price (when having a flexible price)

Preferably there should be a way to predict all of the above in order to increase efficiency.

## Physical part of the control system

The control system is as can be seen from the component list nothing more that a relay, voltmeter and some indicator leds.
This is simple as intented.