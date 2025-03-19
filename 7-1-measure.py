import RPi.GPIO as gpio
import time
import matplotlib.pyplot as plt
#инициализация пинов
dac    = [8, 11, 7, 1, 0, 5, 12, 6]
comp   = 14
troyka = 13
leds   = [2, 3, 4, 17, 27, 22, 10, 9]
#настройка ввода и вывода
gpio.setmode(gpio.BCM)
gpio.setup(dac, gpio.OUT)
gpio.setup(troyka, gpio.OUT, initial = 0)
gpio.setup(comp, gpio.IN)
gpio.setup(leds, gpio.OUT)
#функция перевода десятичного числа в двочный список
def dec_to_bin(val):
    return [int(bit) for bit in bin(val)[2:].zfill(8)]
#функция измерения напряжения с ацп
def adc():
    val = 0
    for i in range(7, -1, -1):
        val += 2 ** i
        val_out = dec_to_bin(val)
        gpio.output(dac, val_out)
        time.sleep(0.001)
        val_in = gpio.input(comp)
        if val_in:
            val -= 2 ** i
    return val
#включения диодов в зависимости от входного списка
def light_up(val):
    num_led = int(val / 256 * 8)
    for i in range(8):
        gpio.output(leds[i], 1 if i < num_led else 0)
        #if i < num_led:
         #   gpio.output(leds[i], 1)
        #else:
         #   gpio.output(leds[i], 0)
#напряжения на тройке
def measure_voltage():
    return adc() * 3.3 / 256

def showVoltage(voltage : float):
    voltage_int = int(voltage * 256 / 3.3)
    gpio.output(leds, dec_to_bin(voltage_int))
    
#основной блок
try:
    measure = []            #хранение измерений
    start_charge = time.time()
    start        = time.time()

    #начало зарядки
    gpio.output(troyka, 1)
    voltage = measure_voltage()
    print("начало зарядки")
    while (voltage < 3.3 * 0.8):
        showVoltage(voltage)
        measure.append(voltage)
        #light_up(int(voltage / 3.3 * 256))
        #print(f"percent of charge : {voltage / 3.3 * 100:.4} %")
        #if voltage >= 3.3 * 0.80:
        #    break
        time.sleep(0.0005)
        voltage = measure_voltage()

    end_charge = time.time()
    start_dis  = time.time()   

    #разрядка 
    voltage = measure_voltage()
    gpio.output(troyka, 0)
    print("разрядка")

    while (voltage > 3.3 * 0.05):
        showVoltage(voltage)
        measure.append(voltage)
        #light_up(int(voltage / 3.3 * 256))
        #print(f"percent of discharge {voltage:.2}%")
        #if voltage <= 3.3 * 0.05:
        #    break
        time.sleep(0.0005)
        voltage = measure_voltage()

    end_dis = time.time()
    end = time.time()

    #рассчет времени
    alltime     = end - start
    time_charge = end_charge - start_charge
    time_dis    = end_dis - start_dis

    #открытие файда дата
    with open("data.txt", "w") as file:
        for val in measure:
            file.write(f"{val}\n")

    #подсчет дискретизации
    sampling_rate = len(measure) / alltime

    #подсчет шага квантования
    quant_step = 3.3 / 256

    #открытие файла
    with open("settings.txt", "w") as file:
        file.write(f"средняя частота дискретизации : {sampling_rate:.2f} Гц/n")
        file.write(f"Шаг квантования ацп : {quant_step:.4f} B/n")

    #график зависиомти вальт от номера измерения
    plt.plot(measure)
    plt.title("напряжение от времени")
    plt.xlabel("номер измерения")
    plt.ylabel("Напряжения в В")
    plt.show()

    print(f"продолжительность {alltime:.2f} c")
    print(f"средняя частота дискретизации {sampling_rate:.2f} Гц")
    print(f"колличество одного измерения {len(measure):.4f}")
    print(f"Шаг квантования ацп: {quant_step:.4f} B")
    print(f"time of charge {time_charge} c")
    print(f"time of discharge {time_dis}")

finally:
    gpio.output(dac, 0)
    gpio.output(troyka, 0)
    gpio.output(leds, 0)
    gpio.cleanup


