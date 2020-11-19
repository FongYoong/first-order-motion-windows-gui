# first-order-motion-windows-gui
* All credits to the creators of the popular [First-Order-Motion model](https://aliaksandrsiarohin.github.io/first-order-model-website/)
* A simple Windows GUI coded in Tkinter(Tk) Python to interface with the Pytorch model
* Pretty much a lazy effort to quickly setup this tool conveniently
* [main_gui.py](https://github.com/FongYoong/first-order-motion-windows-gui/blob/master/first-order-model/main_gui.py) contains the main Tk code and initiates network inference. It has not been refactored and pretty messy 😬.
* Only [demo.py](https://github.com/FongYoong/first-order-motion-windows-gui/blob/master/first-order-model/demo.py) and [animate.py](https://github.com/FongYoong/first-order-motion-windows-gui/blob/master/first-order-model/animate.py) from the [original repo](https://github.com/AliaksandrSiarohin/first-order-model) are modified to interface with Tk.
* [start.bat](https://github.com/FongYoong/first-order-motion-windows-gui/blob/master/start.bat) activates the virtual environment and initiates the GUI.
* [start.exe](https://github.com/FongYoong/first-order-motion-windows-gui/blob/master/start.exe) is an executable version of the batch script which does not show the console. Compiled using [this](https://blindhelp.net/software/bat-exe-converter-2480).
* [hide.vbs](https://github.com/FongYoong/first-order-motion-windows-gui/blob/master/hide.vbs) executes [start.bat](https://github.com/FongYoong/first-order-motion-windows-gui/blob/master/start.bat) without showing the console/terminal. It is included here as a backup and is not required.
* [Inno Setup](https://jrsoftware.org/isinfo.php) is used to package the required files into one the [executable file](release link). The [configuration file](https://github.com/FongYoong/first-order-motion-windows-gui/blob/master/inno-setup/first-order-motion-windows-gui.iss) is included in this repo.

***

# Installation

* Install via the executable file which goes through a typical Windows graphical installation process.
* The current release (~1.3 GB after extraction) bundles a 64-bit virtual Python 3.7.5 environment, Pytorch scripts and weights for the Pytorch network.
* No Linux or Mac support because laziness, and the virtual Python environment only includes Windows variants of the required modules
* Current release only includes the CPU version of Pytorch 1.0.0.
* No CUDA support yet because the cudatoolkit version depends on the CUDA version installed in the system. Note to self: write a script to check for CUDA availability and then install appropriate CUDA dependencies.
* Consequently, the current release without CUDA is [slow as heck](https://tenor.com/view/its-been-84-years-titanic-gif-5372593).
* Docker is not considered because Windows installation is troublesome, but could solve cross-platform issues.

***

#Examples

![](https://i.ibb.co/L9vDzzs/1.png?raw=true)
***
![](https://i.ibb.co/tBY27m4/2.png?raw=true)