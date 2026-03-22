#!/usr/bin/env python3
import os
import time
import json
import sys
import subprocess

# --- VENV BOOTSTRAP ---
hook_dir = os.path.dirname(os.path.abspath(__file__))
aim_root = os.path.dirname(hook_dir)
venv_python = os.path.join(aim_root, "venv/bin/python3")

input_data = sys.stdin.read()

if os.path.exists(venv_python) and sys.executable != venv_python:
    try:
        process = subprocess.run([venv_python] + sys.argv, input=input_data, text=True, capture_output=True)
        print(process.stdout)
        sys.exit(process.returncode)
    except Exception: pass

# --- LOGIC ---
src_dir = os.path.join(aim_root, "src")
if src_dir not in sys.path: sys.path.append(src_dir)

try:
    from config_utils import CONFIG, AIM_ROOT
except ImportError:
    print(json.dumps({}))
    sys.exit(0)

STATE_FILE = os.path.join(AIM_ROOT, "archive/scrivener_state.json")
SUMMARIZER_PATH = os.path.join(CONFIG['paths']['hooks_dir'], "tier1_hourly_summarizer.py")
HIGH_IMPACT_TOOLS = ["replace", "write_file", "run_shell_command"]

def check_significance(data):
    """
    Phase 21 Significance Filter.
    Tier 1 Summarizer only wakes up if >= 5 new technical turns OR a 'High-Impact Tool' was used.
    """
    session_id = data.get('sessionId') or data.get('session_id')
    history = data.get('messages', []) or data.get('session_history', [])
    
    if not session_id or not history:
        return False
        
    last_index = 0
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
                val = state.get(session_id, 0)
                if isinstance(val, dict):
                    last_index = val.get('last_narrated_turn', 0)
                else:
                    last_index = val
        except: pass

    new_turns = history[last_index:]
    if len(new_turns) >= 5:
        return True

    for msg in new_turns:
        tool_calls = msg.get('toolCalls') or msg.get('tool_calls') or []
        for call in tool_calls:
            name = call.get('name') or call.get('function', {}).get('name', '')
            if name in HIGH_IMPACT_TOOLS:
                return True
                
    return False

def trigger_checkpoint(data_string):
    """Silently runs the Tier 1 summarizer in the background."""
    if os.path.exists(SUMMARIZER_PATH):
        try:
            subprocess.Popen(
                [venv_python, SUMMARIZER_PATH], 
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                text=True,
                start_new_session=True 
            ).stdin.write(data_string)
            return True
        except Exception: return False
    return False

def get_latest_transcript():
    try:
        raw_dir = os.path.join(AIM_ROOT, "archive/raw")
        files = glob.glob(os.path.join(raw_dir, "*.json"))
        if not files: return None
        latest = max(files, key=os.path.getmtime)
        with open(latest, 'r') as f:
            return f.read()
    except: return None

def main():
    try:
        # PHASE 17: Mirror global transcripts to local archive
        # We do this FIRST so if we need to fall back to reading from disk, the file is fresh.
        porter_path = os.path.join(AIM_ROOT, "scripts/session_porter.py")
        if os.path.exists(porter_path):
            subprocess.run([venv_python, porter_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        data_to_process = input_data
        if not data_to_process:
            data_to_process = get_latest_transcript()
            
        if not data_to_process:
            print(json.dumps({}))
            return
        
        # 1. PILLAR B: ROLLING INTERIM BACKUP & FALLBACK TAIL
        backup_path = os.path.join(AIM_ROOT, "continuity/INTERIM_BACKUP.json")
        tail_path = os.path.join(AIM_ROOT, "continuity/FALLBACK_TAIL.md")
        try:
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            with open(backup_path, 'w') as bf:
                bf.write(data_to_process)
                
            # Phase 20: The Failsafe Context Tail
            data = json.loads(data_to_process)
            history = data.get('messages', []) or data.get('session_history', [])
            if history:
                tail_content = "# A.I.M. FALLBACK CONTEXT TAIL\n\n*Note: This is an automatic, zero-token snapshot of the last few turns.* \n\n"
                # Get last 10 turns
                recent_turns = history[-10:]
                for msg in recent_turns:
                    role = msg.get('role', msg.get('type', 'unknown')).upper()
                    tail_content += f"### {role}\n"
                    
                    if role in ['USER', 'SYSTEM']:
                        content_list = msg.get('content', [])
                        if isinstance(content_list, list):
                            text = " ".join([c.get('text', '') for c in content_list if isinstance(c, dict) and 'text' in c])
                        else:
                            text = str(content_list)
                        tail_content += f"{text[:500]}...\n\n" if len(text) > 500 else f"{text}\n\n"
                    elif role in ['GEMINI', 'MODEL', 'ASSISTANT']:
                        content = msg.get('content', '')
                        if content:
                            if isinstance(content, list):
                                text = " ".join([c.get('text', '') for c in content if isinstance(c, dict) and 'text' in c])
                            else:
                                text = str(content)
                            tail_content += f"{text[:500]}...\n\n" if len(text) > 500 else f"{text}\n\n"
                            
                        tool_calls = msg.get('toolCalls') or msg.get('tool_calls') or []
                        for call in tool_calls:
                            if 'function' in call:
                                tool_name = call['function'].get('name', 'tool')
                                args = call['function'].get('arguments', {})
                            else:
                                tool_name = call.get('name', 'tool')
                                args = call.get('args', {})
                            
                            args_str = args if isinstance(args, str) else json.dumps(args)
                            tail_content += f"**Tool Call:** `{tool_name}`\n```json\n{args_str[:200]}\n```\n\n"
                            
                with open(tail_path, 'w') as tf:
                    tf.write(tail_content)
        except: pass

        # 2. SIGNIFICANCE FILTER (Phase 21)
        try:
            data = json.loads(data_to_process)
            if check_significance(data):
                trigger_checkpoint(data_to_process)
        except:
            pass

        print(json.dumps({}))

    except Exception: 
        print(json.dumps({}))

if __name__ == "__main__":
    main()
