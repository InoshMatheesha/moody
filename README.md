


#  ███  █   █  ███   █  █  ███  
#  █ █ █ █ █ █ █  █ █ █ █  █  
#  ███  █  █  ███   █ █   ███  

Welcome to moody — the little lab where scripts go to learn tricks. WELCOME TO THE HIVE.

> "playground for curious hackers" — (not a license to harm)

## Terminal Vibes

This repo is a tiny, personal testbed for experimenting with scripts and microcontroller-style payloads (Pro Micro / Promicro style). Think of it as a sandboxed console where you can watch how payloads behave, learn scripting flows, and practise safe, ethical pentesting techniques.

BEFORE YOU PROCEED: this is educational material only. Do not run anything on systems or networks you do not own or have explicit permission to test.

## Safety — Read this like your lab rules

- Use an isolated VM or an offline test network. Snapshots are your friend.
- Never deploy these scripts on public or production networks.
- Get explicit, written permission before testing on someone else's device or network.
- The repository owner is not responsible for misuse. If in doubt, stop and ask.

## What's lurking in the repo

- `index.html` — tiny web playground (use in a local browser, not on the open web).
- `indexfileDownload.ps1` — PowerShell example for testing download behavior (local/test use only).
- `rickroll.vbs` & `rickrollPrank.ps1` — harmless prank examples used to test script execution flows.
- `wifi_script.bat` & `wifi_script simple.bat` — batch-script experiments for Windows networking commands (only in test networks).

Each file is a simple example — meant for learning, not for production use.

## Quickstart — get a safe lab running

1) Clone into an isolated lab machine (VM recommended):

```powershell
# Clone repo (example)
git clone https://github.com/InoshMatheesha/moody.git
cd moody
```

2) Create a VM snapshot before running anything.
3) Prefer host-only or an offline network. Revert the snapshot after tests.

## Lab tips (pro-hacker but safe)

- Use temporary/disposable USB devices or microcontroller emulators when testing payloads.
- Keep a dedicated analysis VM for unpacking or running unknown scripts.
- Document what you run and the exact steps to reproduce issues.

## Want it darker / louder / different?

If you'd like a different theme (retro green-on-black terminal, neon cyberpunk, more ASCII art, or a badge), tell me which style and I'll apply it.

## Contributing & contact

Open an issue or PR if you want to add more example payloads or better notes. If you need to contact the owner, open an issue with your question.

## License

No license file is included. This repo is shared for personal/educational use. Consider adding an explicit license (MIT, Apache-2.0) if you plan to share more widely.

---

Hacker-theme rewrite complete. If you want an even flashier ASCII header or badges, say the word (and which color/style).

