"""Provider authentication helpers. Credentials are obtained from native credential chains."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class AuthResult:
    provider: str
    identity: Any
    project_or_account: Optional[str] = None
    region: Optional[str] = None
    details: Optional[dict] = None

def authenticate_gcp(project_id: str | None = None, impersonate_service_account: str | None = None, scopes=None, interactive_colab: bool = True) -> AuthResult:
    """Authenticate via Colab user ADC, existing ADC, or service-account impersonation.

    For Workload Identity Federation, set GOOGLE_APPLICATION_CREDENTIALS to the
    external-account credential configuration file before calling this function.
    """
    try:
        import google.auth
        from google.auth import impersonated_credentials
    except ImportError as e:
        raise RuntimeError("Install GCP extras: pip install 'notebook-cloud[gcp]'") from e
    if interactive_colab:
        try:
            from google.colab import auth as colab_auth
            colab_auth.authenticate_user()
        except ImportError:
            pass
    credentials, detected_project = google.auth.default(scopes=scopes or ["https://www.googleapis.com/auth/cloud-platform"])
    if impersonate_service_account:
        credentials = impersonated_credentials.Credentials(
            source_credentials=credentials,
            target_principal=impersonate_service_account,
            target_scopes=scopes or ["https://www.googleapis.com/auth/cloud-platform"],
            lifetime=3600,
        )
    return AuthResult("gcp", credentials, project_id or detected_project, details={"mode": "service_account_impersonation" if impersonate_service_account else "application_default_credentials"})

def authenticate_aws(region: str | None = None, role_arn: str | None = None, session_name: str = "notebook-cloud-session") -> AuthResult:
    """Use boto3's standard chain; optionally exchange current identity for an STS role."""
    try: import boto3
    except ImportError as e: raise RuntimeError("Install AWS extras: pip install 'notebook-cloud[aws]'") from e
    session=boto3.Session(region_name=region)
    if role_arn:
        sts=session.client("sts")
        assumed=sts.assume_role(RoleArn=role_arn,RoleSessionName=session_name)
        c=assumed["Credentials"]
        session=boto3.Session(aws_access_key_id=c["AccessKeyId"],aws_secret_access_key=c["SecretAccessKey"],aws_session_token=c["SessionToken"],region_name=region)
    identity=session.client("sts").get_caller_identity()
    return AuthResult("aws",session,identity.get("Account"),region,{"arn":identity.get("Arn"),"role_arn":role_arn})

def authenticate_azure(tenant_id: str | None = None, interactive: bool = False) -> AuthResult:
    """Use Azure DefaultAzureCredential; opt into interactive browser only on request."""
    try:
        from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
    except ImportError as e: raise RuntimeError("Install Azure extras: pip install 'notebook-cloud[azure]'") from e
    cred=InteractiveBrowserCredential(tenant_id=tenant_id) if interactive else DefaultAzureCredential(exclude_interactive_browser_credential=True, tenant_id=tenant_id)
    return AuthResult("azure",cred,tenant_id,details={"mode":"interactive_browser" if interactive else "default_credential_chain"})

def authenticate_oci(config_file: str | None = None, profile: str = "DEFAULT", use_instance_principal: bool = False) -> AuthResult:
    """Use OCI config profile locally, or instance principals on OCI compute."""
    try: import oci
    except ImportError as e: raise RuntimeError("Install OCI extras: pip install 'notebook-cloud[oci]'") from e
    if use_instance_principal:
        signer=oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
        cfg={"region":signer.region}
    else:
        cfg=oci.config.from_file(file_location=config_file or oci.config.DEFAULT_LOCATION, profile_name=profile)
        signer=None
    return AuthResult("oci",{"config":cfg,"signer":signer},cfg.get("tenancy"),cfg.get("region"),{"profile":profile,"instance_principal":use_instance_principal})
