import json
import sys
import datetime

def run_resonant_audit(avg_g_force):
    try:
        g_force = float(avg_g_force)
    except:
        g_force = 0.0
    
    # UESP PRCE Surface Diagnostic Thresholds
    if g_force >= 1.2:
        surface = "STONE"
        slope = 51.8
        status = "LOCKED"
        hz = 144000
    elif g_force >= 0.4:
        surface = "WOOD"
        slope = 32.4
        status = "DRIFT"
        hz = 0
    else:
        surface = "SOFT/HAND"
        slope = 0.0
        status = "DAMPENED"
        hz = 0

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

    with open('vektor-manifest.json', 'w') as f:
        json.dump(audit_result, f, indent=2)
    
    print(f"Audit Complete: {surface} Detected")

if __name__ == "__main__":
    input_g = sys.argv[1] if len(sys.argv) > 1 else 0.0
    run_resonant_audit(input_g)
