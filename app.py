import streamlit as st
import pandas as pd
import numpy as np
import json

# --- Existing Python Logic Functions ---
# These functions were developed and refined in our previous turns.
# They are included directly in this Streamlit app for simplicity.


def interpret_24hr_urine(urine_profile, patient_profile=None):
    """
    Interprets 24-hour urine parameters based on Box 5 of the manuscript.
    Returns a dictionary of findings and potential implications.
    """
    findings = {}

    # Volume
    if urine_profile["volume_L"] < 2.5:
        findings["urine_volume"] = f"Low urine volume ({urine_profile['volume_L']} L/d). Goal is ~2.5 L/d for reducing recurrence risk."

    # pH
    if urine_profile["ph"] < 6.0:
        findings["urine_ph"] = f"Acidic urine pH ({urine_profile['ph']}). May increase risk of uric acid stones."
    # Explicitly check for RTA
    elif patient_profile and "Renal Tubular Acidosis" in patient_profile.get("medical_conditions", []):
        # As per manuscript, pH >= 6.0 with RTA suggests CaP stones
        if urine_profile["ph"] >= 6.0:
            findings["urine_ph"] = f"Alkaline urine pH ({urine_profile['ph']}) with diagnosed Renal Tubular Acidosis (RTA). Suggests a risk for calcium phosphate stones."
    elif urine_profile["ph"] > 7.0:
        findings["urine_ph"] = f"Very alkaline urine pH ({urine_profile['ph']}). May indicate urine infection by bacteria with urease and a risk for struvite stones."

    # Calcium
    # Graded increase in risk from 150 mg/d as per manuscript
    if urine_profile["calcium_mg"] > 150:
        findings["urine_calcium"] = f"Hypercalciuria ({urine_profile['calcium_mg']} mg/d). Levels >150 mg/d increase stone risk. Correlate with urine sodium."

    # Oxalate
    if urine_profile["oxalate_mg"] > 40:
        findings["urine_oxalate"] = f"Elevated urine oxalate ({urine_profile['oxalate_mg']} mg/d). Values >40 mg/d are excessive."
        if urine_profile["oxalate_mg"] > 80:
            findings["urine_oxalate"] += " For values >80 mg/d, consider primary hyperoxaluria."

    # Citrate
    if urine_profile["citrate_mg"] < 400:
        findings["urine_citrate"] = f"Low urine citrate ({urine_profile['citrate_mg']} mg/d). Values <400 mg/d may limit risk for calcareous stones."

    # Uric Acid
    # Using ~750-800 mg/d as general upper limit
    if urine_profile["uric_acid_mg"] > 750:
        findings["urine_uric_acid"] = f"High urine uric acid ({urine_profile['uric_acid_mg']} mg/d). Consider xanthine oxidase inhibitor or reduced purine intake if recurrent calcium oxalate or uric acid stones persist."

    # Sodium
    # If hypercalciuria is present, sodium target is <100 mEq/d
    if "urine_calcium" in findings and urine_profile["sodium_mEq"] > 100:
        findings["urine_sodium"] = f"High urine sodium ({urine_profile['sodium_mEq']} mEq). If hypercalciuria is present, a goal of <100 mEq/d is sought."

    # Sulfate (indicative of animal protein intake)
    if urine_profile["sulfate_mmol"] > 30:
        findings["urine_sulfate"] = f"High urine sulfate ({urine_profile['sulfate_mmol']} mmol/d). Suggests excessive dietary animal protein."

    # Ammonium (indicative of acid production)
    if urine_profile["ammonium_mmol"] > 45:
        findings["urine_ammonium"] = f"High urine ammonium ({urine_profile['ammonium_mmol']} mmol/d). Suggests excess acid production from diet, chronic diarrhea, or other cause."

    # Cystine
    if urine_profile.get("cystine_mg", 0) > 30:  # Normal <30 mg/d
        findings["urine_cystine"] = f"Elevated urine cystine ({urine_profile['cystine_mg']} mg/d). Normal individuals typically excrete <30 mg/d. Patients with cystinuria generally excrete >400 mg/d."
        if urine_profile.get("cystine_mg", 0) > 400:
            findings["urine_cystine"] += " Highly suggestive of cystinuria."

    # Supersaturation (simplified for this example, actual calculation is complex)
    findings["supersaturation_targets"] = "General supersaturation targets for reducing risk are <4 for calcium oxalate stones and <1 for calcium phosphate and uric acid stones."

    return findings


