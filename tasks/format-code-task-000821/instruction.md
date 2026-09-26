Mutli-label text classification export issues: same classes but in different orders
How to reproduce the behaviour
---------
<!-- Before submitting an issue, make sure to check the docs and closed issues and FAQ to see if any of the solutions work for you. https://github.com/doccano/doccano/wiki/Frequently-Asked-Questions -->
We are two annotators on a multi-label classification project. When I export the annotations, for some examples, me and my co-annotator have put the same labels, but on the exported CSV, they do not appear in the same order:

Annotator 1:

| text | labels |
| example 1 | label1#label2#label3 |

Annotator 2:

| text | labels |
| example 1 | label2#label3#label1 |

As I try to use these CSVs for comparing our annotations, this brings more difficulty.

<!-- Include a code example or the steps that led to the problem. Please try to be as specific as possible. -->

Your Environment
---------
<!-- Include details of your environment.-->
*   Operating System: Debian
*   Python Version Used: Don't know, I pulled the latest version from Docker Hub
*   When you install doccano: 3 days ago
*   How did you install doccano (Heroku button etc): Docker
