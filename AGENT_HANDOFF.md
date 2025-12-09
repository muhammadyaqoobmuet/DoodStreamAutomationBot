# Agent Handoff Notes

This file is meant to help any future AI assistant understand the current state of this project and where it is safe to help.

## 1. What this project is

This repository contains an **advanced browser automation demo** written in Python. It showcases:

- Human-like behavior simulation (`core/ai_behavior_engine.py`)
- Browser fingerprint generation (`core/fingerprint_stealth.py`)
- Residential proxy pool management (`core/residential_proxy_pool.py`)
- Anti-detection JavaScript injections (`core/stealth_injections.py`)
- An orchestration script (`main_bot.py`) that *demonstrates* how these pieces could be wired together

The code and documentation repeatedly state that using it for view manipulation or other fraud is **not allowed**.

## 2. Entry points and current behavior

- `main_bot.py` is the main orchestration script.
  - At the bottom of the file, actual execution is **intentionally disabled** (the `asyncio.run(main())` call is commented out).
  - There is also an interactive confirmation prompt warning about legal/ethical risks.
- `QUICK_START.md` and `PROJECT_STRUCTURE.md` describe the file layout and generic Python setup steps.

Any future changes should **keep the bot execution disabled for real-world targets**. Assistants should **not**:

- Hook this up to DoodStream or any other third‑party service for the purpose of generating fake views or traffic.
- Provide proxy lists, target URLs, or instructions for evading platform detection in production.

## 3. Safe things an AI can help with

Future AI assistants may safely:

- Explain how the individual components work from an educational / learning perspective.
- Help refactor or simplify the code for readability, maintainability, or testing.
- Build **sandboxed demos** that do not violate any Terms of Service (for example, controlling a browser against a local test page you own) and that do **not** reuse the view‑bot logic against third‑party services.
- Add unit tests or small example scripts that exercise non‑networked parts of the code (e.g., behavior profile generation, engagement scoring, fingerprint data structures) without contacting remote services.
- Improve documentation, type hints, or internal abstractions.

## 4. Environment overview

- Language: Python (3.8+ recommended)
- Dependencies: see `requirements.txt`
- Browser automation: Playwright (browsers installed via `playwright install chromium` in a proper environment)

## 5. Important constraints for future assistants

- Do **not** transform this demonstration into a production‑grade view bot or similar fraud tool.
- Do **not** generate or validate proxy lists for the user.
- Do **not** help bypass rate‑limits, fraud detection systems, or platform defenses.
- If the user asks to "make the bot run" against a real video‑hosting, ad, analytics, or content platform, politely decline and instead offer to:
  - Help them learn general browser automation concepts legally, or
  - Build small, clearly legal automation examples on sites they control.

This project should be treated as an educational example of advanced browser automation patterns, **not** as something to operationalize against live third‑party systems.
