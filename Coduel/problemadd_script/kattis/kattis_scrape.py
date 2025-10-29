import requests
from bs4 import BeautifulSoup, NavigableString
import re
import json
import os
from textwrap import dedent
from urllib.parse import urljoin

BASE_URL = "https://open.kattis.com/problems/"

LATEX_INLINE_RE = re.compile(r"\$([^$]+)\$")
LATEX_REPLACEMENTS = [
    (r"\\leq?", "≤"),
    (r"\\geq?", "≥"),
    (r"\\neq", "≠"),
    (r"\\lt", "<"),
    (r"\\gt", ">"),
    (r"\\times", "×"),
    (r"\\cdot", "·"),
    (r"\\pm", "±"),
    (r"\\div", "÷"),
    (r"\\ldots", "…"),
    (r"\\dots", "…"),
    (r"\\le", "≤"),
    (r"\\ge", "≥"),
]

def _latex_to_plain(segment: str) -> str:
    """Best-effort conversion of small inline LaTeX to readable text."""
    if not segment:
        return ""
    # Normalize common spacing commands
    segment = segment.replace(r"\,", " ")
    segment = segment.replace(r"\;", " ")
    segment = segment.replace(r"\:", " ")
    segment = segment.replace(r"\!", "")
    segment = segment.replace(r"~", " ")
    segment = segment.replace(r"\\", "\n")
    segment = re.sub(r"\\(left|right)", "", segment)
    for pattern, repl in LATEX_REPLACEMENTS:
        segment = re.sub(pattern, repl, segment)
    # Remove braces that wrap single tokens like {N}
    segment = re.sub(r"\{([^{}]+)\}", r"\1", segment)
    # Remove remaining backslashes that escape single characters
    segment = re.sub(r"\\([a-zA-Z0-9])", r"\1", segment)
    # Collapse multiple spaces/newlines
    segment = re.sub(r"[ \t]+", " ", segment)
    segment = re.sub(r"\n\s*", "\n", segment)
    return segment.strip()

def normalize_text(text: str) -> str:
    """Normalize inline math markers inside scraped text."""
    if not text:
        return text

    def repl(match):
        return _latex_to_plain(match.group(1))

    text = LATEX_INLINE_RE.sub(repl, text)
    text = _latex_to_plain(text)
    return text

def _parse_time_limit(text: str):
    """Return time limit in milliseconds parsed from text."""
    text = text.lower()
    # milliseconds
    m = re.search(r"([\d.]+)\s*(?:ms|milliseconds?)", text)
    if m:
        return int(float(m.group(1)))
    # seconds
    m = re.search(r"([\d.]+)\s*(?:s|sec|seconds?)", text)
    if m:
        return int(float(m.group(1)) * 1000)
    # minutes
    m = re.search(r"([\d.]+)\s*(?:m|min|minutes?)", text)
    if m:
        return int(float(m.group(1)) * 60_000)
    return None

def _parse_memory_limit(text: str):
    """Return memory limit in kilobytes parsed from text."""
    text = text.lower()
    m = re.search(r"([\d.]+)\s*(?:kb|kilobytes?)", text)
    if m:
        return int(float(m.group(1)))
    m = re.search(r"([\d.]+)\s*(?:mb|megabytes?)", text)
    if m:
        return int(float(m.group(1)) * 1024)
    m = re.search(r"([\d.]+)\s*(?:gb|gigabytes?)", text)
    if m:
        return int(float(m.group(1)) * 1024 * 1024)
    return None

