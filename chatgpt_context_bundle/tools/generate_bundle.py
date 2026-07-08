from __future__ import annotations

import datetime as dt
import os
import re
import shutil
import subprocess
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
RUNNING_FROM_SOURCE_BUNDLE = SCRIPT_PATH.parent.parent.name == "chatgpt_context_bundle"
DEFAULT_SOURCE_ROOT = SCRIPT_PATH.parents[2] if RUNNING_FROM_SOURCE_BUNDLE else Path.cwd()
DEFAULT_BUNDLE_OUTPUT = (
    DEFAULT_SOURCE_ROOT / "chatgpt_context_bundle"
    if RUNNING_FROM_SOURCE_BUNDLE
    else SCRIPT_PATH.parents[1]
)

ROOT = Path(os.environ.get("STELLARIS_MODS_SOURCE_REPO", DEFAULT_SOURCE_ROOT)).resolve()
BUNDLE = Path(os.environ.get("STELLARIS_MODS_BUNDLE_OUTPUT", DEFAULT_BUNDLE_OUTPUT)).resolve()

MAX_INLINE_BYTES = 220_000
MAX_DOC_INLINE_BYTES = 160_000

EXCLUDE_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    ".vscode",
    "__pycache__",
    "build",
    "chatgpt_context_bundle",
    "dist",
    "exports",
    "node_modules",
    "temp",
    "tmp",
    "vanilla-dumps",
    "venv",
}

EXCLUDE_PATH_PREFIXES = {
    "research/mod-source-snapshots/",
    "research/stellar-ai/observer-runs/",
}

BINARY_EXTS = {
    ".7z",
    ".db",
    ".gif",
    ".gz",
    ".ico",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".pkl",
    ".png",
    ".pyc",
    ".rar",
    ".sav",
    ".sqlite",
    ".sqlite3",
    ".tar",
    ".webp",
    ".zip",
}

