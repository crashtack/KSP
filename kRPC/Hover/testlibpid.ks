clearscreen.
set seekAlt to 15.
set done to false.
on ag9 { set done to true. }.

print "A simple test of libpid.".
print "Does a hover script at " + seekAlt + "m AGL.".
print " ".
print "  Try flying around with WASD while it hovers.".
print "  (steering is unlocked. under your control.".
print " ".
print "  Keys:".
print "     Action Group 1 : lower hover altitude".
print "     Action Group 2 : raise hover altitude".
print "     LANDING LEGS   : Deploy to exit script".
print " ".
print " Seek ALT_RADAR = ".
print "  Cur ALT_RADAR = ".
print "    1G Throttle = ".
print "Throttle offset = ".
print " total throttle = ".

// load the functions I'm using:
run lib_physics.
run lib_pid.

on ag1 { set seekAlt to seekAlt - 1. preserve. }.
on ag2 { set seekAlt to seekAlt + 1. preserve. }.

set ship:control:pilotmainthrottle to 0.

// hit "stage" until there's an active engine:
until ship:availablethrust > 0 {
  wait 0.5.
  stage.
}.

// Call to update the display of numbers:
declare function display_block {
  declare parameter
    startCol, startRow. // define where the block of text should be positioned

  print round(seekAlt,2) + "m    " at (startCol,startRow).
  print round(alt_radar,2) + "m    " at (startCol,startRow+1).
  print round(midThrottle,3) + "      " at (startCol,startRow+2).
  print round(thOffset,3) + "      " at (startCol,startRow+3).
  print round(throttle,3) + "      " at (startCol,startRow+4).
}.

// midThrottle is the throttle setting that would exactly
// hover against gravity:
lock midThrottle to Fg_here()/ship:availablethrust.

// thOffset is how far off from midThrottle to be.
// It's the value I'll be letting the PID controller
// adjust for me.
set thOffset to 0.

lock throttle to midThrottle + thOffset.

set hoverPID to pid_init( 0.02, 0.05, 0.05 ). // Kp, Ki, Kd vals.

gear on.  gear off. // on then off because of the weird KSP 'have to hit g twice' bug.

until gear {
  set thOffset to pid_seek( hoverPID, seekAlt, alt_radar ).
  display_block(18,11).
  wait 0.001.
}.

set ship:control:pilotmainthrottle to throttle.
print "------------------------------".
print "Releasing control back to you.".
print "------------------------------".

