Forbid upgrading to Kubernetes v1.25 if Pod Security Policy are enabled
**User Story** 

Starting from Kubernetes v1.25, support for pod security policy has been removed. If a user cluster has PSP enabled and they try to upgrade to v1.25, they'll end up with a broken cluster.

To avoid this we should either block such upgrades or prompt the user that the PSP admission plugin will be disabled when they upgrade to v1.25. 


![Screenshot 2023-01-26 at 14 30 53](https://user-images.githubusercontent.com/18264334/214855904-2a6f8b1e-dd4c-48ce-88ff-95de9ae63b35.png)

![Screenshot 2023-01-26 at 14 36 03](https://user-images.githubusercontent.com/18264334/214855911-5c55c32a-082a-4ac2-954b-23e08c697a7a.png)

![Screenshot 2023-01-26 at 14 34 47](https://user-images.githubusercontent.com/18264334/214857236-a9c0be53-736e-4073-8601-2d1493aa6649.png)



At the time of creating this ticket, we haven't completely figured out the best solution or implementation details for this.

**Acceptance Criteria** 
- No Kubernetes clusters on v1.25+ with PSP enabled in the configuration.
