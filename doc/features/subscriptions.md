- [Subscriptions](#subscriptions)
  - [Overview](#overview)
  - [Sign Up Flow](#sign-up-flow)
  - [Individual Subscription Types](#individual-subscription-types)
  - [Organization Subscription Types](#organization-subscription-types)
  - [Individual Subscriptions](#individual-subscriptions)
  - [Organization Subscriptions](#organization-subscriptions)
  - [History Tracking](#history-tracking)
  - [Background Processing](#background-processing)

# Subscriptions

This document describes how Subscriptions work in Project Tracker.

## Overview

Subscriptions in theory will let us do a few things:

- Recurring revenue
- Selectively lock features
- Delete old data

(I'm sure there are more activities subscriptions allow)

In Project Tracker, a subscription can be of 2 types:

- Individual Subscription
- Organization Subscription

We need 2 types because:
- A user can be working solo and tracking their projects
- A user can be a member of multiple Organizations that have many projects per Organization

At some point we will want to lock down features based on subscription type, whether an Organization is involved, etc. The feature-set-per-subscription-type has not yet been fully scoped.

Both subscription types have the same general fields right now:

- `name`: The name of the subscription
- `description`: A description of the subscription
- `is_active`: Whether the subscription type is active (selectable during signup/payment)
- `term_length_days`: How long the subscription is valid
- `user_limit`: The number of users allowed to be associated with a subscription type

## Sign Up Flow

The current sign up flow is:

- A user (Individual) signs up for a Project Tracker account
  - They are automatically put into a Trial subscription with expiration date set (implemented)
- A user can create an Organization
  - It is automatically put into a Trial subscription with expiration date set (not implemented)

There is currently no way to actually subscribe, as pricing, payment methods (banking), and subscription management need to be fleshed out.

## Individual Subscription Types

There are currently 4 Individual Subscription Types:

- `Trial`: lasts for 7 days and allows 1 user (the person signed up)
- `Free`: Trial subscriptions can be converted to Free subscriptions that last for 30 days and allows 1 user (the person signed up)
- `Standard`: lasts for 30 days and allows up to 5 users
- `Premium`: lasts for 30 days and allows for up to 10 users

The idea behind "Free" is if a user is just a part of an Organization, and doesn't have any personal projects, etc. If they are in an Organization and their "Free" subscription is expired and they try to do something on a personal item, we may want to block it, for example.

Currently, none of these subscription types lock any features yet, either functionally or when expired, this is just getting bootstrapped.

Individual Subscription expiration dates are set at Sign Up (or extension by admin (or when paid/subscribed once implemented)).

Individual Subscription Types are bootstrapped by `IndividualSubscriptionType.objects.initialize_subscriptions()`. Going forward, if a subscription type is modified in any way (a whole new subscription type, renamed, term length, etc.), we manage them there until such time as a payment processor is involved.

## Organization Subscription Types

There are currently 6 Organization Subscription Types:

- `Trial`: lasts for 7 days and allows 1 user (usually the person signed up)
- `Free`: Trial subscriptions can be converted to Free subscriptions that last for 30 days and allows 1 user (usually the person signed up)
- `Standard`: lasts for 30 days and allows up to 5 users
- `Premium`: lasts for 30 days and allows for up to 10 users
- `Enterprise`: does not end and has unlimited users
- `On Premise`: does not end and has unlimited users

The idea behind "Enterprise" is a separate, single-tenant instance of Project Tracker hosted by us, vs. the "Trial", "Free", "Standard", and "Premium" subscriptions are hosted in our multi-tenant instance, shared with other Project Tracker users.

The idea behind "On Premise" is if a customer buys Project Tracker to host themselves, vs. the other Organization Subscription types that are hosted by us.

Organization Subscription Types are bootstrapped by `OrganizationSubscriptionType.objects.initialize_subscriptions()`. Going forward, if a subscription type is modified in any way (a whole new subscription type, renamed, term length, etc.), we manage them there until such time as a payment processor is involved.

Again, none of the subscription types actually disable any functionality if expired at this time, until we can figure out what to feature-flag.

## Individual Subscriptions

Individual Subscriptions track:

- `individual`: typically the signed up user
- `subscription_type`: the Individual Subscription Type
- `expiration_date`: the date the subscription expires
- `expired`: whether the current subscription is expired or not

## Organization Subscriptions

Organization Subscriptions track:

- `organization`: the Organization
- `subscription_type`: the Organization Subscription Type
- `expiration_date`: the date the subscription expires
- `expired`: whether the current subscription is expired or not

## History Tracking

To track history, we create a new subscription and link it to the user. We can then query the IndividualSubscription table for the individual's subscription history or OrganizationSubscription table for the organization's subscription history. See `subscribe_to_trial()` on the CoreUser class for details.

## Background Processing

we use Celery to let background processes parse and set expiration per individual subscription and per organization subscription, so that every web request isn't validating subscriptions and to avoid database issues.

The background processes are set up to run once a day, and only on unexpired subscriptions that have an expiration prior to the day the job is executed. This does mean potentially someone/org gets a free extra day, but that's OK. For now.
