'Notify me about token promotions' switch doesn't work if you've already said 'Maybe Later'
<!--
Have you searched for similar issues? We have received a lot of feedback and bug reports that we have closed as duplicates. Before submitting this issue, please visit our community site for common ones: https://community.brave.com/c/common-issues
-->

### Description
If you are prompted for a promotion and you select 'Maybe Later', the remindTimestamp is set to remind you 24h later. If you then go into Adv Settings and toggle 'Notify me about token promotions' off, you will still be reminded 24h later.


### Steps to Reproduce
<!--
Please add a series of steps to reproduce the problem. See https://stackoverflow.com/help/mcve for in depth information on how to create a minimal, complete, and verifiable example.
-->

  1. Clean install of 0.20 using ledger_environment=staging.
  2. Get notification.
  3. Select Maybe Later.
  4. Go to Adv Settings, toggle 'Notify me about token promotions' off.
  5. Close Brave.
  6. Open session-store-1 and locate remindTimestamp. Using https://www.epochconverter.com/ you can see that it is set to 24h later.
  7. Change this value to 5-10 minutes from now.
  8. Relaunch Brave (make sure you still use ledger_env staging)



**Actual result:**
In 30-60 minutes you will be notified about the promotion again. 


**Expected result:**
You should not be notified about the promotion since you toggled the switch to off.

**Reproduces how often:**
Easily


### Brave Version

**about:brave info:**
0.20.30


**Reproducible on current live release:**
Yes


### Additional Information
Missed when testing https://github.com/brave/browser-laptop/issues/12313
