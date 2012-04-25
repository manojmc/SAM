This is a sample project demonstrating how to use ReportLab's Report Markup Language (RML) from inside django.

It's a simple demonstration of how to harness ReportLab's Report Markup Language (RML) from inside django, allowing you to create PDFs with dynamic content by using RML templates with text substitution.  We have chosen the simplest possible way of doing this which is just to read the RML file into memory and search and replace a specific piece of text.

To run the demonstration, you need working installations of Python and django, along with the open source ReportLab toolkit, pyRXP, and the ReportLab PLUS bundle, which you can download by registering at http://www.reportlab.com

RML is an XML-style language for describing the layout of a document.  The RML is converted to PDF using a python module named rml2pdf.pyc

Because the RML is a just a text file, it can be manipulated dynamically very easily from inside any language or framework.  This example simply reads the template file 'hello.rml' into memory, and then substitutes a particular string using built in Python string methods.  It then uses the rml2pdf python module's 'go' method to create a PDF from the RML.  The resulting PDF is turned into a byte stream and returned to the browser.

RML2PDF and RML are part of the ReportLab PLUS software package.  For further information and extensive documentation, please see our website at http://www.reportlab.com/software
