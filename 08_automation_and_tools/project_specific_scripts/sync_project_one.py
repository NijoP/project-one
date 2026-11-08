"""
Project One Synchronization Engine.
Synchronizes live execution logs, telemetry, failure records, and design revisions
from DESK into the Project One permanent engineering knowledge base and pushes to GitHub.
"""

import os
import shutil
import subprocess
import sys
import time

DESK_ROOT = r"C:\watch\desk"
PROJECT_ONE_ROOT = r"C:\watch\project-one"


def sync(commit_msg: str = None) -> bool:
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting Project One synchronization...")

    # 1. Sync Execution Logs & Failures
    field_dir = os.path.join(DESK_ROOT, "field")
    if os.path.exists(field_dir):
        # Progress
        progress_src = os.path.join(field_dir, "progress")
        progress_dst = os.path.join(PROJECT_ONE_ROOT, "06_execution_logs", "progress")
        if os.path.exists(progress_src):
            shutil.copytree(progress_src, progress_dst, dirs_exist_ok=True)

        # Failures
        fail_dst = os.path.join(PROJECT_ONE_ROOT, "06_execution_logs", "failures")
        for f in ["execution_failures.md", "errors.jsonl"]:
            src_f = os.path.join(field_dir, f)
            if os.path.exists(src_f):
                shutil.copy2(src_f, os.path.join(fail_dst, f))

        # Python scripts audit
        audit_src = os.path.join(field_dir, "python_scripts_audit.md")
        audit_dst = os.path.join(PROJECT_ONE_ROOT, "06_execution_logs", "python_scripts", "python_scripts_audit.md")
        if os.path.exists(audit_src):
            shutil.copy2(audit_src, audit_dst)

    # 2. Sync Hardware Design Revisions
    rework_src = os.path.join(DESK_ROOT, "projects", "WATCH_REWORK_V2")
    if os.path.exists(rework_src):
        # Deliverables
        mfg_dst = os.path.join(PROJECT_ONE_ROOT, "10_deliverables", "manufacturing")
        reports_dst = os.path.join(PROJECT_ONE_ROOT, "10_deliverables", "final_reports")
        os.makedirs(mfg_dst, exist_ok=True)
        os.makedirs(reports_dst, exist_ok=True)

        for bom_f in ["updated_bom.csv", "updated_bom.md"]:
            bf = os.path.join(rework_src, bom_f)
            if os.path.exists(bf):
                shutil.copy2(bf, os.path.join(mfg_dst, bom_f.replace("updated_", "")))

        for rep_f in ["requirements_traceability_matrix.md", "placement_comparison.md", "erc_drc_results.md", "change_log.md"]:
            rf = os.path.join(rework_src, rep_f)
            if os.path.exists(rf):
                shutil.copy2(rf, os.path.join(reports_dst, rep_f))

    # 3. Update Sync Timestamp in PROJECT_STATUS.md
    status_file = os.path.join(PROJECT_ONE_ROOT, "PROJECT_STATUS.md")
    if os.path.exists(status_file):
        with open(status_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(status_file, "w", encoding="utf-8") as f:
            for line in lines:
                if line.startswith("**Last Synchronization:**"):
                    f.write(f"**Last Synchronization:** {time.strftime('%Y-%m-%dT%H:%M:%S%z')}\n")
                else:
                    f.write(line)

    # 4. Git Add, Commit & Push
    msg = commit_msg or f"sync: synchronize engineering telemetry and design revision at {time.strftime('%Y-%m-%d %H:%M')}"
    cmd_add = ["git", "-C", PROJECT_ONE_ROOT, "add", "."]
    cmd_commit = ["git", "-C", PROJECT_ONE_ROOT, "commit", "-m", msg]
    cmd_push = ["git", "-C", PROJECT_ONE_ROOT, "push", "origin", "main"]

    try:
        subprocess.run(cmd_add, check=True, capture_output=True)
        # Check if there are changes to commit
        status = subprocess.run(["git", "-C", PROJECT_ONE_ROOT, "status", "--porcelain"], check=True, capture_output=True, text=True)
        if status.stdout.strip():
            subprocess.run(cmd_commit, check=True, capture_output=True)
            print(f"Committed changes: {msg}")
            subprocess.run(cmd_push, check=True, capture_output=True)
            print("Pushed to GitHub origin/main successfully.")
        else:
            print("Working tree clean, no new changes to commit.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git sync error: {e}")
        if e.stderr:
            print(f"Details: {e.stderr.decode('utf-8', errors='ignore')}")
        return False


if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else None
    success = sync(msg)
    sys.exit(0 if success else 1)
