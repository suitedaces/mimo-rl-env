## Feature request: heading-pitch-roll transforms using aircraft (NED) convention

I'm building a flight / UAV visualization on top of Cesium. Most of my pose data comes from autopilot logs and flight simulators, where heading / pitch / roll are defined in the standard aviation way — i.e. relative to a **North-East-Down** local frame at the aircraft's position (heading rotates about the local Down axis, pitch about local East, roll about local North).

I tried to drive a model's `modelMatrix` with the existing helpers:

```js
var origin  = Cesium.Cartesian3.fromDegrees(lon, lat, alt);
var heading = aircraft.heading; // from sim, defined in NED
var pitch   = aircraft.pitch;
var roll    = aircraft.roll;

var m = Cesium.Transforms.headingPitchRollToFixedFrame(origin, heading, pitch, roll);
// also tried Cesium.Transforms.headingPitchRollQuaternion(...)
```

The orientation that comes out doesn't match what the aircraft is actually doing. After staring at it for a while I realized the existing `headingPitchRollToFixedFrame` / `headingPitchRollQuaternion` interpret the angles relative to a local **East-North-Up** frame, which is a different convention from what aviation / autopilot data uses. So the same numeric (heading, pitch, roll) triple means different physical rotations in the two conventions, and feeding aircraft-convention values into the ENU-based helper gives the wrong attitude.

Right now, to get correct attitude I have to roll my own helper on top of `Transforms.northEastDownToFixedFrame` and manually build the rotation from heading/pitch/roll, which feels like something the library should expose directly — especially since the ENU-based versions are already there.

### Ask

Could `Transforms` provide companions to the existing heading/pitch/roll helpers that interpret the angles using the aviation (NED) convention? Concretely, I'd like to be able to write something like:

```js
var origin = Cesium.Cartesian3.fromDegrees(lon, lat, alt);

// 4x4 world transform from aircraft-convention HPR
var transform = /* aircraft-HPR -> fixed frame */(origin, heading, pitch, roll);

// and a quaternion form, mirroring the existing ENU pair
var q = /* aircraft-HPR -> quaternion */(origin, heading, pitch, roll);
```

so that anyone consuming flight / drone telemetry can convert directly to a world-space transform without having to re-derive the NED axis swap themselves. Defaults should match the rest of `Transforms` (WGS84 ellipsoid, optional `result` out-param).

The names I'd expect for these new helpers are something like `aircraftHeadingPitchRollToFixedFrame` and `aircraftHeadingPitchRollQuaternion`, mirroring the existing `headingPitchRoll*` pair.
