"""
Business logic services for kidney stone analysis and management
Migrated from the original Streamlit app
"""


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


def get_acute_management_guidance(symptoms, stone_size):
    """
    Provides acute management guidance based on symptoms and stone size.
    """
    guidance = {
        'admission_needed': False,
        'urgency_level': 'routine',
        'recommendations': []
    }

    # Check for severe symptoms requiring admission
    severe_symptoms = symptoms.get('uncontrolled_pain', False) or symptoms.get(
        'vomiting', False) or symptoms.get('fevers', False) or symptoms.get('hydronephrosis', False)

    if severe_symptoms:
        guidance['admission_needed'] = True
        guidance['recommendations'].append("Consider Admission.")

        # Check for urgent symptoms
        urgent_symptoms = symptoms.get('fevers', False) or symptoms.get(
            'aki', False) or symptoms.get('anuria', False)
        if urgent_symptoms:
            guidance['urgency_level'] = 'urgent'
            guidance['recommendations'].append(
                "Urgent urology evaluation is required!")
        else:
            guidance['urgency_level'] = 'moderate'
    else:
        guidance['recommendations'].append("Can likely manage as outpatient.")

    # Add stone size specific guidance
    if stone_size == "< 5mm":
        guidance['recommendations'].append(
            "Acute Management: >60% chance of passing. Supportive treatment, Hydration, Strain urine.")
    elif stone_size == "5-10mm":
        guidance['recommendations'].append(
            "Acute Management: ~50% chance of passing. Supportive care, Hydration, Medical expulsive therapy (e.g., alpha-blockers for distal stones), Strain urine.")
    elif stone_size == "> 10mm":
        guidance['recommendations'].append(
            "Acute Management: <25% chance of passing. Urology evaluation, Strain urine.")
    else:
        guidance['recommendations'].append(
            "Acute Management: Supportive care, Hydration, Strain urine. Consider imaging for size if not done.")

    return guidance
