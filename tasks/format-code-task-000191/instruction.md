## Analysis doesn't catch dispense-without-aspirate

I wrote a quick protocol and noticed that the analysis step happily accepts it even though it clearly doesn't make sense — I'm dispensing without ever aspirating. Reproducer:

```python
requirements = {
    "robotType": "OT-2",
    "apiLevel": "2.15",
}


def run(protocol_context):
    tiprack1 = protocol_context.load_labware("opentrons_96_tiprack_300ul", "1")
    pipette = protocol_context.load_instrument(
        "p300_single_gen2", mount="right", tip_racks=[tiprack1]
    )
    pipette.pick_up_tip(tiprack1.wells()[0])
    well_plate = protocol_context.load_labware("nest_96_wellplate_200ul_flat", "2")
    # note: no aspirate here
    pipette.dispense(20, well_plate.wells()[0])
```

The pipette never aspirated anything, so dispensing 20 µL out of an empty tip is nonsense. I'd expect analysis to reject the protocol up front so I can fix the script before sending it to the robot, instead of silently passing.

Same concern for the case where the requested dispense volume is greater than what was previously aspirated — there's no liquid in the tip to support that dispense, so analysis should refuse it as well.

Both situations are statically detectable from the command sequence and should fail analysis with a clear error for protocols on `apiLevel` 2.15+. A dedicated error type along the lines of `InvalidDispenseVolumeError` would be appropriate here.
