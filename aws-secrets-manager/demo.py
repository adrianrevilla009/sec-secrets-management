"""Create, read and rotate a secret in AWS Secrets Manager (LocalStack, dummy credentials)."""
import boto3

sm = boto3.client(
    "secretsmanager",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)


def main():
    sm.create_secret(Name="orders/db", SecretString="v1-password")
    first = sm.get_secret_value(SecretId="orders/db")["SecretString"]
    sm.put_secret_value(SecretId="orders/db", SecretString="v2-password")
    current = sm.get_secret_value(SecretId="orders/db")["SecretString"]
    previous = sm.get_secret_value(SecretId="orders/db", VersionStage="AWSPREVIOUS")["SecretString"]
    assert (first, current, previous) == ("v1-password", "v2-password", "v1-password")
    sm.delete_secret(SecretId="orders/db", ForceDeleteWithoutRecovery=True)
    print("OK: created, rotated (AWSCURRENT/AWSPREVIOUS) and deleted")


if __name__ == "__main__":
    main()
