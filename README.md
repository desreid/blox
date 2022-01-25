# Gathering contact information POC

## Architecture

An HTML form is used to gather information from the customer. 
I've tidied up the appearance a little with Bootstrap. 
Data are validated client side using Vue.js before being POSTed to the server.
The POST request is received by an API Gateway and associated Lambda function hosted on AWS.
I have written the Lamdba function in Python.
Data is stored in a DynamoDB database. This is an AWS nosql database.

## Deployment

1. Create a new Lamdba function in AWS, when doing this create a role to associate with it that includes DynamoDB and CloudWatch access.
2. In the same AWS account set up a DynamoDB table called 'contacts'
3. Upload the python code from the server_side folder to the new AWS lamdba function
4. Set up a API Gateway trigger for the Lambda function, this gives you the end point for the form post
5. Modify the form action url in index.html in the client_side folder to match the API Gateway end point
6. Upload contents of client_side folder to a static web hosting service eg S3 bucket

## Testing Approaches

### Unit testing

The Python code could have unit tests written for it in unittest. The vue.js code could be tested in a Javascript framework like Mocha or Jest.

### End to end testing

Selenium could be used to test the in-browser behaviour. Testing the API could be done using Postman, which can run suites of API calls. 

AWS also provides a facility for testing Lambda functions which would be appropriate here, although I've not investigated it.

## TODO

* Setting up HTTPS is a must for gathering personal data, but simple hosting that I've used on S3 just gives you HTTP
* Retrieve the list of countries using a API call rather than hard coding a huge list
* Document API using swagger
* Tests for the API endpoint
* Create a pure API instead of a form POST
* Server side validation
* Better exception handling on server side for missing form params
* Validate the multiple select inputs as enums
* Use AWS Pinpoint, which is AWS' customer engagement platform for the whole thing - depending on the broader requirements
* Set up a configuration file containing the DynamoDB table name and the form POST url, instead of this being hard coded
* Run the Python code through pylint
 
