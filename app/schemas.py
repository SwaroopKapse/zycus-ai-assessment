from enum import Enum

from pydantic import BaseModel


class Urgency(str, Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class TriageResult(BaseModel):
    product_area: str
    issue_category: str
    urgency: Urgency
    reasoning: str
    known_issue: bool
    relevant_documents: list[str]
    recommended_team: str
    draft_response: str

class IssueCategory(str, Enum):
    BILLING = "Billing"
    BUG = "Bug"
    DATA_LOSS = "Data Loss"
    FEATURE_REQUEST = "Feature Request"
    HOW_TO = "How-To"
    INTEGRATION = "Integration"
    ONBOARDING = "Onboarding"
    PERFORMANCE = "Performance"
class Product(str, Enum):
    ANALYTICS_HUB = "AnalyticsHub"
    CLOUD_SYNC = "CloudSync"
    DATA_BRIDGE_PRO = "DataBridge Pro"
    SECURE_VAULT = "SecureVault"
    WORKFLOW_ENGINE = "WorkflowEngine"

class ProductArea(str, Enum):
    API = "API"
    ACTIONS = "Actions"
    ALERTS = "Alerts"
    AUDIT_LOGS = "Audit Logs"
    AUTHENTICATION = "Authentication"
    BANDWIDTH_LIMITS = "Bandwidth Limits"
    CONFLICT_RESOLUTION = "Conflict Resolution"
    CONNECTORS = "Connectors"
    DASHBOARD = "Dashboard"
    DATA_INGESTION = "Data Ingestion"
    DATA_SOURCES = "Data Sources"
    ENCRYPTION = "Encryption"
    ERROR_HANDLING = "Error Handling"
    EXPORTS = "Exports"
    FILE_SYNC = "File Sync"
    INTEGRATIONS = "Integrations"
    KEY_MANAGEMENT = "Key Management"
    PERMISSIONS = "Permissions"
    PIPELINE_MONITORING = "Pipeline Monitoring"
    REPORTS = "Reports"
    SSO = "SSO"
    SCHEDULING = "Scheduling"
    SCHEMA_MANAGEMENT = "Schema Management"
    TEMPLATES = "Templates"
    TRIGGERS = "Triggers"

class TriageResult(BaseModel):
    product_area: ProductArea
    issue_category: IssueCategory
    urgency: Urgency
    reasoning: str
    known_issue: bool
    relevant_documents: list[str]
    recommended_team: str
    draft_response: str