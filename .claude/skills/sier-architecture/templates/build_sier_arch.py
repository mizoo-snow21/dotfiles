"""
SIer-style enterprise architecture diagram template.

汎用テンプレート — 配色・形状・helper は固定だが、加工 band の layout は domain に応じて自由設計。

Usage:
    1. Copy: cp ~/.claude/skills/sier-architecture/templates/build_sier_arch.py ./build.py
    2. Customize CONFIG block (sources, bands, targets, etc.)
    3. **Customize draw_storage_and_processing()** — ドメインに応じて 蓄積+加工 を自由設計
    4. Run: python3 build.py
    5. Render: drawio -x -f png -b 20 -s 2 -o ./<name>.png ./<name>.drawio

加工 band の典型パターン (SKILL.md 参照):
    - linear: 単純な L→R チェーン
    - 2-path: 上下 2 系統を中央データストアで橋渡し (RAG/ML 学習+推論 等)
    - branching: 1入力 → 並列処理 → 1出力
    - fan-out: 1処理 → 複数出力
    - layered: 認証→業務→永続化 等の階層
"""

# ============================================================
# COLOR PALETTE (固定)
# ============================================================
NAVY_HDR      = "#2A5C9B"
NAVY_TXT      = "#FFFFFF"
BAND_HDR_BG   = "#C9D9EC"
BAND_HDR_TXT  = "#2A5C9B"
RED_SIDE      = "#A82E2E"
RED_EDGE      = "#A82E2E"
RAW_FILL      = "#F2A5A5"   # raw store (DataLake/DocLake) — red
RAW_STROKE    = "#B22222"
DB_FILL       = "#BDDDA8"   # structured store (Vector DB / RDB / Cache) — green
DB_STROKE     = "#4E8639"
YELLOW_FILL   = "#FBE581"   # input (ingest/trigger) — yellow
YELLOW_STROKE = "#C99700"
LBLUE_FILL    = "#D5E2F0"   # output (utilize/distribute) — light blue
LBLUE_STROKE  = "#2A5C9B"
PROC_FILL     = "#FFFFFF"   # generic process — white
PROC_STROKE   = "#6B7B8E"
CORE_FILL     = "#FFE0B2"   # core element (LLM/main engine) — orange
CORE_STROKE   = "#E65100"
GOV_FILL      = "#E8EDF3"
GOV_HDR_FILL  = "#5B6B85"
TEXT_DARK     = "#2C3E50"
GRAY_LINE     = "#A8B0BC"
ARROW_DARK    = "#3A4654"
ARROW_REG     = "#4E8639"


# ============================================================
# === CONFIG: 必須項目 ========================================
# ============================================================

PAGE_W = 1500
PAGE_H = 470
TITLE  = "サンプル アーキテクチャ全体像"
HDR_LABEL = "システム基盤"

# 帯 (jp_label, en_label, width)
BANDS = [
    ("収  集", "Collect / Ingest", 155),
    ("蓄  積", "Store",            155),
    ("加  工", "Process",          720),
]

# 入力列 (左)
SRC_COL_HEADER = "データソース"
SRC_W = 135
SOURCES = [
    {"label": "文書DB",  "kind": "rect"},
    {"label": "ファイル", "kind": "rect"},
    {"label": "業務DB",  "kind": "rect"},
]

# 出力列 (右)
TGT_COL_HEADER = "活用先"
TGT_W = 135
TARGETS = [
    {"label": "業務ユーザー", "kind": "actor", "row": 3},
]

# 用途別ラベル (右端、行ごと)
EDGE_W = 100
EDGE_LABELS = [
    {"label": "定期レポート配信", "row": 3},
]

# 横断機能 (Cross-cutting band)。空リスト = 描画しない
GOV_BAND_ITEMS = []

# 入力 → 1帯目 (収集 band) の box (SOURCES と 1:1 mapping)
INGESTS = [
    "文書取込",
    "ファイル取込",
    "DBコネクタ",
]

FOOTER_NOTE = (
    "※ 加工 band の layout は domain に応じて自由設計。"
    "デフォルト実装は RAG 例 (Indexing 上 + Query 下 + Vector DB 橋渡し)。"
)

