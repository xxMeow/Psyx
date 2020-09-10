# API

> JSON에서는
>
> - {}는 object이고 파이썬의 dictionary처럼 key:value 쌍으로 구성됨. key는 꼭 문자열이어야 하고 value는 제한이 없음
> - []는 array임. 엔트리들이 서로 타입 다를 수 있음
>
> HTTP Request할 때 보통 짧은 매개변수는 URL뒤에다 붙이고 긴 매개변수나 서버한테 제출할 내용은 따로 콘텐츠에다 넣음
>
> 콘텐츠가 붙여있을 때 contents-type값을 성정해줘야 함 (여기서는 "application/json"임)

### Admin

##### `GET : ohfish.me/api/admin/list`

> 기존 실험 세트의 상세 정보 읽어오기

- Return

    ```json
    {
        "length" : 4,
        "packs" : [
            {
                "pack_id" : 1,
                "pack_name" : "aaaa",
                "age_lower" : 20,
                "age_upper" : 29,
                "gender" : 1,
                "date" : "2002/01/28",
                "reply_num" : 34
            },
            {
                "pack_id" : 2,
                "pack_name" : "bbbb",
                ...
            },
            {
                "pack_id" : 3,
                "pack_name" : "cccc",
                ...
            },
            {
                "pack_id" : 4,
                "pack_name" : "dddd",
                ...
            }
        ]
    }
    ```

##### `POST : ohfish.me/api/admin/create`

> 새 실험 세트 추가
>
> - ```bash
>     # make new pack
>     cd; mkdir what; cd what; touch w{1..600}.jpg; cd;
>     ```

- Body

    ```json
    {
        "age_lower" : 20,
        "age_upper" : 29,
        "gender" : 1,
        "pack_name" : "xxxx",
    }
    ```

    - 나이는 closed interval로 설정됨
    - pack_name은 소문자와 숫자만으로 구성됨

- Return

    ```json
    {
        "result" : "succeed"
    }
    ```

    - 실패할 때 failed로 반환됨
    - 추가가 성공적으로 실행됐을 때 새로고침하라고 팝업창 뜸

##### `GET : ohfish.me/api/admin/remove?id=3`

> 기존 실험 세트 삭제

- Return

    ```json
    {
        "result" : "succeed"
    }
    ```

##### `GET : ohfish.me/api/admin/download?id=7`

>  응답 csv 다운로드

- Return

    ```json
    미정
    ```

### Participant

##### `POST : ohfish.me/api/reply/start`

> 나이와 성별로 참여할 실험 세트 선정

- Body

    ```json
    {
        "mail" : "aaaa@gmail.com",
        "gender" : 1,
        "age" : 25,
        "student_no" : "aa2000000",
        "affiliation" : "A대학교"
    }
    ```

- Return

    ```json
    {
        "result" : "succeed"
    }
    ```
    - 인적사항을 제출하면 서버에서 검사해 줄 거임. 검사 통과해서 응답하기 시작하면 인적사항을 변견하면 절대 안 되니까 막아줘야함
    - 인적사항에 불법 입력이 존재하거나 조건에 맞는 실험 세트가 없을 때 failed로 반환되고 이 때 pack_name은 무시하면 됨

##### `POST : ohfish.me/api/reply/submit`

> 응답 제출

- Body

    ```json
    {
        "mail" : "aaaa@gmail.com",
        "gender" : 1,
        "age" : 25,
        "student_no" : "aa2000000",
        "affiliation" : "A대학교",
        "answers" : [
            ["j", 2.3341],
            ["f", 1.0004],
            [" ", 3.0000],
            ["f", 0.9902],
            ...
        ]
    }
    ```

- Return

    ```json
    {
        "result" : "succeed"
    }
    ```
    
    
