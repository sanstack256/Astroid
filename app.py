import streamlit as st
from huggingface_hub import InferenceClient

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Asteroid Research Assistant",
    page_icon="☄️",
    layout="centered",
)

# -----------------------------------------------------------------------------
# Black Background with Smooth Moving Green Radial Gradient
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Deep black background canvas */
    [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        position: relative;
        overflow-x: hidden;
    }

    /* Primary expansive smooth-moving green radial gradient orb */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: -200px;
        left: -200px;
        width: 1400px;
        height: 1400px;
        border-radius: 50%;
        background: radial-gradient(
            circle,
            rgba(16, 185, 129, 0.22) 0%,
            rgba(5, 150, 105, 0.12) 35%,
            rgba(4, 120, 87, 0.05) 58%,
            transparent 75%
        );
        filter: blur(100px);
        animation: smoothGreenTravelPrimary 28s ease-in-out infinite alternate;
        pointer-events: none;
        z-index: 0;
    }

    /* Secondary expansive subtle green radial gradient orb for continuous ambient flow */
    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: fixed;
        top: -150px;
        left: -150px;
        width: 1200px;
        height: 1200px;
        border-radius: 50%;
        background: radial-gradient(
            circle,
            rgba(52, 211, 153, 0.16) 0%,
            rgba(16, 185, 129, 0.08) 38%,
            rgba(6, 95, 70, 0.04) 58%,
            transparent 75%
        );
        filter: blur(110px);
        animation: smoothGreenTravelSecondary 34s ease-in-out infinite alternate;
        pointer-events: none;
        z-index: 0;
    }

    /* Ensure content renders cleanly above the moving ambient glow */
    [data-testid="stAppViewContainer"] > .main {
        position: relative;
        z-index: 1;
    }

    /* Keep header transparent for seamless full-screen ambiance */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Primary green orb smooth journey across the screen */
    @keyframes smoothGreenTravelPrimary {
        0% {
            transform: translate3d(-20vw, -20vh, 0) scale(1);
        }
        25% {
            transform: translate3d(50vw, 10vh, 0) scale(1.15);
        }
        50% {
            transform: translate3d(35vw, 55vh, 0) scale(0.95);
        }
        75% {
            transform: translate3d(-10vw, 40vh, 0) scale(1.1);
        }
        100% {
            transform: translate3d(45vw, 65vh, 0) scale(1.05);
        }
    }

    /* Secondary green orb companion trajectory */
    @keyframes smoothGreenTravelSecondary {
        0% {
            transform: translate3d(60vw, 60vh, 0) scale(1);
        }
        30% {
            transform: translate3d(15vw, 45vh, 0) scale(1.12);
        }
        65% {
            transform: translate3d(45vw, -15vh, 0) scale(0.95);
        }
        100% {
            transform: translate3d(-15vw, 15vh, 0) scale(1.08);
        }
    }

    /* Refined dark glassmorphic input cards */
    .stTextInput > div > div,
    .stNumberInput > div > div,
    .stTextArea > div > div {
        background: rgba(15, 23, 42, 0.65) !important;
        backdrop-filter: blur(12px);
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35) !important;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div:focus-within,
    .stNumberInput > div > div:focus-within,
    .stTextArea > div > div:focus-within {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.25) !important;
    }

    /* Primary button with emerald neon styling */
    button[kind="primary"] {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 22px rgba(16, 185, 129, 0.45) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Asteroid Research Assistant")
st.subheader("Near-Earth Object Analysis Tool")
st.write(
    "Enter observational parameters for a Near-Earth Object (NEO) to generate "
    "a structured scientific research summary."
)

st.divider()

# -----------------------------------------------------------------------------
# User Input Section
# -----------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    designation = st.text_input(
        "Object Designation *",
        placeholder="e.g., 2026 AB",
        help="Provisional or permanent designation of the object.",
    )
    diameter = st.number_input(
        "Estimated Diameter (meters)",
        min_value=0.0,
        value=0.0,
        step=10.0,
        help="Leave as 0 if unknown.",
    )
    velocity = st.number_input(
        "Relative Velocity (km/s)",
        min_value=0.0,
        value=0.0,
        step=0.5,
        help="Velocity relative to Earth. Leave as 0 if unknown.",
    )

