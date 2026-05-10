---
name: sier-architecture
description: Use when user asks to create a SIer-style enterprise architecture diagram (NTT Data / IBM / Accenture / 日本SIer house style). Covers any architecture — RAG基盤, データ基盤, マイクロサービス, MLパイプライン, クラウド構成, システム全体像, 業務フロー. Generates compact, professional drawio diagrams with horizontal phase bands, side columns for actors/sources/targets, uniform color palette, and clean orthogonal arrow routing. Outputs .drawio + .png to current working directory. Self-reviews rendered image and iterates autonomously until no defects remain. **加工 band layout は domain ごとに自由設計** — 配色・形状・helper のみ固定、layout は flexible。
---

# SIer-Style Architecture Diagram Skill

## 出力規約 (絶対遵守)

- **CWD に作るのは `.drawio` + `.png` の 2 点のみ**
- **build script (.py) は `/tmp/` に置く** — CWD は汚染しない
- 保存先は **CWD (作業ディレクトリ)** — `~/Desktop` や `/Users/mizoo/` に置かない
- ファイル名: `<name>.drawio` / `<name>.png`
- **完成したら必ず Read tool で PNG を表示** — ユーザーが見えるようにする

## 設計原則 — **何を固定し、何を自由にするか**

| 観点 | 方針 |
|---|---|
| **配色パレット** | 🔒 固定 (NAVY/RED/RAW/DB/YELLOW/LBLUE/CORE) |
| **形状語彙 (helper)** | 🔒 固定 (絵文字禁止、19 helper を組み合わせる) |
| **骨組み** (タイトル/帯ヘッダ/列/横断機能) | 🔒 固定 (`draw_skeleton()` で自動) |
| **加工 band の中身 (layout)** | 🆓 **自由** — domain に応じて選ぶ |
| **蓄積 band の中身** | 🆓 自由 (典型は raw cylinder 1 個) |
| **加工 → 活用先 矢印** | 🆓 自由 |

ようするに **「制服 (color/shape) は固定だけど、中身 (layout) は domain に最適化」** が原則。

## 自律実行プロトコル

```
[1] 描画 (template の draw_storage_and_processing() を domain 仕様で書く)
   ↓
[2] PNG レンダリング (drawio CLI)
   ↓
[3] Read tool で画像確認 (必須、スキップ厳禁)
   ↓
[4] Self-review checklist
   ↓
[5] 問題あり? → YES: 修正してループ ([1] へ戻る)
              → NO: 完成、ユーザーに報告
```

「修正した?」と聞かれた時は実画像を再確認してから答える。憶測で答えない。

### Self-review checklist

- [ ] 矢印が cylinder/box を貫通していないか
- [ ] ラベルが要素に被っていないか
- [ ] 形状・色・サイズが統一されているか
- [ ] 縦書き回転テキスト (rotation=-90 + CJK) が残っていないか
- [ ] 矢印が完全直交 (orthogonal) か
- [ ] 帯から overflow していないか (特に bottom chain が右にはみ出してないか)
- [ ] scope と要素数が整合しているか
- [ ] 中核要素 (core_box) が他と区別できるか
- [ ] 行 (row) 単位で y 整列されているか
- [ ] **加工 layout が domain に適切か** (RAG パターンを別 domain に流用してないか)
- [ ] **arrow の semantic が正しいか** (例: Model Registry → モデル推論であって 推論リクエストではない)

## Workflow

### Step 1: 要件最低限の確認

聞くこと:
- ドメイン (RAG / データ基盤 / マイクロサービス / ML / etc.)
- scope (単一 vs 全体像)
- ファイル名

聞かないでデフォルト判断:
- 帯構成 (ドメインの典型に従う)
- 色 / 形状 / 横断機能の有無 (scope による)
- 加工 layout (ドメインに応じて pattern を choose)

### Step 2: テンプレートを `/tmp/` にコピー (CWD は汚さない)

```bash
NAME="<name>"   # 例: rag-platform
cp ~/.claude/skills/sier-architecture/templates/build_sier_arch.py /tmp/build_${NAME}.py
```

### Step 3: `/tmp/build_<name>.py` の CONFIG ブロック編集

- BANDS / SOURCES / INGESTS / TARGETS / EDGE_LABELS / GOV_BAND_ITEMS / TITLE / HDR_LABEL
- **OUTPUT_PATH** は `os.path.join(os.getcwd(), "<name>.drawio")` のまま (CWD に出力する)

### Step 4: **`draw_storage_and_processing()` を domain に応じて書き換える** ⭐重要⭐

`/tmp/build_<name>.py` 内の `draw_storage_and_processing(src_y_centers, ingest_y_centers, tgt_y_by_row)` 関数の中身を domain に応じて再実装する。

