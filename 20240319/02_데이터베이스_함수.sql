/*
<함수>
	- 데이터베이스 시스템별로 함수 이름은 모두 상이하며, 개념은 모두 동일
	- 함수이름도 유사하게 존재함
	- 국제표준을 따르지 않으며, DB 사용자에게 편의성을 제공하기 위해서 
	  Databse를 제공하는 기업에서 만들어 놓은 기능
*/ 

/*
replace(컬럼명, 찾을값, 바꿀값) : 값 치환하기
*/

SELECT prod_name, REPLACE(prod_name,'모니터','넌누구?') AS name
FROM prod;

/*
회원의 성씨가 이씨인 회원들에 대해서
성을 리씨로 바꿔서 조회
*/
SELECT mem_name, 
		 CONCAT(REPLACE(SUBSTRING(mem_name,1,1),'이','리'),SUBSTRING(mem_name,2,2)) AS new_name
FROM member;

/*
round(컬럼명,반올림할 자릿수)함수 : 반올림 함수
	- 반올림은 반올림할 자릿수 밑에서 반올림 됨
	- 0의 자릿수는 소숫점 위치를 의미한다.
*/

SELECT 1234.5678 AS orgNo, 
		 ROUND(1234.5678,0)AS NO1, 
		 ROUND(1234.5678,1)AS NO2, 
		 ROUND(1234.5678,-1)AS NO1;
		 
		 
/*
회원 중에 취미가 수영인 회원이 구매한 상품들을 조회
회원 지역이 서울, 대전, 광주에 거주하며,
상품 분류명에 피혁이라는 분류에 속해 있는 상품을 구매한 회원에 대한
상품명, 상품분류명, 원가(소숫점 2자리까지 표시)를 조회
단, 원가 = 매입가/판매가의 백분율 
*/		 

SELECT prod_name,(SELECT lprod_nm FROM lprod WHERE prod_lgu=lprod_gu) , concat(round(( prod_cost/prod_sale * 100 ),2),'%')AS cost
FROM prod
WHERE prod_lgu IN (SELECT lprod_gu 
					  FROM lprod 
					  WHERE lprod_nm LIKE '%피혁%')
AND prod_id IN (SELECT cart_prod FROM cart 
					WHERE cart_member IN 
					(SELECT mem_id 
					FROM member 
					WHERE mem_like LIKE '%수영%' and SUBSTRING(mem_add1,1,2) IN ('서울','대전','광주')));


/*
<case문>
	- 문법
		: Case 조건값 when 값 then 처리로직 Else 처리로직 End;
		: Case when 조건식 then 처리로직 else 처리로직 end;
*/

SELECT (
			Case 1
				 when 1 Then '1입니다'
				 when 0 then '0입니다'
				 ELSE '뭐지;'
			End
		  ) AS temp_value;

SELECT (
			Case 
				 when 1>0 Then '1입니다'
				 when 0>1 then '0입니다'
				 ELSE '뭐지;'
			End
		  ) AS temp_value;

/*
회원아이디, 회원이름, 성별 조회
*/

SELECT mem_id, mem_name,
		(case substring(mem_regno2,1,1) when 1  Then '남자'
		when 3 then '남자'
		when 2  then '여자'
		when 4 then '여자' 
		ELSE '넌 누구?'END) AS sex
FROM member;

/*
회원아이디, 회원이름, 성별, 등급  조회
	- 등급은 마일리지의 값이 5000이상이면 우수,미만은 일반으로 구분하여 조회
*/

SELECT mem_id, mem_name,
		(case substring(mem_regno2,1,1) 
			when 1  Then '남자'
			when 3 then '남자'
			when 2  then '여자'
			when 4 then '여자' 
			ELSE '넌 누구?'
			END) AS sex,
		mem_mileage,
		(case 
		 	when  mem_mileage>=5000 Then '우수고객'
			ELSE '일반고객'
			END) AS grade
FROM member;

/*
IF(조건식, 참일때 처리, 거짓일때 처리) 함수 
*/

SELECT if (10>100, '크다','작다') AS ifval;

/*
회원이름, 성별 조회하기(if 함수 사용)
*/

SELECT mem_name, if (substring(mem_regno2,1,1)IN(1,3),'남자','여자') AS sex 
FROM member;


/*
Null(결측치) 체크
	- Is null : null인 조건
	- is not null : null이 아닌 조건
	
	- null인 경우 : insert시에 값을 입력 안한 경우(공간이 존재하지 않음)
	- null이 아닌 경우 : insert시에 '' 이렇게 넣은 경우는 null이 아니다(공간은 차지함).
*/
-- is null과 is not null은 국제 표준이다.
SELECT *
FROM prod
WHERE prod_mileage IS NULL;

/*
널(null, 결측치) 데이터 대체하기
	- ifnull(컬럼명, null일 경우 대체값) 함수 사용
	: 컬럼값이 null이 아니면 자기 자신값 출력
				  null이면 대체값으로 출력
*/
-- nvl() null을 대체하는 함수(주로 사용됨)
SELECT prod_name,
		 IFNULL(prod_mileage,0) AS nullNum,
		 nvl(prod_mileage,0)
FROM prod;













