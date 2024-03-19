/*
<조인(관계, join)>
	- 조인 종류 : Inner join, left outer join, Right outer join, Self join, Natural join
					: Inner join, Outer join, Self join, 
					: Cross join (사용하지 않음. 관계조건식이 없는 조인)
*/

/*
<Inner Join>
	- 부모와 자식 간의 테이블 관계에서
	  PK와 FK가 같은 경우에만 조회시키는 경우
	- From 절에 사용할 테이블을 모두 제시해서 사용 가능하다
	- PK와 FK가 같은 경우를 관계조건식(PK컬럼명 = FK컬럼명)으로 작성한다.
	- 국제 표준방식과 일반 방식 모두 사용가능하며,
		국내에서는 주로 일반 방식으로 사용한다.
		외국에서는 국제 표준 방식을 주로 사용한다.
*/


/*
회원아이디, 이름, 주문상품코드, 주문수량을 조회
*/

-- 일반 방식
SELECT mem_id, mem_name, cart_prod, cart_qty
FROM member, cart
-- 관계조건식(PK=FK)
WHERE mem_id = cart_member;




/*
회원아이디, 이름, 주문상품코드, 상품명, 주문수량을 조회
*/

-- 일반 방식
SELECT mem_id, mem_name, cart_prod, prod_name, cart_qty
FROM member, cart, prod;
-- 관계조건식(PK=FK)
WHERE mem_id = cart_member AND cart_prod = prod_id;

-- 국제 표준 방식 
SELECT mem_id, mem_name, cart_prod,prod_name, cart_qty
FROM member INNER JOIN  cart ON(mem_id = cart_member) 
											-- 일반 조건이 있는 경우 
											-- AND 컬럼명 >=값)
				INNER JOIN  prod ON(cart_prod = prod_id);

/*
관계조건식 갯수 = 테이블 갯수 - 1
	- 최소 갯수 이다.
*/

-- cross join
-- 28개 행
SELECT COUNT(*) FROM member;
-- 135개 행
SELECT COUNT(*) FROM cart;

-- 3,780 행 생성
SELECT COUNT(*)
FROM member, cart;

/*
상품명에 삼성이 포함되어 있는 상품을 구매한 회원 아이디, 회원 이름, 상품명을 조회
정렬은 회원이름 기준 오름차순
-- 일반 방식과 국제표준방식으로 작성
*/

-- 일반 방식
SELECT mem_id, mem_name, prod_name
FROM member, cart, prod
WHERE (mem_id = cart_member AND cart_prod = prod_id AND prod_name LIKE '%삼성%')
ORDER BY mem_name Asc;


-- 국제 표준 방식 
SELECT mem_id, mem_name, prod_name
FROM member INNER JOIN  cart ON(mem_id = cart_member) 
				INNER JOIN  prod ON(cart_prod = prod_id
										  AND prod_name LIKE '%삼성%')
ORDER BY mem_name Asc;

SELECT mem_id, mem_name, prod_name
FROM member INNER JOIN  cart ON(mem_id = cart_member) 
				INNER JOIN  prod ON(cart_prod = prod_id)
WHERE prod_name LIKE '%삼성%'
ORDER BY mem_name Asc;

/*
회원별 구매 금액의 총액을 조회
조회컬럼은 회원이름, 구매금액의 총액
단, 2005년 5월에 주문한 내역에 대해서 처리
	주문번호의 앞자리 8자리는 년원일을 의미
구매금액 = 구매수량 * 판매가격
*/

SELECT mem_name, SUM(prod_sale * cart_qty) AS purchase_price
FROM member INNER JOIN cart ON(mem_id=cart_member
										 AND SUBSTRING(cart_no,1,8) BETWEEN '20050501' AND '20050531')
				INNER JOIN prod ON(cart_prod = prod_id)
GROUP BY mem_name;

