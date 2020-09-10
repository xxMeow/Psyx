# API

- 나이 구간은 closed interval임. 즉, `age_lower <= age <= age_upper`의 규칙 적용됨
- 성별은 실제값으로 `1`과 `2`만 허용 (F=1, M=2)
- `pack_name`은풀더 이름이며 이에는 대/소문자와 숫자만 들어갈 수 있음
- 응답 페이지
    - 인적사항 확인 단계 : 인적사항을 서버한테 보냄
        - 서버가 모든 입력항목을 validation함
        - 통과하면 해당 실험자의 나이와 성별에 맞는 세트를 검색
        - 세트가 존재하면 `p_id`와 `pack_path` 반환
            - `p_id`는 프런트 엔드가 저장해서 마지막 제출할 때 그대로 제출해야됨 (아니면 서버가 어느 세트에 응답하는 지 모름)
            - `pack_path`는 응답할 사진이 저장되어있는 경로임. 이 경로 뒤에 사진 파일 이름만 붙여주면 사진의 `src`로 쓸 수 있음
    - 실험자 응답 단계
    - 응답 제출 단계 : (`p_id` + 인적사항 + 응답)을 서버한테 보냄

### Admin

##### `GET : ohfish.me/api/admin/list`

> 기존 모든 실험 세트의 상세 정보 읽어오기

- Return

    ```json
    {
        "pack_list": [
            {
                "age_lower": 20,
                "age_upper": 29,
                "count": 4,
                "date": "Thu, 10 Sep 2020 22:07:21 GMT",
                "gender": 2,
                "p_id": 10,
                "pack_name": "what"
            }
        ],
        "pack_num": 1
    }
    ```
    
    - `pack_num` : 현재의 세트 총수
    - `pack_list` : element가 세트 정보인 리스트 (세트 정보에 있는 count는 해당 세트가 현재 이미 받은 응답수)

##### `POST : ohfish.me/api/admin/create`

> ⚠️새 실험 세트를 먼저 서버에 올려서야 요청 가능 (올리고 요청이 실패한 경우 다시 올려야 됨)
>
> - ```bash
>     # make new pack (여기 명령어 프런트엔드와 상관 없음)
>     cd; mkdir what; cd what; touch w{1..600}.jpg; cd;
>     ```

- Body

    ```json
    {
        "age_lower": 20,
        "age_upper": 29,
        "gender": 1,
        "pack_name": "xxxx"
    }
    ```

    - 나이는 closed interval로 설정됨
    - pack_name은 대/소문자와 숫자만으로 구성됨

- Return

    ```json
    {
        "result": "succeed",
        "p_id": 10
    }
```
    
    - 실패할 때 failed로 반환됨 (에러 메세지는 `result[message]`로 읽을 수 있음)
    - 추가가 성공적으로 실행됐을 때 새로고침하라고 팝업창으로 사용자에게 알림 (필요할지 모르겠지만 새로 추가된 세트의 `p_id`도 반환됨)

##### `GET : ohfish.me/api/admin/remove?id=3`

> 기존 실험 세트 삭제

- Return

    ```json
    {
        "result": "succeed"
    }
    ```
    
    - 실패할 때 failed로 반환됨 (에러 메세지는 `result[message]`로 읽을 수 있음)

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
        "mail": "aaaa@gmail.com",
        "gender": 1,
        "age": 25,
        "student_no": "aa2000000",
        "affiliation": "A대학교"
    }
    ```

    - 나이와 성별만 빼고 모든 항목이 문자열임

- Return

    ```json
    {
        "p_id": 10,
        "pack_path": "/home/xmx1025/Psyx/packbase/what",
        "result": "succeed"
    }
    ```
    - 인적사항을 제출하면 서버가 모든 항목을 검사해 주니까 프런트엔드에서는 안 해도 됨
    - 실패할 때 failed로 반환됨 (에러 메세지는 `result[message]`로 읽을 수 있음)

##### `POST : ohfish.me/api/reply/submit`

> 응답 제출

- Body

    ```json
    {
        "p_id": 10,
        "mail": "ss12@any.com",
        "student_no": "hsdbjsbj33",
        "gender": 2,
        "age": 23,
        "affiliation": "mars",
        "answers": [
            ["j", 2.2933],
            ["x", 3.0000],
            ["x", 3.0000],
            ["j", 0.9863],
            ["x", 3.0000]
        ]
    }
    ```

    - `p_id`, 나이, 성별, 응답시간 4개만 빼고 모든 항목이 문자열임

- Return

    ```json
    {
        "result": "succeed"
    }
    ```
    
    - 세트를 선택하고 나서 정보가 중간에 바뀌지만 않았으면 에러 뜰 일이 없는게 정상
