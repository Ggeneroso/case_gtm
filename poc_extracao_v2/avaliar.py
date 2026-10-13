"""Compara saidas/*.json (extração do modelo) com o gabarito e gera relatorio.md.
Uso: python avaliar.py [--gabarito gabarito.json] [--saidas saidas]"""
import json, re, argparse, unicodedata
from pathlib import Path
BASE = Path(__file__).parent
def norm(s): return re.sub(r"\s+", " ", "".join(c for c in unicodedata.normalize("NFD", (s or "").lower()) if unicodedata.category(c) != "Mn"))
def bate(grupos, texto): t = norm(texto); return any(all(norm(w) in t for w in g) for g in grupos)
ap = argparse.ArgumentParser(); ap.add_argument("--gabarito", default=str(BASE / "gabarito.json")); ap.add_argument("--saidas", default=str(BASE / "saidas")); a = ap.parse_args()
gab = {k: v for k, v in json.load(open(a.gabarito, encoding="utf-8")).items() if not k.startswith("_")}
T = dict(qg=0, qg_ok=0, qe=0, qe_ok=0, q_st=0, q_st_n=0, pg=0, pg_ok=0, pe=0, pe_ok=0, cum_ok=0, cum_n=0, n=0)
C = {c: 0 for c in ("bola_com", "razao_do_cliente", "falha_principal_subtipo", "perda_evitavel")}
rel = ["# Relatório de avaliação\n"]
for k in sorted(gab, key=int):
    f = Path(a.saidas) / f"conversa_{int(k):02d}.json"
    if not f.exists(): continue
    o = json.load(open(f, encoding="utf-8")); g = gab[k]; T["n"] += 1
    rel.append(f"## Conversa {k}")
    # ---- perguntas (todas, com status) ----
    qs = o.get("pedidos_e_perguntas_do_cliente", []); txt_q = [q["texto"] for q in qs]
    for i in g["perguntas"]:
        T["qg"] += 1
        m = next((q for q, t in zip(qs, txt_q) if bate(i["palavras"], t)), None)
        if m:
            T["qg_ok"] += 1; T["q_st_n"] += 1; T["q_st"] += (m["status"] == i["status"])
            if m["status"] != i["status"]: rel.append(f"  - status divergente em '{i['desc']}': modelo={m['status']} | gabarito={i['status']}")
        else: rel.append(f"  - PERGUNTA OMITIDA: {i['desc']}")
    extras = [t for t in txt_q if not any(bate(i["palavras"], t) for i in g["perguntas"])]
    T["qe"] += len(qs); T["qe_ok"] += len(qs) - len(extras)
    rel.append(f"- Perguntas: {len(g['perguntas'])} no gabarito, {len(qs)} extraídas; extras (revisar se são invenção): {extras or 'nenhuma'}")
    # ---- promessas ----
    pr = o.get("promessas_do_vendedor", []); txt_p = [p["promessa"] + " " + (p.get("evidencia") or "") for p in pr]
    for i in g["promessas"]:
        T["pg"] += 1
        m = next((p for p, t in zip(pr, txt_p) if bate(i["palavras"], t)), None)
        if m:
            T["pg_ok"] += 1; T["cum_n"] += 1; T["cum_ok"] += (m["cumprida"] == i["cumprida"])
            if m["cumprida"] != i["cumprida"]: rel.append(f"  - 'cumprida' divergente em '{i['desc']}': modelo={m['cumprida']} | gabarito={i['cumprida']}")
        else: rel.append(f"  - PROMESSA OMITIDA: {i['desc']}")
    extrap = [t for t in txt_p if not any(bate(i["palavras"], t) for i in g["promessas"])]
    T["pe"] += len(pr); T["pe_ok"] += len(pr) - len(extrap)
    rel.append(f"- Promessas: {len(g['promessas'])} no gabarito, {len(pr)} extraídas; extras (revisar): {extrap or 'nenhuma'}")
    # ---- diagnóstico (campos únicos) ----
    for c in C:
        mv, gv = o.get(c), g[c]; C[c] += (mv == gv)
        rel.append(f"- {c}: modelo={mv} | gabarito={gv} {'OK' if mv == gv else 'DIVERGE'}")
    rel.append(f"- Código: categoria da falha={o.get('_diagnostico_codigo', {}).get('falha_categoria')} | alertas={o.get('_alertas_codigo')} | confiança={o.get('diagnostico_confianca')}\n")
pct = lambda a_, b_: f"{100 * a_ / b_:.0f}% ({a_}/{b_})" if b_ else "n/a"
resumo = [f"# Resumo ({T['n']} conversas)",
          f"- Cobertura de perguntas: {pct(T['qg_ok'], T['qg'])}", f"- Precisão de perguntas: {pct(T['qe_ok'], T['qe'])}", f"- Status correto nas perguntas achadas: {pct(T['q_st'], T['q_st_n'])}",
          f"- Cobertura de promessas: {pct(T['pg_ok'], T['pg'])}", f"- Precisão de promessas: {pct(T['pe_ok'], T['pe'])}", f"- 'cumprida' correto nas promessas achadas: {pct(T['cum_ok'], T['cum_n'])}"]
resumo += [f"- {c} correto: {pct(v, T['n'])}" for c, v in C.items()] + [""]
(BASE / "relatorio.md").write_text("\n".join(resumo + rel), encoding="utf-8"); print("\n".join(resumo))
