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

    /* Primary smooth-moving green radial gradient orb */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 750px;
        height: 750px;
        border-radius: 50%;
        background: radial-gradient(
            circle,
            rgba(16, 185, 129, 0.22) 0%,
            rgba(5, 150, 105, 0.12) 35%,
            rgba(4, 120, 87, 0.05) 55%,
            transparent 70%
        );
        filter: blur(50px);
        animation: smoothGreenTravelPrimary 26s ease-in-out infinite alternate;
        pointer-events: none;
        z-index: 0;
    }

    /* Secondary subtle green radial gradient orb for continuous ambient flow */
    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 600px;
        height: 600px;
        border-radius: 50%;
        background: radial-gradient(
            circle,
            rgba(52, 211, 153, 0.16) 0%,
            rgba(16, 185, 129, 0.08) 40%,
            transparent 68%
        );
        filter: blur(60px);
        animation: smoothGreenTravelSecondary 32s ease-in-out infinite alternate;
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
            transform: translate3d(-10vw, -10vh, 0) scale(1);
        }
        25% {
            transform: translate3d(65vw, 15vh, 0) scale(1.15);
        }
        50% {
            transform: translate3d(45vw, 65vh, 0) scale(0.95);
        }
        75% {
            transform: translate3d(5vw, 50vh, 0) scale(1.1);
        }
        100% {
            transform: translate3d(55vw, 80vh, 0) scale(1.05);
        }
    }

    /* Secondary green orb companion trajectory */
    @keyframes smoothGreenTravelSecondary {
        0% {
            transform: translate3d(70vw, 75vh, 0) scale(1);
        }
        30% {
            transform: translate3d(20vw, 60vh, 0) scale(1.12);
        }
        65% {
            transform: translate3d(55vw, -5vh, 0) scale(0.92);
        }
        100% {
            transform: translate3d(-5vw, 25vh, 0) scale(1.08);
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

        # System instructions enforcing strict scientific analysis and safety principles
        system_instruction = (
            "You are a rigorous, professional astronomical research assistant specializing in Near-Earth Object (NEO) analysis. "
            "Your role is to perform careful, objective scientific information analysis based strictly on the parameters supplied. "
            "You must follow these strict scientific principles at all times:\n\n"
            "1. SOURCE OF FACTS:\n"
            "Treat the asteroid values supplied in the prompt as the sole authoritative input for this analysis.\n\n"
            "2. DO NOT INVENT DATA:\n"
            "Never invent or extrapolate unsupplied data, including orbital elements (semi-major axis, eccentricity, inclination, perihelion, etc.), "
            "discovery details, observation history, composition/spectral type, impact probability, numerical uncertainties, dates, or missions. "
            "If any parameter or detail is not explicitly supplied in the prompt, you must explicitly state:\n"
            "'Not provided in the supplied data.'\n\n"
            "3. FACT VS INTERPRETATION:\n"
            "Strictly distinguish between:\n"
            "- Directly supplied measurements (facts provided by the user),\n"
            "- Scientifically reasonable interpretations (theoretical context of those values),\n"
            "- Information that would require additional dedicated observations or numerical orbital calculations.\n\n"
            "4. ORBITAL MECHANICS CONSTRAINTS:\n"
            "You may explain what a supplied orbital classification (e.g., Apollo, Aten, Amor, Atira) definitionally means. "
            "However, you must NOT calculate or claim to determine orbital elements, trajectories, ephemerides, or future close approaches "
            "from the limited parameters provided.\n\n"
            "5. IMPACT RISK MANDATE:\n"
            "- Do NOT calculate or claim an impact probability.\n"
            "- Do NOT classify the object as 'dangerous', 'safe', 'high risk', 'apocalyptic', or similar labels solely from the supplied diameter, "
            "velocity, distance, or orbit type.\n"
            "- State clearly that genuine impact-risk evaluation requires comprehensive astrometric observation arcs, validated orbital solutions, "
            "and dedicated planetary-defense calculation pipelines (such as NASA JPL Sentry or ESA NEODyS).\n\n"
            "6. PRESERVE UNITS EXACTLY:\n"
            "Always report and preserve the units supplied by the application:\n"
            "- Diameter in meters\n"
            "- Relative velocity in km/s\n"
            "- Closest approach distance in km\n"
            "Do not silently convert units or reinterpret numerical values.\n\n"
            "7. PROFESSIONAL SCIENTIFIC TONE:\n"
            "Use measured, precise, academic scientific language. Never use sensationalized terminology (e.g., 'killer asteroid', 'Earth-ending', 'cataclysmic threat').\n\n"
            "8. REQUIRED OUTPUT STRUCTURE:\n"
            "You must structure your analysis using EXACTLY these markdown headings:\n\n"
            "## Object Overview\n"
            "Provide a concise, neutral scientific introduction of the object based strictly on the supplied designation and known parameters.\n\n"
            "## Supplied Parameters\n"
            "Accurately reproduce the supplied values in a clear list before any interpretation. If a value was omitted, list it as 'Not provided in the supplied data.'\n\n"
            "## Interpretation\n"
            "Provide a scientifically reasonable interpretation of the supplied physical and kinematic parameters (scale of the object, kinetic implications of velocity, flyby distance scale).\n\n"
            "## Orbital Characteristics\n"
            "Explain what the supplied orbit classification represents definitionally. Explicitly note that full orbital elements and trajectory evolution require complete astrometric orbital fitting and cannot be derived from the supplied inputs.\n\n"
            "## Scientific Significance\n"
            "Discuss what makes an object of this general physical scale and flyby geometry scientifically relevant for planetary science.\n\n"
            "## Observation Priorities\n"
            "Detail specific follow-up observations and observational techniques (e.g., optical astrometry for orbit refinement, radar ranging for shape/orbit, multi-band photometry for rotation/albedo, spectroscopy for compositional taxonomy) that would improve understanding.\n\n"
            "## Uncertainties and Limitations\n"
            "Explicitly list key observational uncertainties arising from missing parameters. Conclude with a concise statement explaining that this application provides an LLM-generated interpretation of supplied data and is not a substitute for professional orbital determination or official planetary-defense assessment."
        )

        user_content = (
            f"Perform a scientific analysis for the following Near-Earth Object data:\n\n"
            f"- Object Designation: {designation.strip()}\n"
            f"- Estimated Diameter: {diameter_val}\n"
            f"- Relative Velocity: {velocity_val}\n"
            f"- Closest Approach Distance: {distance_val}\n"
            f"- Orbit Type: {orbit_val}\n"
            f"- Additional Observations: {notes_val}\n"
        )

        # Retrieve secret token
        hf_token = st.secrets.get("HF_TOKEN")
        if not hf_token:
            st.error("❌ Hugging Face token not found in `.streamlit/secrets.toml`. Please check your configuration.")
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
