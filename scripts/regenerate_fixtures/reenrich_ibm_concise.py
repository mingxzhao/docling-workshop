"""Re-enrich the IBM annual report with concise (one-line) section summaries.

This monkey-patches DoclingEnrichingAgent._generate_summary to produce a short
topical phrase per section instead of the default 2-3 sentences. Saves the
result as ibm_annual_report_enriched_concise.json.
"""
import os
import time
from pathlib import Path

import litellm
from docling_core.types.doc.document import DoclingDocument
from mellea import MelleaSession
from mellea.backends import model_ids
from mellea.backends.litellm import LiteLLMBackend
from mellea.stdlib.components import Message
from mellea.stdlib.context import ChatContext

from docling_agent.agents import BackendConfig, BaseBackend, DoclingEnrichingAgent, ModelConfig
from docling_agent.backends.mellea_backend import MelleaSessionAdapter

MODEL_ID = model_ids.IBM_GRANITE_4_2_8B

# --- Replicate backend ---
# LiteLLM stops polling a Replicate prediction after about 25 seconds by default.
litellm.DEFAULT_REPLICATE_POLLING_RETRIES = 30


class ReplicateBackend(BaseBackend):
    """Run every docling-agent session on Replicate through Mellea's LiteLLM backend."""

    backend_type = "mellea"

    def __init__(self, model_id):
        self.model_id = model_id
        name = model_id.hf_model_name
        self.config = BackendConfig(models=ModelConfig(reasoning=name, writing=name))

    @classmethod
    def from_config(cls, config):
        raise NotImplementedError("Create ReplicateBackend(model_id) directly.")

    def create_session(self, *, model, system_prompt=None):
        ctx = ChatContext()
        if system_prompt:
            ctx = ctx.add(Message(role="system", content=system_prompt))
        backend = LiteLLMBackend(model_id=f"replicate/{self.model_id.hf_model_name}")
        return MelleaSessionAdapter(MelleaSession(ctx=ctx, backend=backend))

# --- Concise summary monkey-patch ---
def _patched_generate_summary(self, *, m, text, loop_budget=2, scope="section"):
    def _validate(content):
        c = content.strip()
        # Accept one-liner phrases up to ~150 chars, no line breaks
        return 5 < len(c) <= 200 and "\n" not in c

    return self._generate_content(
        m=m,
        text=text,
        task_prompt=(
            "In a single short phrase of at most 15 words, describe the topic of the following section. "
            "Use plain text only — no markdown, no trailing punctuation."
        ),
        requirement_description=(
            "Return one short phrase (at most 15 words) describing the section's topic. "
            "Plain text only, no line breaks, no markdown."
        ),
        validation_fn=_validate,
        loop_budget=loop_budget,
    )

DoclingEnrichingAgent._generate_summary = _patched_generate_summary

# --- Go ---
assert os.environ.get("REPLICATE_API_TOKEN"), "Set REPLICATE_API_TOKEN first"

# Paths default to <repo>/notebooks/fixtures/. The parsed-JSON source is not
# committed to the repo; either drop it at the default path or point IBM_PARSED_JSON
# at it. The destination overwrites the committed fixture in-place.
FIXTURES = Path(__file__).resolve().parents[2] / "notebooks" / "fixtures"
src = Path(os.environ.get("IBM_PARSED_JSON", FIXTURES / "ibm_annual_report_parsed.json"))
dst = FIXTURES / "ibm_annual_report_enriched_concise.json"
assert src.exists(), f"Source parsed JSON not found at {src}. Set IBM_PARSED_JSON or place the file at the default path."

doc = DoclingDocument.load_from_json(src)

enricher = DoclingEnrichingAgent(tools=[], backend=ReplicateBackend(MODEL_ID))
t0 = time.time()
# Skip _fix_heading_levels — it spins up the editor for extra LLM calls we don't need.
result = enricher._summarize_items(document=doc, fix_heading_levels=False, loop_budget=2)
elapsed = time.time() - t0

print(f"\nEnrichment completed in {elapsed/60:.1f} min")

# Save
result.save_as_json(dst)
print(f"Saved: {dst}")

# Quick stats
summaries = []
for t in result.texts:
    meta = getattr(t, 'meta', None)
    if meta and getattr(meta, 'summary', None):
        summaries.append(meta.summary.text)
print(f"\nSections with summaries: {len(summaries)}")
if summaries:
    lens = [len(s) for s in summaries]
    import statistics
    print(f"Summary char length — min {min(lens)}, median {statistics.median(lens):.0f}, max {max(lens)}, total {sum(lens):,}")