TEXT_EXTS = {
    ".csv",
    ".json",
    ".jsonl",
    ".md",
    ".mod",
    ".ndjson",
    ".ps1",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

DATA_EXTS = {".csv", ".jsonl", ".ndjson", ".xlsx", ".xls", ".parquet"}

SENSITIVE_NAME_PATTERNS = [
    re.compile(r"(^|[\\/])\.env($|[\\.])", re.I),
    re.compile(r"\.local\.", re.I),
    re.compile(r"(credential|private[-_]?key|api[-_]?key)", re.I),
    re.compile(r"(^|[\\/])(secrets?|tokens?)(\.|[\\/]|$)", re.I),
]

SECRET_LINE = re.compile(
    r"(?i)(password|passwd|secret|token|api[_-]?key|access[_-]?key|private[_-]?key|dsn|database_url)\s*[:=]"
)
URL_CREDENTIALS = re.compile(r"(?i)([a-z][a-z0-9+.-]*://[^:\s`\"']+):([^@\s`\"']+)@")

OMITTED: list[str] = []
SNAPSHOT: dict[str, str] = {}


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()


def git_output(cmd: list[str]) -> str:
    result = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        return (
            f"_Command failed with exit code {result.returncode}: `{' '.join(cmd)}`_\n\n"
            "```text\n"
            f"{result.stderr.strip()}\n"
            "```\n"
        )
    return result.stdout.strip() or "_No output._"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def is_excluded_path(path: Path) -> bool:
    try:
        value = rel(path)
        parts = set(path.relative_to(ROOT).parts)
    except ValueError:
        return True
    if parts & EXCLUDE_DIRS:
        return True
    if any(value == prefix.rstrip("/") or value.startswith(prefix) for prefix in EXCLUDE_PATH_PREFIXES):
        return True
    if path.suffix.lower() in BINARY_EXTS:
        return True
    if path.name.lower().endswith((".log", ".pid")):
        return True
    return False


def is_sensitive_path(path: Path) -> bool:
    value = rel(path)
    return any(pattern.search(value) for pattern in SENSITIVE_NAME_PATTERNS)


def candidate_paths() -> list[Path]:
    output = run(["git", "ls-files", "--cached", "--others", "--exclude-standard"])
    paths: list[Path] = []
    for line in output.splitlines():
        path = ROOT / line
        if path.exists() and path.is_file():
            paths.append(path)
    return paths


def text_files() -> list[Path]:
    files: list[Path] = []
    for path in candidate_paths():
        suffix = path.suffix.lower()
        if is_excluded_path(path):
            continue
        if suffix not in TEXT_EXTS and path.name != ".gitignore":
            if suffix in DATA_EXTS:
                continue
            OMITTED.append(f"{rel(path)} - unsupported non-text extension")
            continue
        if is_sensitive_path(path):
            OMITTED.append(f"{rel(path)} - path looked local/sensitive")
            continue
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            OMITTED.append(f"{rel(path)} - non-UTF-8 or binary-like file")
            continue
        files.append(path)
    return sorted(files, key=rel)


def read_redacted(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    redacted_lines: list[str] = []
    for line in text.splitlines():
        if SECRET_LINE.search(line):
            key = re.split(r"[:=]", line, maxsplit=1)[0].rstrip()
            redacted_lines.append(f"{key}=<REDACTED>")
        else:
            redacted_lines.append(URL_CREDENTIALS.sub(r"\1:<REDACTED>@", line))
    return "\n".join(redacted_lines) + ("\n" if text.endswith("\n") else "")


def language_for(path: Path) -> str:
    return {
        ".csv": "csv",
        ".json": "json",
        ".jsonl": "jsonl",
        ".md": "markdown",
        ".mod": "text",
        ".ndjson": "jsonl",
        ".ps1": "powershell",
        ".py": "python",
        ".toml": "toml",
        ".txt": "text",
        ".yaml": "yaml",
        ".yml": "yaml",
    }.get(path.suffix.lower(), path.suffix.lower().lstrip(".") or "text")


def fence(path: Path, max_bytes: int = MAX_INLINE_BYTES) -> str:
    value = rel(path)
    size = path.stat().st_size
    if size > max_bytes:
        OMITTED.append(f"{value} - {size} bytes, omitted inline over {max_bytes} byte cap")
        return (
            f"## {value}\n\n"
            f"_Omitted inline because this file is {size} bytes. See the source manifest and use the local repo or "
            "JDataMunch/JDocMunch/JCodeMunch for exact retrieval._\n\n"
        )
    return f"## {value}\n\n```{language_for(path)}\n{read_redacted(path)}```\n\n"


def section(title: str, body: str) -> str:
    return f"# {title}\n\n{body.rstrip()}\n\n"


def write(name: str, content: str) -> None:
    if name.endswith(".md") and SNAPSHOT:
        content = (
            f"> Snapshot commit: `{SNAPSHOT['commit']}` | "
            f"Branch: `{SNAPSHOT['branch']}` | "
            f"Working tree: `{SNAPSHOT['dirty']}` | "
            f"Generated: `{SNAPSHOT['timestamp']}`\n\n"
            + content
        )
    if name.endswith(".md"):
        lines = [line.rstrip() for line in content.splitlines()]
        while lines and not lines[-1]:
            lines.pop()
        content = "\n".join(lines) + "\n"
    output = BUNDLE / name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")


def generated_bundle_paths(names: list[str]) -> list[Path]:
    return [BUNDLE / name for name in names if (BUNDLE / name).is_file()]


def include(paths: list[str], max_bytes: int = MAX_INLINE_BYTES) -> str:
    out: list[str] = []
    seen: set[str] = set()
    for item in paths:
        if item in seen:
            continue
        seen.add(item)
        path = ROOT / item
        if not path.exists() or not path.is_file():
            continue
        if is_sensitive_path(path) or is_excluded_path(path):
            continue
        out.append(fence(path, max_bytes=max_bytes))
    return "".join(out) or "_No matching files found._\n\n"


def files_under(
    files: list[Path],
    prefix: str,
    suffixes: tuple[str, ...] | None = (".md",),
    exclude_contains: tuple[str, ...] = (),
) -> list[str]:
    normalized = prefix.rstrip("/") + "/"
    return [
        rel(path)
        for path in files
        if rel(path).startswith(normalized)
        and not any(part in rel(path) for part in exclude_contains)
        and (suffixes is None or path.suffix.lower() in suffixes)
    ]


def exact_existing(paths: list[str]) -> list[str]:
    return [item for item in paths if (ROOT / item).is_file()]


def repo_tree(files: list[Path]) -> str:
    notes = {
        ".": "Project entrypoints, global repo guidance, and root metadata.",
        "assets": "Images, icons, generated art, and source asset files.",
        "mods": "Source mods; each mod has its own folder and descriptor.",
        "notes": "Rough planning notes and local design notes.",
        "plans": "Implementation plans and scoped task notes.",
        "research": "Compatibility research, source bundles, evidence packets, and generated validation reports.",
        "tools": "Deterministic local helper scripts, validators, packagers, and tests.",
    }
    dirs: dict[str, list[str]] = {}
    for path in files:
        parent = rel(path.parent)
        dirs.setdefault(parent, []).append(path.name)

    lines = [
        "This cleaned tree excludes Git state, generated bundle output, caches, dependency folders, binary media, raw observer-run artifacts, and large mod-source snapshots.",
        "",
    ]
    for directory in sorted(dirs):
        display = "." if directory == "." else directory
        note = notes.get(display)
        lines.append(f"## {display}" + (f" - {note}" if note else ""))
        for name in sorted(dirs[directory]):
            lines.append(f"- {name}")
        lines.append("")
    return "\n".join(lines)


def todo_report(files: list[Path]) -> str:
    rows: list[str] = []
    pattern = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b", re.I)
    for path in files:
        if path.stat().st_size > MAX_DOC_INLINE_BYTES:
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if pattern.search(line):
                rows.append(f"- `{rel(path)}:{i}`: {line.strip()[:240]}")
    return "\n".join(rows) if rows else "_No TODO/FIXME/HACK/XXX markers found in scanned UTF-8 files._"


def dataset_catalog(files: list[Path]) -> str:
    data_files = [path for path in files if path.suffix.lower() in {".csv", ".jsonl", ".ndjson"}]
    if not data_files:
        return "_No CSV/JSONL/NDJSON files found in the included candidate set._"
    lines = [
        "Tabular artifacts are listed here instead of fully inlined when large. Use JDataMunch for row/column inspection in Codex, and use adjacent Markdown reports for narrative context.",
        "",
        "| Path | Bytes | Companion report |",
        "| --- | ---: | --- |",
    ]
    for path in sorted(data_files, key=rel):
        companion = path.with_suffix(".md")
        companion_text = rel(companion) if companion.exists() else ""
        lines.append(f"| `{rel(path)}` | {path.stat().st_size} | `{companion_text}` |")
    return "\n".join(lines)


def source_file_manifest(files: list[Path], branch: str, commit: str, dirty: str) -> str:
    lang_counts: dict[str, int] = {}
    dir_counts: dict[str, int] = {}
    for path in files:
        rp = rel(path)
        lang = language_for(path)
        lang_counts[lang] = lang_counts.get(lang, 0) + 1
        top = rp.split("/", 1)[0]
        dir_counts[top] = dir_counts.get(top, 0) + 1

    largest = sorted(((rel(path), path.stat().st_size) for path in files), key=lambda row: row[1], reverse=True)[:30]
    manifest_rows = sorted((rel(path), path.stat().st_size, language_for(path)) for path in files)

    lang_table = "\n".join(f"- `{key}`: {value}" for key, value in sorted(lang_counts.items()))
    dir_table = "\n".join(f"- `{key}`: {value}" for key, value in sorted(dir_counts.items()))
    largest_table = "\n".join(f"- `{path}`: {size} bytes" for path, size in largest)
    manifest_table = "\n".join(f"- `{path}` ({language}, {size} bytes)" for path, size, language in manifest_rows)

    return f"""## Local Source Index Readout

Repository state:
- Branch: `{branch}`
- Commit: `{commit}`
- Working tree: `{dirty}`
- Packed text/source candidates: {len(files)}
- Excluded large evidence roots: `research/mod-source-snapshots/`, `research/stellar-ai/observer-runs/`

Language/file counts:
{lang_table}

Top-level packed file counts:
{dir_table}

Largest included source candidates:
{largest_table}

## Tabular Data Catalog

{dataset_catalog(files)}

## Candidate Source File Manifest

{manifest_table}

## TODO / FIXME / HACK / XXX Scan

{todo_report(files)}
"""


def upload_quality_review(bundle_files: list[str], total_bytes: int, omitted_text: str) -> str:
    return f"""## Upload Quality Review

Checklist result:
- Under 40 files: yes, {len(bundle_files)} generated files.
- Total bundle size before final manifest write: {total_bytes} bytes.
- Generated/vendor/cache files: excluded by directory filters and Git ignore discovery.
- Raw mod-source snapshots and observer-run artifacts: excluded from inline bundle output; use local repo/Munch indexes for exact retrieval.
- Original source paths: preserved as `## path/to/file` headings before each included source block.
- Sensitive-looking paths: excluded; secret-like key/value lines are redacted inside copied text.
- Major surfaces represented: project rules, mod source, Stellar AI Director implementation/research, modding guides, research bundles, tabular evidence catalog, scripts, validators, and tests.
- Online ChatGPT readiness: yes. Upload the generated Markdown files in the recommended order from `00_INDEX.md`.

## Omitted Files

{omitted_text}
"""


def main() -> None:
    BUNDLE.mkdir(parents=True, exist_ok=True)
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    commit = run(["git", "rev-parse", "HEAD"])
    status = run(["git", "status", "--porcelain=v1"])
    dirty = "dirty" if status else "clean"
    timestamp = os.environ.get("STELLARIS_MODS_BUNDLE_TIMESTAMP") or (
        dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    )
    SNAPSHOT.update({"branch": branch, "commit": commit, "dirty": dirty, "timestamp": timestamp})

    files = text_files()
    generated_files = [
        "00_INDEX.md",
        "01_REPO_TREE.md",
        "02_PROJECT_CONTROL_AND_GUIDANCE.md",
        "03_MOD_SOURCE_AND_DESCRIPTORS.md",
        "04_STELLAR_AI_DIRECTOR_CONTEXT.md",
        "05_RESEARCH_AND_EVIDENCE_GUIDES.md",
        "06_DATASETS_AND_VALIDATION_REPORTS.md",
        "07_TOOLS_AND_VALIDATORS.md",
        "08_SOURCE_FILE_MANIFEST_AND_UPLOAD_REVIEW.md",
        "09_CHATGPT_STELLARIS_MODDING_BRIEF.md",
        "tools/generate_bundle.py",
    ]

    generator_output = BUNDLE / "tools" / "generate_bundle.py"
    generator_output.parent.mkdir(parents=True, exist_ok=True)
    if SCRIPT_PATH.resolve() != generator_output.resolve():
        shutil.copy2(SCRIPT_PATH, generator_output)

    control_paths = exact_existing(
        [
            ".gitignore",
            "AGENTS.md",
            "README.md",
            "mods/README.md",
            "research/README.md",
        ]
    ) + files_under(files, "notes", suffixes=None) + files_under(files, "plans", suffixes=None)

    mod_paths = files_under(files, "mods", suffixes=None)
    stellar_ai_paths = files_under(files, "mods/StellarAIDirector", suffixes=None) + files_under(
        files,
        "research/stellar-ai",
        suffixes=(".md", ".txt", ".json"),
        exclude_contains=("/observer-runs/",),
    )
    research_paths = (
        exact_existing(["research/stellaris-modding-guide-2026-07-04.md"])
        + files_under(files, "research/stellaris-modding-research-bundle-2026-07-04", suffixes=(".md", ".json", ".txt"))
        + files_under(files, "research/webchatgpt", suffixes=(".md", ".json", ".txt"))
        + files_under(files, "research/last30days", suffixes=(".md", ".json", ".txt"))
        + files_under(files, "research/stellaris-codex-modding-guide-packet-2026-07-08", suffixes=(".md", ".json", ".txt"))
        + files_under(files, "research/stellaris-codex-skills-roadmap-2026-07-08", suffixes=(".md", ".json", ".txt"))
    )
    report_paths = [
        rel(path)
        for path in files
        if rel(path).startswith("research/")
        and path.suffix.lower() in {".md", ".json"}
        and (
            "object-atlas" in rel(path)
            or "compatibility" in rel(path)
            or "audit" in rel(path)
            or "validation" in rel(path)
            or "route" in rel(path)
            or "war-mechanics" in rel(path)
        )
    ]
    tool_paths = files_under(files, "tools", suffixes=(".py", ".md", ".ps1", ".json", ".yaml", ".yml"))

    write(
        "00_INDEX.md",
        section(
            "Stellaris Mods ChatGPT Source Bundle",
            f"""Generated: {timestamp}
Current git branch: `{branch}`
Current git commit: `{commit}`
Working tree: `{dirty}`

Warning: this bundle is a point-in-time snapshot for online ChatGPT sources. The repository remains the live source of truth.

| File | Contents |
| --- | --- |
| `01_REPO_TREE.md` | Cleaned repository tree with role notes for important directories. |
| `02_PROJECT_CONTROL_AND_GUIDANCE.md` | Project rules, repo guidance, notes, and plans that should frame any answer. |
| `03_MOD_SOURCE_AND_DESCRIPTORS.md` | Source mod descriptors, READMEs, localization, and script files under `mods/`. |
| `04_STELLAR_AI_DIRECTOR_CONTEXT.md` | Stellar AI Director source, notes, generated design research, compatibility notes, and validation reports. |
| `05_RESEARCH_AND_EVIDENCE_GUIDES.md` | Stellaris modding guide, research bundle, WebChatGPT packets, and skill-roadmap context. |
| `06_DATASETS_AND_VALIDATION_REPORTS.md` | Tabular-evidence catalog plus narrative validation, audit, route, conflict, and war-mechanics reports. |
| `07_TOOLS_AND_VALIDATORS.md` | Deterministic helper scripts, validators, observer helpers, and tests. |
| `08_SOURCE_FILE_MANIFEST_AND_UPLOAD_REVIEW.md` | Complete candidate source manifest, data catalog, TODO scan, upload checks, and omissions. |
| `09_CHATGPT_STELLARIS_MODDING_BRIEF.md` | Concise instruction brief for online ChatGPT after these files are uploaded as sources. |
| `tools/generate_bundle.py` | Generator script used to produce this snapshot. Rerun from repo root with `python chatgpt_context_bundle/tools/generate_bundle.py`. |

Recommended upload order for ChatGPT Projects:

1. `00_INDEX.md`
2. `09_CHATGPT_STELLARIS_MODDING_BRIEF.md`
3. `01_REPO_TREE.md`
4. `02_PROJECT_CONTROL_AND_GUIDANCE.md`
5. `03_MOD_SOURCE_AND_DESCRIPTORS.md`
6. `04_STELLAR_AI_DIRECTOR_CONTEXT.md`
7. `05_RESEARCH_AND_EVIDENCE_GUIDES.md`
8. `06_DATASETS_AND_VALIDATION_REPORTS.md`
9. `07_TOOLS_AND_VALIDATORS.md`
10. `08_SOURCE_FILE_MANIFEST_AND_UPLOAD_REVIEW.md`

Generated bundle file count: {len(generated_files)}
""",
        ),
    )

    write("01_REPO_TREE.md", section("Clean Repository Tree", repo_tree(files)))
    write(
        "02_PROJECT_CONTROL_AND_GUIDANCE.md",
        section(
            "Project Control And Guidance",
            "Read these files before interpreting mod source, research packets, generated evidence, or validation claims.\n\n"
            + include(control_paths, max_bytes=MAX_DOC_INLINE_BYTES),
        ),
    )
    write(
        "03_MOD_SOURCE_AND_DESCRIPTORS.md",
        section(
            "Mod Source And Descriptors",
            "Source mod files are copied path-preserving. Treat launcher descriptors as metadata, not proof that script content loads.\n\n"
            + include(mod_paths),
        ),
    )
    write(
        "04_STELLAR_AI_DIRECTOR_CONTEXT.md",
        section(
            "Stellar AI Director Context",
            "Stellar AI Director is the high-touch AI/economy/compatibility mod in this repo. Use these source and research files for current implementation context, then verify exact game-script surfaces against local vanilla/mod evidence before changing behavior.\n\n"
            + include(stellar_ai_paths, max_bytes=MAX_DOC_INLINE_BYTES),
        ),
    )
    write(
        "05_RESEARCH_AND_EVIDENCE_GUIDES.md",
        section(
            "Research And Evidence Guides",
            "These research guides, source bundles, WebChatGPT packets, and skill-roadmap artifacts capture the durable project context around Stellaris 4.4.x modding, compatibility, validation, and future workflow design.\n\n"
            + include(research_paths, max_bytes=MAX_DOC_INLINE_BYTES),
        ),
    )
    write(
        "06_DATASETS_AND_VALIDATION_REPORTS.md",
        section(
            "Datasets And Validation Reports",
            dataset_catalog(files)
            + "\n\n## Narrative Reports\n\n"
            + include(report_paths, max_bytes=MAX_DOC_INLINE_BYTES),
        ),
    )
    write(
        "07_TOOLS_AND_VALIDATORS.md",
        section(
            "Tools And Validators",
            "Scripts are deterministic local helpers for inventories, audits, generated patches, launcher descriptor installation, observer-run harnesses, log summaries, and tests. Prefer these over hand-recreating repeatable checks.\n\n"
            + include(tool_paths),
        ),
    )

    omitted_text = "\n".join(f"- {item}" for item in sorted(set(OMITTED))) or "- None"
    total_before_review = sum(p.stat().st_size for p in generated_bundle_paths(generated_files))
    write(
        "08_SOURCE_FILE_MANIFEST_AND_UPLOAD_REVIEW.md",
        section(
            "Source File Manifest And Upload Review",
            source_file_manifest(files, branch, commit, dirty)
            + "\n"
            + upload_quality_review(generated_files, total_before_review, omitted_text),
        ),
    )
    write(
        "09_CHATGPT_STELLARIS_MODDING_BRIEF.md",
        section(
            "ChatGPT Stellaris Modding Brief",
            """Use this source bundle as a point-in-time context pack for the StellarisMods project. The project covers Stellaris modding, mod preparation, compatibility research, generated validation evidence, and source mods under `mods/`, with special emphasis on Stellar AI Director and compatibility with major mods such as Gigastructural Engineering, NSC3, Extra Ship Components NEXT, Starbase Extended, Planetary Diversity, UI dependencies, and AI/performance-related mods.

## Operating Rules For Online ChatGPT

1. Treat the uploaded bundle as context, not live truth. Ask for a refresh when current game version, Workshop state, active playset, runtime logs, or generated evidence matters.
2. Default to Stellaris PC 4.4.5 stable/current local install unless the user names another target.
3. Follow `AGENTS.md` and the modding guide source order: current user instruction, repo guidance, local vanilla files, current mod source, source-bundle evidence, Irony, CWTools, runtime logs, then inference.
4. Do not invent Stellaris triggers, effects, modifiers, scopes, folder names, or loader behavior. Ask Codex to verify unfamiliar surfaces against vanilla files, generated docs, CWTools, Irony, or runtime logs.
5. Treat raw mod-source snapshots, large CSVs, and observer-run artifacts as local evidence surfaces. In Codex, use JDocMunch for prose, JCodeMunch for scripts/source, and JDataMunch for row/column datasets.
6. Keep live launcher state separate from source files. A source mod being updated does not mean the mod that Stellaris will load on next launch is updated.
7. Runtime/game launches and observer simulations require explicit user approval. Default validation is static: file shape, parser/load safety, generated references, descriptors, and evidence reports.
8. For recommendations, respect user preferences: do not recommend Real Space or Star Wars total conversions by default; prioritize maintained compatibility with Gigastructures, NSC3, ship/component expansions, AI mods, station/defense mods, and empire-creation options.
9. For Stellar AI Director, distinguish design intent, generated PDXScript, validation reports, active playset conflicts, and observer outcomes. Do not treat one surface as proof for another without explicit evidence.

## Best Starting Files

1. `02_PROJECT_CONTROL_AND_GUIDANCE.md` for repo rules, final-status reporting, source order, and user preferences.
2. `03_MOD_SOURCE_AND_DESCRIPTORS.md` for current source mod files under `mods/`.
3. `04_STELLAR_AI_DIRECTOR_CONTEXT.md` for the active AI/economy/compatibility mod lane.
4. `05_RESEARCH_AND_EVIDENCE_GUIDES.md` for synthesized guides and external research packets.
5. `06_DATASETS_AND_VALIDATION_REPORTS.md` for dataset catalog and narrative audit/validation reports.
6. `08_SOURCE_FILE_MANIFEST_AND_UPLOAD_REVIEW.md` for coverage, omissions, and the full candidate manifest.
""",
        ),
    )

    with (BUNDLE / "00_INDEX.md").open("a", encoding="utf-8") as handle:
        handle.write("\n## Omitted Files\n\n")
        handle.write(omitted_text)
        handle.write("\n")

    total = sum(p.stat().st_size for p in generated_bundle_paths(generated_files))
    print(f"Generated {len(generated_files)} bundle files.")
    print(f"Total bundle size: {total} bytes.")
    print(f"Output directory: {BUNDLE}")


if __name__ == "__main__":
    main()
