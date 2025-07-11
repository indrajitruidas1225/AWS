# AWS Serverless Contact Form

A beginner-friendly, serverless, "Contact Me" form built with :
- **Amazon S3** - Static Website Hosting
- **AWS Lambda** - Backend logic written in Python
- **Amazon API Gateway** - RESTful API endpoint
- **Amazon SES** - Email sending service

## Frontend - S3 Website Hosting 

### Let's get a basic about what S3 is

Amazon S3, or Simple Storage Service, is a cloud-based object storage service offered by Amazon Web Services (AWS). It allows users to store and retrieve any amount of data, from anywhere, at any time, with industry-leading scalability, data availability, security, and performance. It stores data as objects.

### Setup of S3

1. Go to **S3 > Create bucket**
2. Give a bucket name of your choice
3. Uncheck "Block all public access" option becuase you're about to host a static website, and the users need access to its contents
4. After the bucket is created, add the following policy to it from the **Permissions** tab

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::(your bucket name here)/*"
            }
        ]
    }
    ```

5. Now go to the objects tab and upload the `index.html` file
6. From the properties, click on **Bucket website endpoint** and you'll see the UI.
7. Later you'll need to change the api url in the `index.html` file.

## Backend - Lambda Function

### Let's get a basic of what lambda function is in aws

AWS Lambda is a serverless compute service offered by Amazon Web Services (AWS) that allows users to run code without provisioning or managing servers. It's an event-driven service that executes code in response to triggers such as HTTP requests, changes in data, or other events. Lambda automatically manages the underlying compute resources, including scaling, capacity provisioning, and maintenance.

### Setup of lambda

1. Go to **Lambda > Create Function**
2. Give it a name of your choice
3. Keep the runtime in Node or Python or whatever available. For this, we're keeping it in python.
4. Don't forget to click on **deploy** after adding the code
5. You've to set up env variable for the configuration tab for the `TO_EMAIL` variable
6. Below is the code for the lambda function

    ```python
    import json
    import boto3
    import os

    ses = boto3.client('ses')

    TO_EMAIL = os.environ['TO_EMAIL']

    def lambda_handler(event, context):
        data = json.loads(event['body'])

        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        email_body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        response = ses.send_email(
            Source=TO_EMAIL,
            Destination={'ToAddresses': [TO_EMAIL]},
            Message={
                'Subject': {'Data': 'New Contact Form Submission'},
                'Body': {'Text': {'Data': email_body}}
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Email sent successfully!')
        }
    ```

### Grant SES sendEmail Permission to Lambda

1. Go to the AWS Lambda console
2. Click on the function name
3. Click on the **configuration** tab
4. On the left sidebar, click **Permissions**
5. Under Execution Role, click the blue role name.
6. It'll take you to the IAM console
7. From **Add Permissions**, click on **Create Inline Policy**
8. Select **Service** --> Search and select: **SES**
9. Choose **Actions** --> Expand **"Write"**
10. Check `sendEmail`
11. In the resources, click of **All resources** for learning purpose

### API Gateway - HTTP API

#### Let's get to know a basic about API Gateway

Amazon API Gateway is a fully managed AWS service that enables developers to create, publish, maintain, monitor, and secure APIs at any scale.

1. Go to **API Gateway > Create HTTP API**
2. Add a POST route: `/contact`
3. From the Attach Integration option, integrate it to your lambda function
4. Enable CORS -
    - In `Access-Control-Allow-Origin` add `*` for an experimental purpose
    - In Methods, add `OPTIONS`, `POST`
    - In Headers, add `Content-Type`
    - Set `Max-Age` as `3600`

5. After making the changes, deploy it, if you're in default stage, it'll auto deploy.
6. Now copy the invoke url. For example , the invoke url is `http://abc.com`, and the route you created is `contact`, then the api url will be `http://abc.com/contact`. Paste that api in the `index.html` script.

You can create your own stage also and better enable auto-deploy.

### SES - Email Delivery

1. Visit **Amazon SES Console**
2. In **Configuration > Identity**, add the email id in which you want to receive messages. Verify it from the verification mail.

### Test the API

1. To test the API, you can use **postman**, **curl** etc. An example is given below -

    ```bash
    curl -X POST https://your-api \
     -H "Content-Type: application/json" \
     -d '{
        "name" : "Test User",
        "email" : "test@email.com",
        "message" : "This is a test"
     }'
    ```

### Test the App

1. From the s3 bucket properties, click on the **Bucket website endpoint**. 
2. Enter the details, click on **send**.
3. You'll receive it in your email now, the email you registered in SES. Check spam folder also.


## Author

**Indrajit Ruidas**  
📧 [mail me](mailto:indrajitruidas8436@yahoo.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/indrajitruidas1225)