def generate_management_plan(stone_type, urine_interpretation, patient_profile, serum_labs=None):
    """
    Generates a management plan based on stone type, urine interpretation, patient profile, and serum labs.
    """
    plan = ["Increase urine volume to ~2.5 L/day. This is always helpful in lowering supersaturation."]

    if stone_type == "Calcium Oxalate":
        plan.append(
            "Focus on addressing reversible factors for calcium oxalate stones.")
        if "urine_calcium" in urine_interpretation:
            plan.append("Restrict sodium intake (<2,300 mg/d).")
            plan.append("Administer thiazide if hypercalciuric.")
        plan.append(
            "Optimize calcium intake (1,000-1,200 mg/d). Avoid strict calcium restriction as it can worsen hyperoxaluria and bone loss.")
        if "urine_citrate" in urine_interpretation and "Low urine citrate" in urine_interpretation["urine_citrate"]:
            plan.append(
                "Administer potassium citrate and/or treat potassium deficiency if hypocitraturic.")
        if "urine_oxalate" in urine_interpretation and "Elevated urine oxalate" in urine_interpretation["urine_oxalate"]:
            plan.append(
                "Consider oxalate restriction for significant hyperoxaluria.")
            plan.append("Consider sucrose/fructose restriction.")
            plan.append(
                "Consider calcium citrate with meals to bind intestinal oxalate.")
        plan.append("Restrict animal protein.")
        if "Malabsorption (IBD, Bariatric Surgery, etc.)" in patient_profile["medical_conditions"]:
            plan.append(
                "Given history of malabsorption, consider enteric hyperoxaluria. Calcium citrate with meals is particularly relevant.")
        if serum_labs and serum_labs.get("calcium_mg_dL", 0) >= 10.8 and serum_labs.get("intact_pth_pg_mL", 0) >= 70:
            plan.append(
                "Given hypercalcemia and non-suppressed PTH, primary hyperparathyroidism is likely. Parathyroidectomy is the most appropriate therapy.")

    elif stone_type == "Calcium Phosphate":
        plan.append(
            "Focus on addressing reversible factors for calcium phosphate stones.")
        if "urine_ph" in urine_interpretation and "Alkaline urine pH" in urine_interpretation["urine_ph"] and any(med in patient_profile.get("medications", []) for med in ["Topiramate", "Acetazolamide"]):
            plan.append(
                "Discontinuation of offending medications that increase urine pH (e.g., topiramate, acetazolamide) is critical.")
        plan.append("Restrict sodium intake.")
        plan.append("Administer thiazide if hypercalciuric.")
        # Simplified check for hypokalemia
        if serum_labs and serum_labs.get("potassium_mEq_L", 0) < 3.5:
            plan.append("Treat hypokalemia if hypocitraturic.")
            plan.append(
                "Consider adding potassium chloride if there is concomitant potassium deficiency to help lower urine pH and increase citrate.")
        # Simplified check for acidosis
        if "Renal Tubular Acidosis" in patient_profile["medical_conditions"] or (serum_labs and serum_labs.get("bicarbonate_mEq_L", 0) < 22):
            plan.append(
                "Treat metabolic acidosis with potassium citrate while avoiding excessive urinary alkalinization.")

    elif stone_type == "Uric Acid":
        plan.append(
            "Focus on raising urine pH to 6.5-7.0 using alkali therapy (potassium citrate or sodium bicarbonate).")
        if "chronic_diarrhea" in patient_profile["medical_conditions"]:
            plan.append("Treat chronic diarrhea if present.")
        plan.append("Advise lower animal protein intake.")
        if "urine_uric_acid" in urine_interpretation and "High urine uric acid" in urine_interpretation["urine_uric_acid"]:
            plan.append(
                "Consider allopurinol if hyperuricosuric and stones persist despite pH normalization.")

    elif stone_type == "Struvite":
        plan.append(
            "Eradication of infection with antibiotics and early surgical removal of bacteria-laden stones are the cornerstones of treatment.")
        plan.append("Increase urine volume.")
        plan.append(
            "Urease inhibitors (e.g., acetohydroxamic acid) may be considered but have side effects.")

    elif stone_type == "Cystine":
        plan.append("Increase urine volume to achieve urine cystine <250 mg/L.")
        plan.append("Restrict dietary sodium.")
        plan.append(
            "Reduce methionine and cystine intake through dietary restriction of animal protein.")
        plan.append("Apply alkali therapy (potassium citrate or sodium bicarbonate) to maintain urine pH between 7.0 and 7.5 to enhance cystine solubility.")
        plan.append("If stones persist despite initial measures, consider thiol drugs (tiopronin, penicillamine, captopril), acknowledging their cost and side effects.")

    elif stone_type == "Drug-induced":
        plan.append("Withdraw the offending medication.")
        plan.append("Increase urine volume.")

    return plan

