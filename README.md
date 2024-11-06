# certificate-alert

Contains python code to check certificate expiry of a domain and send alerts if about to expire.

To execute the code, install packages present in requirements.txt and pass a list of dictionaries having hostname and port to **check_ssl_expiry()** method in main.py.

Ex: ```[
        {
            'hostname':"google.com",
            'port':443
        },
        {
            'hostname':"meta.com",
            'port':443
        },
        {
            'hostname':"googles.com",
            'port':443
        }
    ]```

Code flow is as follows:

1. Check if socket connection is established on given port.
2. Append returned socket connection object to 
*https_connection_objects* list
3. If connection established, check if tls handshake is successful.
4. Append returned handshake object to *tls_handshake_objects* list
5. If handshake successful, fetch ssl_certificate.
6. Append ssl certificate object in *ssl_certificate_objects* list
7. Convert fetched certificate to pem format.
8. Fetch certificate properties like expiry date, issue date etc.
9. Check if certificate is about to expire and push certificate detail objects in *cert_detail_objects* list
10. Once 1-9 are done, pass all returned list to unwrap_cert_objects, to get list of errors for all certifcates and expiring certificates.

11. Send list of all unwrapped objects to SlackNotifcation module to create appropriate messages and send it to slack chnnel.


**Assumptions Made**

1. If port is not passed, 443 is taken as default port.
2. Expiry threshold is taken as 15 days. if needed can be changed in config/config.yaml file.
3. Slack app is already created with access to its token.
4. Slack chnannel id must be available.
5. Pass slack token and channel id as environement variables.
 
