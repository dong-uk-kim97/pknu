/*
<그룹(집계)함수
	- 국제표준을 따른다.
	- count(), sum(), min(), max(),avg() 5개의 집계함수가 존재한다. 
	- sum 또는 avg를 사용할 경우에는 null체크를 꼭해야 함
		예시: sum(nvl(값,0)), avg(nvl(값,0))
*/
SELECT prod_name,
		 IFNULL(prod_mileage,0) AS nullNum,
		 nvl(prod_mileage,0)
FROM prod;

/*
회원정보 전체에 대한 집계 정보 조회하기
	- 회원총수, 마일리지(총합, 최소값, 최대값, 평균값)조회하기
*/

SELECT COUNT(mem_id) AS total_member, SUM(nvl(mem_mileage,0)) AS sum_mileage, MIN(nvl(mem_mileage,0)) AS minimum,
MAX(nvl(mem_mileage,0)) AS maximum, AVG(nvl(mem_mileage,0)) AS average
FROM member;


/*
서울, 대전, 부산에 거주하는 회원들에 대한
회원수, 마일리지(총합, 최소값, 최대값, 평균값) 조회하기
	-> 해당 조건에 만족하는 전체 집계 결과는 1개 행 
*/


SELECT COUNT(mem_id) AS total_member, SUM(nvl(mem_mileage,0)) AS sum_mileage, MIN(nvl(mem_mileage,0)) AS minimum,
MAX(nvl(mem_mileage,0)) AS maximum, AVG(nvl(mem_mileage,0)) AS average
FROM member
WHERE SUBSTRING(mem_add1, 1,2) IN ('서울','대전','부산');


/*
전체 집계가 아닌, 소그룹 집계(범주별 집계)
	- 지역별 회원들의 정보를 집계
	- 지역명, 지역별 회원수, 마일리지(총합, 최소값, 최대값, 평균값) 조회하기
	
	--> 집계함수와 일반함수(또는 일반 컬럼)을 함께 조회하는 경우에는 
		 일반함수(또는 일반 컬럼)은 무조건 Group By 절에 작성해야 함
		 안 그러면 오류남 
*/

/*
그룹조건 : Having 절에 그룹 조건 제시
			: 그룹 조건은 집계함수를 이용한 조건을 의미함
			: Group by절 다음에 작성
*/


/*
그룹이 이루어진 정렬(Order by)의 경우에는
select절 뒤에 사용된 컬럼들(별칭) 또는 Group by절 뒤에 사용된 컬럼들만 
정렬로 사용할 수 있다.
*/
SELECT SUBSTRING(mem_add1, 1,2) AS AREA, mem_like, 
		 COUNT(mem_id) AS total_member, 
		 SUM(nvl(mem_mileage,0)) AS sum_mileage, 
		 MIN(nvl(mem_mileage,0)) AS minimum,
		 MAX(nvl(mem_mileage,0)) AS maximum, 
		 AVG(nvl(mem_mileage,0)) AS average
FROM member
-- 일반 조건절
WHERE SUBSTRING(mem_add1, 1,2) IN ('서울','대전','부산')
-- 그룹(집계)
Group by SUBSTRING(mem_add1, 1,2), mem_like 
-- 그룹(집계) 조건 
HAVING COUNT(mem_id)>=2
ORDER BY mem_like ASC;


