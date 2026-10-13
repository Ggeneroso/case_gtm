"""Compara saidas/*.json (extração do modelo) com o gabarito e gera relatorio.md.
Uso: python avaliar.py [--gabarito gabarito.json] [--saidas saidas]"""
import json, re, argparse, unicodedata
from pathlib import Path
BASE = Path(__file__).parent
def norm(s): return re.sub(r"\s+", " ", "".join(c for c in unicodedata.normalize("NFD", (s or "").lower()) if unicodedata.category(c) != "Mn"))
def bate(grupos, texto): t = norm(texto); return any(all(norm(w) in t for w in g) for g in grupos)
ap = argparse.ArgumentParser(); ap.add_argument("--gabarito", default=str(BASE / "gabarito_rascunho.json")); ap.add_argument("--saidas", default=str(BASE / "saidas")); a = ap.parse_args()
gab = {k: v for k, v in json.load(open(a.gabarito, encoding="utf-8")).items() if not k.startswith("_")}
tot = dict(pg=0, pg_ok=0, pe=0, pe_ok=0, mg=0, mg_ok=0, me=0, me_ok=0, cum_ok=0, cum_n=0, bola=0, mot=0, n=0)
rel = ["# Relatório de avaliação\n"]
for k in sorted(gab, key=int):
    f = Path(a.saidas) / f"conversa_{int(k):02d}.json"
    if not f.exists(): continue
    o = json.load(open(f, encoding="utf-8")); g = gab[k]; tot["n"] += 1
    abertas = [p for p in o["pedidos_e_perguntas_do_cliente"] if p["status"] != "respondida"]
    rel.append(f"## Conversa {k}")
    # perguntas
    txt_a = [p["texto"] + " " + (p.get("evidencia_resposta") or "") for p in abertas]
    ach = [i for i in g["perguntas_abertas"] if any(bate(i["palavras"], t) for t in txt_a)]
    extras = [t for t in txt_a if not any(bate(i["palavras"], t) for i in g["perguntas_abertas"])]
    tot["pg"] += len(g["perguntas_abertas"]); tot["pg_ok"] += len(ach); tot["pe"] += len(abertas); tot["pe_ok"] += len(abertas) - len(extras)
    rel.append(f"- Perguntas abertas: achou {len(ach)}/{len(g['perguntas_abertas'])}; extras (revisar se são invenção): {extras or 'nenhuma'}")
    for i in g["perguntas_abertas"]:
        if i not in ach: rel.append(f"  - OMITIU: {i['desc']}")
    # promessas
    pr = o["promessas_do_vendedor"]; txt_p = [p["promessa"] + " " + (p.get("evidencia") or "") for p in pr]
    achp = []
    for i in g["promessas"]:
        m = next((p for p, t in zip(pr, txt_p) if bate(i["palavras"], t)), None)
        if m: achp.append(i); tot["cum_n"] += 1; tot["cum_ok"] += (m["cumprida"] == i["cumprida"])
        else: rel.append(f"  - PROMESSA OMITIDA: {i['desc']}")
        if m and m["cumprida"] != i["cumprida"]: rel.append(f"  - 'cumprida' divergente em '{i['desc']}': modelo={m['cumprida']} gabarito={i['cumprida']}")
    extrap = [t for t in txt_p if not any(bate(i["palavras"], t) for i in g["promessas"])]
    tot["mg"] += len(g["promessas"]); tot["mg_ok"] += len(achp); tot["me"] += len(pr); tot["me_ok"] += len(pr) - len(extrap)
    rel.append(f"- Promessas: achou {len(achp)}/{len(g['promessas'])}; extras (revisar): {extrap or 'nenhuma'}")
    # bola e motivo
    ob, om = o.get("bola_com"), o.get("motivo_real_principal")
    tot["bola"] += ob == g["bola_com"]; tot["mot"] += om == g["motivo_principal"]
    rel.append(f"- bola_com: modelo={ob} | gabarito={g['bola_com']} {'OK' if ob == g['bola_com'] else 'DIVERGE'}")
    rel.append(f"- motivo_real: modelo={om} (confiança {o.get('motivo_real_confianca')}) | gabarito={g['motivo_principal']} {'OK' if om == g['motivo_principal'] else 'DIVERGE'}\n")
pct = lambda a_, b_: f"{100 * a_ / b_:.0f}% ({a_}/{b_})" if b_ else "n/a"
resumo = [f"# Resumo ({tot['n']} conversas)",
          f"- Cobertura de perguntas abertas: {pct(tot['pg_ok'], tot['pg'])}", f"- Precisão de perguntas abertas: {pct(tot['pe_ok'], tot['pe'])}",
          f"- Cobertura de promessas: {pct(tot['mg_ok'], tot['mg'])}", f"- Precisão de promessas: {pct(tot['me_ok'], tot['me'])}",
          f"- 'cumprida' correto nas promessas achadas: {pct(tot['cum_ok'], tot['cum_n'])}",
          f"- bola_com correto: {pct(tot['bola'], tot['n'])}", f"- motivo_real principal correto: {pct(tot['mot'], tot['n'])}\n"]
(BASE / "relatorio.md").write_text("\n".join(resumo + rel), encoding="utf-8"); print("\n".join(resumo))
