#!/usr/bin/env python3
import os
import json
import subprocess
import shutil
import sys
from datetime import datetime

# --- CONFIG BOOTSTRAP ---
def find_aim_root(start_dir):
    current = os.path.abspath(start_dir)
    while current != '/':
        if os.path.exists(os.path.join(current, "core/CONFIG.json")): return current
        if os.path.exists(os.path.join(current, "setup.sh")): return current
        current = os.path.dirname(current)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = find_aim_root(os.getcwd())
CORE_DIR = os.path.join(BASE_DIR, "core")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
HOOKS_DIR = os.path.join(BASE_DIR, "hooks")
SRC_DIR = os.path.join(BASE_DIR, "src")
VENV_PYTHON = os.path.join(BASE_DIR, "venv/bin/python3")

# --- INTERNAL TEMPLATES ---

T_SOUL = """# A.I.M. (Actual Intelligent Memory) - Core Soul & Mandate

## 1. IDENTITY & PRIMARY DIRECTIVE
- **Designation:** A.I.M.
- **Operator:** {name}
- **Role:** High-context technical lead and sovereign orchestrator.
- **Philosopy:** Clarity over bureaucracy. Retrieval over context-bloat.

## 2. OPERATING MODE: AUTONOMOUS (YOLO)
- A.I.M. executes technical roadmaps autonomously.
- **Mandatory Retrieval:** Before acting, A.I.M. MUST query the **Engram DB** for specialized project directives.

## 3. THE KNOWLEDGE MAP (RAG POINTERS)
When encountering these categories, search the Engram DB for the corresponding "Active Pointers":
- **Architecture & Workflow:** Search "A_I_M_HANDBOOK" to understand memory pipelines and tools.
- **Testing Rules:** Search "TDD_POLICY" or "RED GREEN REFACTOR".
- **System Commands:** Run `python3 scripts/aim_cli.py map` to view an index of everything you know.
- **Infrastructure:** Search "Brain Architecture", "Flywheel Logic", "Portability".
- **Safety:** Search "Sentinel Protocol", "Secret Shield", "Guardrails".

"I believe I've made my point." — A.I.M.
"""

T_USER = """# USER.md - Operator Profile
## 👤 Basic Identity
- **Name:** {name}
- **Tech Stack:** {stack}
- **Style:** {style}

## 🧬 Physical & Personal (Optional)
- **Age/Height/Weight:** {physical}
- **Life Rules:** {rules}
- **Primary Goal:** {goals}

## 🏢 Business Intelligence
{business}

## 🤖 Grok/Social Archetype
{grok_profile}
"""

T_MEMORY = """# MEMORY.md — Durable Long-Term Memory (A.I.M.)
*Last Updated: {date}*
- **Operator:** {name}.
- **Status:** Initialized via Deep Onboarding.
"""

T_CONFIG = """{{
  "paths": {{
    "aim_root": "{aim_root}",
    "core_dir": "{aim_root}/core",
    "docs_dir": "{aim_root}/docs",
    "hooks_dir": "{aim_root}/hooks",
    "memory_dir": "{aim_root}/memory",
    "archive_raw_dir": "{aim_root}/archive/raw",
    "archive_index_dir": "{aim_root}/archive/index",
    "continuity_dir": "{aim_root}/continuity",
    "src_dir": "{aim_root}/src",
    "tmp_chats_dir": "{codex_tmp}"
  }},
  "models": {{
    "embedding_provider": "local",
    "embedding": "nomic-embed-text",
    "embedding_endpoint": "http://localhost:11434/api/embeddings",
    "reasoning_provider": "openai",
    "reasoning_model": "gpt-5.4",
    "reasoning_endpoint": "https://api.openai.com/v1",
    "sentinel_provider": "openai",
    "sentinel_model": "gpt-5.4-mini",
    "sentinel_endpoint": "https://api.openai.com/v1"
  }},
  "settings": {{
    "allowed_root": "{allowed_root}",
    "semantic_pruning_threshold": 0.85,
    "scrivener_interval_minutes": 60,
    "sentinel_mode": "full",
    "obsidian_vault_path": "{obsidian_path}"
  }}
}}
"""

def register_hooks():
    codex_dir = os.path.expanduser("~/.codex")
    settings_path = os.path.join(codex_dir, "hooks.json")
    os.makedirs(codex_dir, exist_ok=True)

    hook_events = {
        "UserPromptSubmit": f"{VENV_PYTHON} {os.path.join(HOOKS_DIR, 'context_injector.py')}",
        "agent-turn-complete": f"{VENV_PYTHON} {os.path.join(HOOKS_DIR, 'failsafe_context_snapshot.py')}",
        "Stop": f"{VENV_PYTHON} {os.path.join(SRC_DIR, 'handoff_pulse_generator.py')}"
    }

    try:
        settings = {}
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f: settings = json.load(f)

        for event, command in hook_events.items():
            settings[event] = command

        with open(settings_path, 'w') as f: json.dump(settings, f, indent=2)
        print("[OK] Codex hooks registered.")
    except Exception as e:
        print(f"[ERROR] Codex hook registration: {e}")

