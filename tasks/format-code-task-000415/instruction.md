FTPHook doesn't not allow to change port
### Apache Airflow Provider(s)

ftp

### Versions of Apache Airflow Providers

3.8.0

### Apache Airflow version

2.6.3

### Operating System

Ubuntu 20.04

### Deployment

Official Apache Airflow Helm Chart

### Deployment details

Irrelevant as it is in source code

### What happened

When setting up an FTP connection with a custom port (different from 21), the FTP Hook does not read it at all and simply passes the hostname and uses the default port set by FTP_PORT in ftplib.FTP_PORT (used by ftplib.FTP.port), thus preventing any modification of default port 21. 
PS: The 'connect' function of the FTP class reads port from the self.port attribute;

### What you think should happen instead

The FTP Hook should be able to read the port (if set) and pass it to the FTP object created 

### How to reproduce

Set up any FTP connection with and test it on Airflow UI. 

### Anything else

_No response_

### Are you willing to submit PR?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/apache/airflow/blob/main/CODE_OF_CONDUCT.md)
