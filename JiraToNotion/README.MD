# Jira To Notion

## Summary

Jira to notion is a collection of tools for import Jira ticket information into different platforms.

### Functionality

- Import All, some, or specific tickets from your current sprint into Notion.
- Print All or only unfinished tickets to console to use in slack as notes.
- Zapier script to fetch unfinished tickets for use in other actions.

## Usage

Developed with Python 3.8 & Pip 20.1

`pip install -r requirements.txt`

`python ./JiraToNotion/main.py`

You will be presented with a CLI menu.

---

If you'd like to use the zapier script, you can find it here `./sprint_notes_builder/zapier_notes_builder.py`. Instructions are in the script. 

## Resources

- [Python Notion API](https://github.com/jamalex/notion-py)
- [Jira integration is built on their Version 3 API for Jira Cloud Platform](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
