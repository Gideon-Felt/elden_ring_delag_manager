# Disclaimer
**all resources are Unofficial**

# Elden Ring EAC Manager, and VKD3D patch manager
I wanted to create a simple way to manage EAC, and also check that it was on or off quickly to ensure any mod <br>
I implemented wasn't gonna trigger a ban. and I also implemented a simple way to toggle a VKD3D patch from
[soupsteam](https://github.com/soupstream/EldenRingStutterFix) <br>
soupstream suggests using [Special K](https://discourse.differentk.fyi/t/download-special-k/1461) 
as they implement the same fix and many others
but I didn't want to have such a complex <br>
solution installed on-top my game just to convert the dx12 api to vulkan.
I've had great success with soupstream's patch, and am now able to <br>
run my game at max performance settings whereas before I had stuttering when attempting those settings.<br>
I may add alternate tweak additions to this project to add more features or better *delag solutions*,
but I'm not sure if I'll do that yet.<br>
Feel free to fork this and add on as many features as you want,
the main benefit being the EAC monitoring<br>
and the warning system if you try to run EAC with the other tweaks enabled.<br>
PR's are also welcome.

# Installation
1. Download the [latest release](https://github.com/Gideon-Felt/elden_ring_delag_manager/releases/latest)
2. Extract zip file to your desired location
3. run ER_EAC_VKD3D.exe

# Build from source
1. install poetry via `pip install poetry`
2. install dependencies via `poetry install`
3. run `auto-py-to-exe` and configure the build however you like.
<br> alternatively you can use `python main.py` to run the program without the build.

