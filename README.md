Run from inside rev shell or ssh on server - that will bypass werkzeug's lockout for 10 failed attempts

Usage: nohup python3 /tmp/pinbuster.py > /tmp/pinbuster.out 2>&1 &
disown

if killed or dies, will restart from last pin tested

test progress via tail: tail -f /tmp/pinbuster.out

adjust script for threads through: MAX_THREADS = 10  (default = 5)
