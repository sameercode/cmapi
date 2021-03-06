#!/usr/bin/env python
"""This script Adds S3 account"""
import argparse
import sys

from cm_api.api_client import ApiException
from cm_api.api_client import ApiResource


def parse_args():
    """
    Parses host and cluster information from the given command line arguments.
    @rtype:  namespace
    @return: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Adding Cloud Account to Cluster "
                                                 "- requires cloud Access and Secret Key ",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--server', metavar='HOST', type=str,
                        help="The Cloudera Manager host")
    parser.add_argument('-p', '--port', metavar='port', type=int, default=7180,
                        help="Cloudera Manager's port.")
    parser.add_argument('-u', '--username', metavar='USERNAME', type=str, default='admin',
                        help="The username to log into Cloudera Manager with.")
    parser.add_argument('-pwd', '--password', metavar='PASSWORD', type=str, default='admin',
                        help="The password to log into Cloudera Manager with.")
    parser.add_argument('--use-tls', action='store_true',
                        help="Whether to use TLS to connect to Cloudera Manager.")
    parser.add_argument("--account-name", metavar='ACCOUNT_NAME', type=str, default='cloudAccount1',
                        help="ALias Name to be created of the Source cluster")
    parser.add_argument('-akey', '--aws-access-key', metavar='AWS_ACCESS_KEY', type=str)
    parser.add_argument('-skey', '--aws-secret-key', metavar='AWS_SECRET_KEY', type=str)
    return parser.parse_args()


def print_usage_message():
    ''' Print usage instructions'''
    print "Usage: add_peer.py [-h] [-s HOST] [-p port] [-u USERNAME] [-pwd PASSWORD] \
                                 [--use-tls] [--source_cm_url Source Cloudera Manager URL] \
                                 [--source-user Source Cloudera Manager Username] \
                                 [--source-password SOURCE_CM_PWD] [--peer-name PEER_NAME]"


def main():
    """
    Add peer to the cluster.
    @rtype:   number
    @returns: A number representing the status of success.
    """
    settings = parse_args()
    if len(sys.argv) == 1 or len(sys.argv) > 17:
        print_usage_message()
        quit(1)

    api_target = ApiResource(settings.server,
                             settings.port,
                             settings.username,
                             settings.password,
                             settings.use_tls,
                             14)
    type_name = 'AWS_ACCESS_KEY_AUTH'
    account_configs = {'aws_access_key': settings.aws_access_key,
                       'aws_secret_key': settings.aws_secret_key}
    try:
        api_target.create_external_account(settings.account_name, settings.account_name, type_name,
                                           account_configs=account_configs)
        print "S3 Account Successfully Added"
    except ApiException as error:
        if 'already exists' in str(error):
            print 'Peer Already exists'
        else:
            raise error

    return 0


if __name__ == '__main__':
    sys.exit(main())
