Visuals of time_picker selection don't always match passed argument
### Discussed in https://github.com/h2oai/wave/discussions/1888

<div type='discussions-op-text'>

<sup>Originally posted by **aranvir** March 14, 2023</sup>
Hi! First of all, I really enjoy working with this framework and exploring this.

I found an issue that can be best reproduced with the time_picker https://wave.h2o.ai/docs/examples/time-picker

When selecting the required time, one needs to explicitly click on the the hour and the minutes to set a proper time. If, for example, you just click on 12 (which auto-completes to 12:00) and then click on the white space around, the value will be displayed BUT when you click Submit, the time passed is actually `None`.

So this is of course a bit counter-intuitive because you see the time you wanted to enter, but it is then not actually set. I assume the same will happen for other "multi-stage" pickers where implicit values are not considered a confirmation of the form input, but I haven't tested it.

Not sure, if this can be solved programmatically or if this is just "how forms work". If it's the latter then I think this is something that should be mentioned in the documentation so frontend noobs like me are not caught by surprise ;)</div>

via @aranvir
