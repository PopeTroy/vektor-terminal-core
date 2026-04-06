import json
import sys
import datetime

def run_resonant_audit(avg_g_force):
    """
    UESP PRCE Surface Diagnostic
    Thresholds:
    - < 0.4G: DAMPENED (Hand/Soft)
    - 0.4G - 1.2G: ABSORBED (Wood/Porous)
    - > 1.2G: REFLECTED (Stone/Granite - Giza Constant)
    """
    g_force = float(avg_g_force)
    
    # Logic to determine Surface Type and Slope
    if g_force >= 1.2:
        surface = "STONE"
        slope = 51.8
        status = "LOCKED"
        hz = 144000
    elif g_force >= 0.4:
        surface = "WOOD"
        slope = 32.4
        status = "DRIFT"
        hz = "UNSTABLE"
    else:
        surface = "SOFT/HAND"
        slope = 0.0
        status = "DAMPENED"
        hz = "OFFLINE"

    audit_result = {
        "terminal_id": f"VEKTOR-{surface}-{datetime.datetime.now().strftime('%M%S')}",
        "operator": "PopeTroy",
        "kinetic_data": {
            "input_g_force": g_force,
            "detected_surface": surface,
            "vector_slope": slope
        },
        "resonance": {
            "bridge_status": status,
            "frequency_lock": hz
        },
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

    # Write to the Manifest for the HUD to fetch
    with open('vektor-manifest.json', 'w') as f:
        json.dump(audit_result, f, indent=2)
    
    print(f"Audit Complete: {surface} Detected | Status: {status}")

if __name__ == "__main__":
    # Get G-force from GitHub Action argument
    input_g = sys.argv[1] if len(sys.argv) > 1 else 0.0
    run_resonant_audit(input_g)
