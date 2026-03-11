from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def send_organization_invite_email(to_email, organization_name, accept_organization_invite_url):
    """
    Sends an organization invite email to the specified email address.
    """

    # Render the plain text content
    text_content = render_to_string(
        "email/organization_invite.txt",
        context={"organization": organization_name, "accept_organization_invite_url": accept_organization_invite_url},
        )

    # Render the HTML content
    html_content = render_to_string(
        "email/organization_invite.html",
        context={"organization": organization_name, "accept_organization_invite_url": accept_organization_invite_url},
        )

    # Create a multipart email
    msg = EmailMultiAlternatives(
        "You've been invited to join" + organization_name + "on Project Tracker!",
        text_content,
        "invites@project-tracker.dev",
        [to_email],
        )

    # Attach the HTML content to the email
    msg.attach_alternative(html_content, "text/html")
    return msg.send()
