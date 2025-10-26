


```
  ███╗   ███╗ ██████╗  ██████╗ ██████╗ ██╗   ██╗
  ████╗ ████║██╔═══██╗██╔═══██╗██╔══██╗╚██╗ ██╔╝
  ██╔████╔██║██║   ██║██║   ██║██║  ██║ ╚████╔╝ 
  ██║╚██╔╝██║██║   ██║██║   ██║██║  ██║  ╚██╔╝  
  ██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██████╔╝   ██║   
  ╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝    ╚═╝   
```

<div align="center">

![Status](https://img.shields.io/badge/status-active-success.svg)
![Purpose](https://img.shields.io/badge/purpose-educational-blue.svg)
![Security](https://img.shields.io/badge/security-ethical%20testing%20only-critical.svg)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)

**A controlled sandbox for ethical payload research and penetration testing education**

*"In the lab, we break things safely so we learn how to protect them properly."*

</div>

---

## 🎯 Mission Brief

**moody** is a personal R&D lab designed for studying script execution, microcontroller-based payloads (Pro Micro / Promicro), and basic penetration testing techniques in a controlled, isolated environment. This repository exists purely for **educational purposes** — helping security practitioners understand attack vectors, payload mechanics, and defensive strategies.

> **⚠️ CRITICAL:** All content is provided for authorized testing only. Unauthorized use against systems you don't own is illegal and unethical.

---

## 🔐 Rules of Engagement

Before you execute a single line of code, read and commit to these principles:

### ✅ Authorized Use Only
- **Test exclusively** in environments you own or have explicit, written permission to assess
- Use isolated virtual machines with snapshot capability
- Operate on air-gapped or host-only networks whenever possible

### ❌ Prohibited Activities
- **Never** deploy these scripts on public networks, production systems, or unauthorized targets
- **Never** use this code to harm others or violate laws
- **Never** test without explicit authorization

### 📋 Legal Notice
The repository owner provides this material for educational purposes and assumes **no liability** for misuse. Users are solely responsible for ensuring their activities comply with applicable laws and regulations.

---

## 📦 Arsenal Contents

| File | Category | Description |
|------|----------|-------------|
| `index.html` | Web Testing | Minimal HTML payload for testing browser-based execution flows |
| `indexfileDownload.ps1` | PowerShell | Download behavior analysis script (local testing only) |
| `rickroll.vbs` | VBScript | Benign execution test — harmless prank for studying script deployment |
| `rickrollPrank.ps1` | PowerShell | PowerShell variant of execution testing payload |
| `wifi_script.bat` | Batch | Windows networking command experiments (authorized networks only) |
| `wifi_script simple.bat` | Batch | Simplified network script variant |

> **Note:** These are deliberately simple proof-of-concept scripts. Treat them as learning tools, not production payloads.

---

## 🚀 Lab Setup & Deployment

### Prerequisites
- Isolated Windows VM (VirtualBox, VMware, Hyper-V)
- Snapshot capability enabled
- Host-only or NAT networking (no bridge to production networks)

### Quick Start

```powershell
# Clone repository to isolated environment
git clone https://github.com/InoshMatheesha/moody.git
cd moody

# Create VM snapshot BEFORE testing
# (Example for VirtualBox CLI)
# VBoxManage snapshot "YourVMName" take "PreTest_Snapshot"
```

### Recommended Lab Configuration

1. **VM Isolation**
   - Configure host-only networking or disconnect network entirely
   - Disable shared folders and clipboard if testing malicious behavior simulation
   - Take snapshot before each test session

2. **USB/HID Testing**
   - Use dedicated, disposable USB devices
   - Test microcontroller payloads on air-gapped systems only
   - Consider hardware emulation tools for safer analysis

3. **Documentation**
   - Log every command executed
   - Document expected vs. actual behavior
   - Maintain a testing journal for reproducibility

---

## 🛡️ Security Best Practices

```
┌─────────────────────────────────────────────────────┐
│  DEFENSE MINDSET: Test to Learn, Learn to Defend   │
└─────────────────────────────────────────────────────┘
```

- **Principle of Least Privilege:** Run scripts with minimal required permissions
- **Network Segmentation:** Never allow test VMs direct access to production networks
- **Incident Response:** Know how to revert/restore before you break things
- **Responsible Disclosure:** If you discover real vulnerabilities, report them ethically

---

## 🤝 Contributing

Contributions are welcome if they advance educational value or improve safety documentation.

- **Bug Reports:** Open an issue with detailed reproduction steps
- **New Payloads:** Submit PRs with clear documentation and ethical use guidelines
- **Documentation:** Improvements to clarity, safety notes, or lab setup guides always appreciated

---

## 📜 License & Disclaimer

This repository is provided **as-is** for personal and educational use. No formal license is currently applied.

**For wider distribution or commercial use:**
- Consider adding an explicit open-source license (MIT, Apache-2.0)
- Include a formal responsible disclosure policy
- Ensure compliance with local security research laws

---

## 📬 Contact

Questions, suggestions, or collaboration inquiries? Open an issue on this repository.

---

<div align="center">

**Built for ethical hackers, by ethical hackers**

*Remember: With great power comes great responsibility. Test smart, test safe, test legal.*

</div>

