# TorPull

**TorPull** is a Python script designed to mass-download files from `.onion` websites using the Tor network. It connects to a specific public disclosures API and recursively downloads files and subdirectories.

## 🧰 Features

- Connects through Tor (SOCKS5 proxy on port 9050)
- Works with `.onion` domains
- Recursively crawls public API directories
- Saves files locally to `downloads/` folder
- Uses Selenium + Chrome headless for automation
- Uses `requests` for fast file transfers

## 🚀 Requirements

- Python 3.x
- Chrome + ChromeDriver installed
- Tor must be running on `localhost:9050`
- Python modules:
  - `requests`
  - `selenium`

Install dependencies:

```bash
pip install requests selenium

## 📦 Usage

1. Start the Tor service (Tor Browser or `tor`)
2. Run the script:

```bash
python TorPull.py

## ⚠️ Disclaimer

This script is intended for ethical use only. Do not use it on services or data you don’t have permission to access.

---

## 👤 Author

Harry Matthews – [@Hgmatthews](https://github.com/Hgmatthews)
