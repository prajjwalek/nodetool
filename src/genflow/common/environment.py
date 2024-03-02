import os
from typing import Any


MISSING_MESSAGE = "Missing required environment variable: {}"

# Default values for environment variables
# These are used if the environment variable is not set.
DEFAULT = {
    "ASSET_BUCKET": "images",
    "TEMP_BUCKET": "temp",
    "COMFY_FOLDER": None,
    "ENV": "development",
    "LOG_LEVEL": "INFO",
    "AWS_REGION": "us-east-1",
    "GENFLOW_API_URL": "http://localhost:8000/api",
}


class Environment(object):
    """
    A wrapper around the environment variables that provides
    default values and type conversions.
    """

    test_mode: bool = False

    @classmethod
    def set_test_mode(cls):
        """
        Set the environment to test mode.
        """
        cls.test_mode = True

    @classmethod
    def get(cls, key: str):
        """
        Get the value of an environment variable, or a default value.

        If the environment variable is not set, and the key is not in the
        default values, raise an exception.
        """

        if key in os.environ:
            return os.environ[key]
        elif key in DEFAULT:
            return DEFAULT[key]
        else:
            raise Exception(MISSING_MESSAGE.format(key))

    @classmethod
    def get_aws_region(cls):
        """
        The AWS region is the region where we run AWS services.
        """
        return cls.get("AWS_REGION")

    @classmethod
    def get_asset_bucket(cls):
        """
        The asset bucket is the S3 bucket where we store asset files.
        """
        return cls.get("ASSET_BUCKET")

    @classmethod
    def get_temp_bucket(cls):
        """
        The temp bucket is the S3 bucket where we store temporary files.
        """
        return cls.get("TEMP_BUCKET")

    @classmethod
    def get_env(cls):
        """
        The environment is either "development" or "production".
        """
        return cls.get("ENV")

    @classmethod
    def is_production(cls):
        """
        Is the environment production?
        """
        return cls.get_env() == "production"

    @classmethod
    def get_log_level(cls):
        """
        The log level is the level of logging that we use.
        """
        return cls.get("LOG_LEVEL")

    @classmethod
    def get_dynamo_endpoint(cls):
        """
        In development, we use a local instance.
        In production, we use the real AWS.
        """
        return os.environ.get("DYNAMO_ENDPOINT_URL", None)

    @classmethod
    def get_dynamo_region(cls):
        """
        The region name is the region of the DynamoDB server.
        """
        return os.environ.get("DYNAMO_REGION", cls.get_aws_region())

    @classmethod
    def get_dynamo_access_key_id(cls):
        """
        The access key id is the id of the AWS user.
        """
        # If we are in production, we don't need an access key id.
        # We use the IAM role instead.
        return os.environ.get("DYNAMO_ACCESS_KEY_ID", cls.get_aws_access_key_id())

    @classmethod
    def get_dynamo_secret_access_key(cls):
        """
        The secret access key is the secret of the AWS user.
        """
        # If we are in production, we don't need a secret access key.
        # We use the IAM role instead.
        return os.environ.get(
            "DYNAMO_SECRET_ACCESS_KEY", cls.get_aws_secret_access_key()
        )

    @classmethod
    def get_db_path(cls):
        """
        The database url is the url of the database.
        """
        return os.environ.get("DB_PATH", "./data/genflow.db")

    @classmethod
    def get_database_adapter(cls, fields: dict[str, Any], table_schema: dict[str, Any]):
        """
        The database adapter is the adapter that we use to connect to the database.
        """
        if cls.is_production():
            from genflow.models.dynamo_adapter import DynamoAdapter

            return DynamoAdapter(
                client=cls.get_dynamo_client(),
                fields=fields,
                table_schema=table_schema,
            )
        else:
            from genflow.models.sqlite_adapter import SQLiteAdapter

            os.makedirs(os.path.dirname(cls.get_db_path()), exist_ok=True)

            return SQLiteAdapter(
                db_path=cls.get_db_path(),
                fields=fields,
                table_schema=table_schema,
            )

    @classmethod
    def get_aws_access_key_id(cls):
        """
        The access key id is the id of the AWS user.
        """
        # If we are in production, we don't need an access key id.
        # We use the IAM role instead.
        return os.environ.get("AWS_ACCESS_KEY_ID")

    @classmethod
    def get_aws_secret_access_key(cls):
        """
        The secret access key is the secret of the AWS user.
        """
        # If we are in production, we don't need a secret access key.
        # We use the IAM role instead.
        return os.environ.get("AWS_SECRET_ACCESS_KEY")

    @classmethod
    def get_s3_endpoint_url(cls):
        """
        The endpoint url is the url of the S3 server.
        """
        return os.environ.get("S3_ENDPOINT_URL", None)

    @classmethod
    def get_s3_access_key_id(cls):
        """
        The access key id is the id of the AWS user.
        """
        # If we are in production, we don't need an access key id.
        # We use the IAM role instead.
        return os.environ.get("S3_ACCESS_KEY_ID", cls.get_aws_access_key_id())

    @classmethod
    def get_s3_secret_access_key(cls):
        """
        The secret access key is the secret of the AWS user.
        """
        # If we are in production, we don't need a secret access key.
        # We use the IAM role instead.
        return os.environ.get("S3_SECRET_ACCESS_KEY", cls.get_aws_secret_access_key())

    @classmethod
    def get_s3_region(cls):
        """
        The region name is the region of the S3 server.
        """
        return os.environ.get("S3_REGION", cls.get_aws_region())

    @classmethod
    def get_openai_api_key(cls):
        """
        The openai api key is the api key of the openai server.
        """
        return cls.get("OPENAI_API_KEY")

    @classmethod
    def get_worker_url(cls):
        """
        The worker url is the url of the worker server.
        """
        return os.environ.get("WORKER_URL")

    @classmethod
    def get_genflow_api_url(cls):
        """
        The genflow api url is the url of the genflow api server.
        """
        if cls.is_production():
            return "https://genflow.run/api"
        else:
            return cls.get("GENFLOW_API_URL")

    @classmethod
    def get_genflow_api_client(cls, auth_token: str):
        """
        The genflow api client is a wrapper around the genflow api.
        """
        from genflow.common.genflow_api_client import GenflowAPIClient

        return GenflowAPIClient(
            auth_token=auth_token, base_url=cls.get_genflow_api_url()
        )

    @classmethod
    def get_openai_client(cls):
        from openai import AsyncClient

        return AsyncClient(api_key=cls.get_openai_api_key())

    @classmethod
    def get_chroma_token(cls):
        """
        The chroma token is the token of the chroma server.
        """
        return cls.get("CHROMA_TOKEN")

    @classmethod
    def get_chroma_url(cls):
        """
        The chroma url is the url of the chroma server.
        """
        return cls.get("CHROMA_URL")

    @classmethod
    def get_chroma_client(cls):
        import chromadb
        from chromadb.config import Settings

        settings = Settings(
            chroma_client_auth_provider="token",
            chroma_client_auth_credentials=cls.get_chroma_token(),
        )

        client = chromadb.HttpClient(host=cls.get_chroma_url(), settings=settings)

        return client

    @classmethod
    def get_comfy_folder(cls):
        """
        The comfy folder is the folder where ComfyUI is located.
        """
        return cls.get("COMFY_FOLDER")

    @classmethod
    def get_replicate_api_token(cls):
        """
        The replicate api token is the api token of the replicate server.
        """
        return cls.get("REPLICATE_API_TOKEN")

    @classmethod
    def get_huggingface_token(cls):
        """
        The huggingface token.
        """
        return cls.get("HF_TOKEN")

    @classmethod
    def get_ngrok_token(cls):
        """
        The ngrok token is the token of the ngrok server.
        """
        return cls.get("NGROK_TOKEN")

    @classmethod
    def get_api_tunnel_url(cls):
        """
        The api tunnel url is the url of the api tunnel server.
        """
        if not hasattr(cls, "api_tunnel_url"):
            from pyngrok import ngrok

            ngrok_token = cls.get_ngrok_token()

            # run ngrok to expose http port 8000 and return the public url
            # Optionally set your ngrok token if you haven't done so globally
            ngrok.set_auth_token(ngrok_token)

            # Establish a tunnel to port 8000 (HTTP by default)
            tunnel = ngrok.connect("localhost:8000")

            # Retrieve the public URL where the tunnel is accessible
            assert tunnel.public_url, "No public url found"
            api_url = tunnel.public_url + "/api"
            print(f'ngrok tunnel "api_url" -> "localhost:8000"')

            cls.api_tunnel_url = api_url

        return cls.api_tunnel_url

    @classmethod
    def get_google_client_id(cls):
        """
        The google client id is the id of the google client.
        """
        return cls.get("GOOGLE_CLIENT_ID")

    @classmethod
    def get_google_client_secret(cls):
        """
        The google client secret is the secret of the google client.
        """
        return cls.get("GOOGLE_CLIENT_SECRET")

    @classmethod
    def get_s3_service(cls, bucket: str):
        """
        Get the S3 service.
        """
        from genflow.common.aws_client import AWSClient

        cls.get_logger().info(
            f"S3 service for {bucket} using endpoint {cls.get_s3_endpoint_url()} and region {cls.get_s3_region()}"
        )
        return AWSClient(
            endpoint_url=cls.get_s3_endpoint_url(),
            access_key_id=cls.get_s3_access_key_id(),
            secret_access_key=cls.get_s3_secret_access_key(),
            region_name=cls.get_s3_region(),
            log=cls.get_logger(),
        ).get_s3_service(bucket)

    @classmethod
    def get_asset_storage(cls, use_s3: bool = False):
        """
        Get the storage adapter for assets.
        """
        if cls.is_production() or cls.get_s3_endpoint_url() is not None or use_s3:
            cls.get_logger().info(f"Using S3 for asset storage")
            return cls.get_s3_service(cls.get_asset_bucket())
        else:
            from genflow.storage.file_storage import FileStorage

            if not hasattr(cls, "asset_storage"):
                if cls.test_mode:
                    from genflow.storage.memory_storage import MemoryStorage

                    cls.asset_storage = MemoryStorage(
                        base_url=f"{cls.get_genflow_api_url()}/storage/"
                        + cls.get_asset_bucket()
                    )
                else:
                    cls.get_logger().info(f"Using local file storage for asset storage")
                    cls.asset_storage = FileStorage(
                        base_path="data/assets",
                        base_url=f"{cls.get_genflow_api_url()}/storage/"
                        + cls.get_asset_bucket(),
                    )

            return cls.asset_storage

    @classmethod
    def get_temp_storage(cls, use_s3: bool = False):
        """
        Get the storage adapter for temporary files.
        """
        if cls.is_production() or cls.get_s3_endpoint_url() is not None or use_s3:
            cls.get_logger().info(f"Using S3 for temp storage")
            return cls.get_s3_service(cls.get_temp_bucket())
        else:
            from genflow.storage.memory_storage import MemoryStorage

            cls.get_logger().info(f"Using local file storage for temp storage")

            if not hasattr(cls, "temp_storage"):
                cls.temp_storage = MemoryStorage(
                    base_url=f"{cls.get_genflow_api_url()}/storage/"
                    + cls.get_temp_bucket()
                )
            return cls.temp_storage

    @classmethod
    def get_logger(cls):
        """
        Get a logger.
        """
        import logging

        if not hasattr(cls, "logger"):
            cls.logger = logging.getLogger("avatai")
            cls.logger.setLevel(cls.get_log_level())
            cls.logger.addHandler(logging.StreamHandler())
        return cls.logger

    @classmethod
    def get_replicate_client(cls):
        """
        The replicate client is a wrapper around the replicate SDK.
        """
        import replicate

        if not hasattr(cls, "replicate_client"):
            cls.replicate_client = replicate.Client(cls.get_replicate_api_token())
        return cls.replicate_client

    @classmethod
    def get_aws_client(
        cls,
        endpoint_url: str | None = None,
        access_key_id: str | None = None,
        secret_access_key: str | None = None,
        region_name: str | None = None,
        session_token: str | None = None,
    ):
        """
        The AWS client is a wrapper around the AWS SDK.

        If the class has an instance of AWSClient, return it.
        """
        from genflow.common.aws_client import AWSClient

        if region_name is None:
            region_name = cls.get_aws_region()
        return AWSClient(
            endpoint_url=endpoint_url,
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            region_name=region_name,
            session_token=session_token,
            log=cls.get_logger(),
        )

    @classmethod
    def get_dynamo_resource(cls):
        """
        The dynamo client is a wrapper around the AWS SDK.
        """
        import boto3

        if not hasattr(cls, "dynamo_resource"):
            cls.dynamo_resource = boto3.resource(
                "dynamodb",
                endpoint_url=cls.get_dynamo_endpoint(),
                aws_access_key_id=cls.get_dynamo_access_key_id(),
                aws_secret_access_key=cls.get_dynamo_secret_access_key(),
                region_name=cls.get_dynamo_region(),
            )
        return cls.dynamo_resource

    @classmethod
    def get_dynamo_client(cls):
        """
        The dynamo client is a wrapper around the AWS SDK.
        """
        import boto3

        if not hasattr(cls, "dynamo_client"):
            cls.dynamo_client = boto3.client(
                "dynamodb",
                endpoint_url=cls.get_dynamo_endpoint(),
                aws_access_key_id=cls.get_dynamo_access_key_id(),
                aws_secret_access_key=cls.get_dynamo_secret_access_key(),
                region_name=cls.get_dynamo_region(),
            )
        return cls.dynamo_client

    @classmethod
    def get_google_oauth2_session(cls, state: str | None = None):
        """
        The google oauth2 session is a wrapper around the google SDK.
        """
        from authlib.integrations.requests_client import OAuth2Session

        return OAuth2Session(
            client_id=cls.get_google_client_id(),
            client_secret=cls.get_google_client_secret(),
            state=state,
            scope="openid email",
        )
