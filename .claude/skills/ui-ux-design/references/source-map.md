# Source Map — provenance of every rule

Every rule and decision point in this skill's references ends with a tag like `⟨laws1-012, rui1-053⟩`. Those are atomic knowledge records extracted from the 7 purchased books that are this skill's ONLY substantive sources (V1 policy: no web, no design systems, no model-derived design knowledge).

## Record-id prefix → book

| Prefix | Book | Author(s) | Covers |
|---|---|---|---|
| laws1 | UXデザインの法則 第2版 | Jon Yablonski | 全章 (CH1-12) |
| psy1 / psy2 | インタフェースデザインの心理学 第2版 | Susan Weinschenk | 1-5章 / 6-10章 |
| ia1 / ia2 / ia3 | 情報アーキテクチャ 第4版 | Rosenfeld, Morville, Arango | 1-5章 / 6-9章 / 10-14章 |
| uxp1 | インタフェースデザインのお約束 (101 UX Principles) | Will Grant | ルール002-101 |
| mi1 / mi2 | マイクロインタラクション | Dan Saffer | 1-3章 / 4-6章+付録A |
| di1-di4 | デザイニング・インターフェース 第2版 | Jenifer Tidwell | 序-2章 / 3-4章 / 5-7章 / 8-11章 |
| rui1 | Refactoring UI v1.0.2 | Adam Wathan, Steve Schoger | 全章 |

## Full traceability

Chapter/PDF-page-level locators for every record live in the build workspace, not in this skill (to keep it lean):
- Per-rule map: `~/.skill-build/ui-ux-design/synthesis/source-map.md`
- Full records (statement, chapter, pdf_page, printed_page, support_type): `~/.skill-build/ui-ux-design/ingestion/<book>.jsonl`
- Registry (ISBN, hashes, chapter maps): `~/.skill-build/ui-ux-design/source-registry.yaml`

When asked to justify a recommendation's source, cite the book (and chapter if needed) via the record prefix — never invent page numbers from memory; look them up in the build files above if precision is required.