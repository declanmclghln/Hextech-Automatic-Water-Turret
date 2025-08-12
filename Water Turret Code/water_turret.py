import time
from hextech_updated import HexTechMuscle, Microsteps

# --- Tweak these if needed ---
PRIME_SECONDS   = 6.0     # long initial fill; set 0 to skip
SPRAY_SECONDS   = 1.5     # pump time each cycle
STEP_SIZE       = 750      # motor steps per move (small = safer)
CYCLES_EACH_WAY = 3       # few cycles forward, then back
SPEED           = 600     # slow
MICRO           = Microsteps.MS_16
COOLDOWN        = 0.4     # pause after every command
# -----------------------------

m = HexTechMuscle(verbose=True)

# Keep serial lines steady (some boards reset when these toggle)
try:
    m.conn.dtr = False
    m.conn.rts = False
except:
    pass

stp = m.stepper0
# Minimal setup, with generous gaps
stp.set_microsteps(MICRO).run(); time.sleep(COOLDOWN)
stp.set_speed(SPEED).run();      time.sleep(COOLDOWN)

def pump_for(seconds: float):
    m.dc.move(1500).run(); time.sleep(COOLDOWN)   # start
    time.sleep(seconds)                            # run
    m.dc.stop().run();          time.sleep(COOLDOWN)

try:
    # Optional long prime so the hose actually fills
    if PRIME_SECONDS > 0:
        print(f"Priming for {PRIME_SECONDS}s…")
        pump_for(PRIME_SECONDS)
        time.sleep(COOLDOWN)

    print("Forward cycles…")
    for i in range(CYCLES_EACH_WAY):
        print(f"Cycle F{i+1}")
        pump_for(SPRAY_SECONDS)                    # spray
        stp.move(STEP_SIZE, stealth=True).run()    # small move
        time.sleep(COOLDOWN + 0.4)                 # extra settle

    print("Backward cycles…")
    for i in range(CYCLES_EACH_WAY):
        print(f"Cycle B{i+1}")
        pump_for(SPRAY_SECONDS)
        stp.move(-STEP_SIZE, stealth=True).run()
        time.sleep(COOLDOWN + 0.4)

    print("Done.")

finally:
    # Safety off
    try: m.dc.stop().run()
    except: pass
    try: stp.stop().run()
    except: pass