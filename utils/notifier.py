import pandas as pd

from config.conf import config
from config.logger import logger
from math import sqrt
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SlackNotification:

    """
    Handle methods to format slack message and send notifications.

    """

    def __init__(self):
        pass


    def __create_message(self, expired_certificates, port_not_443, tls_or_peercert_issue):

        """
        Generates structure of notifications to send to slack.

        :param expired_certificates: Collection of all hostanames whose certificates are about to expire
        :type expired_certificates: []
        :param port_not_443: Collection of all hostanames not running on DEFAULT_HTTPS_PORT i.e 443
        :type port_not_443: []
        :param tls_or_peercert_issue: Collection of all hostanames failing TLS handshake or whose certificate could not be fetched.
        :type tls_or_peercert_issue: []

        :return: Formatted messages.
        :rtype: str

        """
        
        expired_certificate_tls_message = """"""
        
        if len(expired_certificates['Hostname']) == 0:
            expired_certificate_tls_message = """%s%s""" % (expired_certificate_tls_message, "No certificate is expiring in next 30 days.\n\n")
        else:
            expired_certificates_df = pd.DataFrame.from_dict(expired_certificates)
            expired_certificates_markdown = expired_certificates_df.to_markdown()

            expired_certificate_tls_message = """%s%s""" % (expired_certificate_tls_message,"Following certificates are getting expired in next 30 days:\n\n")
            expired_certificate_tls_message = """%s%s""" % (expired_certificate_tls_message, expired_certificates_markdown)
            expired_certificate_tls_message = """%s%s""" % (expired_certificate_tls_message,"\n\n\n\n")
        
        if len(tls_or_peercert_issue['Hostname']) != 0:
            tls_or_peercert_issue_df = pd.DataFrame.from_dict(tls_or_peercert_issue)
            tls_or_peercert_issue_markdown = tls_or_peercert_issue_df.to_markdown()

            expired_certificate_tls_message = """%s%s""" % (expired_certificate_tls_message,"Following hostnames could not be monitored either because TLS Handshake failed or certificate could not be fetched:\n\n")
            expired_certificate_tls_message = """%s%s""" % (expired_certificate_tls_message, tls_or_peercert_issue_markdown)
            expired_certificate_tls_message = """%s%s""" % (expired_certificate_tls_message,"\n\n")

        # Message regarding hostnames not connecting on 443 in sent in chunks because number of such domains can be many and 
        # tabular format not getting pushed to slack properly in one go.
        # Breaking data into n chunks using lenthe of port_not_443_df and its square root.
        # Square root can give optimal number of chunks. 
        if len(port_not_443['Hostname']) != 0:

            port_not_443_df = pd.DataFrame.from_dict(port_not_443)
            port_not_443_message_chunks = []

            port_not_443_df_len = port_not_443_df.shape[0]
            port_not_443_df_len_sqrt = int(sqrt(port_not_443_df_len))
            number_of_chunks = port_not_443_df_len//port_not_443_df_len_sqrt

            previous_chunk_last_index = 0

            while number_of_chunks > 0:

                port_not_443_message = """"""
                # breaks dataframe in a continuous sequence by row.
                port_not_443_df_chunk = port_not_443_df.iloc[previous_chunk_last_index:previous_chunk_last_index+port_not_443_df_len_sqrt,:]

                if number_of_chunks == port_not_443_df_len//port_not_443_df_len_sqrt:
                    port_not_443_message = """%s%s""" % (port_not_443_message,"Connection could not be established with following endpoints as they are not running on standard 443 port:\n\n")
                else:
                    port_not_443_message = """%s%s""" % (port_not_443_message,"Continuation of above table:\n\n")

                port_not_443_message = """%s%s""" % (port_not_443_message, port_not_443_df_chunk.to_markdown())
                port_not_443_message = """%s%s""" % (port_not_443_message,"\n\n")

                port_not_443_message_chunks.append(port_not_443_message)

                previous_chunk_last_index = previous_chunk_last_index+port_not_443_df_len_sqrt
                number_of_chunks = number_of_chunks - 1
            
        
        return expired_certificate_tls_message, port_not_443_message_chunks



    def __post_message(self, message):

        """
        pushes message to slack channel.

        :param message: Message to be pushed.
        :type message: str

        """

        client = WebClient(token=config.slack_bot_token)

        try:
            client.chat_postMessage(channel=config.slack_channel_id, text="```\n" + message + "\n```")
            logger.info("Message successfully posted.")
        except SlackApiError as e:
            logger.error("Could not send message:\n\n"+message+"\n\nbecause of error "+e)

        return 



    def send_notification(self, expired_certificates, port_not_443, tls_or_peercert_issue):

        """
        Initiates a sequence to send messages to slack. It first calls a method to format the messages and then calls a method to 
        post them on slack channel.

        :param expired_certificates: Collection of all hostanames whose certificates are about to expire
        :type expired_certificates: []
        :param port_not_443: Collection of all hostanames not running on DEFAULT_HTTPS_PORT i.e 443
        :type port_not_443: []
        :param tls_or_peercert_issue: Collection of all hostanames failing TLS handshake or whose certificate could not be fetched.
        :type tls_or_peercert_issue: []

        """
        
        expired_certificate_tls_message, port_not_443_message_chunks = self.__create_message(expired_certificates, port_not_443, tls_or_peercert_issue)

        self.__post_message(expired_certificate_tls_message)
        for port_not_443_message in port_not_443_message_chunks:
            self.__post_message(port_not_443_message)

        return