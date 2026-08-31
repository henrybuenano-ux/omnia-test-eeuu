# -*- coding: utf-8 -*-
"""PASO 2 (reunión 28-ago) — Workflow que PAUSA el bot para clientes viejos (Clover).

Diseño: trigger `contact_tag` (tag `cliente-antiguo` agregado) -> 1 acción
`update_conversation_ai_status` = keep-same/inactive (pausa el bot SIN reasignar).

Reglas v2.1 respetadas:
  · idempotente (si el workflow ya existe, no lo recrea)
  · dry-run por defecto; escribe SOLO con --aplicar
  · queda en DRAFT (trigger active:false). Publicar y "enroll existing" es del humano en la UI.
  · nodo ai_status tomado del toolkit validado (no se fabrican atributos).

Uso:
  python3 apagar_ia_clover.py            # dry-run (lee, valida, imprime plan)
  python3 apagar_ia_clover.py --aplicar  # crea el workflow en DRAFT
"""
import os, sys, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent            # ghl-cli-v2.1
ROOT = HERE.parent                                        # /home/user/omnia-test-eeuu
sys.path.insert(0, str(HERE))
# cargar .env de la raíz del proyecto
for l in (ROOT / ".env").read_text().splitlines():
    l = l.strip()
    if l and not l.startswith("#") and "=" in l:
        k, v = l.split("=", 1); os.environ[k.strip()] = v.strip()   # override (el entorno trae un token viejo)

from gohighlevel.utils.wf_toolkit import n_ai_status_apagar, cond_trigger_tag, nid, verificar_triggers
from gohighlevel.utils.ghl_internal_client import InternalGHLClient, TokenManager

LOC = os.environ["GHL_LOCATION_ID"]
C = InternalGHLClient(TokenManager(), LOC)

WF_NAME     = "SETUP · Apagar IA — clientes Clover"
FOLDER_NAME = "🔧 Setup / Control de bot"
TAG         = "cliente-antiguo"
APLICAR     = "--aplicar" in sys.argv


def _list_workflows():
    d = C.request("GET", f"/workflow/{LOC}") or {}
    if isinstance(d, dict):
        return d.get("workflows", d.get("data", [])) or []
    return d or []


def main():
    print(f"== PASO 2 · Apagar IA para clientes Clover ==  ({'APLICAR' if APLICAR else 'DRY-RUN'})\n")

    wfs = _list_workflows()
    if isinstance(wfs, dict) and wfs.get("_error"):
        print("ABORT: no pude listar workflows:", wfs); return
    print(f"Workflows en la subcuenta: {len(wfs)}")

    # idempotencia
    existing = [w for w in wfs if (w.get("name") == WF_NAME)]
    if existing:
        print(f"YA EXISTE '{WF_NAME}' (id {existing[0].get('id')}). No se recrea. ✅")
        return

    # localizar/crear folder
    folder = next((w for w in wfs if w.get("name") == FOLDER_NAME), None)
    folder_id = folder.get("id") if folder else None

    # nodo ai_status (pausar, keep-same/inactive) — forma validada del toolkit
    ai_node = {
        "id": nid(), "order": 0,
        "attributes": n_ai_status_apagar(),
        "name": "Pausar bot (cliente antiguo)",
        "type": "update_conversation_ai_status",
        "workflowsActionType": "INTERNAL",   # obligatorio a nivel de nodo (playbook §3)
        "next": "",
    }
    trigger_cond = cond_trigger_tag(TAG)

    print("\n--- PLAN ---")
    print(f"Folder: {'reusar '+folder_id if folder_id else 'crear ' + FOLDER_NAME}")
    print(f"Workflow (DRAFT): {WF_NAME}")
    print(f"Trigger: contact_tag · tag '{TAG}' agregado · active=false (DRAFT)")
    print("Nodo acción:")
    print("  " + json.dumps(ai_node, ensure_ascii=False))
    print("Condición trigger:")
    print("  " + json.dumps(trigger_cond, ensure_ascii=False))

    if not APLICAR:
        print("\n(dry-run — nada escrito. Corre con --aplicar para crear en DRAFT.)")
        return

    # ---- ESCRITURA ----
    # tag (idempotente)
    C.create_location_tag(TAG)

    # folder
    if not folder_id:
        fr = C.request("POST", f"/workflow/{LOC}", {"name": FOLDER_NAME, "type": "directory"})
        folder_id = fr.get("id") if isinstance(fr, dict) else None
        print("Folder creado:", folder_id)

    # workflow (draft)
    wr = C.request("POST", f"/workflow/{LOC}", {"name": WF_NAME, "parentId": folder_id})
    wid = wr.get("id") if isinstance(wr, dict) else None
    if not wid:
        print("ABORT: no se creó el workflow:", wr); return
    print("Workflow creado (draft):", wid)

    # trigger (DRAFT: active=false — NO publicar por API)
    trigger_body = {
        "status": "draft", "workflowId": wid, "schedule_config": {},
        "conditions": [trigger_cond], "type": "contact_tag", "masterType": "highlevel",
        "name": "Cliente antiguo (Clover)",
        "actions": [{"workflow_id": wid, "type": "add_to_workflow"}],
        "active": False, "location_id": LOC,
    }
    tr = C.request("POST", f"/workflow/{LOC}/trigger", trigger_body)
    tid = tr.get("id") if isinstance(tr, dict) else None
    print("Trigger creado:", tid)
    if tid:
        C.request("PUT", f"/workflow/{LOC}/trigger/{tid}",
                  {**trigger_body, "id": tid, "targetActionId": ai_node["id"]})

    # PUT templates (nodo único). status se preserva (draft).
    put_body = {"name": WF_NAME, "version": wr.get("version", 1),
                "parentId": folder_id, "status": "draft", "allowMultiple": False,
                "workflowData": {"templates": [ai_node]}}
    pr = C.request("PUT", f"/workflow/{LOC}/{wid}", put_body)
    print("PUT templates:", "OK" if pr and not (isinstance(pr, dict) and pr.get("_error")) else pr)

    # verificación
    probs = verificar_triggers(C, LOC, wid)
    print("\nverificar_triggers:", probs if probs else "sin problemas de estructura")
    print("  (nota: el trigger sale INACTIVO a propósito — es DRAFT. Se activa al PUBLICAR desde la UI.)")
    print(f"\n✅ Creado en DRAFT. Siguiente paso HUMANO en la UI:")
    print("   1) Abre el workflow, revisa el nodo, y ponlo en Publish.")
    print("   2) Al publicar, marca 'enroll existing contacts' para apagar la IA de los ~3,635 ya tagueados.")


if __name__ == "__main__":
    main()
