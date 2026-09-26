L1 Job Processor Crashes when IAM_ROLE environment variable is not defined
- **Dragonchain Version**: 4.1.0
- **Entrypoint**: job_processor

When using the job processor on an L1 chain, it will simply crash if you haven't defined the IAM_ROLE environment variable, which shouldn't be required.
