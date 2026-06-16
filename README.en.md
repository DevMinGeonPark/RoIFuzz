[한국어](README.md) | English

# RoIFuzz — A ROS 2 IDL Fuzzer That Runs With Security Policies Enabled

A fuzzer for testing ROS 2 robotic systems. What sets it apart from a typical fuzzer is that it
mutates messages at the IDL type level while SROS 2 security policies are enforced. Coverage
feeds back into how the next inputs are generated.

Presentation: oral talk at the Conference on Information Security and Cryptography,
"RoIFuzz: A Study on a ROS IDL Fuzzer Applying Reinforced Robot Security Policies."
Built on RoboFuzz (FSE '22, https://dl.acm.org/doi/10.1145/3540250.3549164).

## Why I built it

Robotics fuzzers usually test nodes in an open setup with security turned off. But real
deployments run on SROS 2, which adds authentication, encryption, and access control at the DDS
layer. That raises a question: does a robotic program still behave correctly when it is fuzzed
under an enforced security policy? RoIFuzz fuzzes the ROS IDL interface with that security layer
left on.

## What it does

- Mutates every ROS 2 IDL type, from primitives like Bool, Byte, Char, Float32/64, and Int8 to
  Fixed / Bounded / Unbounded arrays (watchlist/idltest.json, librcl_apis/).
- Brings the target up under SROS 2 access-control policies (policies/sros2_node.policy.xml and
  others).
- Drives the campaign with coverage and state feedback (coverage/, feedback.py).
- Uses per-system oracles for PX4 (drone autopilot), TurtleBot, and MoveIt (oracles/) to catch
  semantic bugs, not just crashes.
- Actually runs PX4 SITL missions (takeoff, waypoint flight) through a PX4-ROS-MAVLink bridge.

## Structure

```
fuzzer.py     main loop: mutate IDL messages, publish, observe results
mutator.py    IDL type-aware mutation
scheduler.py  campaign and seed scheduling
executor.py   launch and drive the ROS 2 / PX4 target
feedback.py   coverage and state feedback
oracles/      px4.py, turtlebot.py, moveit.py
policies/     SROS 2 security policies enforced during fuzzing
missions/     PX4 flight scenarios
```

## Requirements and run

You need ROS 2 and SROS 2, PX4 (SITL), and Python 3. Install dependencies with
`pip install -r requirements.txt`.

```bash
python fuzzer.py     # see config.py and constants.py for target and campaign settings
```

This is security research code that extends RoboFuzz with IDL-level mutation and SROS 2 policy
enforcement.
