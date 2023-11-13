# Grenswaarden voor het meldingscentrum !!
import random

#HelmTemperatuur in graden Celcius:
helmmmin_temp = 0.0
helmmax_temp = 66.0

#Hartslagfrequentie:
hartslagfreqmin = 60
harstlagfreqmax = 100

#Ademhalingfrequentie:
ademhalingfreqmin = 60
ademhalingfreqmax = 100

#LichaamsTemperatuur in graden Celcius
lichaammin_tempc = 36.0
lichaammax_tempc = 39.0

#LichaamsVocht (mannen) in procenten:
lichaamsvocht_procentmin = 50.0
lichaamsvocht_procentmax = 70.0

import time

start = time.time()
delta = 0
global helmtemperatuur

def tijd():
    global start, eind, delta
    eind = time.time()
    delta = eind - start
    start_format = time.strftime("%H:%M:%S", time.localtime(start))
    end_format = time.strftime("%H:%M:%S", time.localtime(eind))
    interval_format = time.strftime("%H:%M:%S", time.gmtime(delta))

    return start_format, end_format, interval_format

def print_per_seconde():
    p = True
    while p:
        time.sleep(1)
        start_format, end_format, rounded_interval, = tijd()
        print(f"Start: {start_format}, Eind: {end_format}, Duratie: {rounded_interval}")

def helmsensor():
    global helmtemperatuur
    maximum = 66.0
    minimum = 0.0
    deltavoorbeeld = 60

    while True:
        time.sleep(1)
        start_format, end_format, interval_format = tijd()
        hours, minutes, seconds = map(int, interval_format.split(':'))
        interval_seconds = hours * 3600 + minutes * 60 + seconds
        if delta <= deltavoorbeeld:
            helmtemperatuur = (helmmax_temp / deltavoorbeeld) * interval_seconds
        else:
            helmtemperatuur = helmmax_temp

        # print(f"Tijd: {interval_format}, Helmtemperatuur: {helmtemperatuur:.2f} °C")
        # gebruik yield omdat je meerdere keren moet returnen !!
        yield helmtemperatuur
        #st.write(f"Tijd: {interval_format}, Helmtemperatuur: {helmtemperatuur:.2f} °C:")

def monitorcentrum():
    # zie Grenswaarden bovenaan !!
    global hartslagfreq, ademhalingfreq, lichaamstemperatuur, lichaamsvocht

    while True:
        time.sleep(1)
        #Grenswaarden !!
        if hartslagfreq < hartslagfreqmin or hartslagfreq > harstlagfreqmax:
            print(f"afwijking harstlag ! :{hartslagfreq}")
        elif ademhalingfreq < ademhalingfreqmin or ademhalingfreq > ademhalingfreqmax:
            print(f"afwijking ademhaling ! :{ademhalingfreq}")
        elif helmtemperatuur < helmmmin_temp or helmtemperatuur > helmmax_temp:
            print(f"afwijking helmtemperatuur ! :{helmtemperatuur}")
        elif lichaamstemperatuur < lichaammin_tempc or lichaamstemperatuur > lichaammax_tempc:
            print(f"afwijking lichaamstemperatuur ! :{lichaamstemperatuur}")
        elif lichaamsvocht < lichaamsvocht_procentmin or lichaamsvocht > lichaamsvocht_procentmax:
            print(f"afwijking lichaamsvocht% ! :{lichaamsvocht}")

def extrakoeling(args):
    import streamlit as st
    import matplotlib.pyplot as plt
    #maximum en minimum bereik veranderen bij extra koeling
    # melding zou moeten wegvallen, en temperatuur moet stabiliseren.
    helmtemperatuur = args
    mintemp = 40.0
    maxtemp = 55.0
    while helmtemperatuur > mintemp:
        helmtemperatuur = helmtemperatuur - 1.5
        helmtemperatuur = helmtemperatuur + random.uniform(-1.0, 1.0)
        helmtemperatuur = max(mintemp, min(maxtemp, helmtemperatuur))
        yield helmtemperatuur
        # plt.close(fig)  # Close the figure to avoid warning
        #
        # time.sleep(1.5)
        #st.text(f"Helmtemperatuur: {helmtemperatuur:.2f} °C")
        #chart_placeholder.pyplot(update_pie_chart(helmtemperatuur))
        #print(f"Helmtemperatuur: {helmtemperatuur:.2f} °")
        time.sleep(1.5)

def weerinfo():
    return None


helmsensor()