import os
OUTPUT_PATH = os.path.join(os.getcwd(), "sier-architecture-sample.drawio")

# ============================================================
# === END CONFIG =============================================
# ============================================================


# ============================================================
# Layout dimensions (基本触らない)
# ============================================================
HDR_BAR_Y = 18
HDR_BAR_H = 34
BAND_HDR_Y = HDR_BAR_Y + HDR_BAR_H + 4
BAND_HDR_H = 28
BODY_Y = BAND_HDR_Y + BAND_HDR_H + 4
BODY_H = 320
BODY_END = BODY_Y + BODY_H

SRC_H_ROW = 50
SRC_GAP = 18
SRC_Y_START = BODY_Y + 18
SBOX_H = 42

LEFT_MARGIN = 25
COL_GAP = 10
TGT_GAP = 8

SRC_X = LEFT_MARGIN
COL1_X = SRC_X + SRC_W + COL_GAP
B_X_LIST = []
_x = COL1_X
for _, _, w in BANDS:
    B_X_LIST.append(_x)
    _x += w
BAND_TOTAL_W = _x - COL1_X
TGT_X = _x + TGT_GAP
EDGE_X = TGT_X + TGT_W + COL_GAP

ROW_Y = lambda i: SRC_Y_START + i * (SRC_H_ROW + SRC_GAP)
ROW_MID = lambda i: ROW_Y(i) + SRC_H_ROW // 2

# Band x positions (convenient aliases — 帯名で参照可能にするのも良い)
B1_X = B_X_LIST[0]; B1_W = BANDS[0][2]
B2_X = B_X_LIST[1] if len(B_X_LIST) > 1 else None
B2_W = BANDS[1][2] if len(BANDS) > 1 else None
B3_X = B_X_LIST[2] if len(B_X_LIST) > 2 else None
B3_W = BANDS[2][2] if len(BANDS) > 2 else None
B4_X = B_X_LIST[3] if len(B_X_LIST) > 3 else None
B4_W = BANDS[3][2] if len(BANDS) > 3 else None


# ============================================================
# Cell helpers
# ============================================================
cells = []
counter = [10]


def gid():
    counter[0] += 1
    return f"n{counter[0]}"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&apos;"))


def add_cell(value, style, x, y, w, h):
    cid = gid()
    v = esc(value) if value else ""
    cells.append(
        f'<mxCell id="{cid}" value="{v}" style="{style}" vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>'
    )
    return cid


def add_edge_pts(x1, y1, x2, y2, style, label="", waypoints=None):
    cid = gid()
    v = esc(label)
    waypts = ""
    if waypoints:
        pts = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in waypoints)
        waypts = f'<Array as="points">{pts}</Array>'
    cells.append(
        f'<mxCell id="{cid}" value="{v}" style="{style}" edge="1" parent="1">'
        f'<mxGeometry relative="1" as="geometry">'
        f'<mxPoint x="{x1}" y="{y1}" as="sourcePoint"/>'
        f'<mxPoint x="{x2}" y="{y2}" as="targetPoint"/>'
        f"{waypts}</mxGeometry></mxCell>"
    )
    return cid


def flow_arrow(x1, y1, x2, y2, label="", color=ARROW_DARK, dashed=False, waypoints=None):
    s = (f"endArrow=block;endFill=1;html=1;rounded=0;strokeColor={color};"
         f"strokeWidth=1.6;fontColor={color};fontSize=10;labelBackgroundColor=#FFFFFF;")
    if dashed:
        s += "dashed=1;dashPattern=4 3;"
    add_edge_pts(x1, y1, x2, y2, s, label, waypoints=waypoints)


# ============================================================
# Box helpers (固定語彙 — 絵文字禁止、これらの組み合わせで全表現)
# ============================================================
def plain_box(x, y, w, h, label, fill="#FFFFFF", stroke="#555555"):
    return add_cell(label,
        f"rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
        f"strokeWidth=1.5;fontColor={TEXT_DARK};fontSize=11;align=center;"
        f"verticalAlign=middle;fontStyle=1;",
        x, y, w, h)


