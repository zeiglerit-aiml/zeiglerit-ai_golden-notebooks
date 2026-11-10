# notebook_cloud

Reusable, provider-neutral authentication and teardown helpers for Colab/Jupyter.

## Install

```python
%pip install -e /content/drive/MyDrive/Colab_Notebook_Library_2026-11-06/notebook_cloud
%pip install "notebook-cloud[gcp,aws,azure,oci]"
```

Or add this folder to `sys.path` in a local checkout. The first line is for an editable local package checkout; use the second line for provider SDK dependencies.

## GCP quick start (Colab)

```python
from notebook_cloud import CloudSession
cloud = CloudSession("gcp", project_id="YOUR_PROJECT_ID")
auth = cloud.authenticate()
print(auth.project_or_account, auth.details)
```

GCP auth supports Colab user ADC, existing ADC, service-account impersonation, and external-account/WIF ADC configuration via `GOOGLE_APPLICATION_CREDENTIALS`.

## Other providers

```python
aws = CloudSession("aws", region="us-east-1").authenticate()
azure = CloudSession("azure", tenant_id="YOUR_TENANT_ID").authenticate()
oci = CloudSession("oci", profile="DEFAULT").authenticate()
```

## Teardown contract

```python
cloud.register_resource("gcs_bucket", "my-created-bucket", delete_action=lambda: bucket.delete(force=True))
cloud.plan_destroy()                         # preview only
cloud.destroy()                              # still preview only
cloud.destroy(confirm=True, dry_run=False)   # executes registered delete handlers
# At notebook end: cloud.cleanup()           # preview; set confirm=True, dry_run=False to execute
```

Only explicitly registered resources with explicit delete handlers are eligible. No project-wide, subscription-wide, account-wide, or tenancy-wide deletion is implemented. Review provider-side dependencies, retention, and data-loss impact before confirming.
