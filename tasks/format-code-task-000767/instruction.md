**Describe the bug**
- dbt `>1.5` introduced [model versions](https://docs.getdbt.com/docs/collaborate/govern/model-versions)
- the precommit hooks `Check the model has properties file` and `Check the model has description` fail
- probably because it expects description for each version, while there is none

**To Reproduce**
Steps to reproduce the behavior:
1. Create two versions of the same model `fancy_model_v1.sql` and `fancy_model_v2.sql` 
2. Adapt the `yml` file
```yml
- name: fancy_model
  latest_version: 1
  description: fancy model
  config:
    contract:
      enforced: true
  columns:
    - name: tool_raw
      description: raw name of tool
      data_type: varchar(20)
      constraints:
        - type: not_null
        - type: primary_key
          warn_unenforced: False
    - name: tool
      description: tool name, "jpg-to-pdf"
      data_type: varchar(20)

  versions:
    - v: 1
    - v: 2
      columns:
        - include: all
          exclude: [tool]
        - name: new_column
          data_type: varchar(6)
          description: "I am an experimental column"
```
3. Run the `Check the model has properties file` and `Check the model has description`
4. The error is:
```
#14 [dbt_precommit 4/4] RUN pre-commit run --all-files
...
#14 1.186 Check the model has properties file......................................Failed
#14 8.483 - hook id: check-model-has-properties-file
#14 8.483 - exit code: 1
#14 8.483 models/fancy_model_v1.sql: does not have model properties defined in any .yml file.
#14 8.483 models/fancy_model_v2.sql: does not have model properties defined in any .yml file.
...
#14 8.484 Check the model has description..........................................Failed
#14 34.62 - hook id: check-model-has-description
...
#14 34.62 models/fancy_model_v1.sql: does not have defined description or properties file is missing.
#14 34.62 models/fancy_model_v2.sql: does not have defined description or properties file is missing.
```

**Expected behavior**
- `precommit` should understand that  `fancy_model_v1.sql` and `fancy_model_v2.sql` are the same and have description under `fancy_model` in `yml` file

**Version:**
v0.1.0

**Additional context**
Add any other context about the problem here.
