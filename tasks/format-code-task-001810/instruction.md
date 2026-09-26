Add --config parameter
<!-- 
If you have a general question about how to use Locust, please check Stack Overflow first https://stackoverflow.com/questions/tagged/locust

You can also ask new questions on SO, https://stackoverflow.com/questions/ask just remember to tag your question with "locust".
-->

### Is your feature request related to a problem? Please describe.
<!-- A clear and concise description of what the problem is. Ex. I'm always frustrated when [...] -->
I would like to be able to have multiple config files stored in version control for different purposes (eg one that uses step-mode and one that doesn't).

### Describe the solution you'd like
<!-- A clear and concise description of what you want to happen -->
`ConfigArgParse` makes it easy to add this capability. I think it could be done with a single line in `parse_options`:
`parser.add_argument('--config', is_config_file_arg=True, help='config file path')`

### Describe alternatives you've considered
<!-- A clear and concise description of any alternative solutions or features you've considered -->
Current workaround is to keep multiple sets of configurations in `locust.conf`, with the active one uncommented.
