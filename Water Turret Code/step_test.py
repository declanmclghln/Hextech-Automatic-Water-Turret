# turret_sweep_calibrate.py
import time
from hextech_updated import HexTechMuscle, Microsteps

# ===== CONFIG =====
STEPPER = "stepper0"
MOTOR_STEPS_PER_REV = 200     # most NEMA17
MICROSTEPS = Microsteps.MS_16 # change to match your driver setting
GEAR_RATIO = 3.0              # motor revs per turret rev
TARGET_DEGREES = 270          # desired sweep angle

SPEED = 1200
ACCEL = 600
RMS_CURRENT = 600
STEALTH = True
DWELL_AT_ENDS = 0.5
# ==================

def steps_per_degree(motor_steps, microsteps, gear_ratio):
    return (motor_steps * int(microsteps) * gear_ratio) / 360.0

def main():
    muscle = HexTechMuscle(verbose=True)
    stp = getattr(muscle, STEPPER)

    # Motor setup
    stp.set_speed(SPEED).run()
    stp.set_acceleration(ACCEL).run()
    stp.set_current(RMS_CURRENT).run()
    stp.set_microsteps(MICROSTEPS).run()

    spd = steps_per_degree(MOTOR_STEPS_PER_REV, MICROSTEPS, GEAR_RATIO)
    target_steps = int(round(TARGET_DEGREES * spd))
    print(f"steps/deg ≈ {spd:.3f} → {TARGET_DEGREES}° = {target_steps} steps")

    try:
        while True:
            print(f"→ to {TARGET_DEGREES}°")
            stp.go(target_steps, stealth=STEALTH).run()
            time.sleep(DWELL_AT_ENDS)

            print("← back to 0°")
            stp.go(0, stealth=STEALTH).run()
            time.sleep(DWELL_AT_ENDS)

    except KeyboardInterrupt:
        print("\nStopping…")
        stp.stop().run()
        print("Done.")

if __name__ == "__main__":
    main()