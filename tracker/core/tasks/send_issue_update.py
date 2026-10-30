from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def send_issue_update_email(to_email: str, issue_label: str, issue_update_url: str):
    """
    Sends an issue update email to the specified email address.
    """

    # Render the plain text content
    text_content = render_to_string(
        "email/issue_update.txt",
        context={"issue_label": issue_label, "issue_update_url": issue_update_url},
        )

    # Render the HTML content
    html_content = render_to_string(
        "email/issue_update.html",
        context={"issue_label": issue_label, "issue_update_url": issue_update_url},
        )

    # Create a multipart email
    msg = EmailMultiAlternatives(
        issue_label + " has been updated",
        text_content,
        "tracker@project-tracker.dev",
        [to_email],
        )

    # Attach the HTML content to the email
    msg.attach_alternative(html_content, "text/html")
    return msg.send()
