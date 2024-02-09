# DVFW (Dolby Vision For Windows)

This github repo was made so anyone can contribute to get Dolby Vision working on PCs

Current best known guide:

0. Download [Dolby Vision Extensions](https://www.microsoft.com/en-gb/p/dolby-vision-extensions/9pltg1lwphlf) and [HEVC Video Extensions](https://apps.microsoft.com/detail/9NMZLZ57R3T7?hl=en-US&gl=US)
1. Download [CRU](https://www.monitortests.com/forum/Thread-Custom-Resolution-Utility-CRU)
2. Open CRU
3. Select the display from the dropdown menu
4. Export (dolbyvisionmonitor.bin)
5. Download [AW EDID Editor](https://www.analogway.com/emea/products/software-tools/aw-edid-editor/)
6. Open AW EDID Editor
6. Open the exported bin file (dolbyvisionmonitor.bin)
7. Click on the Vendor-Specific Video
8. Edit the hex string (i own a lg c1 so my hex string was 480376825e6d95 and i changed it to 480377825e6d95)
9. Save As (fixeddolbyvisionmonitor.bin)
10. Open CRU
11. Import the edited bin file (fixeddolbyvisionmonitor.bin)
12. Run Restart64.exe/Restart.exe inside of the cru folder

Uploaded mine [fixeddolbyvisionmonitor.bin](https://github.com/balu100/dolby-vision-for-windows/raw/main/fixeddolbyvisionmonitor.bin) so you only need to do 10-12 steps (LG C1)

![alt text](https://raw.githubusercontent.com/balu100/dolby-vision-for-windows/main/app.png)
![alt text](https://raw.githubusercontent.com/balu100/dolby-vision-for-windows/main/displaysettings.png)

[Thanks to dogelition](https://linustechtips.com/topic/1145733-get-dolby-vision-instead-of-hdr10-on-windows-10/?do=findComment&comment=16314256](https://linustechtips.com/topic/1145733-get-dolby-vision-instead-of-hdr10-on-windows-10/?do=findComment&comment=16297672)https://linustechtips.com/topic/1145733-get-dolby-vision-instead-of-hdr10-on-windows-10/?do=findComment&comment=16297672)