def actor_box(x, y, w, h, label, stroke="#555555"):
    """頭+肩シルエット (NOT umlActor 棒人間)"""
    return add_cell(label,
        f"shape=actor;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={stroke};"
        f"strokeWidth=1.5;fontColor={TEXT_DARK};fontSize=11;align=center;"
        f"verticalAlign=middle;fontStyle=1;",
        x, y, w, h)


def yellow_box(x, y, w, h, label):
    return add_cell(label,
        f"rounded=0;whiteSpace=wrap;html=1;fillColor={YELLOW_FILL};"
        f"strokeColor={YELLOW_STROKE};strokeWidth=1.5;fontColor={TEXT_DARK};"
        f"fontSize=11;align=center;verticalAlign=middle;fontStyle=1;",
        x, y, w, h)


def lblue_box(x, y, w, h, label):
    return add_cell(label,
        f"rounded=0;whiteSpace=wrap;html=1;fillColor={LBLUE_FILL};"
        f"strokeColor={LBLUE_STROKE};strokeWidth=1.5;fontColor={TEXT_DARK};"
        f"fontSize=11;align=center;verticalAlign=middle;fontStyle=1;",
        x, y, w, h)


def proc_box(x, y, w, h, label):
    return add_cell(label,
        f"rounded=0;whiteSpace=wrap;html=1;fillColor={PROC_FILL};"
        f"strokeColor={PROC_STROKE};strokeWidth=1.5;fontColor={TEXT_DARK};"
        f"fontSize=11;align=center;verticalAlign=middle;fontStyle=1;",
        x, y, w, h)


def core_box(x, y, w, h, label, subtitle=""):
    """中核要素 (LLM/エンジン等) を orange 強調"""
    full_label = label
    if subtitle:
        full_label = f"<b>{label}</b><br><font style='font-size:9px;color:#666;font-weight:normal'>{subtitle}</font>"
    return add_cell(full_label,
        f"rounded=0;whiteSpace=wrap;html=1;fillColor={CORE_FILL};strokeColor={CORE_STROKE};"
        f"strokeWidth=2.5;fontColor={TEXT_DARK};fontSize=13;fontStyle=1;align=center;verticalAlign=middle;",
        x, y, w, h)


def cylinder(x, y, w, h, label, fill, stroke, font_size=12, size=18):
    return add_cell(label,
        f"shape=cylinder3;whiteSpace=wrap;html=1;fillColor={fill};"
        f"strokeColor={stroke};strokeWidth=2;size={size};"
        f"fontColor={TEXT_DARK};fontSize={font_size};fontStyle=1;align=center;verticalAlign=middle;",
        x, y, w, h)


def doc_box(x, y, w, h, label, fill="#FFFFFF", stroke=PROC_STROKE):
    return add_cell(label,
        f"shape=document;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
        f"strokeWidth=1.5;fontColor={TEXT_DARK};fontSize=11;align=center;"
        f"verticalAlign=middle;fontStyle=1;",
        x, y, w, h)


def multi_doc_box(x, y, w, h, label, fill="#FFFFFF", stroke=PROC_STROKE):
    return add_cell(label,
        f"shape=mxgraph.flowchart.multi_document;whiteSpace=wrap;html=1;"
        f"fillColor={fill};strokeColor={stroke};strokeWidth=1.5;"
        f"fontColor={TEXT_DARK};fontSize=11;align=center;verticalAlign=middle;fontStyle=1;",
        x, y, w, h)


def cloud_box(x, y, w, h, label, fill="#FFFFFF", stroke=PROC_STROKE):
    return add_cell(label,
        f"shape=cloud;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
        f"strokeWidth=1.5;fontColor={TEXT_DARK};fontSize=11;align=center;"
        f"verticalAlign=middle;fontStyle=1;",
        x, y, w, h)


