"""40 RAG: the two halves of the pipeline on one grid. Ingestion runs once
per corpus (top); retrieval runs per query (bottom). The rows are offset by
one column so the two Embed steps line up (the same model, or the vectors
would not be comparable) and the vector DB sits directly above Retrieve,
which searches it.

The old figure was 680 wide with 9–11 unit text on a ~10-unit grid, so it
rendered small and cramped; this one uses fewer, larger boxes on a 620-wide
canvas. Retrieve's sub-label uses the prose's "top-50–100 from ANN"
(the set the cross-encoder reranks). Static.
"""
from figkit import Fig, BLUE, GREEN, AMBER, PURPLE, INK, MUTED, FAINT, GAP, LABEL, SMALL, TINY

TARGET = ('40-rag', 0)

CW, CG, X0 = 80, 26, 5        # column width, gap, left margin


def col(i):
    return X0 + i * (CW + CG)


def draw():
    f = Fig(620, 246, 'rag')
    y1, y2, h = 44, 150, 44

    def box(i, y, name, sub, color, ink=None):
        return f.box(col(i), y, CW, h, name, sub, stroke=color, color=ink or color, size=LABEL)

    docs = box(0, y1, 'Raw docs', 'PDFs, wikis, …', BLUE)
    chunk = box(1, y1, 'Chunk', 'split + clean', BLUE)
    emb1 = box(2, y1, 'Embed', 'encoder model', BLUE)
    vdb = box(3, y1, 'Vector DB', 'HNSW index', GREEN)

    qry = box(1, y2, 'Query', 'the question', AMBER)
    emb2 = box(2, y2, 'Embed', 'same model', AMBER)
    ret = box(3, y2, 'Retrieve', 'ANN, top 50–100', GREEN)
    rr = box(4, y2, 'Rerank', 'cross-encoder', PURPLE)
    llm = box(5, y2, 'LLM', 'query + top chunks', PURPLE, INK)

    for a, b in ((docs, chunk), (chunk, emb1), (emb1, vdb)):
        f.connect(a, b, BLUE, 1.5)
    for a, b, c in ((qry, emb2, AMBER), (emb2, ret, AMBER), (ret, rr, GREEN), (rr, llm, PURPLE)):
        f.connect(a, b, c, 1.5)
    f.connect(vdb, ret, GREEN, 1.5)
    f.line(emb1.cx, emb1.b + 6, emb1.cx, emb2.t - 6, FAINT, 1.2, dash='3 4')
    f.arrow(llm.cx, llm.b, llm.cx, llm.b + 30, PURPLE, 1.5)

    f.text(col(0), y1 - 14, 'offline · once per corpus', BLUE, SMALL, weight=600)
    f.text(col(1), y2 - 14, 'online · per query', AMBER, SMALL, weight=600)
    f.label('answer, with sources', [(llm.r, llm.b + 44, 'end')], INK, SMALL, weight=600)
    f.label('same vector space', [(emb1.cx + 6, (emb1.b + emb2.t) / 2 + 3, 'start')], FAINT, TINY)
    f.label('search', [(vdb.cx + 6, (vdb.b + ret.t) / 2 + 3, 'start')], GREEN, TINY)
    f.label('most bad answers are retrieval failures',
            [(col(4), y1 + h / 2 + 3, 'start')], MUTED, SMALL)
    return f