デフォルト実装は **RAG 例**。別 domain なら全部書き換え。下記「加工 band 典型パターン」を参考に。

### Step 5: ユーザーの CWD で実行 (出力先がそこになる)

```bash
# Bash の作業ディレクトリ = ユーザーの CWD のまま実行する
python3 /tmp/build_<name>.py
# → ./<name>.drawio が CWD に作られる (os.getcwd() = CWD)

drawio -x -f png -b 20 -s 2 -o ./<name>.png ./<name>.drawio
# → ./<name>.png も CWD に
```

`.py` は `/tmp/` に残るが CWD には侵入しない。

### Step 6: 自律レビュー → 完成

1. **Read tool で `./<name>.png` を表示** (必須、自分で確認するため)
2. Self-review checklist 実施
3. 問題あれば `/tmp/build_<name>.py` を修正 → Step 5 を再実行 → 再 Read
4. 問題なくなったら完成宣言

### Step 7: 完成時の報告 — 必ず PNG を Read で表示

報告時は以下:
1. **`./<name>.png` を Read tool で表示** (ユーザーが画像を見れるように)
2. ファイルパスを明記:

```
| ファイル | パス |
|---|---|
| 編集元 | ./<name>.drawio |
| Slide貼付 | ./<name>.png |
```

## 加工 band 典型パターン集

domain に応じて以下のいずれかを choose、または複数組み合わせる。

### Pattern A: Linear (単純チェーン)

```
[box1] → [box2] → [box3] → [core] → [out]
```

**適用例**: 業務フロー (BPMN)、ETL、シンプルな処理パイプライン

```python
# 加工 band 内に L→R で box を並べる
y_center = ROW_MID(0)  # or 任意の行
y_box = y_center - SBOX_H // 2
x_cursor = B3_X + 18
chain = [("step1", 80), ("step2", 90), ("step3", 90, True)]  # 最後 core
ids = []
for *spec, in chain:
    name, w, is_core = (spec[0], spec[1], spec[2] if len(spec) > 2 else False)
    if is_core: core_box(x_cursor, y_box - 4, w, SBOX_H + 8, name)
    else: proc_box(x_cursor, y_box, w, SBOX_H, name)
    ids.append((x_cursor, x_cursor + w, y_center))
    x_cursor += w + 12
for i in range(len(ids) - 1):
    flow_arrow(ids[i][1], ids[i][2], ids[i+1][0], ids[i+1][2])
```

### Pattern B: 2-Path Converging (上下並走 + 中央データストア)

```
TOP:    [a] → [b] → [c] → ↘
                          [center cyl]
BOT:                      ↗ → [d] → [e] → [core]
```

**適用例**: RAG (Indexing top + Query bottom + Vector DB)、ML 学習+推論 (Training + Inference + Model Registry)

中央 store の **接続先は domain で正しく選ぶ**:
- RAG: Vector DB → ハイブリッド検索 (検索が VDB を参照)
- ML: Model Registry → モデル推論 (推論が Model を load)
- データ基盤: DWH → BI (BI が DWH を読む)

接続先を **bot_ids[0] に決め打ちしない**。意味的に正しい box を target に。

### Pattern C: Branching (1 入力 → 並列処理 → 集約)

```
[input] ─┬→ [proc A] ─┐
         ├→ [proc B] ─┼→ [aggregator] → [out]
         └→ [proc C] ─┘
```

**適用例**: マイクロサービス (1 リクエストを複数サービスで並列処理)、A/B テスト

### Pattern D: Fan-out (1 処理 → 複数出力)

```
                    ┌→ [out A]
[input] → [proc] → ├→ [out B]
                    └→ [out C]
```

**適用例**: イベント駆動 (1 イベント → 複数 subscriber)、複数活用先への配信

### Pattern E: Layered (階層、上から順次処理)

```
Layer 1: [API GW]  [API GW]  [API GW]
Layer 2: [認証]    [認証]    [認証]
Layer 3: [業務]    [業務]    [業務]
Layer 4: [DB]      [DB]      [DB]
```

**適用例**: マイクロサービス全体像、3-tier アーキテクチャ

### Pattern F: Hub & Spoke (中央ハブ ↔ 複数サテライト)

```
              [satellite A]
                  ↕
[satellite C] ↔ [HUB] ↔ [satellite B]
                  ↕
              [satellite D]
```

**適用例**: ESB / メッセージング基盤、API gateway 中心構成

### Pattern G: Free-form (上記に当てはまらない場合)

domain 固有の構造を helper の組み合わせで自由に表現。
**ただし配色・形状・align ルールは守る**。