def hexagon_box(x, y, w, h, label, fill="#FFFFFF", stroke=PROC_STROKE):
    return add_cell(label,
        f"shape=hexagon;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
        f"strokeWidth=1.5;fontColor={TEXT_DARK};fontSize=11;align=center;"
        f"verticalAlign=middle;fontStyle=1;perimeter=hexagonPerimeter2;",
        x, y, w, h)


def step_box(x, y, w, h, label, fill="#FFFFFF", stroke=PROC_STROKE):
    return add_cell(label,
        f"shape=step;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
        f"strokeWidth=1.5;fontColor={TEXT_DARK};fontSize=11;align=center;"
        f"verticalAlign=middle;fontStyle=1;",
        x, y, w, h)


def terminator_box(x, y, w, h, label, fill="#FFFFFF", stroke=PROC_STROKE):
    return add_cell(label,
        f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
        f"strokeWidth=1.5;fontColor={TEXT_DARK};fontSize=11;align=center;"
        f"verticalAlign=middle;fontStyle=1;arcSize=50;",
        x, y, w, h)


def decision_box(x, y, w, h, label, fill="#FFFFFF", stroke=PROC_STROKE):
    return add_cell(label,
        f"shape=rhombus;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
        f"strokeWidth=1.5;fontColor={TEXT_DARK};fontSize=11;align=center;"
        f"verticalAlign=middle;fontStyle=1;",
        x, y, w, h)


def manual_input_box(x, y, w, h, label, fill=YELLOW_FILL, stroke=YELLOW_STROKE):
    return add_cell(label,
        f"shape=mxgraph.flowchart.manual_input;whiteSpace=wrap;html=1;"
        f"fillColor={fill};strokeColor={stroke};strokeWidth=1.5;"
        f"fontColor={TEXT_DARK};fontSize=11;align=center;verticalAlign=middle;fontStyle=1;",
        x, y, w, h)


def database_box(x, y, w, h, label, fill=DB_FILL, stroke=DB_STROKE):
    return add_cell(label,
        f"shape=mxgraph.flowchart.database;whiteSpace=wrap;html=1;"
        f"fillColor={fill};strokeColor={stroke};strokeWidth=1.5;"
        f"fontColor={TEXT_DARK};fontSize=11;align=center;verticalAlign=middle;fontStyle=1;",
        x, y, w, h)


def storage_box(x, y, w, h, label, fill="#FFFFFF", stroke=PROC_STROKE):
    return add_cell(label,
        f"shape=mxgraph.flowchart.internal_storage;whiteSpace=wrap;html=1;"
        f"fillColor={fill};strokeColor={stroke};strokeWidth=1.5;"
        f"fontColor={TEXT_DARK};fontSize=11;align=center;verticalAlign=middle;fontStyle=1;",
        x, y, w, h)


def server_box(x, y, w, h, label, fill="#FFFFFF", stroke=PROC_STROKE):
    return add_cell(label,
        f"shape=mxgraph.networks.server;whiteSpace=wrap;html=1;"
        f"fillColor={fill};strokeColor={stroke};strokeWidth=1.5;"
        f"fontColor={TEXT_DARK};fontSize=11;align=center;verticalAlign=middle;fontStyle=1;"
        f"verticalLabelPosition=bottom;verticalAlign=top;",
        x, y, w, h)


