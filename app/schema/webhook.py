from typing import List, Optional, Union
from pydantic import BaseModel, Field


class User(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    login: Optional[str] = None
    id: Optional[int] = None
    node_id: Optional[str] = None
    avatar_url: Optional[str] = None
    gravatar_id: Optional[str] = None
    url: Optional[str] = None
    html_url: Optional[str] = None
    followers_url: Optional[str] = None
    following_url: Optional[str] = None
    gists_url: Optional[str] = None
    starred_url: Optional[str] = None
    subscriptions_url: Optional[str] = None
    organizations_url: Optional[str] = None
    repos_url: Optional[str] = None
    events_url: Optional[str] = None
    received_events_url: Optional[str] = None
    type: Optional[str] = None
    user_view_type: Optional[str] = None
    site_admin: Optional[bool] = None


class Repository(BaseModel):
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    owner: User
    html_url: str
    description: Optional[str] = None
    fork: bool
    url: str
    forks_url: str
    keys_url: str
    collaborators_url: str
    teams_url: str
    hooks_url: str
    issue_events_url: str
    events_url: str
    assignees_url: str
    branches_url: str
    tags_url: str
    blobs_url: str
    git_tags_url: str
    git_refs_url: str
    trees_url: str
    statuses_url: str
    languages_url: str
    stargazers_url: str
    contributors_url: str
    subscribers_url: str
    subscription_url: str
    commits_url: str
    git_commits_url: str
    comments_url: str
    issue_comment_url: str
    contents_url: str
    compare_url: str
    merges_url: str
    archive_url: str
    downloads_url: str
    issues_url: str
    pulls_url: str
    milestones_url: str
    notifications_url: str
    labels_url: str
    releases_url: str
    deployments_url: str
    created_at: Union[int, str]
    updated_at: str
    pushed_at: Union[int, str]
    git_url: str
    ssh_url: str
    clone_url: str
    svn_url: str
    homepage: Optional[str] = None
    size: int
    stargazers_count: int
    watchers_count: int
    language: Optional[str] = None
    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    has_discussions: bool
    forks_count: int
    mirror_url: Optional[str] = None
    archived: bool
    disabled: bool
    open_issues_count: int
    license: Optional[str] = None
    allow_forking: bool
    is_template: bool
    web_commit_signoff_required: bool
    topics: List[str]
    visibility: str
    forks: int
    open_issues: int
    watchers: int
    default_branch: str
    stargazers: Optional[int] = None  # Only present in push events
    master_branch: Optional[str] = None  # Only present in push events


class Label(BaseModel):
    id: int
    node_id: str
    url: str
    name: str
    color: str
    default: bool
    description: Optional[str] = None


class Milestone(BaseModel):
    """GitHub Milestone model for issues and pull requests."""
    url: str
    html_url: str
    labels_url: str
    id: int
    node_id: str
    number: int
    title: str
    description: Optional[str] = None
    creator: User
    open_issues: int
    closed_issues: int
    state: str
    created_at: str
    updated_at: str
    due_on: Optional[str] = None
    closed_at: Optional[str] = None


class Team(BaseModel):
    """GitHub Team model for requested reviewers in pull requests."""
    id: int
    node_id: str
    url: str
    html_url: str
    name: str
    slug: str
    description: Optional[str] = None
    privacy: str
    notification_setting: Optional[str] = None
    permission: str
    members_url: str
    repositories_url: str
    parent: Optional[str] = None

# ------- Push Request Schemas---------------

class Commit(BaseModel):
    id: str
    tree_id: str
    distinct: bool
    message: str
    timestamp: str
    url: str
    author: User
    committer: User
    added: List[str]
    removed: List[str]
    modified: List[str]


class PushWebhookPayload(BaseModel):
    ref: str
    before: str
    after: str
    repository: Repository
    pusher: User
    sender: User
    created: bool
    deleted: bool
    forced: bool 
    base_ref: Optional[str] = None
    compare: str
    commits: List[Commit]
    head_commit: Optional[Commit] = None

# Alias for backwards compatibility
WebhookPayload = PushWebhookPayload

# ------- Merge Webhook Schema ---------------
MergeWebhookPayload = PushWebhookPayload


# ------- Pull Request Schemas---------------

class PullRequestRepo(BaseModel):
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    owner: User
    html_url: str
    description: Optional[str] = None
    fork: bool
    url: str
    forks_url: str
    keys_url: str
    collaborators_url: str
    teams_url: str
    hooks_url: str
    issue_events_url: str
    events_url: str
    assignees_url: str
    branches_url: str
    tags_url: str
    blobs_url: str
    git_tags_url: str
    git_refs_url: str
    trees_url: str
    statuses_url: str
    languages_url: str
    stargazers_url: str
    contributors_url: str
    subscribers_url: str
    subscription_url: str
    commits_url: str
    git_commits_url: str
    comments_url: str
    issue_comment_url: str
    contents_url: str
    compare_url: str
    merges_url: str
    archive_url: str
    downloads_url: str
    issues_url: str
    pulls_url: str
    milestones_url: str
    notifications_url: str
    labels_url: str
    releases_url: str
    deployments_url: str
    created_at: str
    updated_at: str
    pushed_at: str
    git_url: str
    ssh_url: str
    clone_url: str
    svn_url: str
    homepage: Optional[str] = None
    size: int
    stargazers_count: int
    watchers_count: int
    language: Optional[str] = None
    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    has_discussions: bool
    forks_count: int
    mirror_url: Optional[str] = None
    archived: bool
    disabled: bool
    open_issues_count: int
    license: Optional[str] = None
    allow_forking: bool
    is_template: bool
    web_commit_signoff_required: bool
    topics: List[str]
    visibility: str
    forks: int
    open_issues: int
    watchers: int
    default_branch: str
    # PR-specific merge settings
    allow_squash_merge: Optional[bool] = None
    allow_merge_commit: Optional[bool] = None
    allow_rebase_merge: Optional[bool] = None
    allow_auto_merge: Optional[bool] = None
    delete_branch_on_merge: Optional[bool] = None
    allow_update_branch: Optional[bool] = None
    use_squash_pr_title_as_default: Optional[bool] = None
    squash_merge_commit_message: Optional[str] = None
    squash_merge_commit_title: Optional[str] = None
    merge_commit_message: Optional[str] = None
    merge_commit_title: Optional[str] = None


class PullRequestBranch(BaseModel):
    label: str
    ref: str
    sha: str
    user: User
    repo: PullRequestRepo


class LinkItem(BaseModel):
    href: str


class PullRequestLinks(BaseModel):
    self: LinkItem
    html: LinkItem
    issue: LinkItem
    comments: LinkItem
    review_comments: LinkItem
    review_comment: LinkItem
    commits: LinkItem
    statuses: LinkItem


class PullRequest(BaseModel):
    url: str
    id: int
    node_id: str
    html_url: str
    diff_url: str
    patch_url: str
    issue_url: str
    number: int
    state: str
    locked: bool
    title: str
    user: User
    body: Optional[str] = None
    created_at: str
    updated_at: str
    closed_at: Optional[str] = None
    merged_at: Optional[str] = None
    merge_commit_sha: Optional[str] = None
    assignee: Optional[User] = None
    assignees: List[User]
    requested_reviewers: List[User]
    requested_teams: List[Team]
    labels: List[Label]
    milestone: Optional[Milestone] = None
    draft: bool
    commits_url: str
    review_comments_url: str
    review_comment_url: str
    comments_url: str
    statuses_url: str
    head: PullRequestBranch
    base: PullRequestBranch
    links: PullRequestLinks = Field(alias="_links")
    author_association: str
    auto_merge: Optional[str] = None
    active_lock_reason: Optional[str] = None
    merged: bool
    mergeable: Optional[bool] = None
    rebaseable: Optional[bool] = None
    mergeable_state: str
    merged_by: Optional[User] = None
    comments: int
    review_comments: int
    maintainer_can_modify: bool
    commits: int
    additions: int
    deletions: int
    changed_files: int


class PullRequestWebhookPayload(BaseModel):
    action: str
    number: int
    pull_request: PullRequest
    repository: Repository
    sender: User
