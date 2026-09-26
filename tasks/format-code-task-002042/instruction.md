AttributeError crash if shortcut cmd is undefined
If one tries to create a shortcut with an empty cmd it fails with the message `AttributeError: 'NoneType' object has no attribute 'split'`. 

    cmd = shutil.which("my-script")    # not in PATH, so returns nothing
    scut = make_shortcut(cmd, name="My Script", icon=iconpath)

It could be more explicit about what's wrong. I'm not sure where's best place to put an error message, or very clear on the best practice for how.
