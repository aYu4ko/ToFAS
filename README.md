# ⚔️ ToFAS: Tower of Fantasy Automation Script

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv&logoColor=white)
![Status](https://img.shields.io/badge/Status-Archived%20%2F%20Unmaintained-red?style=for-the-badge)

> **⚠️ NOTICE: THIS PROJECT IS NO LONGER MAINTAINED ⚠️**  
> This automation project has been officially archived and is no longer receiving actively developed updates, bug fixes, or compatibility patches. Because *Tower of Fantasy* frequently updates its game client, UI scaling, and graphics engine, this script may no longer work out-of-the-box.  
> 
> This repository remains public as an **open-source educational reference** for developers interested in desktop Robotic Process Automation (RPA), OpenCV template matching, and Win32 COM spreadsheet integration! Feel free to fork and adapt the code for your own coding adventures!

---

## 📖 About The Project

**ToFAS** is an autonomous desktop workflow and Robotic Process Automation (RPA) tool designed to eliminate the daily manual farming grind in *Tower of Fantasy*. 

Instead of using blind, fragile time delays or hardcoded screen coordinates, ToFAS utilizes a resilient **Computer Vision detection engine** powered by **OpenCV**. It dynamically identifies in-game UI elements, scales to window geometry, handles slow loading screens, and autonomously tracks task completion across **20+ profile accounts** in real-time via Microsoft Excel!

---

## ✨ Key Features

* 👁️ **Resilient Visual Detection Engine:** Uses OpenCV template matching (`cv2.TM_CCOEFF_NORMED`) with dynamic threshold scaling and automated retry loops, achieving high UI recognition accuracy even during latency spikes or visual effects.
* 📊 **Real-Time Excel State Tracking:** Integrates directly with spreadsheets via **Win32 COM objects** and **Pandas**. It dynamically reads login credentials and logs daily task milestones row-by-row without manual database setup.
* 🔄 **Multi-Account Profile Rotation:** Fully automates logging in, executing daily routines, logging out, and switching to the next account seamlessly across 20+ distinct configurations.
* 🛡️ **Fail-Safe Exception Handling:** Equipped with customized keyboard-interrupt (`Ctrl+C`) catching and error-leniency fallbacks to ensure workbook states are safely saved before script termination.
* ⚡ **Comprehensive Daily Task Coverage:**
  * 🎁 **Supply Run:** Auto-claims daily login rewards and summer welfare packages.
  * 🍜 **Mia's Kitchen:** Navigates to the kitchen, tastes food, and clears dialogs.
  * ⚔️ **Vitality / Dimensional Trials:** Selects Quick Battle, executes runs, and confirms operation success.
  * 🏰 **Bygone Phantasm & Oldman:** Handles level skipping and weekly challenge checks.
  * 📬 **Mailbox & Guild:** Auto-claims all attached mail, deletes read messages, and submits daily crew donations.
  * 🛒 **Weekly Shop:** Purchases monthly/weekly Synthesia boxes, Augment factors, and Spacetime store modules.

---

## 🛠️ Technical Stack

| Tool / Library | Role in the Pipeline |
| :--- | :--- |
| **Python 3.x** | Core application logic and automation architecture |
| **OpenCV (`cv2`)** | Visual template matching, thresholding, and UI image recognition |
| **PyAutoGUI & PyGetWindow** | Mouse/keyboard simulation, window focusing, and geometry calibration |
| **Pandas & NumPy** | Data manipulation, array processing for coordinates, and credential indexing |
| **Win32 COM (`win32com.client`)** | Real-time background integration with active Microsoft Excel workbooks |

---

## 🚀 How It Worked (Setup & Architecture)

For developers analyzing the codebase, here is how the local environment was structured:

### 1. Prerequisites
Ensure you have Python installed along with the required libraries:
```bash
pip install opencv-python numpy pandas pyautogui pygetwindow pywin32 openpyxl
```

### 2. Directory Structure
The script relies on local assets and spreadsheets placed in the root execution directory:
* `/images/`: Contains target UI `.png` templates used by OpenCV for matching.
* `/temp/`: A temporary workspace for capturing real-time screen slices (auto-cleaned on exit).
* `accounts.xlsx`: A structured spreadsheet containing `ign`, `email`, `password`, and dynamically updated status columns (`daily dono`, `dimensional trials`, `supply run`).

### 3. Execution
To launch the automation pipeline:
```bash
python main.py
```
*(Note: The script automatically calibrates the game window to a `720x480` resolution anchor before initiating visual scanning!)*

---

## 📝 License & Disclaimer

This project was created for **educational purposes only**. Automated scripting and macro usage may violate the Terms of Service (ToS) of online multiplayer games. The creator assumes no liability for account penalties, suspensions, or software incompatibilities resulting from the use of this code. Use at your own risk!
