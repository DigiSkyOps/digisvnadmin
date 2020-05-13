SVN Permission Management System
=======================

Feature list
-----------------------

1. Manage SVN user passwords
2. Manage SVN repo
3. Manage user group information
4. Manage the authorization of the SVN repo
5. Automatically update the user account file and permission profile of the SVN configuration

Design
-----------------------

+ The SVN service runs by default, and the password cannot be saved using django's password, so a separate field stores the user password
+ The SVN service operates on three files, password, group, and authz.The SVN service configuration is required to use these three files for management

Configuration
-----------------------

1. Modify the config.py. Sample file under the digisvn folder to config.py
2. According to the profile address of your SVN service

Licensing
-----------------------
minio-admin is under the Apache 2.0 license.
