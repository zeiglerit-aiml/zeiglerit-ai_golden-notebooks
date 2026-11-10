"""Session-scoped cloud resource registry with preview-first teardown."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Callable, Any
from .auth import authenticate_gcp, authenticate_aws, authenticate_azure, authenticate_oci

@dataclass
class ResourceRecord:
    provider: str
    resource_type: str
    resource_id: str
    delete_action: Callable[[], Any] | None = None
    created_at: str = ""
    metadata: dict | None = None
    status: str = "managed"

class CloudSession:
    """One notebook run's identity and explicitly registered resources.

    This SDK never discovers and deletes arbitrary cloud resources. Only resources
    registered through this session can appear in its teardown plan.
    """
    def __init__(self, provider: str = "gcp", **auth_options):
        self.provider=provider.lower(); self.auth_options=auth_options
        self.auth=None; self.resources=[]; self.session_id=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    def authenticate(self):
        methods={"gcp":authenticate_gcp,"aws":authenticate_aws,"azure":authenticate_azure,"oci":authenticate_oci}
        if self.provider not in methods: raise ValueError(f"Unsupported provider: {self.provider}")
        self.auth=methods[self.provider](**self.auth_options); return self.auth
    def register_resource(self, resource_type: str, resource_id: str, delete_action: Callable[[],Any] | None = None, metadata: dict | None = None):
        if not resource_id: raise ValueError("resource_id is required")
        rec=ResourceRecord(self.provider,resource_type,resource_id,delete_action,datetime.now(timezone.utc).isoformat(),metadata or {})
        self.resources.append(rec); return rec
    def plan_destroy(self):
        return [{"provider":r.provider,"type":r.resource_type,"id":r.resource_id,"has_delete_handler":bool(r.delete_action),"status":r.status} for r in reversed(self.resources) if r.status=="managed"]
    def destroy(self, confirm: bool = False, dry_run: bool = True):
        plan=self.plan_destroy()
        if dry_run: return {"dry_run":True,"requires_confirm":True,"planned":plan}
        if confirm is not True: raise PermissionError("Destruction requires destroy(confirm=True, dry_run=False) after reviewing plan_destroy().")
        results=[]
        by_id={r.resource_id:r for r in self.resources}
        for item in plan:
            rec=by_id[item["id"]]
            if rec.delete_action is None:
                results.append({**item,"result":"skipped_no_delete_handler"}); continue
            rec.delete_action(); rec.status="destroyed"
            results.append({**item,"result":"destroyed"})
        return {"dry_run":False,"results":results}
    def cleanup(self, confirm: bool = False, dry_run: bool = True):
        """Alias for destroy; safe to call at the end of a notebook."""
        return self.destroy(confirm=confirm,dry_run=dry_run)
