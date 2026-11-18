# Custom

Utility scripts and the global `awake` and `cursor` commands for PowerShell / the VSCode terminal.

| Command  | Script              | What it does                                         |
|----------|---------------------|------------------------------------------------------|
| `awake`  | `keep_awake.py`     | Keeps the computer awake (600 min, display on)       |
| `cursor` | `move_cursor_to.py` | Moves the cursor through 3 points, 200 repetitions   |

## Setup

1. Clone the repo (or copy the folder) to a fixed path, for example:
   `C:\Users\<user>\OneDrive - Stellus Rx\Custom`
2. Open the PowerShell profile for all hosts (includes VSCode):

   ```powershell
   New-Item -ItemType File -Force $PROFILE.CurrentUserAllHosts | Out-Null
   code $PROFILE.CurrentUserAllHosts
   ```

3. Paste these functions. **Adjust the path** to wherever the `Custom` folder is:

   ```powershell
   function awake {
       python "C:\Users\<user>\OneDrive - Stellus Rx\Custom\keep_awake.py" --minutes 600 --display @args
   }

   function cursor {
       python "C:\Users\<user>\OneDrive - Stellus Rx\Custom\move_cursor_to.py" --points '[[100,100],[500,300],[900,600]]' --repeat 200 --duration 5 --pause 0.2 @args
   }
   ```

4. Save and open a new terminal in VSCode (or run `. $PROFILE.CurrentUserAllHosts`).
5. Type `awake` or `cursor` from any directory.

## Usage

- Extra arguments are appended: `awake --minutes 120`.
- To stop either command: `Ctrl+C`.

## Troubleshooting

- **"awake" is not recognized**: open a new terminal; the profile loads on startup.
- **Profile does not load (execution policy)**:
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
- **`python` not found**: check with `python --version` that Python is on the PATH.
