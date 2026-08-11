import json
import sys
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT PATH SETUP
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ============================================================
# IMPORT EXISTING TASK FUNCTIONS
# ============================================================

try:
    from app.triage import triage_ticket
except Exception as e:
    triage_ticket = None
    TRIAGE_IMPORT_ERROR = str(e)

try:
    from task2.account_health import generate_account_brief
except Exception as e:
    generate_account_brief = None
    ACCOUNT_IMPORT_ERROR = str(e)


# ============================================================
# DATA LOADING
# ============================================================

DATA_DIR = ROOT_DIR / "data"

TICKETS_FILE = DATA_DIR / "tickets.json"
ACCOUNTS_FILE = DATA_DIR / "accounts.json"

EVAL_FILE = ROOT_DIR / "task3" / "eval_report.json"


def load_json(path):
    """Load JSON data safely."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


tickets = load_json(TICKETS_FILE)
accounts = load_json(ACCOUNTS_FILE)
evaluation = load_json(EVAL_FILE)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Support Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #777;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    /* Clean metric cards — work in both Streamlit light and dark themes */
    .metric-card {
        width: 100%;
        min-height: 112px;
        padding: 16px 14px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.28);
        background: rgba(128, 128, 128, 0.09);
        color: inherit;
        text-align: center;
        box-sizing: border-box;

        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;

        overflow: hidden;
        box-shadow: 0 2px 7px rgba(0, 0, 0, 0.07);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .metric-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.10);
    }

    .metric-title {
        width: 100%;
        font-size: 0.78rem;
        font-weight: 600;
        opacity: 0.65;
        margin-bottom: 8px;
        line-height: 1.2;
    }

    .metric-value {
        width: 100%;
        font-size: 1.05rem;
        font-weight: 700;
        line-height: 1.3;
        overflow-wrap: anywhere;
        word-break: break-word;
    }

    /* Keep the four cards visually aligned on desktop */
    [data-testid="column"] {
        min-width: 0;
    }

    .success-box {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(80, 180, 90, 0.35);
        background: rgba(80, 180, 90, 0.10);
        color: var(--text-color);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🤖 AI Support Intelligence")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    [
        "🎫 Ticket Triage",
        "🏢 Account Health",
        "📊 Evaluation",
        "ℹ️ About",
    ],
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "AI Engineer - Product Support\n"
    "Support Intelligence Demo"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_value(obj, key, default="N/A"):
    """Safely retrieve a value from dict-like or object-like data."""
    if isinstance(obj, dict):
        return obj.get(key, default)

    try:
        return getattr(obj, key)
    except Exception:
        return default


def _clean_display_value(value):
    """Convert enums / enum-like strings into clean user-facing text."""
    if hasattr(value, "value"):
        value = value.value

    if isinstance(value, bool):
        return "Yes" if value else "No"

    if value is None:
        return "N/A"

    value = str(value)

    # Handles values that were already converted with str(Enum),
    # e.g. "ProductArea.AUTHENTICATION" or "IssueCategory.BUG".
    if "." in value and value.split(".", 1)[0] in {
        "ProductArea",
        "IssueCategory",
        "Urgency",
        "Product",
    }:
        value = value.split(".", 1)[1]
        value = value.replace("_", " ").title()

        # Preserve the standard P1/P2/P3/P4 formatting.
        if value in {"P1", "P2", "P3", "P4"}:
            return value

    return value


def display_metric(label, value):
    """Render a compact, theme-safe metric card."""
    value = _clean_display_value(value)

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def find_ticket(ticket_id):
    for ticket in tickets:
        if ticket.get("ticket_id") == ticket_id:
            return ticket

    return None


# ============================================================
# HOME HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🤖 AI Support Intelligence</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "AI-powered support ticket triage and customer account health analysis"
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# PAGE 1 — TICKET TRIAGE
# ============================================================

if page == "🎫 Ticket Triage":

    st.header("🎫 AI Support Ticket Triage")

    st.write(
        "Analyze a customer support ticket and automatically determine "
        "the product area, issue category, urgency, relevant documentation, "
        "recommended team, and draft response."
    )

    st.markdown("---")

    # --------------------------------------------------------
    # Existing tickets
    # --------------------------------------------------------

    st.subheader("Select an existing ticket")

    ticket_options = ["New Ticket"]

    if tickets:
        ticket_options += [
            f"{t.get('ticket_id', 'Unknown')} — "
            f"{t.get('subject', 'No subject')}"
            for t in tickets[:50]
        ]

    selected_ticket = st.selectbox(
        "Ticket",
        ticket_options,
    )

    # --------------------------------------------------------
    # Ticket input
    # --------------------------------------------------------

    if selected_ticket == "New Ticket":

        subject = st.text_input(
            "Subject",
            placeholder="Example: Unable to connect SecureVault to Key Management",
        )

        body = st.text_area(
            "Ticket Description",
            height=180,
            placeholder="Describe the customer's issue...",
        )

        ticket_id = "STREAMLIT-DEMO"

    else:

        ticket_id = selected_ticket.split(" — ")[0]

        ticket = find_ticket(ticket_id)

        if ticket:

            subject = st.text_input(
                "Subject",
                value=ticket.get("subject", ""),
            )

            body = st.text_area(
                "Ticket Description",
                value=ticket.get("body", ""),
                height=180,
            )

        else:

            subject = ""
            body = ""

    # --------------------------------------------------------
    # Analyze button
    # --------------------------------------------------------

    if st.button(
        "🚀 Analyze Ticket",
        type="primary",
        use_container_width=True,
    ):

        if not subject.strip() or not body.strip():

            st.warning(
                "Please provide both a subject and ticket description."
            )

        elif triage_ticket is None:

            st.error(
                "Could not import the existing Task 1 triage function."
            )

            st.code(TRIAGE_IMPORT_ERROR)

        else:

            with st.spinner("Analyzing ticket..."):

                try:

                    # ------------------------------------------------
                    # IMPORTANT:
                    # This supports the common signatures used in
                    # Task 1 implementations.
                    # ------------------------------------------------

                    try:
                        result = triage_ticket(
                            subject=subject,
                            body=body,
                        )

                    except TypeError:

                        try:
                            result = triage_ticket(
                                {
                                    "ticket_id": ticket_id,
                                    "subject": subject,
                                    "body": body,
                                }
                            )

                        except TypeError:

                            result = triage_ticket(
                                ticket_id,
                                subject,
                                body,
                            )

                except Exception as e:

                    st.error("Ticket analysis failed.")

                    st.exception(e)

                    result = None

            if result is not None:

                st.success("Ticket successfully analyzed!")

                st.markdown("### 📋 Triage Result")

                # ----------------------------------------------------
                # Main metrics
                # ----------------------------------------------------

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    display_metric(
                        "Product Area",
                        get_value(result, "product_area"),
                    )

                with col2:
                    display_metric(
                        "Category",
                        get_value(result, "issue_category"),
                    )

                with col3:
                    display_metric(
                        "Urgency",
                        get_value(result, "urgency"),
                    )

                with col4:
                    display_metric(
                        "Known Issue",
                        get_value(result, "known_issue"),
                    )

                st.markdown("")

                # ----------------------------------------------------
                # Team
                # ----------------------------------------------------

                st.subheader("👥 Recommended Team")

                st.info(
                    str(
                        get_value(
                            result,
                            "recommended_team",
                            "Not specified",
                        )
                    )
                )

                # ----------------------------------------------------
                # Reasoning
                # ----------------------------------------------------

                reasoning = get_value(
                    result,
                    "reasoning",
                    "",
                )

                if reasoning:

                    with st.expander("🧠 AI Reasoning", expanded=True):

                        st.write(str(reasoning))

                # ----------------------------------------------------
                # Documents
                # ----------------------------------------------------

                documents = get_value(
                    result,
                    "relevant_documents",
                    [],
                )

                with st.expander("📚 Relevant Documents"):

                    if documents:

                        for document in documents:
                            st.markdown(f"- `{document}`")

                    else:

                        st.write("No relevant documents identified.")

                # ----------------------------------------------------
                # Draft response
                # ----------------------------------------------------

                draft = get_value(
                    result,
                    "draft_response",
                    "",
                )

                if draft:

                    st.subheader("✉️ Draft Customer Response")

                    st.text_area(
                        "Generated response",
                        value=str(draft),
                        height=180,
                    )


# ============================================================
# PAGE 2 — ACCOUNT HEALTH
# ============================================================

elif page == "🏢 Account Health":

    st.header("🏢 Customer Account Health")

    st.write(
        "Generate an executive account-health brief using account "
        "information and recent support-ticket activity."
    )

    st.markdown("---")

    if not accounts:

        st.error("No account data found.")

    else:

        account_map = {
            account.get("account_id"): account
            for account in accounts
        }

        account_ids = list(account_map.keys())

        selected_account_id = st.selectbox(
            "Select Account",
            account_ids,
        )

        selected_account = account_map[selected_account_id]

        # --------------------------------------------------------
        # Account overview
        # --------------------------------------------------------

        st.subheader("Account Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            display_metric(
                "Company",
                selected_account.get("company", "N/A"),
            )

        with col2:
            display_metric(
                "Health",
                selected_account.get("health_status", "N/A"),
            )

        with col3:
            display_metric(
                "Usage Trend",
                selected_account.get("usage_trend", "N/A"),
            )

        with col4:
            display_metric(
                "Plan",
                selected_account.get("plan_tier", "N/A"),
            )

        st.markdown("")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            display_metric(
                "ARR",
                f"${selected_account.get('arr_usd', 0):,}",
            )

        with col2:
            display_metric(
                "Active Seats",
                selected_account.get("seats_active", "N/A"),
            )

        with col3:
            display_metric(
                "Open Tickets",
                selected_account.get("open_tickets", "N/A"),
            )

        with col4:
            display_metric(
                "Renewal",
                selected_account.get("renewal_date", "N/A"),
            )

        st.markdown("---")

        # --------------------------------------------------------
        # Account details
        # --------------------------------------------------------

        with st.expander("👤 Customer Details"):

            primary_contact = selected_account.get(
                "primary_contact",
                {},
            )

            st.write(
                f"**Primary Contact:** "
                f"{primary_contact.get('name', 'N/A')}"
            )

            st.write(
                f"**Title:** "
                f"{primary_contact.get('title', 'N/A')}"
            )

            st.write(
                f"**TAM:** "
                f"{selected_account.get('tam', 'N/A')}"
            )

            st.write(
                f"**Region:** "
                f"{selected_account.get('region', 'N/A')}"
            )

            st.write(
                f"**Industry:** "
                f"{selected_account.get('industry', 'N/A')}"
            )

            st.write(
                f"**Products:** "
                f"{', '.join(selected_account.get('products', []))}"
            )

        # --------------------------------------------------------
        # Generate health brief
        # --------------------------------------------------------

        if st.button(
            "🚀 Generate Account Health Brief",
            type="primary",
            use_container_width=True,
        ):

            if generate_account_brief is None:

                st.error(
                    "Could not import the existing Task 2 function."
                )

                st.code(ACCOUNT_IMPORT_ERROR)

            else:

                with st.spinner(
                    "Generating account health analysis..."
                ):

                    try:

                        result = generate_account_brief(
                            selected_account_id
                        )

                    except Exception as e:

                        st.error(
                            "Account health analysis failed."
                        )

                        st.exception(e)

                        result = None

                if result is not None:

                    st.success(
                        "Account health brief generated!"
                    )

                    # ------------------------------------------------
                    # Handle result
                    # ------------------------------------------------

                    if isinstance(result, dict):

                        # --------------------------------------------
                        # Executive Summary
                        # --------------------------------------------

                        st.subheader(
                            "📌 Executive Summary"
                        )

                        summary = (
                            result.get(
                                "executive_summary"
                            )
                            or result.get(
                                "summary"
                            )
                        )

                        if summary:
                            st.write(summary)

                        # --------------------------------------------
                        # Risks
                        # --------------------------------------------

                        st.subheader(
                            "⚠️ Open Risks & Flagged Issues"
                        )

                        risks = (
                            result.get(
                                "open_risks"
                            )
                            or result.get(
                                "open_risks_and_flagged_issues"
                            )
                            or result.get(
                                "risks"
                            )
                        )

                        if risks:

                            if isinstance(
                                risks,
                                list,
                            ):

                                for risk in risks:

                                    if isinstance(
                                        risk,
                                        dict,
                                    ):

                                        st.warning(
                                            "\n".join(
                                                [
                                                    f"**{k}:** {v}"
                                                    for k, v
                                                    in risk.items()
                                                ]
                                            )
                                        )

                                    else:

                                        st.warning(
                                            str(risk)
                                        )

                            else:

                                st.warning(
                                    str(risks)
                                )

                        else:

                            st.info(
                                "No open risks identified."
                            )

                        # --------------------------------------------
                        # Talking Points
                        # --------------------------------------------

                        st.subheader(
                            "💬 Recommended Talking Points"
                        )

                        talking_points = (
                            result.get(
                                "recommended_talking_points"
                            )
                            or result.get(
                                "talking_points"
                            )
                        )

                        if talking_points:

                            if isinstance(
                                talking_points,
                                list,
                            ):

                                for point in talking_points:

                                    st.markdown(
                                        f"- {point}"
                                    )

                            else:

                                st.write(
                                    talking_points
                                )

                        # --------------------------------------------
                        # Full result
                        # --------------------------------------------

                        with st.expander(
                            "🔍 View Full Analysis"
                        ):

                            st.json(result)

                    else:

                        # Some versions of Task 2 return
                        # a formatted string rather than a dict.

                        st.markdown(
                            str(result)
                        )


# ============================================================
# PAGE 3 — EVALUATION
# ============================================================

elif page == "📊 Evaluation":

    st.header("📊 Evaluation Results")

    st.write(
        "Automated evaluation results for the implemented AI "
        "support workflows."
    )

    st.markdown("---")

    if not evaluation:

        st.warning(
            "Evaluation report not found."
        )

    else:

        task1 = evaluation.get(
            "task1",
            {},
        )

        task2 = evaluation.get(
            "task2",
            {},
        )

        overall = evaluation.get(
            "overall_score",
            0,
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            display_metric(
                "Task 1 Score",
                f"{task1.get('average_score', 0) * 100:.0f}%",
            )

        with col2:

            display_metric(
                "Task 2 Score",
                f"{task2.get('average_score', 0) * 100:.0f}%",
            )

        with col3:

            display_metric(
                "Overall Score",
                f"{overall * 100:.0f}%",
            )

        st.markdown("")

        if overall >= 1:

            st.success(
                "🎉 All evaluation tests passed successfully."
            )

        elif overall >= 0.8:

            st.info(
                "Most evaluation tests passed."
            )

        else:

            st.warning(
                "Some evaluation tests require attention."
            )

        # --------------------------------------------------------
        # Task 1 tests
        # --------------------------------------------------------

        st.subheader("🎫 Task 1 — Ticket Triage")

        task1_tests = task1.get(
            "tests",
            [],
        )

        if task1_tests:

            for test in task1_tests:

                ticket_id = test.get(
                    "ticket_id",
                    "Unknown",
                )

                score = test.get(
                    "score",
                    0,
                )

                passed = test.get(
                    "passed",
                    False,
                )

                if passed:

                    st.success(
                        f"✅ {ticket_id} — "
                        f"{score * 100:.0f}%"
                    )

                else:

                    st.error(
                        f"❌ {ticket_id} — "
                        f"{score * 100:.0f}%"
                    )

        # --------------------------------------------------------
        # Task 2 tests
        # --------------------------------------------------------

        st.subheader("🏢 Task 2 — Account Health")

        task2_tests = task2.get(
            "tests",
            [],
        )

        if task2_tests:

            for test in task2_tests:

                account_id = test.get(
                    "account_id",
                    "Unknown",
                )

                score = test.get(
                    "score",
                    0,
                )

                passed = test.get(
                    "passed",
                    False,
                )

                if passed:

                    st.success(
                        f"✅ {account_id} — "
                        f"{score * 100:.0f}%"
                    )

                else:

                    st.error(
                        f"❌ {account_id} — "
                        f"{score * 100:.0f}%"
                    )

        # --------------------------------------------------------
        # Raw evaluation report
        # --------------------------------------------------------

        with st.expander(
            "🔍 View Evaluation Report"
        ):

            st.json(evaluation)


# ============================================================
# PAGE 4 — ABOUT
# ============================================================

elif page == "ℹ️ About":

    st.header("ℹ️ About This Project")

    st.markdown(
        """
        ## AI Support Intelligence

        An AI-powered customer support intelligence system designed
        to assist support teams with ticket triage and customer
        account-health analysis.

        ### Core Capabilities

        **🎫 Ticket Triage**

        Automatically classifies support tickets by:

        - Product area
        - Issue category
        - Urgency
        - Known issue status
        - Relevant documentation
        - Recommended team
        - Draft customer response

        **🏢 Account Health**

        Generates customer health briefs using:

        - Account information
        - Usage trends
        - Support-ticket activity
        - Account risks
        - Recommended TAM talking points

        **📚 Knowledge Retrieval**

        Uses product documentation to ground support decisions.

        **📊 Evaluation**

        Includes automated evaluation across representative
        and adversarial test cases.

        ### Technology

        - Python
        - LLM
        - Groq
        - Retrieval / RAG
        - FastAPI
        - Streamlit
        - JSON
        - Git / GitHub
        """
    )

    st.markdown("---")

    st.info(
        "This Streamlit interface is a presentation layer over "
        "the existing Task 1 and Task 2 implementations."
    )