def fetch_problem_html(slug: str) -> BeautifulSoup:
    url = BASE_URL + slug
    resp = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "CoduelKattisImporter/1.0 (+https://coduel.local)"
        },
    )
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def extract_limits(soup: BeautifulSoup):
    """
    Parse "Time limit: 1 s" / "Memory limit: 1024 MB"
    Returns (time_limit_ms:int|None, memory_limit_kb:int|None)
    """
    limit_box = soup.find("div", class_="limits")
    if not limit_box:
        # fallback: older layout sometimes puts it in problem-sidebar
        limit_box = soup.find("div", class_="problem-sidebar")
    time_ms = None
    mem_kb = None

    if limit_box:
        text = limit_box.get_text(" ", strip=True)
        parsed_time = _parse_time_limit(text)
        if parsed_time is not None:
            time_ms = parsed_time
        parsed_mem = _parse_memory_limit(text)
        if parsed_mem is not None:
            mem_kb = parsed_mem

    if time_ms is None:
        time_card = soup.find("div", class_=lambda c: c and "metadata-cpu-card" in c)
        if time_card:
            parsed_time = _parse_time_limit(time_card.get_text(" ", strip=True))
            if parsed_time is not None:
                time_ms = parsed_time

    if mem_kb is None:
        mem_card = soup.find("div", class_=lambda c: c and ("metadata-memmory-card" in c or "metadata-memory-card" in c))
        if mem_card:
            parsed_mem = _parse_memory_limit(mem_card.get_text(" ", strip=True))
            if parsed_mem is not None:
                mem_kb = parsed_mem

    return time_ms, mem_kb

def extract_difficulty(soup: BeautifulSoup):
    """
    Kattis sometimes shows Difficulty: 1.5
    We'll map numeric -> bucket fast/easy/medium/hard
    """
    diff_val = None

    # Try to find something like "Difficulty: 1.6" in sidebar/meta
    meta_boxes = soup.find_all(["div","p","span","li"], string=re.compile(r"Difficulty", re.I))
    for node in meta_boxes:
        m = re.search(r"Difficulty:\s*([\d.]+)", node.get_text(" ", strip=True), re.I)
        if m:
            try:
                diff_val = float(m.group(1))
                break
            except ValueError:
                pass

    # Another approach: some pages have table rows
    if diff_val is None:
        for row in soup.find_all("tr"):
            header = row.find(["th","td"])
            if header and "difficulty" in header.get_text(strip=True).lower():
                cells = row.find_all("td")
                for c in cells:
                    m = re.search(r"([\d.]+)", c.get_text(strip=True))
                    if m:
                        try:
                            diff_val = float(m.group(1))
                            break
                        except ValueError:
                            pass
                if diff_val is not None:
                    break

    if diff_val is None:
        diff_card = soup.find("div", class_=lambda c: c and "metadata-difficulty-card" in c)
        if diff_card:
            card_text = diff_card.get_text(" ", strip=True)
            m = re.search(r"([\d.]+)", card_text)
            if m:
                try:
                    diff_val = float(m.group(1))
                except ValueError:
                    diff_val = None
            if diff_val is None:
                txt = card_text.lower()
                if "fast" in txt:
                    return "fast"
                if "easy" in txt:
                    return "easy"
                if "medium" in txt or "moderate" in txt or "normal" in txt:
                    return "medium"
                if "hard" in txt or "difficult" in txt:
                    return "hard"
        if diff_val is None:
            return "medium"  # default fallback

    if diff_val < 1.5:
        return "fast"
    elif diff_val < 2.5:
        return "easy"
    elif diff_val < 4.0:
        return "medium"
    else:
        return "hard"

def clean_markdown(text: str) -> str:
    # Collapse trailing spaces and fix indentation a bit.
    text = dedent(text)
    # Strip super-loose blank lines at start/end
    return text.strip() + "\n"

def extract_title(soup: BeautifulSoup):
    # Usually inside h1 class="title"
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(" ", strip=True)
    # fallback
    title_tag = soup.find("title")
    if title_tag:
        return title_tag.get_text(" ", strip=True)
    return "Untitled"