# --- Streamlit UI Code ---


st.set_page_config(layout="wide")  # Use wide layout for better data display

st.title("Kidney Stone Navigator: Clinical Decision Support & Patient Education")

# Initialize session state variables if not already present
# This ensures that data persists across page changes within the app session
if 'patient_profile' not in st.session_state:
    st.session_state['patient_profile'] = {}
if 'urine_profile' not in st.session_state:
    st.session_state['urine_profile'] = {}
if 'serum_labs' not in st.session_state:
    st.session_state['serum_labs'] = {}

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Patient Profile", "24-Hour Urine Analysis",
                                  "Acute Stone Management", "Chronic Management Plan", "Educational Resources", "Oxalate Content Finder"])

# --- Patient Profile & History Page ---
if page == "Patient Profile":
    st.header("Patient Profile & History")
    st.write("Enter the patient's general information and medical history.")

    with st.form("patient_profile_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120,
                                  value=st.session_state['patient_profile'].get('age', 45))
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=[
                                  "Male", "Female", "Other"].index(st.session_state['patient_profile'].get('gender', 'Female')))
        with col3:
            num_prior_stones = st.number_input(
                "Number of Prior Stone Episodes", min_value=0, value=st.session_state['patient_profile'].get('num_prior_stones', 1))

        first_stone_age = st.number_input("Age of First Stone Episode (if known)", min_value=0, max_value=120,
                                          value=st.session_state['patient_profile'].get('first_stone_age', 28), help="Enter 0 if unknown")
        family_history = st.checkbox("Family history of kidney stones",
                                     value=st.session_state['patient_profile'].get('family_history', False))
        bmi = st.number_input("BMI (kg/m²)", min_value=10.0, max_value=50.0,
                              value=st.session_state['patient_profile'].get('bmi', 25.0))

        st.subheader("Associated Medical Conditions")
        # List common conditions based on the manuscript
        all_medical_conditions = ["Metabolic Syndrome", "Type 2 Diabetes", "Osteoporosis", "Malabsorption (IBD, Bariatric Surgery, etc.)",
                                  "Renal Tubular Acidosis", "Sjögren's Syndrome", "Gout", "Primary Hyperparathyroidism",
                                  "Polycystic Kidney Disease", "Medullary Sponge Kidney", "chronic_diarrhea", "UTI with urease-producing bacteria"]
        medical_conditions = st.multiselect(
            "Select all applicable conditions",
            all_medical_conditions,
            default=st.session_state['patient_profile'].get(
                'medical_conditions', [])
        )

        st.subheader("Current Medications (comma-separated if multiple)")
        medications_text = st.text_area("List current medications (e.g., Topiramate, Hydrochlorothiazide)", value=", ".join(
            st.session_state['patient_profile'].get('medications', [])))
        medications = [m.strip()
                       for m in medications_text.split(',') if m.strip()]

        st.subheader("Dietary Habits")
        fluid_intake = st.number_input("Daily Fluid Intake (L)", min_value=0.5, max_value=5.0,
                                       value=st.session_state['patient_profile'].get('fluid_intake_L', 2.5), step=0.1)

        submitted = st.form_submit_button("Save Patient Profile")
        if submitted:
            st.session_state['patient_profile'] = {
                "age": age,
                "gender": gender,
                "num_prior_stones": num_prior_stones,
                "prior_stones": num_prior_stones > 0,
                "first_stone_age": first_stone_age if first_stone_age > 0 else "unknown",
                "family_history": family_history,
                "bmi": bmi,
                "medical_conditions": medical_conditions,
                "medications": medications,
                "fluid_intake_L": fluid_intake
            }
            st.success("Patient profile saved!")

