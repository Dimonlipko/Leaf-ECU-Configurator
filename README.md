# Leaf-ECU-Configurator

# Перехід до версії

<img src="https://upload.wikimedia.org/wikipedia/commons/4/49/Flag_of_Ukraine.svg" alt="Ukrainian Flag" style="height: 1em;"/> [Перейти до української версії](#українська-версія) | <img src="https://upload.wikimedia.org/wikipedia/en/a/ae/Flag_of_the_United_Kingdom.svg" alt="British Flag" style="height: 1em;"/> [Go to English Version](#english-version)

# Українська версія

Перед початком роботи з ECU уважно прочитайте [Leaf ECU Manual](https://github.com/Dimonlipko/Leaf-ECU-Configurator/blob/main/Leaf_ecu_manual.pdf), і тільки після цього починайте підключати проводку, після чого встановіть програму конфігуратора.

Перевіряйте актуальні оновлення на цій сторінці, оскільки проект все ще розвивається, і з'являються нові функції у старих контролерах.

## Програма для налаштування та моніторингу параметрів контролера.

### Установка:
1. Встановіть `ddt4all`, запустивши `ddt4all-installer.exe`.
2. Після успішної установки в папці з програмою `ddt4all` у папку `json` покладіть 3 файли: `Leaf_motor.json`, `Leaf_motor.json.layout`, `Leaf_motor.json.targets`.
3. У папці з програмою `ddt4all` у папку `ddtplugins` покладіть файл `ddt4all-FirmwareReceiver.py`.

### Запуск:
При першому запуску потрібно встановити сполучення з ELM327 у налаштуваннях Bluetooth вашого комп'ютера. Пін-код для сполучення з Bluetooth ELM327 зазвичай `1234`, або підключитися до Wi-Fi точки доступу, якщо у вас Wi-Fi версія ELM327.

1. На робочому столі запустіть ярлик `ddt4all` або в папці з програмою.
2. Відкриється вікно, виберіть віртуальний COM порт і натисніть на вікно з символом Bluetooth, якщо це Bluetooth версія ELM, або виберіть Wi-Fi. Налаштування порту не змінюйте, поставте галочку і натисніть **"Підключитися."**
3. Після підключення відкриється основне вікно програми. У меню справа виберіть вкладку **"Custom,"** нижче з'явиться `Leaf_motor.json`.
4. В пустому вікні нижче з'явиться напис `Leaf_motor.json`, натисніть на нього, після чого в вікні ще нижче з'явиться напис **"Parameters."**
5. Натиснувши на **"Parameters,"** вам буде доступно основне меню конфігуратора.

# English Version

Before starting work with the ECU, carefully read the [Leaf ECU Manual](https://github.com/Dimonlipko/Leaf-ECU-Configurator/blob/main/Leaf_ecu_manual.pdf), and only after that begin connecting the wiring, after which install the configuration program.

Check for current updates on this page, as the project is still being developed and new features are being added to the old controllers.

## Program for configuring and monitoring the parameters of the Leaf motor control unit.

### Installation:
1. Install `ddt4all` by running `ddt4all-installer.exe`.
2. After successful installation, place the 3 files: `Leaf_motor.json`, `Leaf_motor.json.layout`, `Leaf_motor.json.targets` in the `json` folder of the ddt4all program directory.
3. Place the file `ddt4all-FirmwareReceiver.py` in the `ddtplugins` folder of the ddt4all program directory.

### Launch:
On the first launch, you need to establish a connection with the ELM327 in the Bluetooth settings of your computer. The PIN code for pairing with the Bluetooth ELM327 is usually `1234`, or connect to the Wi-Fi hotspot if you have the Wi-Fi version of ELM327.

1. On the desktop, launch the `ddt4all` shortcut or find it in the program folder.
2. In the opened window, select the virtual COM port and click on the Bluetooth symbol if it’s the Bluetooth version of ELM, or select Wi-Fi. Do not change the port settings, check the box, and click **"Connect."**
3. After connecting, the main program window will open. In the right menu, select the **"Custom"** tab, and `Leaf_motor.json` will appear below.
4. In the empty window below, the text `Leaf_motor.json` will appear; click on it, and then in the window even lower, the text **"Parameters"** will appear.
5. By clicking on **"Parameters,"** you will have access to the main menu of the configurator.

<img width="247" alt="ddt4all_start" src="https://user-images.githubusercontent.com/59143371/122483083-7785a700-cfda-11eb-992d-a0595c69222d.PNG">

<img width="960" alt="ddt4all" src="https://user-images.githubusercontent.com/59143371/122482928-2b3a6700-cfda-11eb-80e5-947424c3b8d6.PNG">
