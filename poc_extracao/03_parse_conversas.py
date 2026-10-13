"""Converte o PDF de conversas do case (02_conversas_clientes.pdf) em conversas.json.
Uso: python 03_parse_conversas.py caminho/02_conversas_clientes.pdf
Requer o utilitário `pdftotext` (poppler). Datas do PDF não têm ano: assume ANO abaixo."""
import re, json, sys, subprocess
from pathlib import Path
ANO = 2026
pdf = sys.argv[1] if len(sys.argv) > 1 else "02_conversas_clientes.pdf"
txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout

def flex(w): return r"\s*".join(w)
RE_META = re.compile(r"Canal:\s*(.*?)\s*·\s*" + flex("Etapa") + r"\s*mais\s*" + flex("avançada") + r":\s*(.*?)\s*·\s*Proposta:\s*(.*?)\s*·\s*Motivo\s*" + flex("registrado") + r":\s*(.*?)\s*·\s*" + flex("Texto") + r"\s*no\s*CRM:\s*(.*)", re.S)
RE_CONV = re.compile(r"^\s*Conversa\s*(\d+)\s*·\s*(.*)$")
RE_DATA = re.compile(r"·(\d{2})/(\d{2})(?:(\d{1,2}):(\d{2}))?")
SKIP = re.compile(r"Case de GTM Engineering|Material confidencial|Material de apoio|Conversas com clientes perdidos|^\s*\f?\s*$")

def tipo_evento(nospace):
    for pref, t in (("ExecutivoLais·", "executivo"), ("Cliente·", "cliente"), ("RegistronoCRM·", "crm"), ("Transcrição·", "transcricao")):
        if nospace.startswith(pref): return t
    return None

convs, cur, ev, meta_lines, in_meta = [], None, None, [], False
def fecha_ev():
    global ev
    if ev and cur is not None:
        if ev["autor"] == "transcricao":
            turnos = []
            for l in ev["linhas"]:
                if re.match(r"^[A-ZÁÉÍÓÚ][\wÀ-ú]*(\s\([^)]*\))?:", l) or not turnos: turnos.append(l)
                else: turnos[-1] += " " + l
            ev["texto"] = "\n".join(turnos)
        else:
            ev["texto"] = " ".join(ev["linhas"])
        del ev["linhas"]; cur["eventos"].append(ev)
    ev = None
def fecha_meta():
    global in_meta, meta_lines
    if in_meta and cur is not None:
        m = RE_META.search(" ".join(meta_lines))
        if m: cur["canal"], cur["etapa_mais_avancada"], cur["proposta"], cur["motivo_registrado"], cur["texto_crm"] = [x.strip() for x in m.groups()]
    in_meta, meta_lines = False, []

for raw in txt.splitlines():
    line = raw.replace("\f", "").rstrip()
    mc = RE_CONV.match(line)
    if mc:
        fecha_ev(); fecha_meta()
        cur = {"id": int(mc.group(1)), "perfil": mc.group(2).strip(), "eventos": []}; convs.append(cur); in_meta = True; continue
    if cur is None: continue
    if not line.strip():
        if in_meta and meta_lines: fecha_meta()
        fecha_ev(); continue
    if SKIP.search(line): fecha_ev(); continue
    if in_meta: meta_lines.append(line.strip()); continue
    ns = re.sub(r"\s+", "", line)
    t = tipo_evento(ns)
    if t:
        fecha_ev()
        md = RE_DATA.search(ns)
        d, m_, hh, mm = md.groups()
        ev = {"autor": t, "data": f"{ANO}-{m_}-{d}", "hora": f"{int(hh):02d}:{mm}" if hh else None, "linhas": []}
        continue
    if ev is not None: ev["linhas"].append(line.strip())
fecha_ev(); fecha_meta()
for c in convs: c["resultado"] = "ganho" if "ganho" in c.get("etapa_mais_avancada", "").lower() else "perdido"
Path("conversas.json").write_text(json.dumps(convs, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(convs), "conversas;", sum(len(c["eventos"]) for c in convs), "eventos")
