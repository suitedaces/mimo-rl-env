Security history IP Addresses include 127.0.0.1
<!--
    NOTE: This issue should be for problems with PyPI itself, including:
    * pypi.org
    * test.pypi.org
    * files.pythonhosted.org

    This issue should NOT be for a project installed from PyPI. If you are
    having an issue with a specific package, you should reach out to the
    maintainers of that project directly instead.

    Furthermore, this issue should NOT be for any non-PyPI properties (like
    python.org, docs.python.org, etc.)

    If your problem is related to search (a new or updated project doesn't
    appear in the PyPI search results), please wait for a couple of hours
    and check again before reporting it. The search index may take some
    time to be updated.
-->

**Describe the bug**
In the security history under https://pypi.org/manage/account/, the IP addresses which generated the event are listed. This includes mine (starting "2a02"), and what must be the PyPI server, as shows "Redacted". 

However, the event for them email telling me a project of mine has been marked as critical has the IP address 127.0.0.1 (i.e. localhost). 
It's not a problem, just surprising to see, and it might confuse somebody.

**Expected behavior**
For consistency the 127.0.0.1 IP address shows instead as "Redacted", or marked in some other way that it was the PyPI server itself.

**To Reproduce**
https://pypi.org/manage/account/, and scroll down to "Security History", but it might not be in your log so here's a screenshot:

![image](https://user-images.githubusercontent.com/8050853/193627028-55144c29-a849-4320-a716-833122f9e6ef.png)


**My Platform**
N/A

**Additional context**
<!-- Add any other context, links, etc. about the feature here. -->
