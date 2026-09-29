def triage_symptoms(
    symptoms,
    species="Other",
):
    """
    Simple offline symptom-support engine.

    This does not replace veterinary examination.
    It identifies health patterns from entered observations.
    """

    text = symptoms.lower().strip()

    conditions = []

    # ---------------------------------------------------------
    # Foot-and-Mouth Disease
    # ---------------------------------------------------------

    fmd_words = [
        "mouth sore",
        "mouth sores",
        "salivation",
        "drooling",
        "foot sore",
        "lameness",
        "blister",
        "blisters",
        "mouth blister",
    ]

    if any(
        word in text
        for word in fmd_words
    ):
        conditions.append(
            "Foot-and-Mouth Disease"
        )

    # ---------------------------------------------------------
    # Lumpy Skin Disease
    # ---------------------------------------------------------

    lsd_words = [
        "skin lump",
        "skin lumps",
        "skin nodule",
        "skin nodules",
        "nodules",
        "lumps",
        "skin lesions",
    ]

    if any(
        word in text
        for word in lsd_words
    ):
        conditions.append(
            "Lumpy Skin Disease"
        )

    # ---------------------------------------------------------
    # PPR
    # ---------------------------------------------------------

    ppr_words = [
        "diarrhea",
        "diarrhoea",
        "nasal discharge",
        "mouth discharge",
        "cough",
    ]

    if (
        species in ["Goat", "Sheep"]
        and any(
            word in text
            for word in ppr_words
        )
    ):
        conditions.append(
            "PPR"
        )

    # ---------------------------------------------------------
    # Heat Stress
    # ---------------------------------------------------------

    heat_words = [
        "panting",
        "heavy breathing",
        "heat",
        "heat stress",
        "weakness",
        "excessive sweating",
    ]

    if any(
        word in text
        for word in heat_words
    ):
        conditions.append(
            "Heat Stress"
        )

    # ---------------------------------------------------------
    # General status
    # ---------------------------------------------------------

    if not text:
        risk = "Please enter the animal's observations."

    elif len(conditions) >= 2:
        risk = "Multiple health signs need attention."

    elif len(conditions) == 1:
        risk = "Health signs need attention."

    else:
        risk = "No specific health pattern found."

    # ---------------------------------------------------------
    # Care suggestions
    # ---------------------------------------------------------

    precautions = [
        "Keep the affected animal under observation.",
        "Provide clean drinking water.",
        "Keep housing and feeding areas clean.",
        "Avoid unnecessary movement of visibly sick animals.",
        "Watch appetite, movement, breathing and behaviour.",
        "Contact a veterinary professional if symptoms continue or worsen.",
    ]

    return {
        "risk": risk,
        "possible_conditions": conditions,
        "precautions": precautions,
        "vet_advice": (
            "Share the animal's observations with "
            "a veterinary professional for further assessment."
        ),
    }