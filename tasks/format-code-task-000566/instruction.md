[bug] fix the prompt when asking to document a model for the first time
when we document a model for the first time we get this:
```
      Installed dbt-sugar version: 0.0.0


       ____    __                                   
  ____/ / /_  / /_      _______  ______ _____ ______
 / __  / __ \/ __/_____/ ___/ / / / __ `/ __ `/ ___/
/ /_/ / /_/ / /_/_____(__  ) /_/ / /_/ / /_/ / /    
\__,_/_.___/\__/     /____/\__,_/\__, /\__,_/_/     
                                /____/              

Getting sweetness out of the cupboard 🍬! 

The model 'fct_orders' has not been docummented yet. Creating a new entry.
? Do you want to change the model description of fct_orders (Y/n)
```

We probably should change it to "Do you want to write a description for fct_orders?"
