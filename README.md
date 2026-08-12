# 🔐 Advanced Password Checker

A Python-based desktop application for password strength analysis, entropy estimation, and secure password generation.

## 📌 Overview

Advanced Password Checker is a personal cybersecurity project designed to provide a simple way to analyze password characteristics and generate stronger password options.

The application performs its analysis locally, without sending passwords to external services.

## ✨ Features

- 🔍 Password strength analysis
- 🧮 Estimated entropy / search-space calculation
- 📊 Circular strength indicator
- ✅ Character requirement analysis
- 🔑 Secure password generation using Python's `secrets` module
- 👁️ Show / Hide password
- 📋 One-click password copying
- 🌙 Dark / Light mode
- 🖥️ Resizable desktop interface
- 💬 Humanized strength feedback

## 🛠️ Technologies

- **Python 3**
- **Tkinter** — Desktop GUI
- **secrets** — Cryptographically secure random generation
- **string** — Character-set handling
- **math** — Entropy calculations

## 📂 Project Structure

```text
advanced-password-checker/
├── main.py
├── entropy_engine.py
├── generator_engine.py
├── theme_config.py
└── ui_helpers.py