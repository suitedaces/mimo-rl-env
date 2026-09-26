[Proposal] Add transitional probabilities to Taxi and Cliff Walking toy text environments
### Proposal

Only Frozen Lake in the toy text grid world environments implements transitional probabilities. 

Taxi is supposed to have it based on the previous documentation but has never been implemented, always returning 1.0. 

At the same time cliff walking could also be set up to use transitional probabilities using the same approach.

### Motivation

Adding transitional probabilities to taxi will close out a TODO that has been on the list for a long time. It will also bring the environment in line with the source paper, The Fickle Taxi Task - Section 7.1 of Hierarchical Reinforcement Learning with the MAXQ Value Function Decomposition (https://www.jair.org/index.php/jair/article/view/10266/24463).

For cliff walking, it presents and opportunity to add depth to the environment and since it uses the same approach would not add significantly more time or risk.

### Pitch

Taxi
Add transitional probability into taxi toy text environment:
- leverage approach from frozen_lake to supply a transitional probability of 0.8 direction intended, 0.1 left and 0.1 right of intended direction for movement actions.
- the paper proposes that, once the taxi has picked up the passenger and moved one square away from the passenger's source location, the passenger changes their destination location with probability 0.3.
- for taxi transition probabilities for pick up and drop off actions remain 1.0.
- add arguments to enable/disable features: 
      - `is_rainy = True | False` to enable transitional probabilities on taxi movement, defaults to `False`.
      - `fickle_passenger = True | False` to enable the passenger to change their destination once picked up, defaults to `False`.

Cliff walking
Add transitional probability into cliff walking toy text environment by leverage approach from frozen_lake to supply a transitional probability of 0.3 direction intended, 0.3 left and 0.3 right of intended direction for movement actions.
- add arguments to enable/disable transitional probabilities.  
      - `is_slippery = True | False` to enable transitional probabilities on player movement, defaults to `False`.

For both:
- Update unit tests.
- Update documentation.
- Increment versions in registry.

### Alternatives

1. Do nothing. Misses an opportunity to make the toy_text environments consistent and more useful for beginner RL practitioners.

2. Remove transitional probability from taxi and/or cliff walking. In either case `prob` would be removed from the info returned. Removes the need to complete taxi work and will simplify any ongoing maintenance.

### Additional context

_No response_

### Checklist

- [X] I have checked that there is no similar [issue](https://github.com/Farama-Foundation/Gymnasium/issues) in the repo
