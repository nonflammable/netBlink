# netBlink ulity
Simple tool to get Raspberry Pi IP address without network scaner, just by blinking it by onboard ACK_LED (mmc led).

It's easy to setup by just running one python executable. 

**Service will start about a minute after powering on and run every minute in first ten minutes of uptime.** Ulity will send only last octet of address i just assume that you know anything else (its possible to change that by commenting marked line in setup.py).


Note that only that part of address is transmitted by default:

|  192 |  168 |  88 |103  |
| ------------ | ------------ | ------------ | ------------ |
|   |   |   | default





## Instalation

`$  git clone https://github.com/Laczekdev/netBlink.git`

`$ cd netBlink`

`$ sudo python3 setup.py`

## How to decode 
> I tried to make its easy human readable.

> I said "I tried"

First to indicate starting transmission it will turn off diode complitly for 2 seconds, then light it up for same time. 

In transmition default state is on, and sum of fast blinks (0.3sec off) means one number. After every number diode stay on (1.5 sec on) and start next number.  If you get long off blink (1 sec off) that indicate that this number is 0.

I know that it's sound difficult but most persons (almost 4 of 5) decode it at first try.

## Example 

**.125** (fast 1 blink)(1 second on)(fast 2 blink)(1 second on)(fast 5 blink)

**.102** (fast 1 blink)(1 second on)(1 second off)(1 second on)(fast 2 blink)

**.100** (fast 1 blink)(1 second on)(1 second off)(1 second on)(1 second off)

**.1** (fast 1 blink)(1 second on)

If raspberry don't have an Ip address it will blink "404".
After finished transmision diode returns to default mode (disk usage indication).

**~! Remember that "0" is 1 second off led state!**


## Checked Compability
- Raspberry Pi 3 B+
- Raspberry Pi 3 B
- Raspberry Pi Zero
- Raspberry Pi Zero W

**Should work on every raspberry Pi**
## Disabling 
`$   sudo systemctl disable netblink.service`
