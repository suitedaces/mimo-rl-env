/escalate Slack Dropdown Duplicates Teams for Each Route in Direct Paging
### What went wrong?

**What happened**:
- Teams with more than 1 Route defined in Direct Paging are being duplicated in the Create Escalation menu from the /escalate command. e.g. a Direct Paging Integration with 3 routes will be shown 3 times in the "Team to notify" menu (pictured below). It seems to stop incrementing at 3 (e.g. making 5 routes doesn't create 5 entries in the dropdown) but I don't know what to make of why that is.

**What did you expect to happen**:
- Expected that each Team would only appear once in the "Team to notify" dropdown menu.


<img width="264" alt="Screenshot 2023-11-20 110420" src="https://github.com/grafana/oncall/assets/80909828/de8401a4-a338-4aef-b45f-5d22c46df213">

![Screenshot 2023-11-20 110758](https://github.com/grafana/oncall/assets/80909828/97d5ca27-4d91-4a42-821d-a2d75d420e78)



### How do we reproduce it?

1. Create a Direct Paging Integration for a team.
2. Create 2 or more Routes for that team's Direct Paging.
3. Run the /escalate command in Slack, then select "Team to notify" -- in screenshots pictured above there are duplicate entries for this team displayed.


### Grafana OnCall Version

v1.3.59

### Product Area

Chatops

### Grafana OnCall Platform?

Kubernetes

### User's Browser?

Slack Production 4.35.126

### Anything else to add?

_No response_