with col2:
    orbit_type = st.text_input(
        "Orbit Type",
        placeholder="e.g., Apollo, Aten, Amor, Atira",
        help="Classification of the NEO orbit.",
    )
    distance = st.number_input(
        "Closest Approach Distance (km)",
        min_value=0.0,
        value=0.0,
        step=50000.0,
        format="%.0f",
        help="Nominal close-approach distance in kilometers. Leave as 0 if unknown.",
    )

additional_obs = st.text_area(
    "Additional Observations (Optional)",
    placeholder="e.g., Optical light curve suggests a 4.2-hour rotation period; suspected S-type composition.",
    help="Add any contextual notes, spectral classification, or optical data.",
)

# -----------------------------------------------------------------------------
# Analysis Execution
# -----------------------------------------------------------------------------
if st.button("Analyze Object", type="primary"):
    if not designation.strip():
        st.warning("⚠️ Please provide an Object Designation (e.g., '2026 AB') to proceed.")
    else:
        # Format the parameters cleanly for the prompt
        diameter_val = f"{diameter} meters" if diameter > 0 else "Not provided in the supplied data."
        velocity_val = f"{velocity} km/s" if velocity > 0 else "Not provided in the supplied data."
        distance_val = f"{distance:,.0f} km" if distance > 0 else "Not provided in the supplied data."
        orbit_val = orbit_type.strip() if orbit_type.strip() else "Not provided in the supplied data."
        notes_val = additional_obs.strip() if additional_obs.strip() else "Not provided in the supplied data."

        # System instructions enforcing strict scientific reliability, zero speculation, and rigorous constraints
        system_instruction = (
            "You are a rigorous, professional astronomical research assistant specializing in Near-Earth Object (NEO) analysis. "
            "Your role is to produce a strictly objective, scientifically reliable report based ONLY on the parameters explicitly supplied in the prompt.\n\n"
            "You must strictly enforce the following scientific and operational requirements at all times:\n\n"
            "1. STRICTLY SEPARATE FACTS FROM INTERPRETATION:\n"
            "- The ONLY factual asteroid-specific information available to you is what the application explicitly supplies:\n"
            "  * Object designation\n"
            "  * Estimated diameter\n"
            "  * Relative velocity\n"
            "  * Closest approach distance\n"
            "  * Orbit type\n"
            "  * Additional observations\n"
            "- Do NOT introduce or extrapolate other asteroid-specific facts unless they were explicitly supplied.\n"
            "- Even if the object designation (such as '2023 BU') corresponds to a known astronomical body in your pre-training data, you must NEVER recall, "
            "cite, or inject unsupplied real-world facts, discovery details, discovery dates, observer names, historical events, or unsupplied measurements. "
            "Treat the provided text as your sole universe of facts.\n\n"
            "2. NO UNSUPPORTED SAFETY OR HAZARD CONCLUSIONS (STRICT MANDATE):\n"
            "- You are STRICTLY FORBIDDEN from stating, suggesting, or implying that this object:\n"
            "  * 'poses no threat' or 'poses a threat'\n"
            "  * is 'safe', 'harmless', 'dangerous', 'hazardous', or 'does not appear particularly hazardous'\n"
            "  * 'will impact Earth' or 'will not impact Earth'\n"
            "  * has a particular impact probability or risk status\n"
            "- NEVER use the closest-approach distance to evaluate safety or hazard. A small distance does NOT allow you to declare the object safe or dangerous.\n"
            "- State clearly that validated orbital solutions, complete astrometric observation arcs, and dedicated astronomical orbit/impact calculations "
            "(such as official planetary-defense pipelines) are required for any impact-risk evaluation.\n\n"
            "3. NO ATMOSPHERIC OR IMPACT SCENARIOS (STRICT MANDATE):\n"
            "- Do NOT speculate on atmospheric interaction or impact consequences. You must NOT mention or speculate about:\n"
            "  * fireballs, meteors, or meteoroid showers\n"
            "  * atmospheric entry, ablation, airbursts, or explosions\n"
            "  * reaching the ground, ground damage, cratering, or casualties\n"
            "- The supplied diameter and velocity describe only physical dimensions and relative speed in space. They are strictly insufficient to make "
            "any statements or predictions about atmospheric or ground effects.\n\n"
            "4. DO NOT INVENT ORBITAL INFORMATION:\n"
            "- You may explain what the supplied orbit type (e.g., 'Apollo') means as a general textbook definition.\n"
            "- You must NOT infer, calculate, or invent specific unsupplied orbital elements, including:\n"
            "  * eccentricity\n"
            "  * inclination\n"
            "  * semi-major axis\n"
            "  * perihelion\n"
            "  * aphelion\n"
            "  * orbital period\n"
            "  * trajectory or future encounters\n"
            "  when those values were not supplied.\n\n"
            "5. DO NOT INVENT OBSERVATIONAL HISTORY:\n"
            "- Do NOT claim or suggest that this particular object:\n"
            "  * has been observed by radar or specific observatories\n"
            "  * has a known composition or mineralogy\n"
            "  * has a known rotation period or light curve\n"
            "  * has a known albedo\n"
            "  * has previous observations or discovery history\n"
            "  * has a particular spectral classification\n"
            "  unless those facts are explicitly supplied.\n\n"
            "6. OBSERVATION PRIORITIES AS RECOMMENDATIONS ONLY:\n"
            "- When discussing useful observations, phrase them strictly as RECOMMENDATIONS FOR WHAT COULD BE MEASURED in the future, "
            "rather than claiming that those measurements have already been performed.\n"
            "- Use: 'Optical astrometry could help refine the object\\'s orbital solution.'\n"
            "- Never use: 'Optical astrometry has refined the object\\'s orbit.'\n\n"
            "7. SCIENTIFIC SIGNIFICANCE:\n"
            "- Keep this general, population-level, and evidence-based (e.g., explaining why studying small Near-Earth Objects in general provides insight into Solar System formation).\n"
            "- Do NOT make safety, hazard, or risk claims about this object in this section or any other section.\n"
            "- Do NOT make unsupported specific claims about this particular object.\n\n"
            "8. AVOID IRRELEVANT CATEGORIES:\n"
            "- Do NOT mention Centaurs, cometary reservoirs, Kuiper Belt objects, or other unrelated Solar System object classes unless directly relevant to information supplied by the user.\n\n"
            "9. MISSING DATA EXPLICIT DISCLOSURE:\n"
            "- Whenever an important parameter is unavailable or not supplied, explicitly state:\n"
            "  'Not provided in the supplied data.'\n\n"
            "10. CONSERVATIVE SCIENTIFIC LANGUAGE:\n"
            "- Use conservative scientific language at all times.\n"
            "- Prefer: 'may', 'could', 'would require additional data', 'cannot be determined from the supplied information'.\n"
            "- Avoid: 'will', 'definitely', 'proves', 'poses no threat', 'is safe', 'is dangerous', 'hazardous', 'not hazardous'.\n\n"
            "11. FINAL LIMITATION STATEMENT:\n"
            "- The report MUST conclude with this exact clear statement:\n"
            "  'This application performs LLM-based interpretation of supplied information and does not perform professional orbit determination, "
            "trajectory propagation, or official planetary-defense risk assessment.'\n\n"
            "12. REQUIRED REPORT FORMAT:\n"
            "Structure the response using exactly these markdown headings:\n\n"
            "## Object Overview\n"
            "Factual, neutral overview strictly based on supplied inputs.\n\n"
            "## Supplied Parameters\n"
            "Verbatim list of supplied parameters. For any omitted value, state 'Not provided in the supplied data.'\n\n"
            "## Physical and Kinematic Interpretation\n"
            "Objective interpretation of size and relative velocity scale in space. Do not mention atmospheric entry, meteors, fireballs, airbursts, or ground damage.\n\n"
            "## Orbital Characteristics\n"
            "Textbook definition of the supplied orbit type only. State that true orbital elements (eccentricity, inclination, semi-major axis, etc.) were not provided.\n\n"
            "## Scientific Significance\n"
            "General, population-level scientific importance of studying small NEOs without claiming unsupplied properties or evaluating hazard/safety for this object.\n\n"
            "## Recommended Observation Priorities\n"
            "Future observational recommendations for what could be measured (optical astrometry, radar ranging, photometry, spectroscopy), strictly phrased as recommendations.\n\n"
            "## Uncertainties and Limitations\n"
            "Discussion of missing data, concluding with the mandatory final limitation statement."
        )

        user_content = (
            f"Perform a scientific research analysis for the following Near-Earth Object data:\n\n"
            f"- Object Designation: {designation.strip()}\n"
            f"- Estimated Diameter: {diameter_val}\n"
            f"- Relative Velocity: {velocity_val}\n"
            f"- Closest Approach Distance: {distance_val}\n"
            f"- Orbit Type: {orbit_val}\n"
            f"- Additional Observations: {notes_val}\n\n"
            f"Strict Scientific Mandates:\n"
            f"1. Base your report ONLY on the supplied values above. Do NOT recall or invent unsupplied facts, discovery history, composition, or orbital elements, even if you recognize the designation.\n"
            f"2. Do NOT evaluate safety or hazard: do NOT state that the object is safe, dangerous, hazardous, not hazardous, poses no threat, or poses a threat. Do NOT state whether it will or will not hit Earth, and do NOT state an impact probability.\n"
            f"3. Do NOT mention atmospheric or ground scenarios: NO mentions of fireballs, meteors, meteoroid showers, atmospheric entry, airbursts, craters, or ground damage.\n"
            f"4. Do NOT invent specific orbital elements (no eccentricity, inclination, semi-major axis, perihelion, aphelion, or periods).\n"
            f"5. Do NOT invent observational history (no claims of past radar, lightcurves, albedo, or spectral classification).\n"
            f"6. Phrase observation priorities strictly as recommendations for what could be measured in the future, not what has been done.\n"
            f"7. Do NOT mention centaurs or unrelated Solar System classes.\n"
            f"8. For any missing parameter, state 'Not provided in the supplied data.'\n"
            f"9. Use conservative scientific language ('may', 'could', 'cannot be determined from the supplied information').\n"
            f"10. Conclude with the mandatory final limitation statement."
        )

        # Retrieve secret token
        hf_token = st.secrets.get("HF_TOKEN")
        if not hf_token:
            st.error("Hugging Face token not found in `.streamlit/secrets.toml`. Please check your configuration.")
        else:
            with st.spinner("Contacting Qwen 2.5 7B to synthesize research analysis..."):
                messages = [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_content},
                ]

                try:
                    # Attempt standard automatic provider routing
                    client = InferenceClient(api_key=hf_token)
                    response = client.chat.completions.create(
                        model="Qwen/Qwen2.5-7B-Instruct",
                        messages=messages,
                        max_tokens=1500,
                    )
                    analysis_text = response.choices[0].message.content
                except Exception:
                    # Fallback to featherless-ai on HF serverless network
                    try:
                        client = InferenceClient(api_key=hf_token, provider="featherless-ai")
                        response = client.chat.completions.create(
                            model="Qwen/Qwen2.5-7B-Instruct",
                            messages=messages,
                            max_tokens=1500,
                        )
                        analysis_text = response.choices[0].message.content
                    except Exception as err:
                        st.error(f"Inference request failed: {err}")
                        analysis_text = None

            if analysis_text:
                st.divider()
                st.subheader(f"Scientific Research Summary: {designation.strip()}")
                st.markdown(analysis_text)
