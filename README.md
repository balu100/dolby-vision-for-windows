# DVFW (Dolby Vision For Windows)

Welcome to the DVFW GitHub repository! This project aims to help users get Dolby Vision working on PCs. Contributions are welcome to improve and refine the process.

### Updates

2025.03.30 - Waiting for the new "Use Dolby Vision Mode" setting in the latest Windows 11 Insider Dev build. If it drops, I'll be sure to update the guide.
2025.04.01 - KB5053656 - [Display kernel] Fixed: This update addresses an issue affecting High Dynamic Range (HDR) content playback on Dolby Vision capable displays, where users might see regular HDR instead of Dolby Vision, missing specific content indicators.

## Current Best Known Guide

Follow these steps to enable Dolby Vision on your PC:

### Prerequisites

1. Download and install [Dolby Vision Extensions](https://www.microsoft.com/en-gb/p/dolby-vision-extensions/9pltg1lwphlf) and [HEVC Video Extensions](https://apps.microsoft.com/detail/9NMZLZ57R3T7?hl=en-US&gl=US).

### Steps

1. Download [Custom Resolution Utility (CRU)](https://www.monitortests.com/forum/Thread-Custom-Resolution-Utility-CRU).
2. Open CRU.
3. Select your display from the dropdown menu.
4. Export the current EDID to a file (e.g., `dolbyvisionmonitor.bin`).
5. Download [AW EDID Editor](https://www.analogway.com/emea/products/software-tools/aw-edid-editor/).
6. Open AW EDID Editor.
7. Open the exported EDID file (`dolbyvisionmonitor.bin`).
8. Navigate to the Vendor-Specific Video section.
9. Edit the Payload (HEX String).
    1. Below are some known, pre-computed (`original` -> `updated`) values:
        * `480376825e6d95` -> `480377825e6d95` (LG C1)
        * `480a7e86607694` -> `480a7f86607694` (LG C2)
        * `4d4e4a725a7776` -> `4d4e4b725a7776` (TCL C825)
        * `48039e5898aa5c` -> `48039f5898aa5c` (Sony A95L)
        * `4403609248458f` -> `4403619248458f` (unknown model of Sony Bravia)
    1. If your hex string is not listed above, then compute it via:
        ```shell
        python.exe enable_dolby_vision_hdmi.py __HEX_STRING__
        ```
    1. (If you want to dive deeper into the hex string config, consult [dolby_vsvdb_calc.xlsm](./dolby_vsvdb_calc.xlsm) from [here](https://discourse.coreelec.org/t/edid-override-injecting-a-dolby-vsvdb-block/51510?page=1)).
10. Save the edited EDID as a new file (e.g., `fixeddolbyvisionmonitor.bin`).
11. Open CRU again.
12. Import the edited EDID file (`fixeddolbyvisionmonitor.bin`).
13. Run `Restart64.exe` or `Restart.exe` found in the CRU folder to apply the changes.

## Screenshots

![App Screenshot](https://raw.githubusercontent.com/balu100/dolby-vision-for-windows/main/app.png)
![Display Settings Screenshot](https://raw.githubusercontent.com/balu100/dolby-vision-for-windows/main/displaysettings.png)

## Acknowledgements

- Special thanks to [dogelition](https://linustechtips.com/topic/1145733-get-dolby-vision-instead-of-hdr10-on-windows-10/?do=findComment&comment=16314256) for the initial guide.
- Thanks to [djnice](https://github.com/balu100/dolby-vision-for-windows/issues/1) for the VSVDB Calc tool.