# --- 24-Hour Urine Analysis Page ---
elif page == "24-Hour Urine Analysis":
    st.header("24-Hour Urine Analysis")
    st.write(
        "Enter the results from the patient's 24-hour urine collection and relevant serum labs.")

    with st.form("urine_analysis_form"):
        st.subheader("24-Hour Urine Profile")
        urine_profile_input = {}
        col_urine1, col_urine2, col_urine3 = st.columns(3)

        with col_urine1:
            urine_profile_input["volume_L"] = st.number_input(
                "Volume (L)", value=st.session_state['urine_profile'].get("volume_L", 2.5), format="%.2f")
            urine_profile_input["ph"] = st.number_input(
                "pH", value=st.session_state['urine_profile'].get("ph", 6.0), format="%.1f")
            urine_profile_input["calcium_mg"] = st.number_input(
                "Calcium (mg)", value=st.session_state['urine_profile'].get("calcium_mg", 200))
            urine_profile_input["oxalate_mg"] = st.number_input(
                "Oxalate (mg)", value=st.session_state['urine_profile'].get("oxalate_mg", 35))

        with col_urine2:
            urine_profile_input["phosphorus_mg"] = st.number_input(
                "Phosphorus (mg)", value=st.session_state['urine_profile'].get("phosphorus_mg", 800))
            urine_profile_input["uric_acid_mg"] = st.number_input(
                "Uric Acid (mg)", value=st.session_state['urine_profile'].get("uric_acid_mg", 600))
            urine_profile_input["sodium_mEq"] = st.number_input(
                "Sodium (mEq)", value=st.session_state['urine_profile'].get("sodium_mEq", 150))
            urine_profile_input["potassium_mEq"] = st.number_input(
                "Potassium (mEq)", value=st.session_state['urine_profile'].get("potassium_mEq", 40))

        with col_urine3:
            urine_profile_input["magnesium_mg"] = st.number_input(
                "Magnesium (mg)", value=st.session_state['urine_profile'].get("magnesium_mg", 60))
            urine_profile_input["sulfate_mmol"] = st.number_input(
                "Sulfate (mmol)", value=st.session_state['urine_profile'].get("sulfate_mmol", 25))
            urine_profile_input["ammonium_mmol"] = st.number_input(
                "Ammonium (mmol)", value=st.session_state['urine_profile'].get("ammonium_mmol", 50))
            urine_profile_input["citrate_mg"] = st.number_input(
                "Citrate (mg)", value=st.session_state['urine_profile'].get("citrate_mg", 350))
            urine_profile_input["cystine_mg"] = st.number_input(
                "Cystine (mg, optional)", value=st.session_state['urine_profile'].get("cystine_mg", 0))

        st.subheader("Relevant Serum Labs (for context)")
        serum_labs_input = {}
        col_serum1, col_serum2, col_serum3 = st.columns(3)
        with col_serum1:
            serum_labs_input["calcium_mg_dL"] = st.number_input(
                "Serum Calcium (mg/dL)", value=st.session_state['serum_labs'].get("calcium_mg_dL", 9.5), format="%.1f")
            serum_labs_input["intact_pth_pg_mL"] = st.number_input(
                "Intact PTH (pg/mL)", value=st.session_state['serum_labs'].get("intact_pth_pg_mL", 30))
        with col_serum2:
            serum_labs_input["bicarbonate_mEq_L"] = st.number_input(
                "Bicarbonate (mEq/L)", value=st.session_state['serum_labs'].get("bicarbonate_mEq_L", 24))
            serum_labs_input["potassium_mEq_L"] = st.number_input(
                "Serum Potassium (mEq/L)", value=st.session_state['serum_labs'].get("potassium_mEq_L", 4.0), format="%.1f")
        with col_serum3:
            serum_labs_input["creatinine_mg_dL"] = st.number_input(
                "Serum Creatinine (mg/dL)", value=st.session_state['serum_labs'].get("creatinine_mg_dL", 0.9), format="%.1f")

        submitted_urine = st.form_submit_button("Analyze Urine")
        if submitted_urine:
            st.session_state['urine_profile'] = urine_profile_input
            st.session_state['serum_labs'] = serum_labs_input

            if not st.session_state['patient_profile']:
                st.warning("Please fill out the 'Patient Profile' first.")
            else:
                st.subheader("24-Hour Urine Interpretation")
                interpretation = interpret_24hr_urine(
                    st.session_state['urine_profile'],
                    st.session_state['patient_profile']
                )

                # Convert interpretation dictionary to DataFrame for better display
                interpretation_data = []
                for param, finding in interpretation.items():
                    interpretation_data.append(
                        {"Parameter": param.replace('_', ' ').title(), "Finding": finding})

                st.table(pd.DataFrame(interpretation_data))

                # Replace matplotlib with a native Streamlit bar chart to reduce bundle size
                st.subheader("Urine Volume: Current vs. Goal")
                # Create data in a linter-friendly way
                data = {'Category': ["Current Volume", "Goal Volume"],
                        'Volume (L)': [st.session_state['urine_profile']['volume_L'], 2.5]}
                chart_df = pd.DataFrame(data).set_index('Category')
                st.bar_chart(chart_df)