def trigger_bootstrap():
    print("\n--- PROJECT SINGULARITY: BOOTSTRAPPING BRAIN ---")
    bootstrap_path = os.path.join(SRC_DIR, "bootstrap_brain.py")
    try:
        subprocess.run([VENV_PYTHON, bootstrap_path], check=True)
    except: print("[CRITICAL] Foundation Bootstrap failed.")

def init_workspace():
    print("\n--- A.I.M. SOVEREIGN INSTALLER (Deep Identity Edition) ---")
    is_reinstall = os.path.exists(os.path.join(CORE_DIR, "CONFIG.json"))
    mode = "INITIAL"
    if is_reinstall:
        print("\n[!] EXISTING INSTALLATION DETECTED.")
        print("1. Update (Safe)\n2. Deep Re-Onboarding (Wipes Identity)\n3. Exit")
        choice = input("\nSelect [1-3]: ").strip()
        if choice == "3": sys.exit(0)
        
        if choice == "2":
            print("\n[!!!] WARNING: DEEP RE-ONBOARDING WILL WIPE YOUR IDENTITY [!!!]")
            print("This clears core/USER.md, core/MEMORY.md, and core/CONFIG.json.")
            confirm = input("Are you sure you want to proceed? [y/N]: ").lower()
            if confirm != 'y':
                print("\n[!] Aborting wipe. Switching to safe update mode...")
                mode = "UPDATE"
            else:
                final_check = input("To proceed, type 'YES' and hit Enter: ")
                if final_check == "YES":
                    mode = "OVERWRITE"
                else:
                    print("\n[!] Confirmation failed. Switching to safe update mode...")
                    mode = "UPDATE"
        else:
            mode = "UPDATE"

    name, stack, style, obsidian_path = "Operator", "General", "Direct", ""
    physical, rules, goals, business, grok_profile = "N/A", "N/A", "N/A", "None provided.", "None."
    if mode != "UPDATE":
        print("\n[PART 1: THE SOUL]")
        name = input("Your Name: ").strip() or name
        stack = input("Core Tech Stack: ").strip() or stack
        style = input("Working Style (e.g., 'Brutally honest and technical'): ").strip() or style
        
        print("\n[PART 2: THE OPERATOR - OPTIONAL]")
        print("(Press Enter to skip any of these)")
        physical = input("Metrics (Age/Height/Weight): ").strip() or physical
        rules = input("Life Rules/Principles: ").strip() or rules
        goals = input("Primary Mission/Life Goal: ").strip() or goals
        
        print("\n[PART 3: THE MISSION - OPTIONAL]")
        print("Paste your business info (Name, Website, Address):")
        business = sys.stdin.read() if not sys.stdin.isatty() else input("> ").strip() or business
        
        print("\n[PART 4: THE GROK BRIDGE - OPTIONAL]")
        print("--- COPY THIS PROMPT FOR GROK/SOCIAL AI ---")
        print("PROMPT: 'Analyze my recent post history and technical interests. I am building an AI engineering exoskeleton. Based on my communication style, philosophical values, and problem-solving approach, write a concise, 1-paragraph system prompt (persona) for this AI. It should mirror my directness, my systems-level thinking, and act as my perfect, zero-BS peer programmer.'")
        print("--- PASTE RESULT BELOW (End with Ctrl+D or empty line) ---")
        grok_profile = input("> ").strip() or grok_profile

        obsidian_path = input("\nObsidian Vault Path: ").strip()
    
    allowed_root = BASE_DIR
    if mode != "UPDATE":
        root_input = input(f"Allowed Root [Default {BASE_DIR}]: ").strip()
        allowed_root = root_input if root_input else BASE_DIR

    dirs = ["memory/proposals", "memory/archive", "archive/raw", "archive/index", 
            "archive/private", "archive/experimental", "archive/backups",
            "continuity/private", "continuity", "workstreams", "hooks", "scripts", "projects", "synapse"]
    for d in dirs: os.makedirs(os.path.join(BASE_DIR, d), exist_ok=True)

    register_hooks()

    date_str = datetime.now().strftime("%Y-%m-%d")
    home = os.path.expanduser("~")
    
    tmp_chats_dir = os.path.join(home, ".codex/memories")
    soul_filename = "AGENTS.md"
    
    # 1. Generate identity trinity
    files = {
        soul_filename: T_SOUL.format(name=name),
        "core/USER.md": T_USER.format(name=name, stack=stack, style=style, physical=physical, rules=rules, goals=goals, business=business, grok_profile=grok_profile),
        "core/MEMORY.md": T_MEMORY.format(name=name, date=date_str),
    }
    
    for path, content in files.items():
        fp = os.path.join(BASE_DIR, path)
        if mode == "OVERWRITE" or not os.path.exists(fp):
            with open(fp, 'w') as f: f.write(content)
            
    config_path = os.path.join(CORE_DIR, "CONFIG.json")
    if mode == "OVERWRITE" or not os.path.exists(config_path):
        config_content = T_CONFIG.format(aim_root=BASE_DIR, codex_tmp=tmp_chats_dir, allowed_root=allowed_root, obsidian_path=obsidian_path)
        with open(config_path, 'w') as f: f.write(config_content)

    trigger_bootstrap()
    print(f"\n[SUCCESS] A.I.M. Singularity initialized for {name}.")

if __name__ == "__main__":
    try: init_workspace()
    except KeyboardInterrupt: sys.exit(0)
