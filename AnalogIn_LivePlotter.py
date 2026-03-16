import nidaqmx
from nidaqmx.constants import AcquisitionType
from nidaqmx.system import System
from nidaqmx.constants import TerminalConfiguration
import matplotlib.pyplot as plt

"""
This code will live plot data from your DAQ connected to your computer via USB. If you are taking a differential measurement,
e.g, from a load cell, update  terminal_config=TerminalConfiguration.RSE to  terminal_config=TerminalConfiguration.DIFFERENTIAL

To save the plotted figure, click "save" from the plotting GUI or you can keyboard interrupt with several different keystrokes within a short timespan
To stop the plotting, stop the Python script (closing plot will not abort script)
"""
mysystem = System.local()

rate = 1000 # update if your DAQ can't support 1kS/sec

for device in mysystem.devices:
    print(device.name)
    mydaq = device.name

plt.ion()
fig, ax = plt.subplots()

xdata = []
ydata = []
line, = ax.plot([], [])

sample_index = 0

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan(
        f"{mydaq}/ai0",
        terminal_config=TerminalConfiguration.RSE
    )

    task.timing.cfg_samp_clk_timing(
        rate,
        sample_mode=AcquisitionType.CONTINUOUS
    )

    task.start()

    try:
        while True:
            data = task.read(number_of_samples_per_channel=50)
            for v in data:
                xdata.append(sample_index)
                ydata.append(v)
                sample_index += 1
            line.set_data(xdata, ydata)
            ax.relim()
            ax.autoscale_view()
            ax.set_ylabel("Measured voltage (V)", fontsize=14)
            ax.set_xlabel(f"Sample number, rate = {rate} S/s", fontsize=14)
            ax.set_title("Analog input", fontsize=14)
            plt.pause(0.001)
            plt.tight_layout()
    # except KeyboardInterrupt:
    #     pass
    finally:
        task.stop()
plt.show()