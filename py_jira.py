from jira import JIRA
# There is a Project key and Project id for different project

# Different Issue type have different id. It may differ from organization to organization

class PyJira:
    def __init__():
        options = {"server": "https://jira.atlassian.com"}
        jira_user = "you jira user form env variable"
        jira_password = "your jira password from env"

        self.jira = JIRA(basic_auth=(jira_user, jira_password),
                         options=options)

    def create_jira_ticket(self, summary, project_id='', project_key='',
                           description='', issue_type='Bug', priority='1',
                           labels=[]):
        # Create new Jira ticket in the given project_id or project name
        if not project_id and not project_key:
            return
        else:
            issue_dict = {
                'project': {},
                'summary': summary,
                'description': description,
                'issuetype': {'name': issue_type},
                'priority': {
                    'id': priority,
                },
                'labels': labels,
            }
            if not project_key:
                issue_dict['project']['id'] = project_id
            else:
                issue_dict['project']['key'] = project_key

            created_issue = self.jira.create_issue(fields=issue_dict)
            return created_issue

    def link_jira_ticket(self, parent_ticket_id, ticket_id_to_add):
        # Linking a remote jira ticket with another
        issue1 = self.jira.issue(parent_ticket_id)
        issue2 = self.jira.issue(ticket_id_to_add)

        self.jira.add_remote_link(issue1, issue2)

    def delete_jira_ticket(self, ticket_id):
        # Delete a given jira ticket
        issue = self.jira.issue(ticket_id)
        issue.delete()

    def update_jira_ticket(self, ticket_id, new_summary='', new_description='',
                           send_notif=True):
        # Update a given jira ticket with new summary and description
        # You can choose to notify the watchers or not.
        # Please note - To discard the user notification either admin or
        # project admin permissions are required
        if not new_summary and not new_description:
            return True
        elif not new_summary:
            issue = self.jira.issue(ticket_id)
            issue.update(notify=send_notif, description=new_description)
        elif not new_description:
            issue = self.jira.issue(ticket_id)
            issue.update(notify=send_notif, summary=new_summary)
        else:
            issue = self.jira.issue(ticket_id)
            issue.update(notify=send_notif,
                         summary=new_summary, description=new_description)

    def add_comment(self, ticket_id, comment_text):
        # Add a new comment to already created ticket
        issue = self.jira.issue(ticket_id)
        self.jira.add_comment(issue, comment_text)

    def add_labels(self, ticket_id, labels):
        # Append new labels to to the jira ticket
        # The new label is unicode with no spaces
        issue = self.jira.issue(ticket_id)
        for label in labels:
            issue.fields.labels.append(label)

        issue.update(fields={'labels': issue.fields.labels})

    def get_all_projects(self):
        # List all projects in the the Jira System
        projects_details = []
        for project in self.jira.projects():
            projects_details.append({
                'Name': project.key,
                'Description': project.name,
                'Id': project.id
            })
        return projects_details

    def add_attachments(self, ticket_id, attachments):
        # Add attachments to the already created ticket
        issue = self.jira.issue(ticket_id)
        for attachment in attachments:
            self.jira.add_attachment(issue=issue, attachment=attachment)

    def get_issue_details(self, ticket_id):
        # Get the details for a particular jira ticket
        issue = self.jira.issue(ticket_id)
        comments = []
        attachments = []
        for comment in issue.fields.comment.comments:
            comments.append({
                'Comment text': comment.body,
                'Commented by': comment.author.name
            })

        if issue.fields.attachment:
            for attachment in issue.fields.attachment:
                attachments.append({
                    'Name': attachment.filename,
                    'Size': attachment.size,
                    'Content': attachment.get()
                })

        issue_details = {
            'project_key': issue.fields.project.key,
            'issue_type': issue.fields.issuetype.name,
            'reported_by': issue.fields.reporter.displayName,
            'labels': issue.fields.labels,
            'summary': issue.fields.summary,
            'description': issue.fields.description,
            'comment': comments,
            'attachments': attachments
        }
        return issue_details
