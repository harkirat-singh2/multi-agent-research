from app.agents.search_agent import build_search_agent
from app.agents.reader_agent import build_reader_agent
from app.chains.writer import writer_chain
from app.chains.critic import critic_chain
from app.core.utils import extract_urls, safe_invoke
from app.core.config import llm
import time
import concurrent.futures


# =========================================================
# 🚀 MAIN PIPELINE
# =========================================================

def run_research_pipeline(topic: str):

    state = {
        "topic": topic,
        "steps": [],
        "search_result": "",
        "urls": [],
        "scraped_content": "",
        "summary": "",
        "report": "",
        "critique": ""
    }

    print(f"\n🚀 Starting research for: {topic}")

    # ===== STEP 1: SEARCH =====
    search_agent = build_search_agent()
    state["steps"].append("Searching web")

    search_output = safe_invoke(
        search_agent,
        {"messages": [("user", f"Find reliable and recent info about: {topic}")]}
    )

    state["search_result"] = search_output
    print("\n🔍 SEARCH RESULT:\n", search_output[:500])

    # ===== STEP 2: EXTRACT URLS =====
    urls = extract_urls(search_output)

    if not urls:
        state["steps"].append("No URLs found")
        state["scraped_content"] = "No sources available."
        print("\n⚠️ No URLs found.")
    else:
        urls = urls[:3]
        state["urls"] = urls
        state["steps"].append(f"{len(urls)} URLs extracted")

        print("\n🌐 URLS:\n", urls)

        # ===== STEP 3: PARALLEL SCRAPING =====
        reader_agent = build_reader_agent()
        state["steps"].append("Parallel scraping started")

        def scrape(url):
            result = safe_invoke(reader_agent, {
                "messages": [("user", f"Extract useful content from:\n{url}")]
            })

            # 🔁 Retry once if failed
            if "Error" in result:
                result = safe_invoke(reader_agent, {
                    "messages": [("user", f"Extract useful content from:\n{url}")]
                })

            return result

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(scrape, urls))

        state["scraped_content"] = "\n\n".join(results)

    print("\n📖 SCRAPED CONTENT:\n", state["scraped_content"][:500])

    # =========================================================
    # 🧠 STEP 4: SUMMARIZATION (NEW)
    # =========================================================
    state["steps"].append("Summarizing content")

    try:
        summary = llm.invoke(
            f"Extract key insights, trends, and important facts:\n{state['scraped_content'][:1200]}"
        )
        state["summary"] = summary
    except Exception as e:
        state["summary"] = f"Summary failed: {str(e)}"

    print("\n🧠 SUMMARY:\n", state["summary"][:500])

    # =========================================================
    # ✍️ STEP 5: WRITING
    # =========================================================
    state["steps"].append("Generating report")

    try:
        report = writer_chain.invoke({
            "topic": topic,
            "research": state["summary"]   # ✅ using summary (IMPORTANT)
        })
        state["report"] = report
    except Exception as e:
        state["report"] = f"Report generation failed: {str(e)}"

    print("\n✍️ REPORT:\n", state["report"][:800])

    # =========================================================
    # 🧠 STEP 6: CRITIC
    # =========================================================
    state["steps"].append("Reviewing report")

    try:
        critique = critic_chain.invoke({
            "report": state["report"]
        })
        state["critique"] = critique
    except Exception as e:
        state["critique"] = f"Critique failed: {str(e)}"

    print("\n🧠 CRITIQUE:\n", state["critique"])

    # =========================================================
    # ✅ FINAL OUTPUT
    # =========================================================
    state["steps"].append("Pipeline completed")

    return {
        "report": state["report"],
        "critique": state["critique"],
        "sources": state["urls"],   # 🔗 important
        "steps": state["steps"]
    }


# =========================================================
# 🌊 STREAMING VERSION (UPDATED)
# =========================================================

def run_research_stream(topic: str):

    yield "🔍 Searching...\n"

    search_agent = build_search_agent()
    search_result = safe_invoke(
        search_agent,
        {"messages": [("user", topic)]}
    )

    yield "🌐 Extracting URLs...\n"
    urls = extract_urls(search_result)[:2]

    reader_agent = build_reader_agent()

    yield "📖 Scraping sources...\n"

    contents = []
    for url in urls:
        content = safe_invoke(reader_agent, {
            "messages": [("user", url)]
        })

        # retry
        if "Error" in content:
            content = safe_invoke(reader_agent, {
                "messages": [("user", url)]
            })

        contents.append(content)
        yield f"✔ Scraped: {url}\n"

    yield "\n🧠 Summarizing...\n"

    summary = llm.invoke(
        f"Extract key insights:\n{str(contents)[:1200]}"
    )

    yield "\n✍️ Writing report...\n\n"

    report = writer_chain.invoke({
        "topic": topic,
        "research": summary
    })

    for char in report:
        yield char

    yield "\n\n🧠 Reviewing...\n"

    critique = critic_chain.invoke({
    "report": report
})

    yield "\n\n=== CRITIQUE ===\n"

# stream critique character by character
    for char in critique:
        yield char
        time.sleep(0.002)

    yield "\n\n🔗 SOURCES:\n"
    for url in urls:
        yield f"- {url}\n"