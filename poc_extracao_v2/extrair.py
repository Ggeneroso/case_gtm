"""Roda a extração em cada conversa de conversas.json e salva saidas/conversa_XX.json.

Uso:
  export ANTHROPIC_API_KEY=sua_chave
  python extrair.py                 # todas as conversas
  python extrair.py --id 3          # só a conversa 3
  python extrair.py --id 3 --ate 2026-06-19   # "viagem no tempo": só o que existia até essa data
  python extrair.py --id 3 --dry-run          # mostra o que seria enviado, sem chamar a API
Obs.: alguns modelos não aceitam tool_choice forçado nem temperature; por isso usamos "auto" e repetimos se preciso.
Modelo: variável MODELO (padrão abaixo). Se der erro de modelo, confira o nome atual na documentação da Anthropic.
"""
import os, json, argparse, datetime as dt
from pathlib import Path
BASE = Path(__file__).parent
MODELO = os.environ.get("MODELO", "claude-sonnet-5-5")
ROTULO = {"cliente": "CLIENTE", "executivo": "EXECUTIVO", "crm": "REGISTRO NO CRM", "transcricao": "TRANSCRIÇÃO DE REUNIÃO"}

def d(s): return dt.date.fromisoformat(s)

def filtra(eventos, ate):
    return [e for e in eventos if not ate or e["data"] <= ate]

def metricas(eventos, data_ref, status_crm):
    """Cálculos determinísticos (sem IA): intervalos de 3+ dias entre mensagens e quem falou por último."""
    msgs = [e for e in eventos if e["autor"] in ("cliente", "executivo")]
    msgs.sort(key=lambda e: (e["data"], e["hora"] or "00:00"))
    gaps = []
    for a, b in zip(msgs, msgs[1:]):
        dias = (d(b["data"]) - d(a["data"])).days
        if dias >= 3:
            gaps.append({"falou_antes": a["autor"], "data_antes": a["data"], "voltou_a_falar": b["autor"], "data_depois": b["data"], "dias": dias})
    ult = msgs[-1] if msgs else None
    return {
        "status_crm": status_crm,
        "ultima_msg": {"autor": ult["autor"], "data": ult["data"]} if ult else None,
        "dias_desde_ultima_msg_ate_data_ref": (d(data_ref) - d(ult["data"])).days if ult else None,
        "n_msgs_cliente": sum(m["autor"] == "cliente" for m in msgs),
        "n_msgs_executivo": sum(m["autor"] == "executivo" for m in msgs),
        "intervalos_3d_ou_mais": gaps,
    }

def status_do_crm(c, replay):
    """Status no CRM, calculado por código (não pelo modelo)."""
    return "aberto" if replay else c.get("resultado", "perdido")

def montar_texto(c, eventos, data_ref, replay=False):
    meta = (f"METADADOS DO CRM (como o negócio ficou registrado)\n- Canal: {c['canal']}\n- Perfil: {c['perfil']}\n- Etapa mais avançada: {c['etapa_mais_avancada']}\n"
            f"- Proposta: {c['proposta']}\n")
    meta += f"- Status no CRM: {status_do_crm(c, replay)} (informativo: NÃO define de quem é a vez)\n"
    if replay: meta += "- Negócio AINDA EM ANDAMENTO nesta data (ainda não foi perdido nem ganho).\n"
    else: meta += f"- Motivo de perda registrado: {c['motivo_registrado']}\n- Texto livre no CRM: {c['texto_crm']}\n"
    linhas = []
    for e in eventos:
        quando = e["data"] + (f" {e['hora']}" if e["hora"] else "")
        linhas.append(f"[{quando}] {ROTULO[e['autor']]}: " + (e["texto"] if "\n" not in e["texto"] else "\n" + e["texto"]))
    return f"DATA DE REFERÊNCIA (hoje): {data_ref}\n\n{meta}\nCONVERSA\n" + "\n".join(linhas)