# --- Acute Stone Management Page ---
elif page == "Acute Stone Management":
    st.header("Acute Stone Management Guidance")
    st.write("Select the symptoms and known stone size for acute guidance.")

    with st.form("acute_management_form"):
        st.subheader("Current Symptoms")
        uncontrolled_pain = st.checkbox("Uncontrolled Pain", value=False)
        vomiting = st.checkbox("Vomiting", value=False)
        fevers = st.checkbox("Fevers", value=False)
        hydronephrosis = st.checkbox(
            "Hydronephrosis (on imaging)", value=False)
        aki = st.checkbox("Acute Kidney Injury", value=False)
        anuria = st.checkbox("Anuria", value=False)

        st.subheader("Known Stone Size")
        stone_size = st.radio("Select stone size (if known)", [
                              "< 5mm", "5-10mm", "> 10mm", "Unknown"], index=3)

        submitted_acute = st.form_submit_button("Get Acute Guidance")
        if submitted_acute:
            # Logic based on Figure 2 (Acute management of nephrolithiasis flowchart)
            if uncontrolled_pain or vomiting or fevers or hydronephrosis:
                st.info("Consider Admission.")
                if fevers or aki or anuria:
                    st.error("Urgent urology evaluation is required!")
                else:
                    if stone_size == "< 5mm":
                        st.success(
                            "Acute Management: >60% chance of passing. Supportive treatment, Hydration, Strain urine.")
                    elif stone_size == "5-10mm":
                        st.warning(
                            "Acute Management: ~50% chance of passing. Supportive care, Hydration, Medical expulsive therapy (e.g., alpha-blockers for distal stones), Strain urine.")
                    elif stone_size == "> 10mm":
                        st.error(
                            "Acute Management: <25% chance of passing. Urology evaluation, Strain urine.")
                    else:
                        st.info(
                            "Acute Management: Supportive care, Hydration, Strain urine. Consider imaging for size if not done.")
            else:
                st.success("Can likely manage as outpatient.")
                if stone_size == "< 5mm":
                    st.success(
                        "Acute Management: >60% chance of passing. Supportive treatment, Hydration, Strain urine.")
                elif stone_size == "5-10mm":
                    st.warning(
                        "Acute Management: ~50% chance of passing. Supportive care, Hydration, Medical expulsive therapy (e.g., alpha-blockers for distal stones), Strain urine.")
                elif stone_size == "> 10mm":
                    st.error(
                        "Acute Management: <25% chance of passing. Urology evaluation, Strain urine.")
                else:
                    st.info(
                        "Acute Management: Supportive care, Hydration, Strain urine. Consider imaging for size if not done.")

# --- Chronic Management Plan Page ---
elif page == "Chronic Management Plan":
    st.header("Chronic Management Plan")
    st.write("Based on the patient's profile and urine analysis, here's the recommended long-term management.")

    if not st.session_state['patient_profile'] or not st.session_state['urine_profile']:
        st.warning(
            "Please complete 'Patient Profile' and '24-Hour Urine Analysis' first to generate a comprehensive plan.")
    else:
        st.subheader(
            "Confirmed Stone Type (If known, otherwise select most likely)")
        stone_type_options = ["Calcium Oxalate", "Calcium Phosphate",
                              "Uric Acid", "Struvite", "Cystine", "Drug-induced", "Unknown"]
        confirmed_stone_type = st.selectbox(
            "Select the primary stone type", stone_type_options, index=0)  # Default to Calcium Oxalate

        if st.button("Generate Chronic Plan"):
            # Re-run interpretation to ensure it's up-to-date
            interpretation = interpret_24hr_urine(
                st.session_state['urine_profile'], st.session_state['patient_profile'])

            # Pass all necessary data to the management plan function
            management_plan_list = generate_management_plan(
                confirmed_stone_type,
                interpretation,
                st.session_state['patient_profile'],
                st.session_state['serum_labs']
            )

            st.subheader(f"Recommendations for {confirmed_stone_type} Stones:")
            for i, step in enumerate(management_plan_list):
                st.write(f"{i+1}. {step}")

            st.info("Long-term management requires periodic reevaluation of dietary changes and medications on urine indices as well as reassessments of stone burden by imaging (Figure 3).")