# ============================================================
# AUTO: 骨組み描画 (title / header / 帯 / 列 / source→ingest)
# ============================================================
def draw_skeleton():
    """共通の骨組みを描画。返り値: (src_y_centers, ingest_y_centers, tgt_y_by_row)"""
    # Title
    add_cell(TITLE,
        f"text;html=1;align=center;verticalAlign=middle;fontSize=12;fontColor={TEXT_DARK};fontStyle=1;",
        0, 2, PAGE_W, 14)

    # Header bar
    add_cell(HDR_LABEL,
        f"rounded=0;whiteSpace=wrap;html=1;fillColor={NAVY_HDR};strokeColor={NAVY_HDR};"
        f"fontColor={NAVY_TXT};fontSize=14;fontStyle=1;align=center;verticalAlign=middle;",
        COL1_X, HDR_BAR_Y, BAND_TOTAL_W, HDR_BAR_H)

    # Band headers + backgrounds
    for i, ((jp, en, w), x) in enumerate(zip(BANDS, B_X_LIST)):
        html = (f'<b><font style="font-size:13px;color:{BAND_HDR_TXT}">{jp}</font></b>'
                f'<br><font style="font-size:9px;color:#5C7A99">{en}</font>')
        add_cell(html,
            f"shape=mxgraph.flowchart.process;whiteSpace=wrap;html=1;"
            f"fillColor={BAND_HDR_BG};strokeColor={NAVY_HDR};strokeWidth=1;"
            f"fontColor={BAND_HDR_TXT};align=center;verticalAlign=middle;",
            x + 4, BAND_HDR_Y, w - 8, BAND_HDR_H)
        fill = "#F8FAFC" if i % 2 == 0 else "#EEF3F8"
        add_cell("",
            f"rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={GRAY_LINE};strokeWidth=1;",
            x, BODY_Y, w, BODY_H)

    # Outer container (navy border)
    add_cell("",
        f"rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor={NAVY_HDR};strokeWidth=2;",
        COL1_X, BAND_HDR_Y, BAND_TOTAL_W, BAND_HDR_H + BODY_H + 4)

    # Source column
    add_cell(SRC_COL_HEADER,
        f"rounded=0;whiteSpace=wrap;html=1;fillColor={RED_SIDE};strokeColor={RED_SIDE};"
        f"fontColor=#FFFFFF;fontSize=12;fontStyle=1;align=center;verticalAlign=middle;",
        SRC_X, BAND_HDR_Y, SRC_W, BAND_HDR_H)
    src_y_centers = []
    for i, src in enumerate(SOURCES):
        y = ROW_Y(i)
        if src["kind"] == "actor":
            actor_box(SRC_X + 14, y, SRC_W - 28, SRC_H_ROW, src["label"])
        else:
            plain_box(SRC_X + 14, y, SRC_W - 28, SRC_H_ROW, src["label"])
        src_y_centers.append(ROW_MID(i))

    # Target column
    add_cell(TGT_COL_HEADER,
        f"rounded=0;whiteSpace=wrap;html=1;fillColor={RED_SIDE};strokeColor={RED_SIDE};"
        f"fontColor=#FFFFFF;fontSize=12;fontStyle=1;align=center;verticalAlign=middle;",
        TGT_X, BAND_HDR_Y, TGT_W, BAND_HDR_H)
    tgt_y_by_row = {}
    for tgt in TARGETS:
        row = tgt["row"]; y = ROW_Y(row)
        if tgt["kind"] == "actor":
            actor_box(TGT_X + 14, y, TGT_W - 28, SRC_H_ROW, tgt["label"])
        else:
            plain_box(TGT_X + 14, y, TGT_W - 28, SRC_H_ROW, tgt["label"])
        tgt_y_by_row[row] = ROW_MID(row)

    # Edge labels
    for el in EDGE_LABELS:
        row = el["row"]; y = ROW_Y(row)
        add_cell(el["label"],
            f"rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={RED_EDGE};"
            f"strokeWidth=1.5;fontColor={RED_EDGE};fontSize=10;fontStyle=1;align=center;"
            f"verticalAlign=middle;",
            EDGE_X, y, EDGE_W, SRC_H_ROW)

    # 収集 band: ingest boxes + Source → Ingest arrows
    ingest_y_centers = []
    for i, name in enumerate(INGESTS):
        y = ROW_Y(i) + (SRC_H_ROW - SBOX_H) // 2
        yellow_box(B1_X + 18, y, B1_W - 36, SBOX_H, name)
        cy = y + SBOX_H // 2
        ingest_y_centers.append(cy)
        flow_arrow(SRC_X + SRC_W, src_y_centers[i], B1_X + 18, cy)

    return src_y_centers, ingest_y_centers, tgt_y_by_row


