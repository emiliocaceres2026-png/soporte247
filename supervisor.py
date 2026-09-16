import os
import time
import sys
import requests

GITHUB_TOKEN = os.getenv("POLLO_PAT")
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}
OWNER = "emiliocaceres2026-png"
REPOS = ["PLAY1", "PLAY2", "PLAY3", "PLAY4", "PLAY5", "PLAY6", "PLAY7", "PLAY8", "PLAY9", "PLAY10"]
WORKFLOW_FILE = "run.yml"

def verificar_estado_proyecto(repo_name):
    url = f"https://api.github.com/repos/{OWNER}/{repo_name}/actions/workflows/{WORKFLOW_FILE}/runs?per_page=1"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            runs = response.json().get("workflow_runs", [])
            if runs:
                return runs[0].get("status"), runs[0].get("conclusion")
    except Exception as e:
        print(f"[EXCEPCIÓN] Error: {e}", flush=True)
    return None, None

def trigger_workflow(repo_name):
    url = f"https://api.github.com/repos/{OWNER}/{repo_name}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    payload = {"ref": "main"}
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        if response.status_code == 204:
            print(f"¡Workflow relanzado con éxito para: {repo_name}!", flush=True)
        else:
            print(f"Error al relanzar: {response.text}", flush=True)
    except Exception as e:
        print(f"[EXCEPCIÓN] Error al disparar: {e}", flush=True)

if __name__ == "__main__":
    print("Supervisor 24/7 iniciado correctamente.", flush=True)
    ronda = 1
    
    while True:
        print(f"\n--- [RONDA #{ronda}] Iniciando revisión ---", flush=True)
        for repo in REPOS:
            status, conclusion = verificar_estado_proyecto(repo)
            print(f"[{repo}] Estado actual: {status} | Conclusión: {conclusion}", flush=True)
            
            if status == "completed":
                print(f"¡El proyecto {repo} terminó! Relanzando...", flush=True)
                trigger_workflow(repo)
            elif status == "in_progress":
                print(f"[{repo}] Sigue trabajando en curso...", flush=True)
            else:
                print(f"[{repo}] Estado detectado: {status}", flush=True)
                
        print(f"Ronda #{ronda} terminada. Esperando 60 segundos...", flush=True)
        sys.stdout.flush()
        ronda += 1
        time.sleep(60)
