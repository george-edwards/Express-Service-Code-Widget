# Express-Service-Code-Widget
Get the Express Service Code of a Dell asset by providing its serial number.

An Express Service Code can be obtained from support.dell.com after providing the Serial Number. Dell provide no API for this however.
This Python script spins up a pseudo-Firefox in RAM (Selenium for Python), pulls down support.dell.com, submits the appropriate HTTP post for the given serial number, then scrapes the express service code.
