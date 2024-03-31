# 주석
-- 주석

/*
여러줄 주석
*/


# <MariaDB>
- MySQL과 동일한 IP 또는 호스트 이름 을 가진다.
	(port 번호도 같다.)
	- IP : 127.0.0.1
	- Host : localhost
	- Port : 3306
	- 내 PC에 설치(구축)된는 모든 Server는 127.0.0.1 or localhost를 가진다.
		(port 번호로 구분한다)

# <root 계정>
	- Database의 절대 계정은 root
	- 패스워드는 설치 시에 지정하게 됨
	- 사용자를 생성하거나 권한을 설정하기 위해서는 
	   root 계정으로 접속해야 한다.
	- root 계정이 관리하는 Database들은 변경하면 안되며,
		이곳에 프로젝트를 위한 Database를 생성하는 것은 바람직하지 않음 
   - root 계정에 대한 패스워드는 외부에 유출되면 DB 자체가 뚫린다고 보면 됨.




# <Database, DB>
	- 행/렬의 데이터를 관리하는 메모리 공간을 DB라고 한다.
	- DB는 메모리공간을 의미하며 행렬의 데이터 자체는 아니다.
	- 최초에 프로젝트를 위해 DB 메모리 공간을 만들어야 한다.
	- DB 메모리 공간에 접근할 수 있는 사용자 계정과 비밀번호를 생성한다.
	- 생성된 사용자에게는 접근 권한을 부여시킨다. 
	- 여기까지는 root 계정을 통해서 수행한다.



# <1.사용자 계정  생성하기>
	- 계정 : pknu
	- 패스워드 : Password


-- 내부접근자(localhost) : 외부에서 접근 안됨
-- IDENTIFIED BY : 패스워드 설정 


# <2. Database 생성>

CREATE DATABASE pknudb;


# <3. 사용자에게 DB 접근 권한 부여하기>
	- grant : 권한 생성
	- all : 모든 권한(접속, 생성, 조회, 수정, 삭제,입력)

-- 내부사용자
GRANT ALL PRIVILEGES ON pknudb.* TO 'pknu'@'localhost';
-- 외부 사용자 
GRANT ALL PRIVILEGES ON pknudb.* TO 'pknu'@'%';

-- 권한 회수하기
-- REVOKE : 권한 회수 
REVOKE ALL PRIVILEGES ON pknudb.* FROM 'pknu'@'localhost'; 
REVOKE ALL PRIVILEGES ON pknudb.* FROM 'pknu'@'%'; 

-- DB 접근 권한 정보 확인하기
SELECT *
FROM db;



사용자, DB, 권한에 대한 생성 또는 삭제 또는 회수가 일어난 경우 
마지막에 항상 실행해야함


-- 메모리 반영(MySQL, MariaDB에만 있는 명령어)
FLUSH PRIVILEGES;

# <최초 해야할 작업 순서>
- DB 설계를 진행한다.
- 설계는 보통 상위 레벨의 작업자가 수행한다.
- DB 설계 : 테이블 설계를 수행한다.
	-- 테이블 공간 생성
	-- 테이블 공간 내에 사용할 컬럼명, 타입, 사이즈 등 정의
	-- 테이블과 테이블 간의 관계 정의
- DB 설계 시 작성되는 문서 : 테이블 정의서, ERD(객체관계도,테이블관계도), 스크립트(SQL) 명세서 (이외 다수 있으나, 기본적으로 위에 문서는 있어야 함)

0. DB : 예를 들어 DB는 엑셀파일 1개라고 생각하면 됨.	
1. 테이블 생성
	- 엑셀 파일 내에 시트를 테이블이라고 생각하면 됨.
	- 행/열을 관리하는 공간
		
2. 데이터 입력
3. 데이터 조회, 수정, 삭제 등 SQL구문 처리

# <테블 관계>
- 제약조건 : PK 또는ㄴ FK와 같은 정의를 제약조건이라고 칭함
- PK :고유한 값을 정의하는 컬럼에 정의함
		  : PK가 있는 테이블을 "부모 테이블"이라고 칭함
		  : 부모 테이블 쪽 선 끝에는 바(|)표시가 붙어 있다.
		  
- FK : 부모를 참조한다고 해서 "참조 테이블"이라고 칭함
		  : 부모 테이블의 PK값과 같은 값이 존재하며, PK를 참조하게 된다.
		  : 자식 테이블 쪽 선 끝에는 삼바리 또는 닭다리 표시가 붙어 있다.

# <테이블 컬럼 정의>
- 테이블을 생성할 때는 최소 1개 이상의 컬럼이 존재해야 한다.
- 컬럼은 영문명으로 작명한다.
- 컬럼 하나당 : 타입, 사이즈, NULL 여부, PK 또는 FK 여부를 정의
- 타입
	-- 문자열 : Varchar(가변형,길이를 알 수 없는 문자),
						char(고정형, 코드성 데이터로 길이를 사전에 알고 있는 경우)
	-- 숫자 : int
	-- 날짜 : datetime
	-- 문장 : text(최근에는 많이 사용 안함, Varchar의 사이즈를 늘려서 사용)
- 사이즈(메모리, 자릿수)
	-- 영문, 숫자, 특수문자 : 1byte, 1자리 사용
	-- 한글 : 한글 문자1개 당 2byte 사용(사이즈를 지정할 때 한글은 곱하기 2해야 함)