Deployment

1) Create a new lamdba function in AWS, when doing this create a role to associate with it that includes DynamoDB and CloudWatch access.
2) In the same AWS account set up a DynamoDB table called 'contacts'
3) Upload the python code from the server_side folder to the new AWS lamdba function
4) Set up a API Gateway trigger for the lambda function, this gives you the end point for the form post
5) Modify the form action url in index.html in the client_side folder to match the API Gateway end point
6) Upload contents of client_side folder to a static web hosting service eg S3 bucket

TODO

HTTPS is a must, but simple hosting on S3 just gives you HTTP
Document API using swagger
Tests for the API endpoint
Create a pure API instead of a form post
server side validation
exception handling on server side for missing form params
Validate the multiple select inputs as enums
Retrieve the list of countries using a API call rather than hard coding a huge list
Use AWS Pinpoint for the whole thing - depending on the broader requirements
