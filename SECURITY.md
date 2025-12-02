# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of our software seriously. If you believe you have found a security vulnerability in the LLM Vulnerability Scanner, please report it to us as described below.

**DO NOT report security vulnerabilities through public GitHub issues.**

### How to Report

Please send a detailed description of the issue to our security team at `security@example.com`. We will acknowledge receipt of your vulnerability report within 48 hours and strive to send you regular updates about our progress.

### What to Include

*   A detailed description of the vulnerability.
*   Steps to reproduce the issue (POC scripts or instructions are highly appreciated).
*   The version of the software you are using.
*   Any relevant logs or output.

### Our Process

1.  **Triage**: We will review your report and determine if it is a valid security issue.
2.  **Fix**: We will work on a fix for the vulnerability.
3.  **Release**: We will release a security update.
4.  **Disclosure**: We will publicly disclose the vulnerability after a reasonable period to allow users to upgrade.

## Safety Guidelines for Using This Tool

This tool is designed for **educational and defensive purposes only**.

*   **Authorization**: Only run this scanner against LLMs and systems you own or have explicit written permission to test.
*   **Safe Simulation**: The default mode uses a "Mock LLM" to simulate vulnerabilities safely. Use this for testing and development.
*   **API Costs**: When scanning real APIs (e.g., OpenAI), be aware that this tool generates multiple prompts which may incur costs.
*   **Content Safety**: While this tool attempts to use safe, synthetic test cases, interacting with LLMs can sometimes produce unpredictable outputs.

## Disclaimer

The authors of this project are not responsible for any misuse of this software. By using this tool, you agree to use it responsibly and in compliance with all applicable laws and regulations.
