Scripting string splits with newline separator
Hi,

Really enjoying using this so far, and am now digging more into some advanced scripting to get some cleaner metadata out of the YouTube exports. I have a sub for which I only want to save the first line of the description. 

This seems like it should be possible with the scripting functions, but I'm probably making a rookie error. I've got this as the overrides of my custom preset:


>     overrides:
>       description_to_array: >-
>         {
>           %split(description, "\n")
>         }
>       first_line_of_description: >-
>         {
>           %array_at(description_to_array, 0)
>         }
>       episode_plot: "{first_line_of_description}"

Which just returns the entire description, seemingly not having split it at all. Escaping the newline character doesn't appear to work either, and as far as I'm aware looking at the underlying code of ytdl-sub, you're wrapping the basic python string split function to do this, which should accept something in the form of str.split('\n').

Thanks for any advice you can give.
