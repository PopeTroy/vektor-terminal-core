import json
import sys
import datetime

def run_resonant_audit(avg_g_force):
    try:
        g_force = float(avg_g_force)
    except:
        g_force = 1.25 # Calibration default
    
    # Logic for 51.8° Bridge
    if g_force >= 1.2:
        surface, slope, status, hz = "STONE", 51.8, "LOCKED", 144000
    elif g_force >= 0.4:
        surface, slope, status, hz = "WOOD", 32.4, "DRIFT", 0
    else:
        surface, slope, status, hz = "SOFT/HAND", 0.0, "DAMPENED", 0

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

    # Ensure the file is written with perfect structure
    with open('vektor-manifest.json', 'w') as f:
        json.dump(audit_result, f, indent=2)
    
    print("CORE MANIFEST WRITTEN SUCCESSFULLY")

if __name__ == "__main__":
    input_g = sys.argv[1] if len(sys.argv) > 1 else 1.25
    run_resonant_audit(input_g)
