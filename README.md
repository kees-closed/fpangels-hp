[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

# TZM Chapters Map

## About
>_`fprsmap` - abbreviation for "Fairphoners Map"_

This map is based on the work from the [WeAreFairphone Community][fpangels]. Without their amazing work and their willingness to make it open-source, we could not have made our TZM Chapters Map this easily. We will do our best to merge back any improvements we make, back to the WeAreFairphone Community.

## Dependencies and usage
The installation and management of the map on our server is fully automated with Ansible. This also includes server hardening. Due to the sensitive nature of our Ansible Playbooks, we maintain it in our private GitLab. To at least provide the basics; this map depends on a [Discourse forum][discourse] to retrieve the data. Furthermore, a [custom Discourse plugin][discourse-plugin] is required for the additional custom group fields for e.g. location.

If any help or extra information is required, we are happy to help out. Please reach out to us at: https://forum.tzm.community

[fpangels]: https://github.com/WeAreFairphone/fpangels-hp
[discourse-plugin]: https://github.com/kees-closed/discourse-group-custom-fields
[discourse]: https://discourse.org
