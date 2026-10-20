from datetime import datetime
from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------- config ----
st.set_page_config(
    page_title="FileFlow | File Manager",
    page_icon="🗂️",
    initial_sidebar_state="expanded",
)

WORKSPACE = Path("workspace")
WORKSPACE.mkdir(exist_ok=True)

# ----------------------------------------------------------------- style ----
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .block-container { padding-top: 2rem; max-width: 1100px; }

    .hero {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%);
        padding: 2.2rem 2.4rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 1.6rem;
        box-shadow: 0 12px 32px rgba(124, 58, 237, 0.30);
    }
    .hero h1 { margin: 0; font-size: 2.3rem; font-weight: 800; letter-spacing: -0.5px; }
    .hero p  { margin: 0.4rem 0 0 0; font-size: 1.05rem; opacity: 0.92; }

    .section-title { font-size: 1.35rem; font-weight: 700; margin-bottom: 0.2rem; }
    .section-sub   { color: #6b7280; margin-bottom: 1.1rem; }

    .file-card {
        display: flex; justify-content: space-between; align-items: center;
        background: rgba(124, 58, 237, 0.06);
        border: 1px solid rgba(124, 58, 237, 0.18);
        border-radius: 14px;
        padding: 0.8rem 1.1rem;
        margin-bottom: 0.6rem;
        transition: transform .15s ease, box-shadow .15s ease;
    }
    .file-card:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(124,58,237,.18); }
    .file-name { font-weight: 600; }
    .file-meta { color: #6b7280; font-size: 0.85rem; }

    div[data-testid="stMetric"] {
        background: rgba(124, 58, 237, 0.07);
        border: 1px solid rgba(124, 58, 237, 0.18);
        padding: 1rem 1.2rem;
        border-radius: 16px;
    }

    .stButton > button, .stDownloadButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 0.55rem 1.4rem;
        border: none;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        transition: all .15s ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.35);
        color: white;
    }

    .footer { text-align: center; color: #9ca3af; font-size: 0.85rem; margin-top: 3rem; }
    #MainMenu, footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------------------- helpers ----
def safe_path(name: str):
    """Keep every operation inside the workspace folder."""
    name = (name or "").strip()
    if not name:
        return None
    return WORKSPACE / Path(name).name


def list_files():
    return sorted((p for p in WORKSPACE.iterdir() if p.is_file()), key=lambda p: p.name.lower())


def human_size(num_bytes: int) -> str:
    size = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def modified(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%d %b %Y, %H:%M")


def header(title: str, sub: str):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">{sub}</div>', unsafe_allow_html=True)


def no_files_notice():
    st.info("No files yet. Head over to **Create** to make your first one.", icon="📭")


# ---------------------------------------------------------------- sidebar ----
with st.sidebar:
    st.markdown("## 🗂️ FileFlow")
    st.caption("A tiny file manager built with Python & Streamlit")
    st.divider()
    page = st.radio(
        "Navigate",
        ["🏠 Dashboard", "➕ Create", "📖 Read", "✏️ Update", "🗑️ Delete"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption(f"📁 Workspace: `{WORKSPACE.name}/`")
    st.caption("Built with ❤️ using pathlib + Streamlit")

# ------------------------------------------------------------------- hero ----
st.markdown(
    """
    <div class="hero">
        <h1>🗂️ FileFlow</h1>
        <p>Create, read, update and delete files, all from a clean, simple interface.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------- dashboard ----
if page == "🏠 Dashboard":
    files = list_files()
    total = sum(f.stat().st_size for f in files)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total files", len(files))
    c2.metric("Total size", human_size(total))
    c3.metric("Last activity", modified(max(files, key=lambda p: p.stat().st_mtime)) if files else "—")

    st.write("")
    header("Your files", "Everything currently stored in the workspace.")

    if not files:
        no_files_notice()
    else:
        for f in files:
            st.markdown(
                f"""
                <div class="file-card">
                    <div>
                        <div class="file-name">📄 {f.name}</div>
                        <div class="file-meta">Modified {modified(f)}</div>
                    </div>
                    <div class="file-meta">{human_size(f.stat().st_size)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ----------------------------------------------------------------- create ----
elif page == "➕ Create":
    header("Create a file", "Give it a name, write something, and save.")

    with st.form("create_form", clear_on_submit=True):
        name = st.text_input("File name", placeholder="notes.txt")
        data = st.text_area("Content", height=220, placeholder="Whatever you want to write in your file...")
        submitted = st.form_submit_button("Create file")

    if submitted:
        path = safe_path(name)
        if path is None:
            st.warning("Please enter a file name.", icon="⚠️")
        elif path.exists():
            st.error(f"`{path.name}` already exists.", icon="🚫")
        else:
            try:
                path.write_text(data, encoding="utf-8")
                st.success(f"`{path.name}` created successfully!", icon="✅")
                st.balloons()
            except Exception as err:
                st.error(f"An error occurred: {err}")

# ------------------------------------------------------------------- read ----
elif page == "📖 Read":
    header("Read a file", "Pick a file to view its contents.")
    files = list_files()

    if not files:
        no_files_notice()
    else:
        choice = st.selectbox("Select a file", [f.name for f in files])
        path = WORKSPACE / choice
        try:
            content = path.read_text(encoding="utf-8")
            c1, c2 = st.columns(2)
            c1.metric("Size", human_size(path.stat().st_size))
            c2.metric("Modified", modified(path))
            st.text_area("Content", content, height=300, disabled=True)
            st.download_button("⬇️ Download file", content, file_name=path.name)
        except UnicodeDecodeError:
            st.error("This file isn't plain text, so it can't be displayed.", icon="🚫")
        except Exception as err:
            st.error(f"An error occurred: {err}")

# ----------------------------------------------------------------- update ----
elif page == "✏️ Update":
    header("Update a file", "Rename it, append to it, or overwrite it completely.")
    files = list_files()

    if not files:
        no_files_notice()
    else:
        choice = st.selectbox("Select a file", [f.name for f in files])
        path = WORKSPACE / choice
        rename_tab, append_tab, overwrite_tab = st.tabs(["🔤 Rename", "➕ Append", "📝 Overwrite"])

        with rename_tab:
            new_name = st.text_input("New file name", key="rename_input")
            if st.button("Rename file"):
                new_path = safe_path(new_name)
                if new_path is None:
                    st.warning("Please enter a new name.", icon="⚠️")
                elif new_path.exists():
                    st.error(f"`{new_path.name}` already exists.", icon="🚫")
                else:
                    path.rename(new_path)
                    st.toast(f"Renamed to {new_path.name}", icon="✅")
                    st.rerun()

        with append_tab:
            extra = st.text_area("Text to append", height=150, key="append_input")
            if st.button("Append content"):
                try:
                    with open(path, "a", encoding="utf-8") as fs:
                        fs.write("\n" + extra)
                    st.success("Content appended successfully.", icon="✅")
                except Exception as err:
                    st.error(f"An error occurred: {err}")

        with overwrite_tab:
            try:
                current = path.read_text(encoding="utf-8")
            except Exception:
                current = ""
            new_content = st.text_area("New content", value=current, height=220, key=f"over_{choice}")
            if st.button("Overwrite file"):
                try:
                    path.write_text(new_content, encoding="utf-8")
                    st.success("File overwritten successfully.", icon="✅")
                except Exception as err:
                    st.error(f"An error occurred: {err}")

# ----------------------------------------------------------------- delete ----
elif page == "🗑️ Delete":
    header("Delete a file", "This action can't be undone.")
    files = list_files()

    if not files:
        no_files_notice()
    else:
        choice = st.selectbox("Select a file", [f.name for f in files])
        path = WORKSPACE / choice
        st.warning(f"You're about to permanently delete `{path.name}`.", icon="⚠️")
        confirm = st.checkbox("Yes, I'm sure")
        if st.button("Delete file", disabled=not confirm):
            try:
                path.unlink()
                st.toast(f"{choice} deleted successfully", icon="🗑️")
                st.rerun()
            except Exception as err:
                st.error(f"An error occurred: {err}")

st.markdown('<div class="footer">FileFlow · Python · pathlib · Streamlit</div>', unsafe_allow_html=True)