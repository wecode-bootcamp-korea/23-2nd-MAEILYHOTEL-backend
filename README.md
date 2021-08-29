## MAEILYHOTEL 프로젝트 Front-end/Back-end 소개

- 신개념 밀키트 판매 사이트 [DAILYHOTEL](https://www.dailyhotel.com/) 클론 프로젝트
- 짧은 프로젝트 기간동안 개발에 집중해야 하므로 페이지를 선택해 구현했습니다.
- 개발은 초기 세팅부터 전부 직접 구현했으며, 아래 데모 영상에서 보이는 부분은 모두 백앤드와 연결하여 실제 사용할 수 있는 서비스 수준으로 개발한 것입니다.

### 개발 인원 및 기간

- 개발기간 : 2021/08/17 ~ 2021/08/27
- 개발 인원 : 프론트엔드 3명, 백엔드 2명
- [프론트엔드 github 링크](https://github.com/wecode-bootcamp-korea/23-2nd-MAEILYHOTEL-frontend)

### 프로젝트 선정이유

- 원하는 조건의 국내 숙소들을 편리하게 검색할 수 있는 점이 매력적이어서 선정했습니다

### 데모 영상(이미지 클릭)

- https://youtu.be/qDQXFb2oayE

## 적용 기술 및 구현 기능

### 적용 기술

> - Front-End : React.js, sass
> - Back-End : Python, Django web framework, Bcrypt, My SQL, Docker, S3, boto3
> - Common : KAKAO social login, RESTful API, AWS(RDS/EC2)

### 구현 기능
#### 소셜 로그인
- 카카오 로그인 API 사용 및 JWT 토큰 발행
- 유저 프로필 정보 조회
- 회원등급별 할인 적용

#### 검색페이지
- 지역별, 날짜별 필터링 검색
- 날짜별 예약가능한 숙소 필터링 기능

#### 리스트페이지
- 카테고리별 필터링 검색

#### 상세페이지
- 객실리스트 조회
- 지도 API 
- 달력에서 예약날짜 선택 및 예약가능한 객실 필터링 기능
- 객실별 예약 및 결제 기능

#### 마이페이지
- 예약리스트 조회
<br>

## Reference

- 이 프로젝트는 [DAILYHOTEL](https://www.dailyhotel.com/) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
