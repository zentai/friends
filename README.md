**New Friend**
----
  create relationship between multiple email.

|Param |Description|
|---|---|
|friends|email list to build relationship|
  `POST /new_friends HTTP/1.1`

  ```json
  {
    "friends":
      [
        "andy@example.com",
        "john@example.com"
      ]
  }
  ```

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "success": true }`

**List Friend**
----
  create relationship between multiple email.

|Param |Description|
|---|---|
|email|list out all registered friends by email|
  `POST /friends_list HTTP/1.1`

  ```json
  {
  "email": "andy@example.com"
  }
  ```

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
```json
{
  "success": true,
  "friends" :
    [
      "john@example.com"
    ],
  "count" : 1
}
```

**Common Friends**
----
  filter out common friends between more user.

|Param |Description|
|---|---|
|friends|list out common friends by email list|
  `POST /common_friends HTTP/1.1`

  ```json
{
  "friends":
    [
      "andy@example.com",
      "john@example.com"
    ]
}
  ```

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
```json
{
  "success": true,
  "friends" :
    [
      "common@example.com"
    ],
  "count" : 1
}
```

**Subscribe**
----
  get notify without build friendship connection

|Param |Description|
|---|---|
|requestor|Who will be notify|
|target|Who need to be monitor|

  `POST /subscribe HTTP/1.1`

  ```json
{
  "requestor": "lisa@example.com",
  "target": "john@example.com"
}
  ```

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
```json
{
  "success": true
}
```


**Block**
----
if they are connected as friends, then "andy" will no longer receive notifications from "john"
if they are not connected as friends, then no new friends connection can be added

|Param |Description|
|---|---|
|requestor|Who will be notify|
|target|Who need to be monitor|

  `POST /block HTTP/1.1`

  ```json
{
  "requestor": "andy@example.com",
  "target": "john@example.com"
}
  ```

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
```json
{
  "success": true
}
```


**Notify List**
----
* has not blocked updates from "john@example.com", and
at least one of the following:
  * has a friend connection with "john@example.com"
  * has subscribed to updates from "john@example.com"
  * has been @mentioned in the update

|Param |Description|
|---|---|
|sender|who we are focus on|
|text|text message, if email address included, will also added into notify list|

  `POST /notify_list HTTP/1.1`

  ```json
{
  "sender":  "john@example.com",
  "text": "Hello World! kate@example.com"
}
  ```

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
```json
{
  "success": true,
  "recipients":
    [
      "lisa@example.com",
      "kate@example.com"
    ]
}
```


