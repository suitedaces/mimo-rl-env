## Exception inside a tag block leaves the tag unclosed

I'm writing an Erector widget where the block passed to a tag calls into some helper code that can raise. Something like:

```ruby
class MyPage < Erector::Widget
  def content
    p do
      some_helper_that_might_raise
    end
  end
end
```

When `some_helper_that_might_raise` actually raises, I catch the exception further up the stack so I can still inspect / log whatever HTML was emitted so far. The problem is that the partial output is malformed: the opening `<p>` is in there, but there's no matching `</p>`. The internal indentation state also seems to be off after the failure — subsequent tags rendered by the same widget look like they're nested one level too deep.

I'd expect that even if the block raises, the tag that was opened still gets closed before the exception propagates out, so the emitted HTML stays balanced at the tag level (the caller can then decide what to do with the exception). Right now the close tag is just silently dropped whenever the block doesn't return normally, which makes the output unusable for any kind of "render partial result on failure" or just for diagnosing what happened.

This affects all the regular full tags (`div`, `p`, `span`, etc., since they all go through the same code path).
