![request sent to dummjson without any modification](image.png)

![request sent ot dummyjson after removing the user agent](image-1.png)

![request sent to dummyjson with fake auth token](image-2.png)


![compared the results from fake auth token request and from the request not conating the user agent](image-3.png)

![sent the etag to check caching and got the expected response 304 not modified](image-4.png)



![/echo route for the node server](image-5.png)

![/slow route working as expected](image-6.png)