# ============================================================
# AUTO: 横断機能 band + footer + XML output
# ============================================================
def draw_governance_band():
    if not GOV_BAND_ITEMS:
        return BODY_END
    GOV_Y = BODY_END + 12
    GOV_H = 70
    add_cell("横断機能 / 運用・ガバナンス  (Cross-cutting Concerns)",
        f"rounded=0;whiteSpace=wrap;html=1;fillColor={GOV_HDR_FILL};strokeColor={GOV_HDR_FILL};"
        f"fontColor=#FFFFFF;fontSize=11;fontStyle=1;align=left;verticalAlign=middle;spacingLeft=14;",
        COL1_X, GOV_Y, BAND_TOTAL_W, 22)
    add_cell("",
        f"rounded=0;whiteSpace=wrap;html=1;fillColor={GOV_FILL};strokeColor={GOV_HDR_FILL};strokeWidth=1.5;",
        COL1_X, GOV_Y + 22, BAND_TOTAL_W, GOV_H - 22)
    item_w = (BAND_TOTAL_W - 28) // len(GOV_BAND_ITEMS)
    item_y = GOV_Y + 28
    for i, (t, s) in enumerate(GOV_BAND_ITEMS):
        x = COL1_X + 14 + i * item_w
        label = f'<b>{t}</b><br><font style="color:#666;font-size:9px;font-weight:normal">{s}</font>'
        add_cell(label,
            f"rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={GOV_HDR_FILL};"
            f"strokeWidth=1;fontColor={TEXT_DARK};fontSize=10;align=center;verticalAlign=middle;",
            x, item_y, item_w - 10, GOV_H - 36)
    return GOV_Y + GOV_H


def draw_footer(below_y):
    if FOOTER_NOTE:
        add_cell(FOOTER_NOTE,
            "text;html=1;align=left;verticalAlign=middle;fontSize=9;fontColor=#666666;",
            SRC_X, below_y + 6, PAGE_W - 50, 14)


def write_drawio():
    body = "\n        ".join(cells)
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" agent="Claude" version="22.0.0">
  <diagram name="SIer Architecture" id="sier-arch">
    <mxGraphModel dx="{PAGE_W}" dy="{PAGE_H}" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{PAGE_W}" pageHeight="{PAGE_H}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        {body}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"Wrote {OUTPUT_PATH} (cells={len(cells)})")
    png = OUTPUT_PATH.replace(".drawio", ".png")
    print(f"Render: drawio -x -f png -b 20 -s 2 -o {png} {OUTPUT_PATH}")


