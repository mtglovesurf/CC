#!/bin/bash

rake --trace -f /usr/src/redmine/Rakefile redmine:email:receive_imap RAILS_ENV="production" host=imap.mail.us-east-1.awsapps.com username=support@zukosha-it.com password=Zks0155332200 folder=Inbox move_on_success=redmine_success move_on_failure=redmine_failure port=993 ssl=1 project=support unknown_user=accept no_permission_check=1
