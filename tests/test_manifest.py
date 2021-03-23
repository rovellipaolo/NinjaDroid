import unittest

from ninjadroid.parsers.manifest import AndroidManifest, AppActivity, AppBroadcastReceiver, AppService, AppSdk, \
    AppVersion


class TestAndroidManifest(unittest.TestCase):
    """
    Test AndroidManifest class.
    """

    def test_manifest_as_dict(self):
        manifest = AndroidManifest(
            filename="any-file-name",
            size=10,
            md5hash="any-file-md5",
            sha1hash="any-file-sha1",
            sha256hash="any-file-sha256",
            sha512hash="any-file-sha512",
            package_name="any-package-name",
            version=AppVersion(code=1, name="any-version-name"),
            sdk=AppSdk(min_version="10", target_version="15", max_version="20"),
            permissions=["any-permission-1", "any-permission-2"],
            activities=[
                AppActivity(
                    name="any-activity-name-1",
                    metadata=[
                        {
                            "name": "any-activity-metadata-name",
                            "value": "any-activity-metadata-value"
                        }
                    ],
                    intent_filters=[
                        {
                            "priority": "100",
                            "action": ["any-activity-intent-filter-action"],
                            "category": ["any-activity-intent-filter-category"],
                            "data": [
                                {"scheme": "any-activity-intent-filter-data-scheme"},
                                {"mimeType": "any-activity-intent-filter-data-mimetype"}
                            ]
                        }
                    ],
                    parent_name="any-activity-parent-name",
                    launch_mode="1",
                    no_history="true",
                ),
                AppActivity(name="any-activity-name-2")
            ],
            services=[
                AppService(
                    name="any-service-name-1",
                    metadata=[
                        {
                            "name": "any-service-metadata-name",
                            "value": "any-service-metadata-value"
                        }
                    ],
                    intent_filters=[
                        {
                            "priority": "100",
                            "action": ["any-service-intent-filter-action"],
                            "category": ["any-service-intent-filter-category"],
                            "data": [
                                {"scheme": "any-service-intent-filter-data-scheme"},
                                {"mimeType": "any-service-intent-filter-data-mimetype"}
                            ]
                        }
                    ],
                    enabled=False,
                    exported=True,
                    process="any-service-process",
                    isolated_process=True
                ),
                AppService(name="any-service-name-2")
            ],
            receivers=[
                AppBroadcastReceiver(
                    name="any-broadcast-receiver-name-1",
                    metadata=[
                        {
                            "name": "any-broadcast-receiver-metadata-name",
                            "value": "any-broadcast-receiver-metadata-value"
                        }
                    ],
                    intent_filters=[
                        {
                            "priority": "100",
                            "action": ["any-broadcast-receiver-intent-filter-action"],
                            "category": ["any-broadcast-receiver-intent-filter-category"],
                            "data": [
                                {"scheme": "any-broadcast-receiver-intent-filter-data-scheme"},
                                {"mimeType": "any-broadcast-receiver-intent-filter-data-mimetype"}
                            ]
                        }
                    ],
                    enabled=True,
                    exported=False
                ),
                AppBroadcastReceiver(name="any-broadcast-receiver-name-2")
            ]
        )

        result = manifest.as_dict()

        self.assertEqual(
            {
                "file": "any-file-name",
                "size": 10,
                "md5": "any-file-md5",
                "sha1": "any-file-sha1",
                "sha256": "any-file-sha256",
                "sha512": "any-file-sha512",
                "package": "any-package-name",
                "version": {
                    "code": 1,
                    "name": "any-version-name"
                },
                "sdk": {
                    "min": "10",
                    "target": "15",
                    "max": "20"
                },
                "permissions": [
                    "any-permission-1",
                    "any-permission-2"
                ],
                "activities": [
                    {
                        "name": "any-activity-name-1",
                        "meta-data": [
                            {
                                "name": "any-activity-metadata-name",
                                "value": "any-activity-metadata-value"
                            }
                        ],
                        "intent-filter": [
                            {
                                "priority": "100",
                                "action": ["any-activity-intent-filter-action"],
                                "category": ["any-activity-intent-filter-category"],
                                "data": [
                                    {
                                        "scheme": "any-activity-intent-filter-data-scheme"
                                    },
                                    {
                                        "mimeType": "any-activity-intent-filter-data-mimetype"
                                    }
                                ]
                            }
                        ],
                        "parentActivityName": "any-activity-parent-name",
                        "launchMode": "1",
                        "noHistory": "true"
                    },
                    {
                        "name": "any-activity-name-2"
                    }
                ],
                "services": [
                    {
                        "name": "any-service-name-1",
                        "meta-data": [
                            {
                                "name": "any-service-metadata-name",
                                "value": "any-service-metadata-value"
                            }
                        ],
                        "intent-filter": [
                            {
                                "priority": "100",
                                "action": ["any-service-intent-filter-action"],
                                "category": ["any-service-intent-filter-category"],
                                "data": [
                                    {
                                        "scheme": "any-service-intent-filter-data-scheme"
                                    },
                                    {
                                        "mimeType": "any-service-intent-filter-data-mimetype"
                                    }
                                ]
                            }
                        ],
                        "enabled": False,
                        "exported": True,
                        "process": "any-service-process",
                        "isolatedProcess": True
                    },
                    {
                        "name": "any-service-name-2"
                    }
                ],
                "receivers": [
                    {
                        "name": "any-broadcast-receiver-name-1",
                        "meta-data": [
                            {
                                "name": "any-broadcast-receiver-metadata-name",
                                "value": "any-broadcast-receiver-metadata-value"
                            }
                        ],
                        "intent-filter": [
                            {
                                "priority": "100",
                                "action": ["any-broadcast-receiver-intent-filter-action"],
                                "category": ["any-broadcast-receiver-intent-filter-category"],
                                "data": [
                                    {
                                        "scheme": "any-broadcast-receiver-intent-filter-data-scheme"
                                    },
                                    {
                                        "mimeType": "any-broadcast-receiver-intent-filter-data-mimetype"
                                    }
                                ]
                            }
                        ],
                        "enabled": True,
                        "exported": False
                    },
                    {
                        "name": "any-broadcast-receiver-name-2"
                    }
                ]
            },
            result
        )

    def test_manifest_as_dict_without_extended_processing(self):
        manifest = AndroidManifest(
            filename="any-file-name",
            size=10,
            md5hash="any-file-md5",
            sha1hash="any-file-sha1",
            sha256hash="any-file-sha256",
            sha512hash="any-file-sha512",
            package_name="any-package-name",
            version=AppVersion(code=1, name="any-version-name"),
            sdk=AppSdk(min_version="10", target_version="15", max_version="20"),
            permissions=["any-permission-1", "any-permission-2"],
            activities=[],
            services=[],
            receivers=[]
        )

        result = manifest.as_dict()

        # NOTE: no "activities", "services" and "receivers" keys are returned
        self.assertEqual(
            {
                "file": "any-file-name",
                "size": 10,
                "md5": "any-file-md5",
                "sha1": "any-file-sha1",
                "sha256": "any-file-sha256",
                "sha512": "any-file-sha512",
                "package": "any-package-name",
                "version": {
                    "code": 1,
                    "name": "any-version-name"
                },
                "sdk": {
                    "min": "10",
                    "target": "15",
                    "max": "20"
                },
                "permissions": [
                    "any-permission-1",
                    "any-permission-2"
                ]
            },
            result
        )

    def test_app_version_as_dict_with_missing_version_code(self):
        version = AppVersion(code=None, name="any-version-name")

        result = version.as_dict()

        self.assertEqual(
            {
                "code": "",
                "name": "any-version-name"
            },
            result
        )


if __name__ == "__main__":
    unittest.main()
