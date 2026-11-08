# Web UI tests with Playwright

## Setup

Run all commands from the `WebUI` folder.

1. Create a virtual environment:

   macOS / Linux:

   ```bash
   python3 -m venv .venv
   ```

   Windows:

   ```powershell
   python -m venv .venv
   ```

2. Activate it (`(.venv)` will appear at the start of the terminal prompt):

   macOS / Linux:

   ```bash
   source .venv/bin/activate
   ```

   Windows (PowerShell/bat):

   ```powershell
   .venv\Scripts\Activate.ps1
   ```


3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Download the browser for Playwright:

   macOS / Windows:

   ```bash
   playwright install chromium
   ```

   Linux (also installs the system libraries the browser needs; may ask for `sudo`):

   ```bash
   playwright install --with-deps chromium
   ```

## Running the tests

The virtual environment must be active before running (see step 2).
The commands are the same on macOS, Linux and Windows:

```bash
pytest
pytest --headed --slowmo 500
pytest -k about
```

Without activating the environment, call pytest from `.venv` directly:

macOS / Linux:

```bash
.venv/bin/pytest
```

Windows:

```powershell
.venv\Scripts\pytest
```
