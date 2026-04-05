# CSF-OSINT 🔍
An efficient OSINT framework for analyzing publicly accessible data linked to regional mobile identifiers. Facilitates both individual queries and high-volume batch processing — an essential utility for cybersecurity analysts, academic researchers, and penetration testers.

> **Disclaimer:** This tool is for **educational and research purposes only**.  
> The author does **not** encourage or support illegal use.

---

## Features ✨
- Fetches name, CNIC, and address linked to a number *(if available)*  
- Lookup **single numbers** or **bulk lists**
- Automatically saves bulk results to `results.txt`  

---
## Installation ⚙️
```
git clone https://github.com/Muhammad-Muzammil-Khokhar/CSF-OSINT.git
cd CSF-OSINT
pip install -r requirements.txt
```

## Usage 🚀

`python CSF-OSINT.py -num 03001234567`

`python CSF-OSINT.py -l numbers.txt`
