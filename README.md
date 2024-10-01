# project-tracker

[![Tests](https://github.com/nickrnet/project-tracker/actions/workflows/test.yml/badge.svg)](https://github.com/nickrnet/project-tracker/actions/workflows/test.yml)

# A Project Tracker for Developers

The idea behind Project Tracker is to be able to track a project and its issues, of varying issue types and priorities and severities and progress states, through sprints, including test execution. The sprint and test execution bits are still work in progress. All of it is work in progress, frankly (it's a fairly new project), we're still making the app responsive vs hard page navigation, friendly links, etc.

Inspiration comes from Jira, Trello, TestRail, Trac, Vivify, ServiceNow, and GitHub.

Eventually, if one assigns git repositories to a project, then tests _could_ get automatically flagged as executed for a project/sprint release, and their state (pass, fail).

## Under the Hood

Project Tracker is a Django app with a Bootstrap front end. The front end is made responsive with HTMX and only updating parts of a page that are affected by UI controls. No React, please, just standard HTML and CSS wizardry.

## Documentation Notes

See the [`doc`](doc) directory for additional documentation.

[Development Documentation](doc/development.md)

[Project Structure Documentation](doc/project_structure.md)

[Setup Instructions](doc/setup.md)
