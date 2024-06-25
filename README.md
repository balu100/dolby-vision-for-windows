# DVFW (Dolby Vision For Windows)

Welcome to the DVFW GitHub repository! This project aims to help users get Dolby Vision working on PCs. Contributions are welcome to improve and refine the process.

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
9. Edit the hex string. For example, if you own an LG C1, change the hex string from `480376825e6d95` to `480377825e6d95`. If your string is different, use [VSVDB Calc](https://discourse.coreelec.org/uploads/short-url/uJlVOw1StIgxqJnJyKuGwlC57vQ.xlsm) to calculate the correct value.
10. Save the edited EDID as a new file (e.g., `fixeddolbyvisionmonitor.bin`).
11. Open CRU again.
12. Import the edited EDID file (`fixeddolbyvisionmonitor.bin`).
13. Run `Restart64.exe` or `Restart.exe` found in the CRU folder to apply the changes.

### Pre-Edited EDID for LG C1

If you own an LG C1, you can use the pre-edited EDID file and skip to steps 11-13:

- [Download fixeddolbyvisionmonitor.bin](https://github.com/balu100/dolby-vision-for-windows/raw/main/fixeddolbyvisionmonitor.bin)

## Screenshots

![App Screenshot](https://raw.githubusercontent.com/balu100/dolby-vision-for-windows/main/app.png)
![Display Settings Screenshot](https://raw.githubusercontent.com/balu100/dolby-vision-for-windows/main/displaysettings.png)

## Acknowledgements

- Special thanks to [dogelition](https://linustechtips.com/topic/1145733-get-dolby-vision-instead-of-hdr10-on-windows-10/?do=findComment&comment=16314256) for the initial guide.
- Thanks to [djnice](https://github.com/balu100/dolby-vision-for-windows/issues/1) for the VSVDB Calc tool.
