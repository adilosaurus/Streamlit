import threading
import time
import matplotlib.pyplot as plt
import streamlit as st
from Backend_Monza import helmsensor, extrakoeling

current_helmtemperatuur = None  # Initialize the variable globally

def update_pie_chart(helmtemperatuur):
    labels = ['Helmtemperatuur']
    sizes = [helmtemperatuur]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='', startangle=90, colors=['#1F77B4'])
    ax.text(0, 0, f'{helmtemperatuur:.2f} °C', ha='center', va='center', fontsize=12, color='#FFFFFF')

    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular

    plt.close(fig)  # Explicitly close the figure to avoid the warning

    return fig

def update_chart_thread(chart_placeholder, generator):
    global current_helmtemperatuur  # Declare as global
    while True:
        current_helmtemperatuur = next(generator)
        chart_placeholder.pyplot(update_pie_chart(current_helmtemperatuur))
        time.sleep(1)

def main():
    global current_helmtemperatuur

    st.title("Real-time Helmtemperatuur Monitor")

    helm_generator = helmsensor()
    koeling_generator = extrakoeling(current_helmtemperatuur)
    # Display the initial chart
    chart_placeholder = st.empty()
    chart_placeholder.pyplot(update_pie_chart(next(helm_generator)))

    # Create the "Extra Koeling" button outside the loop
    extra_koeling_button = st.button("Extra Koeling")

    # Main loop to update the chart with the helmtemperatuur
    t = True
    while t :
        current_helmtemperatuur = next(helm_generator)
        chart_placeholder.pyplot(update_pie_chart(current_helmtemperatuur))
        time.sleep(1)
        # Bij indrukken van de knop, moeten het temperatuur bereik dalen volgens de functie def extrakoeling in Backend_Monza.py
        if extra_koeling_button:
            # Update the html bestand
            while True:
                chart_placeholder.pyplot(update_pie_chart(current_helmtemperatuur))

                # Start
                thread = threading.Thread(target=extrakoeling, args=current_helmtemperatuur)
                thread.start()
                # refresh
                time.sleep(1)

if __name__ == "__main__":
    main()
