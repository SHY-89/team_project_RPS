# team_project_RPS
## 가위 바위 보 게임 웹 버전
## 1조 퍼스트 코딩

## 개발 일정

## 요구사항

	-회원 가입 페이지
		-회원 정보
			이름
			이메일(아이디)
			비밀번호

	-로그인 페이지
		회원 가입한 이메일 과 비밀번호를 입력

	-게임 페이지
		플레이어가 가위, 바위, 보 중 하나를 선택
		컴퓨터도 무작위로 가위, 바위, 보 중 하나를 선택
		플레이어와 컴퓨터의 선택을 비교하여 승패를 판정
		결과를 출력하여 플레이어가 이겼는지, 컴퓨터가 이겼는지, 비겼는지를 노출

	-전적 페이지
		게임의 승,무,패를 리스트 형식으로 노출
		최대 노출 수만큼 노출 후 페이징
		회원 수정
		비밀번호만 수정 가능
		변경시 로그인 변경전 비밀번호 입력 필요
	
	-데이터베이스

		회원정보(users)
			idx int primary key 고유 키
			uname varchar not null 유저 이름
			-> user_name 명칭 수정
			email varchar not null 유저 아이디(이메일)
			-> user_id 명칭 수정
			pw varchar not null 유저 패스워드 보안
			-> user_pw 명칭 수정
		게임기록(game_log)
			idx int primary key 고유 키
			round int not null 유저의 게임 횟수
			player varchar not null 유저가 선택한 가위,바위,보(1:가위,2:바위,보:3)
			computer varchar not null 컴퓨터가 선택한 가위,바위,보(1:가위,2:바위,보:3)
			win_lose char not null 유저의 승,무,패(승: w, 패: l, 무: d)

## 개발환경 & 사용기술

	Python 				3.8.6
	flask				3.0.3
	jquery 				1.11.1
	sweetalert 			2.1.2
	Flask-Cors         		4.0.1
	flask-sqlalchemy		3.1.1
	hashlib
	random

## 개발사항

	회원 가입 페이지 		개발완료
	로그인 페이지			프론트 완료, 백단 작업 대기
	게임 페이지			프론트 완료, 게임 동작 완료, 데이터베이스 생성 및 입출력 작업 대기
	전적 페이지			게임 페이지 노출, 데이베이스 연결 및 출력 작업 대기