# --- Educational Resources Page ---
elif page == "Educational Resources":
    st.header("Educational Resources")
    st.write("Learn more about kidney stone disease.")

    st.subheader("Overview of Kidney Stone Pathogenesis")
    st.write(
        "Kidney stone disease, also known as nephrolithiasis or urolithiasis, is a disorder in which urinary solutes precipitate to form aggregates of crystalline material in the urinary space. The formation is a complex biologic process involving a balance of crystallization inhibitors and promoters, urine volume, and urine pH.")

    # Insert the actual Figure 1 image
    st.image('figure1_pathogenesis.png',
             caption='Figure 1: Overview of Pathogenesis', use_container_width=True)
    st.markdown("---")

    st.subheader("Common Stone Types")
    st.write(
        "The type of stone formed significantly influences management strategies.")

    with st.expander("Calcium Oxalate Stones"):
        st.write(
            "The majority of kidney stones are composed of calcium oxalate. Predisposing factors include low urine volume, hypercalciuria, hypocitraturia, and hyperoxaluria.")
        st.write("**Chronic Management Principles:**")
        st.markdown(
            "- **Increase urine volume** (target $\\sim2.5~L/d$).")
        st.markdown("- **Restrict sodium** ($<2,300~mg/d$).")
        st.markdown(
            "- **Optimize calcium intake** ($1,000-1,200~mg/d$).")
        st.markdown(
            "- Administer **thiazide** if hypercalciuric.")
        st.markdown(
            "- Administer **potassium citrate** if hypocitraturic.")
        st.markdown(
            "- **Oxalate restriction** for significant hyperoxaluria.")
        st.markdown(
            "- **Restrict animal protein** and sucrose/fructose.")

    with st.expander("Calcium Phosphate Stones"):
        st.write(
            "Calcium phosphate stones are less soluble at a higher pH. A major pathophysiologic factor leading to calcium phosphate stone formation is higher urine pH (typically $\\ge6.2$), often with hypocitraturia.")
        st.write("**Chronic Management Principles:**")
        st.markdown(
            "- **Address reversible factors** (e.g., discontinuation of offending medications like topiramate/acetazolamide).")
        st.markdown(
            "- **Increase urine volume** and **restrict sodium**.")
        st.markdown(
            "- Administer **thiazide** if hypercalciuric.")
        st.markdown(
            "- Treat metabolic acidosis with **potassium citrate** while avoiding excessive urinary alkalinization.")
        st.markdown(
            "- Consider **potassium chloride** if concomitant potassium deficiency.")

    with st.expander("Uric Acid Stones"):
        st.write(
            "Uric acid stones are the most common radiolucent stone. Low urine pH (<5.5), low urine volume, and hyperuricosuria are key factors in their pathogenesis.")
        st.write("**Chronic Management Principles:**")
        st.markdown(
            "- **Raise urine pH** to $6.5-7.0$ using alkali therapy (potassium citrate or sodium bicarbonate).")
        st.markdown("- **Increase urine volume**.")
        st.markdown(
            "- Advise **lower animal protein intake**.")
        st.markdown(
            "- Consider **allopurinol** if hyperuricosuric and stones persist despite pH normalization.")

    with st.expander("Struvite Stones (Magnesium Ammonium Phosphate)"):
        st.write(
            "Struvite stones comprise about 1% of all stones and result from chronic urinary tract infection by urease-producing organisms such as Proteus. These can rapidly grow to fill the renal pelvis (staghorn calculi).")
        st.write("**Chronic Management Principles:**")
        st.markdown(
            "- **Eradication of infection** with antibiotics and **early surgical removal** of bacteria-laden stones.")
        st.markdown("- **Increase urine volume**.")
        st.markdown(
            "- Urease inhibitors (e.g., acetohydroxamic acid) may be considered but have significant side effects.")

    with st.expander("Cystine Stones"):
        st.write(
            "Cystinuria is a rare genetic disorder causing kidney stones, accounting for about 1% to 2% of kidney stones in adults and 6% to 8% in children. Cystine is poorly soluble in urine at typical pH.")
        st.write("**Chronic Management Principles:**")
        st.markdown(
            "- **Increase urine volume** to achieve urine cystine $<250~mg/L$.")
        st.markdown("- **Restrict dietary sodium**.")
        st.markdown(
            "- **Reduce methionine and cystine intake** through dietary restriction of animal protein.")
        st.markdown(
            "- Apply **alkali therapy** (potassium citrate or sodium bicarbonate) to maintain urine pH between $7.0$ and $7.5$ to enhance cystine solubility.")
        st.markdown(
            "- If stones persist, consider **thiol drugs** (tiopronin, penicillamine, captopril), acknowledging their cost and side effects.")

    st.subheader("Associated Systemic Conditions")
    st.write(
        "Kidney stones are frequently manifestations of underlying systemic medical conditions such as the metabolic syndrome, genetic disorders, or endocrinopathies. They are associated with increased risk of chronic kidney disease (CKD), cardiovascular disease, and reduced bone mineral density.")
    st.markdown(
        "- **Metabolic Syndrome/Type 2 Diabetes:** Linked to uric acid and calcium oxalate stones due to acidic urine and other metabolic derangements.")
    st.markdown(
        "- **Osteoporosis/Bone Health:** The skeleton can be a source of excessive urinary calcium.")
    st.markdown(
        "- **Malabsorption Syndromes (e.g., Crohn's, Gastric Bypass, Celiac, Cystic Fibrosis):** Predispose to calcium oxalate stones (enteric hyperoxaluria).")
    st.markdown(
        "- **Renal Tubular Acidosis (RTA) & Sjögren's Syndrome:** Can lead to calcium phosphate stones due to high urine pH.")
    st.markdown(
        "- **Gout:** Almost doubles the risk of nephrolithiasis, often linked to metabolic syndrome.")
    st.markdown(
        "- **Primary Hyperparathyroidism:** Causes hypercalcemia and hypercalciuria, leading to calcium stones.")

    st.subheader("External Resources")
    st.markdown("[Recurrence of Kidney Stone (ROKS) nomogram](https://www.qxmd.com/calculate/calculator_438/roks-recurrer-of-kidney-stone-2018)")
    st.markdown("[Kidney Stone Pathophysiology, Evaluation and Management: Core Curriculum 2023](https://www.ajkd.org/article/S0272-6386(23)00670-4/fulltext)")

