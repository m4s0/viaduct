Rate-limited API Challenge - Viaduct
====================================

Goal
====
Create a Dockerized REST API that exposes a single rate-limited endpoint **/limit**. No single user should be able to
hit the endpoint more than 10 requests per second. You can identify a user by their API key in the **X-API-KEY** in the
request header. If there is no API key, then you should immediately reject the request. You should not spend more than
3-4 hours working on this. If you feel pressed for time leave comments to explain what you would have done with more
time. You can implement this in any language of your choice; however, please implement this yourself and do not use an
existing rate limiter library. Finally, focus on code quality and readability.

# Application

Application runs with Python 3.8 and MySQL 5.7

#### Build and run

```
make init
```

Build container

```
make build
```

Run container

```
make up
```

Enter into python container

```
make bash
```

#### Tests

Application has been designed using a Test Driven Design approach

Run tests

```
make tests
```

#### Architecture

The architecture of this server is very simple, I decided to use a relational database like MySQL and three
tables, `user` for users, `api_key` which is related to `user` and contains the apiKey of the users and `api_key_usage`
which contains the information about the use of apiKey related to `api_key`. In this way I reached the compromise of
moving some of the logic to get the number of `api_key` per second in the MySQL query,

```  SELECT count(used_at)
    FROM api_key_usage
    WHERE api_key_id = %(api_key_id)s
    AND used_at = %(used_at)s
    GROUP BY api_key_id, used_at
    ORDER BY used_at DESC
    LIMIT 1
```

is a compromise that allows not to have the control logic in the code but to use the SQL language, the disadvantage of
this approach is that the granularity of the usage information is to the second. An alternative would be to register the
timestamp with microseconds and move the usage control logic per second into the code.

I'm clear on the difference but preferred to use this approach to make the application very simple.

#### Deploying

This server can be deployed as a container on
ECS [https://aws.amazon.com/blogs/containers/deploy-applications-on-amazon-ecs-using-docker-compose/]

#### Scalability

Given the architecture of this server scalability is easily achievable since the storage source, MySQL, is centralized
and can for example be an AWS MySQL service.

#### Monitoring

To monitor the server and the rate of requests per API key, simply add a new endpoint that queries the database and
the `api_key_usage` table