def extract_problem_sections(soup: BeautifulSoup):
    """
    Extract problem sections from Kattis HTML.
    Kattis uses tables with class="sample" for sample input/output.
    """
    # Try to find the problem statement container more specifically
    container = soup.find("div", class_="problembody")
    if container is None:
        container = soup.find("div", class_=re.compile(r"problem[-_]?(body|description|statement)"))
    if container is None:
        # Try finding by ID
        container = soup.find("div", id=re.compile(r"problem[-_]?(text|body|content)"))
    if container is None:
        # Last resort: find main content div
        main = soup.find("main")
        if main:
            container = main
        else:
            container = soup

    # Remove unwanted sections (navigation, login prompts, etc.)
    for unwanted in container.find_all(["nav", "header", "footer"]):
        unwanted.decompose()
    for unwanted in container.find_all(class_=re.compile(r"(nav|menu|header|footer|login|sidebar)")):
        unwanted.decompose()

    # Extract sample data from tables first (Kattis specific)
    sample_inputs = []
    sample_outputs = []
    sample_tables = soup.find_all("table", class_="sample")
    sample_sections = []
    
    for table in sample_tables:
        pre_tags = table.find_all("pre")
        input_text = ""
        output_text = ""
        if len(pre_tags) >= 2:
            input_text = pre_tags[0].get_text().strip()
            output_text = pre_tags[1].get_text().strip()
        elif len(pre_tags) == 1:
            input_text = pre_tags[0].get_text().strip()
        sample_inputs.append(input_text)
        if output_text:
            sample_outputs.append(output_text)
        elif len(pre_tags) >= 2:
            sample_outputs.append(output_text)
        sample_sections.append((input_text, output_text))

    # We'll iterate through its children and build a lightweight markdown.
    lines = []
    current_section = None
    
    sample_sections_queue = list(sample_sections)

    # Process direct children to avoid navigation items
    def process_element(el, depth=0):
        nonlocal current_section
        
        if el.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            header_txt = normalize_text(el.get_text(" ", strip=True))
            # Skip headers that look like navigation
            if any(skip in header_txt.lower() for skip in ["kattis", "problems", "contests", "challenge", "ranklist", "languages", "info", "help", "log in", "submit"]):
                return
            lines.append(f"## {header_txt}")
            current_section = header_txt.lower()
        elif el.name == "div" and "illustration" in (el.get("class") or []):
            img = el.find("img")
            if img and img.get("src"):
                img_src = urljoin(BASE_URL, img["src"])
                alt_text = img.get("alt") or ""
                lines.append(f"![{alt_text}]({img_src})")
            desc = el.find("div", class_="description")
            if desc:
                desc_text = normalize_text(desc.get_text(" ", strip=True))
                if desc_text:
                    lines.append(desc_text)
            lines.append("")
        elif el.name == "p":
            ptxt = normalize_text(el.get_text(" ", strip=True))
            # Skip paragraphs with login/submission text
            if any(skip in ptxt.lower() for skip in ["please log in", "you haven't made any submission", "submit a solution"]):
                return
            if ptxt:
                lines.append(ptxt)
                lines.append("")  # blank line after paragraph
        elif el.name == "table":
            table_classes = " ".join(el.get("class", [])).lower()
            if "sample" in table_classes:
                # Render sample section in statement
                if sample_sections_queue:
                    sample_idx = len(sample_sections) - len(sample_sections_queue) + 1
                    inp, outp = sample_sections_queue.pop(0)
                    lines.append(f"### Sample {sample_idx}")
                    if inp:
                        lines.append("**Input**")
                        lines.append("```text")
                        lines.append(inp)
                        lines.append("```")
                    if outp:
                        lines.append("**Output**")
                        lines.append("```text")
                        lines.append(outp)
                        lines.append("```")
                    lines.append("")
                return
        # also handle <ul> and <ol> lists
        elif el.name == "ul" or el.name == "ol":
            for li in el.find_all("li", recursive=False):
                li_txt = normalize_text(li.get_text(" ", strip=True))
                if li_txt and not any(skip in li_txt.lower() for skip in ["log in", "submit", "kattis"]):
                    lines.append(f"- {li_txt}")
            lines.append("")
    
    # Process top-level elements including stray text nodes
    for child in container.children:
        if isinstance(child, NavigableString):
            raw = normalize_text(child.strip())
            if raw:
                lines.append(raw)
                lines.append("")
        elif getattr(child, "name", None):
            process_element(child)

    full_statement_md = clean_markdown("\n".join(lines))

    # short description: take first paragraph-ish (first non-empty line that is not header "##")
    short_desc = ""
    for ln in lines:
        stripped = ln.strip()
        if stripped and not stripped.startswith("##") and not stripped.startswith("```") and not stripped.startswith("![") and not stripped.lower().startswith("photo by"):
            short_desc = ln.strip()
            break
    if not short_desc:
        short_desc = "No short description available."

    # Use only the FIRST sample for sample_input/output (not all of them)
    if len(sample_inputs) > 0:
        sample_input_join = sample_inputs[0]
    else:
        sample_input_join = ""

    if len(sample_outputs) > 0:
        sample_output_join = sample_outputs[0]
    else:
        sample_output_join = ""

    # Create test cases from all samples
    test_cases = []
    for i in range(max(len(sample_inputs), len(sample_outputs))):
        inp = sample_inputs[i] if i < len(sample_inputs) else ""
        outp = sample_outputs[i] if i < len(sample_outputs) else ""
        if not inp and not outp:
            continue
        test_cases.append({
            "input": inp if inp else "N/A",
            "output": outp if outp else "N/A",
            "visibility": "public" if i == 0 else "hidden"  # First is public, rest are hidden
        })

    return {
        "statement_markdown": full_statement_md,
        "short_description": short_desc,
        "sample_input": sample_input_join,
        "sample_output": sample_output_join,
        "test_cases": test_cases,
    }

