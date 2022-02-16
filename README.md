# simple-auth-server

## Get Started

### Prerequisites

```text
1. debian/ubuntu/centos linux/x86-64 release
2. python 3.7 linux/amd64 or higher
```

### Installation

#### Clone

* Clone this repo to your local machine using https://github.com/amazingchow/simple-auth-server.git.

#### Setup

```shell
pip install -r requirements.txt

# for debug/dev
make run_server_local

# for prod
make run_serverd
```

### Api List

1. generate a new auth code

```shell
curl -X POST -H 'content-type: application/json' -d '{"user_email": "abc@xyz.com", "expired_date": "2022-02-25"}' "http://127.0.0.1:15555/api/v1/authcode"

{
  "auth_code": "127803", 
  "expired_date": "2022-02-25", 
  "user_email": "abc@xyz.com"
}
```

2. verify the auth code

```shell
curl -I "http://127.0.0.1:15555/api/v1/authcode/verify?authcode=127803"
```

3. delete the auth code

```shell
curl -X DELETE "http://127.0.0.1:15555/api/v1/authcode?authcode=127803"
```

4. list all auth code

```shell
curl -i "http://127.0.0.1:15555/api/v1/authcode"
```

## Contributing

### Step 1

* 🍴 Fork this repo!

### Step 2

* 🔨 HACK AWAY!

### Step 3

* 🔃 Create a new PR using https://github.com/amazingchow/simple-auth-server/compare!

## Support

* Reach out to me at <jianzhou42@163.com>.

## License

* This project is licensed under the MIT License - see the **[MIT license](http://opensource.org/licenses/mit-license.php)** for details.
