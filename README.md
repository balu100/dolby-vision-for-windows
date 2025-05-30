# DVFW (Dolby Vision For Windows)

Welcome to the DVFW GitHub repository! This project aims to help users get Dolby Vision working on PCs. Contributions are welcome to improve and refine the process.

### Updates

2025.03.30 - Waiting for the new "Use Dolby Vision Mode" setting in the latest Windows 11 Insider Dev build. If it drops, I'll be sure to update the guide.

2025.03.31 - KB5053656 - [Display kernel] Fixed: This update addresses an issue affecting High Dynamic Range (HDR) content playback on Dolby Vision capable displays, where users might see regular HDR instead of Dolby Vision, missing specific content indicators.

2025.04.03 [Windows Insider - Use Dolby Vision Mode](https://github.com/balu100/dolby-vision-for-windows/issues/17)


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
        * `480a6e845a6d94` -> `480a6f845a6d94` (LG B2)
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

## Troubleshooting / Advanced Debugging

If you've followed the Guide and Dolby Vision is still not working, or if the `enable_dolby_vision_hdmi.py` script reported that your hex string was "already enabled" but you don't have Dolby Vision in Windows, this section is for you.

The simple LLDV-HDMI flag (toggled by `enable_dolby_vision_hdmi.py`) is necessary but often not sufficient. Other parameters within the 7-byte Dolby Vision VSVDB (Vendor Specific Video Data Block) payload are critical.

We'll use a more comprehensive tool, `VsvdbInfo.py` (available in this repository), to decode, inspect, and modify your VSVDB.

**Steps for Advanced Debugging:**

1.  **Get Your Current VSVDB Hex String:**
    *   If you haven't modified it yet, find this in AW EDID Editor under the "Vendor-Specific Video" section (it's the "Payload").
    *   If you used `enable_dolby_vision_hdmi.py` and it said "already enabled," use that original hex string.

2.  **Download and Run `VsvdbInfo.py`:**
    *   Ensure you have Python installed.
    *   Download `VsvdbInfo.py` from this repository.
    *   Open a command prompt or terminal, navigate to where you saved the script, and run it:
        ```shell
        python VsvdbInfo.py
        ```
    *   When prompted, enter your 7-byte VSVDB hex string.

3.  **Inspect Key Decoded Fields:**
    *   Once the payload is loaded, choose option "1. Show Current VSVDB Info". Pay close attention to the following:
        *   **`Max Display Luminance Index`**: This is CRITICAL. It shows the peak brightness your EDID is reporting.
            *   **Problem Sign:** If this value is very low (e.g., "97 nits", "155 nits") for a display capable of much higher brightness (most HDR TVs are 400-1000+ nits), this is a likely reason DV isn't working. Windows might think your display isn't bright enough for HDR/DV.
            *   **Typical Good Values:** For an LG OLED, this should ideally report around 700-800+ nits (e.g., Index 14 for 807 nits, Index 25 for 4060 nits if using a high value from some common EDIDs, though 807 nits is a safer bet for compatibility).
        *   **`DM Version Bits`**: Should typically be `3.x` or `4.x`.
        *   **`DV Mode Bits`**: Ensure this reflects a valid mode, including LLDV if that's your goal (e.g., "Std + LLDV + LLDV-HDMI" or "LLDV + LLDV-HDMI").
        *   **`Min Display Luminance Index`**: Should be a low value, appropriate for your display's black level (e.g., 0.001 nits, 0.005 nits).
        *   **`Color Primary Coordinate Bits` (Gx, Gy, Rx, Ry, Bx, By)**: These define the color gamut. While the Max Luminance is often the first blocker, incorrect gamut information could also cause issues. You can compare these to known presets like BT.2020 if problems persist after fixing luminance. The `VsvdbInfo.py` script has a BT.2020 preset based on common examples.

4.  **Modify Fields if Necessary:**
    *   If you identify an incorrect field (especially Max Display Luminance), use option "2. Modify VSVDB Fields" in `VsvdbInfo.py`.
    *   Select the field to change and enter the correct value. For luminance, the script allows you to pick from a table of nits values.
    *   After modification, the script will show the new hex payload. **Copy this new hex string.**

5.  **Apply the Corrected VSVDB:**
    *   Go back to AW EDID Editor, open your exported EDID file (`dolbyvisionmonitor.bin`).
    *   Navigate to the Vendor-Specific Video section.
    *   Replace the old Payload (HEX String) with your **newly generated hex string** from `VsvdbInfo.py`.
    *   Save the edited EDID as a new file (e.g., `fixeddolbyvisionmonitor_advanced.bin`).
    *   Open CRU, import this new EDID file, and run `Restart64.exe` (or `Restart.exe`).

6.  **Test Again:** Check Windows Advanced Display Settings for Dolby Vision certification.

**If Still Not Working:**
When opening a new issue on GitHub, please include:
*   Your original VSVDB hex string.
*   The **full decoded output** from `VsvdbInfo.py` for your original string.
*   Any modifications you made and the resulting new hex string.
*   Details about your display model, GPU, and how you are applying the EDID.

This detailed information will significantly help in diagnosing the problem.

## Acknowledgements

- Special thanks to [dogelition](https://linustechtips.com/topic/1145733-get-dolby-vision-instead-of-hdr10-on-windows-10/?do=findComment&comment=16314256) for the initial guide.
- Thanks to [djnice](https://github.com/balu100/dolby-vision-for-windows/issues/1) for the VSVDB Calc tool.
