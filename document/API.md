# API

> JSON에서는
>
> - {}는 object이고 파이썬의 dictionary처럼 key:value 쌍으로 구성됨. key는 꼭 문자열이어야 하고 value는 제한이 없음
> - []는 array임. 엔트리들이 서로 타입 다를 수 있음
>
> HTTP Request할 때 보통 짧은 매개변수는 URL뒤에다 붙이고 긴 매개변수나 서버한테 제출할 내용은 따로 콘텐츠에다 넣음
>
> 콘텐츠가 붙여있을 때 contents-type값을 성정해줘야 함 (여기서는 "application/json"임)

### Gunicorn + Flask

##### Start

```bash
gunicorn -w 1 -b 0.0.0.0:5000 API:api
```

### /Pack

##### GET(gender, age) -> packName

- 요청: `https://ohfish.me/pack?gender=1&age=23`

- 리턴:

    ```json
    {
        "pairNum" : 300,
        "packName" : "packxxx"
    }
    ```

### /Reply

##### POST(packName) -> Send a reply

- 요청: `https://ohfish.me/reply`

    콘텐츠:

    ```json
    {
        "packName" : "packxxx",
        "mail" : "xxxx@gmail.com",
        "gender" : 1,
        "age" : 25,
        "studentNo" : "xx38490023",
        "affiliation" : "X대학교",
        "answers" : [
            ["j", 2.0031],
            ["x", 3.0000],
            ["f", 2.8977],
            ["j", 1.2404],
            ["j", 1.5003]
        ]
    }
    ```

- 리턴:

    ```json
    {
        "result" : "succeed"
    }
    ```

##### GET(packName) -> All Replies to the Pack

- 요청: `https://ohfish.me/reply?packname=packxxx`

- 리턴:

    ```json
    {
        "answerNum" : 5,
        "replyNum" : 3,
        "replies" : [
                        {
                            "mail" : "aaaa@gmail.com",
                            "gender" : 1,
                            "age" : 25,
                            "studentNo" : "aa2000000",
                            "affiliation" : "A대학교",
                            "answers" : "jffxj"
                        },
                        {
                            "mail" : "bbbb@naver.com",
                            "gender" : 2,
                            "age" : 20,
                            "studentNo" : "bb200100",
                            "affiliation" : "B대학교",
                            "answers" : "xfjxx"
                        },
                        {
                            "mail" : "cccc@any.com",
                            "gender" : 2,
                            "age" : 27,
                            "studentNo" : "cc38002222",
                            "affiliation" : "C회사",
                            "answers" : "jjjjf"
                        }
                    ]
    }
    ```