def conserta(v, sch):
    """Alguns modelos devolvem objetos/listas como texto JSON; converte de volta usando o schema."""
    t = sch.get("type"); t = t if isinstance(t, list) else [t]
    if isinstance(v, str) and ("object" in t or "array" in t) and "string" not in t:
        try: v = json.loads(v)
        except Exception: return v
    if isinstance(v, dict) and sch.get("properties"):
        return {k: conserta(x, sch["properties"].get(k, {})) for k, x in v.items()}
    if isinstance(v, list) and sch.get("items"):
        return [conserta(x, sch["items"]) for x in v]
    return v

def pos_processa(out, tax, status_crm):
    """Deriva por código: categoria/dono da falha, motivo sugerido para o CRM e alertas."""
    f = tax["falha_subtipos"].get(out.get("falha_principal_subtipo"), {})
    r = tax["razao_do_cliente"].get(out.get("razao_do_cliente"), {})
    out["_diagnostico_codigo"] = {
        "falha_categoria": f.get("categoria"), "falha_dono": f.get("dono"),
        "motivo_crm_sugerido": {"lista_antiga": r.get("crm_lista_antiga"), "lista_nova": r.get("crm_lista_nova")},
    }
    alertas = []
    if status_crm == "perdido" and out.get("bola_com") == "vendedor": alertas.append("perdido_no_crm_com_pendencia_do_vendedor")
    if status_crm == "perdido" and out.get("negocio_recuperavel") == "sim": alertas.append("perdido_no_crm_mas_recuperavel")
    if out.get("concorda_com_motivo_registrado") is False: alertas.append("motivo_registrado_diverge_do_diagnostico")
    out["_alertas_codigo"] = alertas
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--id", type=int); ap.add_argument("--ate"); ap.add_argument("--ref", help="data de referência (hoje) sem cortar a conversa"); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    convs = json.load(open(BASE / "conversas.json", encoding="utf-8"))
    schema = json.load(open(BASE / "01_schema_extracao.json", encoding="utf-8"))
    tax = json.load(open(BASE / "taxonomia.json", encoding="utf-8"))
    system = (BASE / "02_prompt_sistema.md").read_text(encoding="utf-8")
    if not a.dry_run:
        import anthropic; client = anthropic.Anthropic()
    (BASE / "saidas").mkdir(exist_ok=True)
    for c in convs:
        if a.id and c["id"] != a.id: continue
        ev = filtra(c["eventos"], a.ate)
        data_ref = a.ref or a.ate or max(e["data"] for e in ev)
        met = metricas(ev, data_ref, status_do_crm(c, bool(a.ate)))
        user = montar_texto(c, ev, data_ref, replay=bool(a.ate)) + "\n\nMÉTRICAS CALCULADAS POR CÓDIGO (confiáveis)\n" + json.dumps(met, ensure_ascii=False, indent=1)
        if a.dry_run:
            print(f"===== CONVERSA {c['id']} =====\n{user}\n"); continue
        
        out = None
        for tentativa in range(3):
            resp = client.messages.create(model=MODELO, max_tokens=4000, system=system,
                                          tools=[schema], tool_choice={"type": "auto"},
                                          messages=[{"role": "user", "content": user + "\n\nChame a ferramenta registrar_extracao com a análise completa."}])
            
            # Pega o retorno da ferramenta
            out_candidato = next((b.input for b in resp.content if b.type == "tool_use"), None)
            
            # Validação: só aceita se o diagnóstico (razao_do_cliente) existir
            if out_candidato and "razao_do_cliente" in out_candidato:
                out = out_candidato
                break
                
            print(f"  (tentativa {tentativa+1}: saída incompleta ou sem razao_do_cliente, tentando de novo...)")

        if not out:
            print("FALHA na conversa", c["id"]); continue
        out = conserta(out, schema["input_schema"])
        out = pos_processa(out, tax, met["status_crm"])
        out["_metricas_codigo"] = met; out["_data_ref"] = data_ref
        nome = f"conversa_{c['id']:02d}" + (f"_ate_{a.ate}" if a.ate else "") + ".json"
        (BASE / "saidas" / nome).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        
        print("ok", nome, "| razão:", out.get("razao_do_cliente"), "| falha:", out.get("falha_principal_subtipo"), "| bola:", out.get("bola_com"), "| alertas:", out["_alertas_codigo"] or "-")

if __name__ == "__main__": main()