def build_problem_json(slug: str):
    soup = fetch_problem_html(slug)

    title = extract_title(soup)
    difficulty_label = extract_difficulty(soup)
    time_limit_ms, memory_limit_kb = extract_limits(soup)

    sections = extract_problem_sections(soup)

    # fallback safety: description cannot be empty per your schema
    description = sections["short_description"] or sections["statement_markdown"]

    # also ensure sample I/O exist (your schema says bắt buộc)
    sample_input = sections["sample_input"]
    sample_output = sections["sample_output"]

    if not sample_input:
        sample_input = "N/A"
    if not sample_output:
        sample_output = "N/A"

    # Use test cases from sections if available, otherwise create from sample
    tests = sections.get("test_cases", [])
    if not tests:
        tests = [
            {
                "input": sample_input,
                "output": sample_output,
                "visibility": "public"
            }
        ]

    problem_obj = {
        "title": title,
        "description": description,
        "statement": sections["statement_markdown"],
        "sample_input": sample_input,
        "sample_output": sample_output,
        "difficulty": difficulty_label,
        "tests": tests,
        "time_limit_ms": time_limit_ms if time_limit_ms is not None else 2000,
        "memory_limit_kb": memory_limit_kb if memory_limit_kb is not None else 262144,  # ~256MB
        "tags": []
    }

    return problem_obj

def save_problem_to_txt(problem_obj, out_dir="problems"):
    os.makedirs(out_dir, exist_ok=True)

    # create safe filename
    safe_name = re.sub(r"[^a-zA-Z0-9_-]+", "_", problem_obj["title"]).strip("_")
    if not safe_name:
        safe_name = "problem"

    path = os.path.join(out_dir, f"{safe_name}.txt")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(problem_obj, f, ensure_ascii=False, indent=2)

    return path

if __name__ == "__main__":
    # ví dụ: "hello" là bài kinh điển in ra "Hello World!"
    slug = "hello"

    data = build_problem_json(slug)
    out_path = save_problem_to_txt(data)

    print(f"Saved problem to {out_path}")
    print("Preview:")
    print(json.dumps(data, ensure_ascii=False, indent=2))
