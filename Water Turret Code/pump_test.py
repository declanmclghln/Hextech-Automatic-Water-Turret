from hextech_updated import HexTechMuscle
import time

# How long the DC channel is allowed to run (big number so it won't auto-stop)
DC_LONG_SECONDS = 9999

m = HexTechMuscle(verbose=True)

# Prevent auto-reset on some boards
try:
    m.conn.dtr = False
    m.conn.rts = False
except Exception:
    pass

print("Starting pump… Press <Enter> when water begins flowing.")
m.dc.move(DC_LONG_SECONDS).run()

try:
    input()  # Wait for user to confirm water flow
finally:
    print("Stopping pump…")
    m.dc.stop().run()
    time.sleep(0.5)
    print("Pump OFF. Done.")