# ============================================================
# === MANUAL: 蓄積 band + 加工 band + 加工→活用先 矢印 =========
# === ↓↓↓ ここを domain に応じて自由設計 ↓↓↓ =================
# ============================================================
def draw_storage_and_processing(src_y_centers, ingest_y_centers, tgt_y_by_row):
    """蓄積 band 〜 加工 band 〜 加工出力→活用先 までを domain に応じて設計。

    利用可能変数:
        src_y_centers: list[int] — 各 source 行の y center
        ingest_y_centers: list[int] — 各 ingest box の y center
        tgt_y_by_row: dict[row, y] — target の y center
        B1_X, B1_W, B2_X, B2_W, B3_X, B3_W: 帯の x/width
        ROW_Y(i), ROW_MID(i): 行 y
        SBOX_H, SRC_H_ROW: ボックス高さ
        TGT_X: 活用先列の左 x

    利用可能 helpers (絵文字禁止、これらの組み合わせで全表現):
        plain_box / proc_box / yellow_box / lblue_box / core_box
        actor_box / cylinder / database_box / storage_box
        doc_box / multi_doc_box / cloud_box / server_box
        terminator_box / decision_box / manual_input_box / step_box / hexagon_box
        flow_arrow

    --- 以下は RAG default 例。別 domain なら全部書き換える ---
    """
    # === 蓄積 band: Document Lake (red cylinder, 全 source 行を span) ===
    last_src_row = len(SOURCES) - 1
    raw_x = B2_X + 22
    raw_w = B2_W - 44
    raw_top = ROW_Y(0) + 4
    raw_bot = ROW_Y(last_src_row) + SRC_H_ROW - 4
    raw_h = raw_bot - raw_top
    cylinder(raw_x, raw_top, raw_w, raw_h, "ドキュメント<br>レイク", RAW_FILL, RAW_STROKE, font_size=12, size=18)
    raw_mid_y = (raw_top + raw_bot) // 2

    # Ingest → DocLake (converging)
    for cy in ingest_y_centers:
        flow_arrow(B1_X + B1_W - 18, cy, raw_x, raw_mid_y,
                   waypoints=[(B2_X + 4, cy), (B2_X + 4, raw_mid_y)])

    # === 加工 band: 2-path (RAG style) ===
    TOP_Y_CENTER = ROW_MID(0)
    TOP_BOX_Y = TOP_Y_CENTER - SBOX_H // 2

    # 出力 row を取得 (target の最後 row)
    last_tgt_row = max(t["row"] for t in TARGETS)
    BOT_Y_CENTER = ROW_MID(last_tgt_row)
    BOT_BOX_Y = BOT_Y_CENTER - SBOX_H // 2

    # TOP chain (Indexing): 抽出 → チャンク → 埋め込み
    top_x = B3_X + 18
    top_chain_specs = [("抽出 / OCR", 80), ("チャンク分割", 85), ("埋め込み", 70)]
    top_ids = []
    for name, w in top_chain_specs:
        proc_box(top_x, TOP_BOX_Y, w, SBOX_H, name)
        top_ids.append((top_x, top_x + w, TOP_Y_CENTER))
        top_x += w + 12

    # DataLake → 抽出
    flow_arrow(raw_x + raw_w, raw_mid_y, top_ids[0][0], top_ids[0][2])
    # Sequential top chain
    for i in range(len(top_ids) - 1):
        flow_arrow(top_ids[i][1], top_ids[i][2], top_ids[i + 1][0], top_ids[i + 1][2])

    # Center store (Vector DB)
    center_x = top_ids[-1][1] + 12
    center_w = 90
    center_y = TOP_BOX_Y + SBOX_H + 6
    center_h = (BOT_BOX_Y - 6) - center_y
    cylinder(center_x, center_y, center_w, center_h, "Vector DB", DB_FILL, DB_STROKE, font_size=12, size=15)

    # 埋め込み → Vector DB (登録)
    flow_arrow(top_ids[-1][1], top_ids[-1][2], center_x, center_y + center_h // 4, label="登録")

    # BOTTOM chain (Generation): 検索 → リランク → プロンプト → LLM
    bot_x = center_x + center_w + 14
    bot_chain_specs = [("検索", 60, False), ("リランキング", 75, False),
                       ("プロンプト組立", 90, False), ("LLM", 80, True)]
    bot_ids = []
    for name, w, is_core in bot_chain_specs:
        if is_core:
            core_box(bot_x, BOT_BOX_Y - 4, w, SBOX_H + 8, name, subtitle="大規模言語モデル")
        else:
            proc_box(bot_x, BOT_BOX_Y, w, SBOX_H, name)
        bot_ids.append((bot_x, bot_x + w, BOT_Y_CENTER))
        bot_x += w + 10

    # Vector DB → 検索 (参照, dashed green)
    flow_arrow(center_x + center_w, center_y + center_h - center_h // 4,
               bot_ids[0][0], bot_ids[0][2],
               label="参照", color=ARROW_REG, dashed=True)
    # Sequential bottom chain
    for i in range(len(bot_ids) - 1):
        flow_arrow(bot_ids[i][1], bot_ids[i][2], bot_ids[i + 1][0], bot_ids[i + 1][2])

    # === 加工出力 → 活用先 ===
    last_box = bot_ids[-1]
    for tgt in TARGETS:
        row = tgt["row"]
        flow_arrow(last_box[1], last_box[2], TGT_X + 14, tgt_y_by_row[row])


# ============================================================
# === 実行 ===================================================
# ============================================================
src_y_centers, ingest_y_centers, tgt_y_by_row = draw_skeleton()
draw_storage_and_processing(src_y_centers, ingest_y_centers, tgt_y_by_row)
gov_bottom = draw_governance_band()
draw_footer(gov_bottom)
write_drawio()
