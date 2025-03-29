REMEDIATION_LIBRARY = {
    "CKV_AWS_21": {
        "title": "S3 Bucket allows public read access",
        "why": "Public buckets can expose sensitive or internal data to the internet.",
        "remediation": "Set 'AccessControl' to 'Private' or define restrictive bucket policies.",
        "doc": "https://docs.bridgecrew.io/docs/s3_1-enable-bucket-private-acl"
    },
    "CKV_AWS_18": {
        "title": "S3 Bucket does not have encryption enabled",
        "why": "Unencrypted buckets may lead to unauthorized data exposure at rest.",
        "remediation": "Enable default encryption using AES-256 or AWS-KMS.",
        "doc": "https://docs.bridgecrew.io/docs/s3_16-enable-default-encryption"
    },
    "CKV_AWS_20": {
        "title": "S3 Bucket does not have access logging enabled",
        "why": "Without logging, it's hard to audit access to your bucket.",
        "remediation": "Enable access logging and target logs to a secure bucket.",
        "doc": "https://docs.bridgecrew.io/docs/s3_13-enable-logging"
    },
    "CKV_AWS_57": {
        "title": "IAM role allows wildcard (*) actions",
        "why": "Wildcard permissions are overly permissive and increase risk of abuse.",
        "remediation": "Use least privilege principle by scoping actions and resources.",
        "doc": "https://docs.bridgecrew.io/docs/iam_4-no-wildcard-actions"
    },
    "CKV_AWS_111": {
        "title": "Security Group allows ingress from 0.0.0.0/0 to port 22",
        "why": "This exposes SSH to the entire internet, increasing attack risk.",
        "remediation": "Restrict SSH access to known IPs or VPN ranges.",
        "doc": "https://docs.bridgecrew.io/docs/networking_1-no-public-ingress"
    },
    "CKV_AWS_23": {
        "title": "RDS storage is not encrypted",
        "why": "Unencrypted databases can expose data at rest to attackers.",
        "remediation": "Enable encryption in your RDS cluster or instance configuration.",
        "doc": "https://docs.bridgecrew.io/docs/database_7-enable-at-rest-encryption"
    },
    "CKV_AWS_17": {
        "title": "CloudTrail not enabled across all regions",
        "why": "Not logging in all regions can create blind spots in monitoring.",
        "remediation": "Enable CloudTrail multi-region logging.",
        "doc": "https://docs.bridgecrew.io/docs/logging_1-enable-cloudtrail-all-regions"
    },
    "CKV_AWS_108": {
        "title": "EBS volume not encrypted",
        "why": "EBS volumes store data at rest. Unencrypted disks risk data exposure.",
        "remediation": "Enable encryption in volume configuration using KMS or AES-256.",
        "doc": "https://docs.bridgecrew.io/docs/general_15"
    },
    "CKV_AWS_40": {
        "title": "API Gateway caching is not enabled",
        "why": "Caching improves performance and reduces cost by limiting backend calls.",
        "remediation": "Enable caching in your stage settings.",
        "doc": "https://docs.bridgecrew.io/docs/api_1-enable-caching"
    },
    "CKV_AWS_45": {
        "title": "Redshift cluster is not encrypted",
        "why": "Unencrypted clusters may expose sensitive analytical data.",
        "remediation": "Enable encryption using KMS during cluster creation.",
        "doc": "https://docs.bridgecrew.io/docs/redshift_1-enable-cluster-encryption"
    },
}
