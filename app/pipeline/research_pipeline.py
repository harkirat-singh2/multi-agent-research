import re
from app.agents.search_agent import build_search_agent
from app.agents.reader_agent import build_reader_agent
from app.chains.writer import writer_chain
from app.chains.critic import critic_chain


# ================================
# Helper Functions
# ================================

def extract_urls(text):
    return re.findall(r'https?://\S+', text)


def to_text(x):
    """Convert LangChain AIMessage → string safely"""
    return x.content if hasattr(x, "content") else str(x)


# ================================
# MAIN PIPELINE (STREAMING)
# ================================

def run_research_pipeline(topic: str):

    state = {}

    # ================================
    # STEP 1: SEARCH
    # ================================
    yield "🔍 Searching...\n"

    try:
        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent reliable information about {topic}")]
        })

        state["search_result"] = search_result["messages"][-1].content

    except Exception as e:
        yield f"❌ Search failed: {str(e)}\n"
        return

    # ================================
    # STEP 2: EXTRACT URLS
    # ================================
    yield "🌐 Extracting URLs...\n"

    urls = extract_urls(state["search_result"])

    if not urls:
        yield "⚠️ No URLs found\n"
        state["scraped_content"] = ""
    else:
        yield f"📖 Scraping {len(urls[:2])} sources...\n"

        reader_agent = build_reader_agent()
        contents = []

        for url in urls[:2]:
            yield f"➡️ {url}\n"

            try:
                result = reader_agent.invoke({
                    "messages": [("user", f"Scrape this URL:\n{url}")]
                })

                content = result["messages"][-1].content
                contents.append(content)

            except Exception as e:
                contents.append(f"Failed to scrape {url}")

        state["scraped_content"] = "\n\n".join(contents)

    # ================================
    # STEP 3: SUMMARIZE (SAFE)
    # ================================
    yield "\n🧠 Summarizing...\n"

    try:
        summary_input = (
            state["search_result"][:500] +
            "\n\n" +
            state["scraped_content"][:800]
        )

        summary = writer_chain.invoke({
            "topic": topic,
            "research": summary_input
        })

        summary = to_text(summary)

    except Exception as e:
        yield f"❌ Summary failed: {str(e)}\n"
        summary = "Summary failed"

    state["summary"] = summary

    # ================================
    # STEP 4: REPORT
    # ================================
    yield "\n✍️ Writing report...\n"

    try:
        report = writer_chain.invoke({
            "topic": topic,
            "research": summary
        })

        report = to_text(report)

    except Exception as e:
        yield f"❌ Report failed: {str(e)}\n"
        report = "Report generation failed"

    state["report"] = report

    # ================================
    # STREAM REPORT
    # ================================
    yield "\n"

    for char in report:
        yield char

    # ================================
    # STEP 5: CRITIQUE
    # ================================
    yield "\n\n=== CRITIQUE ===\n"

    try:
        critique = critic_chain.invoke({
            "report": report
        })

        critique = to_text(critique)

    except Exception as e:
        yield f"❌ Critique failed: {str(e)}\n"
        critique = "Critique failed"

    state["critique"] = critique

    for char in critique:
        yield char

    # ================================
    # STEP 6: SOURCES
    # ================================
    yield "\n\n🔗 SOURCES:\n"

    if urls:
        for url in urls[:5]:
            yield f"- {url}\n"
    else:
        yield "No sources found\n"