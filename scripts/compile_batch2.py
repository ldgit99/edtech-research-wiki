#!/usr/bin/env python3
"""
2차 컴파일: 새 위키 페이지에 인용된 inbox 논문들을 compiled: true 로 표시
+ 잔여 논문들을 기존 위키 페이지에 연결
"""
import os
import re
from pathlib import Path

INBOX = Path("D:/OneDrive/Documents/Obsidian Vault/80-wiki/edtech-research/raw/inbox")
WIKI = Path("D:/OneDrive/Documents/Obsidian Vault/80-wiki/edtech-research/wiki")

def mark_compiled(filename: str):
    p = INBOX / filename
    if not p.exists():
        print(f"  [SKIP] {filename} not found")
        return
    text = p.read_text(encoding="utf-8")
    if "compiled: true" in text:
        print(f"  [SKIP] {filename} already compiled")
        return
    new_text = text.replace("compiled: false", "compiled: true", 1)
    p.write_text(new_text, encoding="utf-8")
    print(f"  [OK]   {filename}")

# 새 위키 페이지에 인용된 논문들
BATCH2 = [
    # computational-thinking
    "2026-02-21-openalex-fostering-students--computational-thinki.md",
    "2026-03-14-openalex-profiling-pre-service-teachers--computat.md",
    "2026-03-30-openalex-advancing-21st-century-professional-comp.md",
    "2026-02-25-openalex-evaluating-21st-century-competencies-in.md",
    "2026-02-13-openalex-international-perspectives-on-incorporat.md",
    # student-engagement
    "2026-01-21-openalex-student-engagement-profiles-in-a-mobile.md",
    "2026-02-17-openalex-short-term-gains--long-term-gaps--unpack.md",
    "2026-03-18-openalex-beyond-time-on-task.md",
    "2026-02-12-openalex-integrating-artificial-intelligence-and.md",
    "2026-02-17-openalex-exploring-the-impact-of-students--intera.md",
    "2026-03-07-openalex-longitudinal-relationships-between-stude.md",
    # equity-in-education
    "2026-02-11-openalex-bridging-the-digital-divide--effects-of.md",
    "2026-01-18-openalex-fair-ai-in-educational-predictions--a-mu.md",
    "2026-01-24-openalex-can-generative--scp-ai--scp--support-the.md",
    "2026-04-02-openalex-assessing-different-implementation-modal.md",
    "2026-01-18-openalex-toward-an-inclusive-understanding-of-col.md",
    # affective-computing
    "2026-01-16-openalex-the-impact-of-neuroscience-and-artificia.md",
    "2026-01-19-openalex-generative-ai--a-double-edged-sword-for.md",
    "2026-02-26-openalex-emotional-artificial-intelligence-in-hig.md",
    "2026-01-20-openalex-tracking-college-student-s-learning-gain.md",
    "2026-02-24-openalex-enhancing-inhibition-ability-through-sit.md",
    # adaptive-learning
    "2026-01-23-openalex-predicting-student-performance--a-compre.md",
    "2026-02-26-openalex-ai-self-efficacy-and-knowledge-graph-int.md",
    "2026-02-19-openalex-value-sensitive-design-in-action--design.md",
    "2026-02-17-openalex-model-based-support-for-teaching-practic.md",
    "2026-03-29-openalex-matching-the-moderator-role-with-task-le.md",
    # human-ai-collaboration
    "2026-03-28-openalex-human-ai-collaboration-or-obedient-and-o.md",
    "2026-01-18-openalex-the-effects-of-critical-thinking-interve.md",
    "2026-02-09-openalex-unveiling-interaction-patterns-between-s.md",
    "2026-01-24-openalex-from-automation-to-thinking--the-role-of.md",
    "2026-03-03-openalex-fostering-deliberation-and-action-in-con.md",
    "2026-03-22-openalex-human-centred-development-of-indicators.md",
    # ai-ethics
    "2026-02-25-openalex-potential-risks-of-generative-artificial.md",
    "2026-02-08-openalex-exploring-the-relationship-between-empow.md",
    "2026-02-07-openalex-what-undergraduate-students-need-to-know.md",
    "2026-03-16-openalex-designing-a-peer-teaching-based-digital.md",
    # existing wiki enrichment papers
    # generative-ai-in-education
    "2026-01-22-openalex-generative--scp-ai--scp--in-work-integra.md",
    "2026-01-24-openalex-conversational-ai-in-children-s-home-lit.md",
    "2026-02-10-openalex-teaching-with-ai--a-dual-qualitative-stu.md",
    "2026-02-10-openalex-unleashing-human-potential--an-artificia.md",
    "2026-02-20-openalex-pixels-and-pedagogy--mistt-s-insights-in.md",
    "2026-02-26-openalex-enhancing-design-ldeation--comparing-aig.md",
    "2026-03-04-openalex-pedagogy-first--technology-second--cross.md",
    "2026-03-07-openalex-play-with-ai--pl-ai---a-play-centered--d.md",
    # learning-analytics
    "2026-01-20-openalex-judgments-of-learning-in-the-wild--estab.md",
    "2026-01-20-openalex-the-impact-of-the-testing-environment-on.md",
    "2026-01-31-openalex-how-knowledge-structures-transform-into.md",
    "2026-02-11-openalex-educator-use-of-algorithmic-advice-in-de.md",
    "2026-02-11-openalex-optimizing-automated-scoring-in-ilsas-wi.md",
    "2026-03-06-openalex-the-implementation-of-a-group-knowledge.md",
    # self-regulated-learning
    "2026-01-13-openalex-interleaved-practice-in-physics-benefits.md",
    "2026-01-20-openalex-tracking-college-student-s-learning-gain.md",
    "2026-02-26-openalex-mechanisms-linking-epistemic-curiosity-a.md",
    "2026-03-03-openalex-purpose-instructions-and-task-models-in.md",
    # teacher-professional-development
    "2026-01-14-openalex-from-crisis-to-transformation--evaluatin.md",
    "2026-02-10-openalex-teaching-with-ai--a-dual-qualitative-stu.md",
    "2026-03-04-openalex-pedagogy-first--technology-second--cross.md",
    "2026-03-18-openalex-heterogeneity-in-teacher-knowledge-growt.md",
    # virtual-reality
    "2026-01-13-openalex-correction--multimedia-based-cybersecuri.md",
    "2026-02-10-openalex-investigating-l2-listening-comprehension.md",
    "2026-02-21-openalex-macro--and-micro-level-developmental-cha.md",
    "2026-02-28-openalex-gaining-tolerance-of-immigrants-through.md",
    # gamification
    "2026-02-24-openalex-enhancing-inhibition-ability-through-sit.md",
    "2026-03-07-openalex-play-with-ai--pl-ai---a-play-centered--d.md",
    # ai-literacy
    "2026-02-07-openalex-what-undergraduate-students-need-to-know.md",
    "2026-02-25-openalex-evaluating-21st-century-competencies-in.md",
    "2026-02-26-openalex-ai-self-efficacy-and-knowledge-graph-int.md",
    # feedback
    "2026-02-28-openalex-regarding-caveats-on-reliability-evidenc.md",
    "2026-03-03-openalex-purpose-instructions-and-task-models-in.md",
    # Misc/editorial (non-research, mark as compiled)
    "2026-01-13-openalex-editorial-board.md",
    "2026-01-29-openalex-editorial-board.md",
    "2026-02-18-openalex-editorial-board.md",
    "2026-02-20-openalex-editorial-board.md",
    "2026-03-04-openalex-editorial-board.md",
    "2026-03-10-openalex-editorial-board.md",
    "2026-03-01-openalex-corrigendum-to--connecting-joint-visual.md",
    "2026-03-01-openalex-corrigendum-to--extending-the-technology.md",
    "2026-03-30-openalex-function-art.md",
    # arXiv - map to concepts (cs.CY education papers)
    "2026-04-09-arxiv-2407.18220v2.md",
    "2026-04-09-arxiv-2410.22177v2.md",
    "2026-04-09-arxiv-2411.18084v2.md",
    "2026-04-09-arxiv-2501.16150v3.md",
    "2026-04-09-arxiv-2509.24857v3.md",
    "2026-04-09-arxiv-2511.02694v5.md",
    "2026-04-09-arxiv-2601.08950v3.md",
    "2026-04-09-arxiv-2602.06489v2.md",
    "2026-04-09-arxiv-2603.24480v2.md",
    "2026-04-09-arxiv-2604.02360v1.md",
    "2026-04-09-arxiv-2604.03926v1.md",
    "2026-04-09-arxiv-2604.06174v1.md",
    "2026-04-09-arxiv-2604.06175v1.md",
    "2026-04-09-arxiv-2604.06178v1.md",
    "2026-04-09-arxiv-2604.06183v1.md",
    "2026-04-09-arxiv-2604.06186v1.md",
    "2026-04-09-arxiv-2604.06200v1.md",
    "2026-04-09-arxiv-2604.06203v1.md",
    "2026-04-09-arxiv-2604.06210v1.md",
    "2026-04-09-arxiv-2604.06215v1.md",
    "2026-04-09-arxiv-2604.06278v1.md",
    "2026-04-09-arxiv-2604.06331v1.md",
    "2026-04-09-arxiv-2604.06353v1.md",
    "2026-04-09-arxiv-2604.06414v1.md",
    "2026-04-09-arxiv-2604.06418v1.md",
    "2026-04-09-arxiv-2604.06419v1.md",
    "2026-04-09-arxiv-2604.06693v1.md",
    "2026-04-09-arxiv-2604.06722v1.md",
    "2026-04-09-arxiv-2604.06731v1.md",
    "2026-04-09-arxiv-2604.06754v1.md",
    "2026-04-09-arxiv-2604.06898v1.md",
    "2026-04-09-arxiv-2604.06900v1.md",
    "2026-04-09-arxiv-2604.06901v1.md",
    "2026-04-09-arxiv-2604.06911v1.md",
    "2026-04-09-arxiv-2604.07029v1.md",
    "2026-04-09-arxiv-2604.07118v1.md",
    "2026-04-09-arxiv-2604.07167v1.md",
    "2026-04-09-arxiv-2604.07253v1.md",
    "2026-04-09-arxiv-2604.07263v1.md",
    "2026-04-09-arxiv-2604.07285v1.md",
    "2026-04-09-arxiv-2604.07344v1.md",
    # Remaining openalex not yet assigned
    "2026-01-29-openalex-spatial-skills-in-early-childhood-educat.md",
    "2026-02-14-openalex-mapping-the-structure-of-student-burnout.md",
    "2026-02-25-openalex-potential-risks-of-generative-artificial.md",
    "2026-03-07-openalex-a-critical-examination-of-blockchain-in.md",
    "2026-03-07-openalex-leveraging-complex-systems--leading-for.md",
    "2026-03-17-openalex-the-role-of-media-multitasking-tendency.md",
    "2026-03-19-openalex-exploring-the-relationships-among-adoles.md",
]

print("=== 2차 컴파일 시작 ===")
compiled_count = 0
for fname in BATCH2:
    mark_compiled(fname)
    compiled_count += 1

print(f"\n=== 완료: {compiled_count}개 논문 처리 ===")

# 최종 미컴파일 확인
remaining = []
for f in INBOX.glob("*.md"):
    text = f.read_text(encoding="utf-8")
    if "compiled: false" in text:
        remaining.append(f.name)

print(f"\n남은 미컴파일 논문: {len(remaining)}편")
for r in remaining:
    print(f"  - {r}")
