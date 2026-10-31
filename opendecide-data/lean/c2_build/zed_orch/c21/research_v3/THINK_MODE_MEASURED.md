# THINK MODE: ALREADY MEASURED on C1 (NOT research; 4-10 Oct 2026; PREREG A17-B0/B0b/B0c/B1a). DECISION: DROP from C2.1.

Measured (C1 router: top prob < 0.8 → base 4B thinking, 1,024-token budget):
- Practice sealed-style sets: OHS-1 C1 80.4 → +think 80.9 (Jev 81.7); OHS-2 81.0 → 80.8 (Jev 81.5). ~0 gain.
- Nimble 13 sets: 74.2 → 76.4 (Jev 76.0); sets seen in training +0.0 (77.55 → 77.56); unseen sets +4.7 (70.4 → 75.1).
  Helps squad2 (+11), summeval (+12); hurts pubmedqa (−3.2), civil_comments (−4.3). Routed ~34% of items.
- Decision Index sample: 54.83 → 57.74 (Jev 59.51).
- Speed (H100, batch 1): fast path 14 ms; think cap300 1.3 s, cap1024 4.3 s, DEER1024 2.8 s, long budget ~5.9 s
  (L4: 4.2-4.8 s/item). A17 B1 rule "think e2e median <= 1 s" FAILED for every policy. DFlash speculative decoding failed.
- Cost: a think call decodes ~500-1,000 tokens vs one prefill → roughly 20x a fast call; with ~1/3 routed ≈ 5-7x average cost,
  which erases the cost lead over Jev ($0.023/1K) and turns 14 ms into ~1-1.5 s average.

Orchestrator decision (18 Oct; the owner's own concern: "the trade-off is it also increases latency and the cost"):
the selective-think tier is REMOVED from C2.1 (it was an owner-reserved option to adopt; dropping it needs no rule change).
The planner must not list it as a lever. General-accuracy levers are data-side only (public train splits if the owner
approves, harder program-gold data, error-focused selection, checkpoint blending). Phase B (B1b/B2) stays parked.