# --- Oxalate Content Finder Page ---
elif page == "Oxalate Content Finder":
    st.header("Oxalate Content Finder")
    st.write(
        "Search for the oxalate content of various foods. Data is loaded from a local file.")

    @st.cache_data
    def get_oxalate_data():
        try:
            import json
            with open('oxalate_en.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            food_data_list = data.get('food_data', [])
            return pd.DataFrame(food_data_list)
        except Exception as e:
            st.error(f"Error loading or parsing oxalate data: {e}")
            return pd.DataFrame()

    oxalate_df = get_oxalate_data()

    if not oxalate_df.empty:
        search_term = st.text_input("Search for a food item or category:", "")

        if search_term:
            results = oxalate_df[oxalate_df['food'].str.contains(
                search_term, case=False) | oxalate_df['type'].str.contains(search_term, case=False)]
            if not results.empty:
                st.write(
                    f"Found {len(results)} matching items for '{search_term}':")
                st.dataframe(results)
            else:
                st.warning(f"No results found for '{search_term}'.")
        else:
            st.info(
                "Enter a food item or category to search for its oxalate content.")
            st.write("Full Oxalate Database:")
            st.dataframe(oxalate_df)

    st.subheader("External Resources")
    st.markdown("[University of Chicago Kidney Stone Center: How to Eat a Low Oxalate Diet](https://kidneystones.uchicago.edu/how-to-eat-a-low-oxalate-diet/)")


# About / Disclaimer in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("**About This App:**")
st.sidebar.info("Developed by a Nephrology Professor and Data Scientist for educational and clinical decision support based on the AJKD Core Curriculum 2023 on Kidney Stone Pathophysiology, Evaluation, and Management. This app is for informational purposes only and does not substitute professional medical advice.")