## Anti-patterns (絶対やらない)

| ❌ NG | ✅ 正解 |
|---|---|
| 加工 band に **常に RAG パターン (TOP/CENTER/BOTTOM)** を当てはめる | domain ごとに pattern を choose |
| 中央 store からの参照矢印を bot_ids[0] に決め打ち | semantic に正しい target box を選ぶ |
| 直列 1 本の長いチェーン (8+ box) | 2-path / branching に分解 |
| 縦書き回転 CJK | 横書き or `<br>` で 1 文字ずつ stack |
| 絵文字 (🤖📊🔒) を box 内に | helper の形状で表現 |
| 矢印が cylinder/box を貫通 | waypoint で迂回 |
| 利用者を入力列に置く | 入力列 = データ知識源のみ |
| 横断機能を footer 注記だけ | visible band として描画 |
| 中核要素が他と同じ見た目 | core_box (orange + h+8) |
| SVG も出力する | png のみ |
| ~/Desktop/ に保存 | CWD のみ |
| **`.py` を CWD に置く** | **`/tmp/` に置く**、CWD は `.drawio` + `.png` のみ |
| 完成宣言時に PNG を表示しない | **必ず Read tool で PNG を表示** |

## 形状カタログ (helper 一覧、絶対これだけ使う)

### 矩形系 (色で意味づけ)

| ヘルパー | 用途 | 色 |
|---|---|---|
| `plain_box` | source/target 列項目 | 白 |
| `proc_box` | 処理 (汎用) | 白 |
| `yellow_box` | 入力 (取込/トリガ) | 黄 |
| `lblue_box` | 出力 (活用/配信) | 青 |
| `core_box` | 中核要素 (LLM/エンジン) | オレンジ + 太枠 |

### 人物・データストア

| ヘルパー | 用途 |
|---|---|
| `actor_box` | ユーザー (頭+肩) |
| `cylinder` | 汎用シリンダー (任意色) |
| `database_box` | データベース (より具体) |
| `storage_box` | キャッシュ/メモリ |

### 文書・インフラ

| ヘルパー | 用途 |
|---|---|
| `doc_box` | 単一文書/ファイル |
| `multi_doc_box` | 複数文書 |
| `cloud_box` | 雲 (外部/SaaS) |
| `server_box` | サーバー (タワー) |

### フロー図要素

| ヘルパー | 用途 |
|---|---|
| `terminator_box` | 開始/終了 |
| `decision_box` | 判断 (ひし形) |
| `manual_input_box` | 手動入力 (平行四辺形, 黄) |
| `step_box` | シェブロン |
| `hexagon_box` | 六角形 |

### 矢印

| ヘルパー | 用途 |
|---|---|
| `flow_arrow(x1,y1,x2,y2,label,color,dashed,waypoints)` | orthogonal 矢印 |

**形状カタログにない shape= は使わない**。AWS アイコン等は別 skill 案件。

## Domain → Layout の選び方ガイド

| Domain | 推奨 Pattern | 中央 store の接続先 |
|---|---|---|
| **RAG基盤** | B (2-path) | Vector DB → ハイブリッド検索 |
| **ML パイプライン** | B (2-path) | Model Registry → モデル推論 |
| **データ基盤** | B (2-path) または A (linear) | DWH → BI/分析 |
| **業務フロー** | A (linear) または E (layered) | — (decision_box, terminator_box 多用) |
| **マイクロサービス** | C (branching) または E (layered) | API GW → 各サービス |
| **イベント駆動** | D (fan-out) | event broker → subscribers |
| **クラウド全体像** | E (layered) | — |
| **ESB/メッセージング** | F (hub & spoke) | — |

## トラブルシューティング

| 症状 | 原因 | 対処 |
|---|---|---|
| 矢印が cylinder 貫通 | waypoints 不足 | 上 (`top - 14`) または下 (`bot + 14`) を迂回 |
| 矢印が斜め | waypoints 不足 | 各 elbow に waypoint 明示 |
| 縦書き読めない | rotation=-90 を CJK に使った | 列幅広げて横書き、または `<br>` で stack |
| 中核要素埋もれる | 同色同サイズ | core_box (orange + h+8) |
| ラベル box 被り | 矢印短く label 位置なし | 削除 or 別 text cell |
| **bottom chain が帯から overflow** | B3_W が狭い、box 幅広い | B3_W 拡大 or box 幅縮小 |
| 加工 layout が domain に合わない | RAG パターンを流用した | pattern A-G から再選定 |

## References

- `templates/build_sier_arch.py` — 骨組み auto + draw_storage_and_processing は手動 (default は RAG)
