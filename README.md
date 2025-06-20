# Startup Mode Selector

This Python script creates a graphical interface using PyQt5 that allows the user to choose between launching applications in "Console Mode" (similar to Steam Big Picture) or "Desktop Mode" (running explorer.exe and other desktop applications). The script reads a configuration file (`config.ini`) to determine which applications to launch in each mode. By default, it will launch Console Mode after a 3-second countdown unless the user presses the Enter key to switch to Desktop Mode.

## Features
- Displays a semi-transparent, borderless window with a countdown timer.
- Reads application paths from a `config.ini` file for Console and Desktop modes.
- Automatically kills `explorer.exe` in Console Mode for a full-screen experience.
- Logs execution details to a file (`startup_mode_log.txt`) for debugging.
- Allows users to press Enter to switch to Desktop Mode during the countdown.

## Prerequisites
- Python 3.6 or higher
- PyQt5 (`pip install PyQt5`)
- PyInstaller (for converting to .exe, `pip install pyinstaller`)
- Windows operating system (for `explorer.exe` integration and registry modifications)

## Installation
1. Clone or download the script to your local machine.
2. Install the required Python packages:
   ```bash
   pip install PyQt5 pyinstaller
   ```
3. Create a `config.ini` file in the same directory as the script with the following structure:
   ```ini
   [consoleMode]
   1 = C:\path\to\console_app1.exe
   2 = C:\path\to\console_app2.exe

   [desktopMode]
   1 = C:\path\to\desktop_app1.exe
   2 = C:\Windows\explorer.exe
   ```
   - Replace the paths with the actual applications you want to launch in each mode.
   - Ensure the keys (e.g., `1`, `2`) are numeric and sequential for proper sorting.

## Converting to Executable
To convert the script to a single executable file (`.exe`) without a console window, use PyInstaller with the following command:
```bash
pyinstaller --noconsole --onefile startup_mode_selector.py
```
- `--noconsole`: Prevents the console window from appearing when running the .exe.
- `--onefile`: Packages the script and its dependencies into a single executable file.
- The output executable will be located in the `dist` folder.

**Note**: Ensure `config.ini` is placed in the same directory as the generated `.exe` for it to work correctly.

## Replacing the Windows Shell
To replace the default Windows shell (explorer.exe) with this script, follow these steps to modify the registry:

1. Log in to a Windows user account with administrative privileges (different from the target user).
2. Open `regedit.exe`.
3. Go to the **File** menu and select **Load Hive**.
4. Navigate to the target user's profile directory (e.g., `C:\Users\myUser\`).
5. Select the `ntuser.dat` file and load it, giving it a temporary name (e.g., `TempHive`).
6. Navigate to the following registry path:
   ```
   HKEY_USERS\TempHive\Software\Microsoft\Windows NT\CurrentVersion\Winlogon
   ```
7. Create a new **String Value** named `Shell`.
8. Set its value to the full path of the generated `.exe` (e.g., `C:\path\to\startup_mode_selector.exe`).
9. Go to the **File** menu and select **Unload Hive** to save changes.
10. Log out and log back in as the target user to apply the new shell.

The script will now run automatically when the user logs in, replacing the default Windows shell.

## Usage
1. Ensure `config.ini` is properly configured with the paths to the applications for Console Mode and Desktop Mode.
2. Run the script (or the generated `.exe`).
3. A window will appear with a 3-second countdown:
   - **Default (Console Mode)**: After 3 seconds, the script will terminate `explorer.exe` and launch the applications listed in the `[consoleMode]` section of `config.ini`.
   - **Desktop Mode**: Press the **Enter** key during the countdown to launch the applications listed in the `[desktopMode]` section (typically including `explorer.exe` for the standard Windows desktop).
4. The script logs all actions to `startup_mode_log.txt` in the same directory for debugging purposes.

## Functionality
The script provides a simple way to choose between two startup modes:
- **Console Mode**: Designed for a full-screen, console-like experience (e.g., launching a gaming frontend like Steam Big Picture). It terminates the Windows Explorer process (`explorer.exe`) and launches the specified console applications.
- **Desktop Mode**: Launches the standard Windows desktop environment (typically by starting `explorer.exe`) along with other specified desktop applications.

This is useful for creating a kiosk-like or gaming-focused setup where the user can choose between a streamlined console interface or the standard Windows desktop.

## Troubleshooting
- **Error: `config.ini` not found or invalid**: Ensure `config.ini` exists in the same directory as the script or `.exe` and is properly formatted.
- **Applications not launching**: Verify that the paths in `config.ini` are correct and that the applications are accessible.
- **Registry modification issues**: Ensure you have administrative privileges and are loading the correct `ntuser.dat` file for the target user.
- Check `startup_mode_log.txt` for detailed error messages and execution logs.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
