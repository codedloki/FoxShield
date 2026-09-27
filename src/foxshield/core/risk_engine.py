# core/risk_engine.py

def calculate_risk_score(pii_entities: list, context_status: str, file_type: str = "municipal") -> dict:
    """
    Calculates forensic risk score (0-100) and Estimated Financial Exposure (DPDP Act 2023).
    """
    
    # 1. Severity Weights for Risk Score
    SEVERITY_WEIGHTS = {
        "AADHAAR_NUMBER": 30, "PAN_CARD": 30, "PASSWORD": 30, "CREDIT_CARD": 30,
        "PHONE_NUMBER": 15, "EMAIL_ADDRESS": 15, "US_SSN": 20,
        "PERSON": 5, "LOCATION": 5, "IP_ADDRESS": 10, "DATE_TIME": 2
    }

    # 2. Per-Record Financial Weights (DPDP Act/GDPR Penalty per record in INR)
    FINANCIAL_WEIGHTS = {
        "AADHAAR_NUMBER": 10000, "PAN_CARD": 5000, "PASSWORD": 15000, "CREDIT_CARD": 20000,
        "PHONE_NUMBER": 2000, "EMAIL_ADDRESS": 1000, "US_SSN": 10000,
        "PERSON": 500, "LOCATION": 500, "IP_ADDRESS": 1000, "DATE_TIME": 100
    }

    # 3. BASE PENALTY (DPDP Act Schedule - Fixed for data breach by entity type)
    BASE_PENALTIES = {
        "municipal": 5000000,      # ₹50 Lakhs
        "healthcare": 10000000,    # ₹1 Crore
        "financial": 10000000,     # ₹1 Crore
        "private": 500000          # ₹5 Lakhs
    }
    
    base_penalty = BASE_PENALTIES.get(file_type, 500000)

    base_score = 0
    per_record_penalty = 0
    severity_breakdown = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}

    for entity in pii_entities:
        entity_type = entity.get("entity_type", "UNKNOWN")
        
        # Risk Score Calculation
        weight = SEVERITY_WEIGHTS.get(entity_type, 5)
        base_score += weight
        
        # Financial Exposure Calculation
        fin_weight = FINANCIAL_WEIGHTS.get(entity_type, 500)
        per_record_penalty += fin_weight
        
        # Categorize for breakdown
        if weight >= 30: severity_breakdown["Critical"] += 1
        elif weight >= 15: severity_breakdown["High"] += 1
        elif weight >= 5: severity_breakdown["Medium"] += 1
        else: severity_breakdown["Low"] += 1

    # 4. Apply Context Multiplier
    if context_status == "LEAK":
        risk_multiplier = 1.5
        fin_multiplier = 1.0   # Full Liability
    elif context_status == "REVIEW":
        risk_multiplier = 1.0
        fin_multiplier = 0.5   # ️ FIXED: 50% Liability for Review (Not Zero!)
    else: # SAFE (RTI)
        risk_multiplier = 0.2
        fin_multiplier = 0.0   # No Penalty for Legal Disclosure

    final_score = min(100, int(base_score * risk_multiplier))
    total_exposure = int((base_penalty + per_record_penalty) * fin_multiplier)

    # 5. Determine Risk Level
    if final_score >= 75: risk_level, color = "CRITICAL", "red"
    elif final_score >= 50: risk_level, color = "HIGH", "orange"
    elif final_score >= 25: risk_level, color = "MEDIUM", "yellow"
    else: risk_level, color = "LOW", "green"

    return {
        "score": final_score,
        "level": risk_level,
        "color": color,
        "breakdown": severity_breakdown,
        "base_score": base_score,
        "multiplier_applied": risk_multiplier,
        "financial_exposure": {
            "base_penalty": base_penalty,
            "per_record_penalty": per_record_penalty,
            "total_exposure": total_exposure
        }
    }