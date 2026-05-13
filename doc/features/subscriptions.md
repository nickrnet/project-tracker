- [Subscriptions](#subscriptions)
  - [Overview](#overview)
  - [Sign Up Flow](#sign-up-flow)
  - [Individual Subscription Types](#individual-subscription-types)
  - [Organization Subscriptions](#organization-subscriptions)
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

There is currently no way to actually subscribe, as payment methods (banking) and management need to be fleshed out.

## Individual Subscription Types

There are currently 4 Individual Subscription Types:

- `Trial`: lasts for 7 days and allows 1 user (the person signed up)
- `Free`: Trial subscriptions can be converted to Free subscriptions that last for 30 days and allows 1 user (the person signed up)
- `Standard`: lasts for 30 days and allows up to 5 users
- `Premium`: lasts for 30 days and allows for up to 10 users

Currently, none of these subscription types lock any features yet, either functionally or when expired, this is just getting bootstrapped.

Individual Subscription expiration dates are set at Sign Up (or extension by admin (or when paid/subscribed once implemented)).

## Organization Subscriptions

There are currently 6 Organization Subscription Types:

- `Trial`: lasts for 7 days and allows 1 user (usually the person signed up)
- `Free`: Trial subscriptions can be converted to Free subscriptions that last for 30 days and allows 1 user (usually the person signed up)
- `Standard`: lasts for 30 days and allows up to 5 users
- `Premium`: lasts for 30 days and allows for up to 10 users
- `Enterprise`: does not end and has unlimited users
- `On Premise`: does not end and has unlimited users

The idea behind "Enterprise" is a separate, single-tenant instance of Project Tracker hosted by us, vs. the "Trial", "Free", "Standard", and "Premium" subscriptions are hosted in our multi-tenant instance, shared with other Project Tracker users.

The idea behind "On Premise" is that if a customer buys Project Tracker to host themselves, vs. the other Organization Subscription types that are hosted by us.

Again, none of the subscription types actually disable any functionality if expired at this time, until we can figure out what to feature-flag.

## Background Processing

In order to let background processes parse and set expiration per individual subscription and per organization subscription, we use Celery so that every web request isn't validating subscriptions and to avoid database issues.

The background processes are set up to run once a day, and only on unexpired subscriptions that have an expiration prior to the day the job is executed. This does mean potentially someone/org gets a free extra day, but that's OK. For now.
