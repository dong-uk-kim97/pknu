-- 주석

/*
여러줄 주석
*/

/*
<MariaDB>
- MySQL과 동일한 IP 또는 호스트 이름 을 가진다.
	(port 번호도 같다.)
	- IP : 127.0.0.1
	- Host : localhost
	- Port : 3306
	- 내 PC에 설치(구축)된는 모든 Server는 127.0.0.1 or localhost를 가진다.
		(port 번호로 구분한다)

<root 계정>
	- Database의 절대 계정은 root
	- 패스워드는 설치 시에 지정하게 됨
	- 사용자를 생성하거나 권한을 설정하기 위해서는 
	   root 계정으로 접속해야 한다.
	- root 계정이 관리하는 Database들은 변경하면 안되며,
		이곳에 프로젝트를 위한 Database를 생성하는 것은 바람직하지 않음 
   - root 계정에 대한 패스워드는 외부에 유출되면 DB 자체가 뚫린다고 보면 됨.
*/


/*
<Database, DB>
	- 행/렬의 데이터를 관리하는 메모리 공간을 DB라고 한다.
	- DB는 메모리공간을 의미하며 행렬의 데이터 자체는 아니다.
	- 최초에 프로젝트를 위해 DB 메모리 공간을 만들어야 한다.
	- DB 메모리 공간에 접근할 수 있는 사용자 계정과 비밀번호를 생성한다.
	- 생성된 사용자에게는 접근 권한을 부여시킨다. 
	- 여기까지는 root 계정을 통해서 수행한다.
*/

/*
<1.사용자 계정  생성하기>
	- 계정 : pknu
	- 패스워드 : Password
*/

-- 내부접근자(localhost) : 외부에서 접근 안됨
-- IDENTIFIED BY : 패스워드 설정 
CREATE USER	pknu@localhost IDENTIFIED BY 'Password';

-- 외부에서도 접근가능하게(localhost 대신에 % 사용)
CREATE USER	'pknu'@'%' IDENTIFIED BY 'Password';

-- 사용자 삭제하기
DROP USER 'pknu'@'localhost';
DROP USER 'pknu'@'%';

-- 사용자 조회(Select)하기
SELECT * 
FROM user;

-- 데이터베이스 지정하기
USE mysql;


/*
<2. Database 생성>
*/
CREATE DATABASE pknudb;

-- DB 정보 조회하기 : root계정 선택 -> 새로고침 

/*
<3. 사용자에게 DB 접근 권한 부여하기>
	- grant : 권한 생성
	- all : 모든 권한(접속, 생성, 조회, 수정, 삭제,입력)
*/
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

/*
사용자, DB, 권한에 대한 생성 또는 삭제 또는 회수가 일어난 경우 
마지막에 항상 실행해야함
*/

-- 메모리 반영(MySQL, MariaDB에만 있는 명령어)
FLUSH PRIVILEGES;
