/*
회원아이디, 회원이름, 주문수량, 상품명 조회하기
단, 구매상품의 거래처 주소가 서울, 대전, 부산인 경우
	그리고,상품분류명에 '전자'가 포함된 경우
	그리고 주문수량이 5이상인 경우
정렬은 아이디 오름차순, 주문수량 내림차순
-- 일반 방식, 표준방식 각각 작성

*/

-- 일반 방식
SELECT mem_id, mem_name, cart_qty, prod_name
FROM member, cart, prod , buyer, lprod
WHERE mem_id=cart_member AND cart_prod = prod_id AND prod_buyer= buyer_id and buyer_lgu =lprod_gu 
and cart_qty>=5 AND substring(buyer_add1,1,2)IN('서울','대전','부산') AND lprod_nm LIKE '%전자%'
ORDER BY mem_id ASC, cart_qty DESC;

-- 표준 방식
SELECT mem_id, mem_name, cart_qty, prod_name
FROM member INNER JOIN  cart ON(mem_id = cart_member
										  and cart_qty>=5) 
				INNER JOIN  prod ON(cart_prod = prod_id)
				INNER JOIN  buyer ON (prod_buyer= buyer_id AND
											substring(buyer_add1,1,2)IN('서울','대전','부산'))
				INNER JOIN lprod ON(buyer_lgu =lprod_gu AND lprod_nm LIKE '%전자%' )
ORDER BY mem_id ASC, cart_qty DESC;


/*
<Outer Join>
	- 선행 조건 : Inner Join을 만족해야 함(관계조건식 그대로 적용)
	- 다만, 일반 방식으로 사용할 수 없음
			  (일반 방식은 관계가 있는, 즉 PK와 FK의 값이 서로 있는 경우만 가능)
	- PK와 FK의 값이 서로 없는 경우에도 조회하고 할 때 사용되는 join 방식
	- 조회할 컬럼의 경우 NULL 체크가 필요한 경우 NVL()함수를 사용하여 NULL 처리를 해야 함
	- 보통 전체에 대한 현황 분석(통계,집계) 시에 사용되는 Join 방식임
	- Left Outer Join과 Right Outer Join 방식이 있으며, Left 방식을 주로 사용함
	- 오라클(Oracle) DB의 경우 Full outer join 방식이 있으나, 사용되는 경우는 거의 없음 
	- Pandas의 데이터프레임(DataFrame)에서 Merge() 함수 사용 시 how=left or how=right와 동일  
*/

/*
회원별 구매금액의 총합을 조회해 주세요
	- 구매금액 = 주문수량 * 판매단가
*/

SELECT mem_name,SUM(nvl(prod_sale * cart_qty,0)) AS purchase_price
FROM member ,cart,prod 
WHERE mem_id=cart_member AND cart_prod = prod_id
GROUP BY mem_id;

SELECT mem_name, SUM(nvl(prod_sale * cart_qty,0)) AS purchase_price
FROM member INNER JOIN cart ON (mem_id=cart_member)
				INNER JOIN prod ON (cart_prod = prod_id)
GROUP BY mem_id;

/*
회원 전체에 대해서 구매금액의 현황을 조회
	- 회원 이름, 구매 금액의 합 조회
*/

SELECT COUNT(*) FROM member;

-- 표준방식
SELECT mem_name, SUM(nvl(prod_sale * cart_qty,0)) AS purchase_price
FROM member LEFT OUTER JOIN cart ON (mem_id=cart_member)
				LEFT  JOIN prod ON (cart_prod = prod_id)
GROUP BY mem_name;

/*
회원 전체에 대해서 구매금액의 현황을 조회
	- 회원 이름, 구매 금액의 합 조회
	- 회원의 거주지역이 서울,대전,부산인 경우
*/

SELECT COUNT(*) FROM member;

-- 표준방식
SELECT mem_name, SUM(nvl(prod_sale * cart_qty,0)) AS purchase_price,SUBSTRING(mem_add1,1,2)
FROM member LEFT OUTER JOIN cart ON (mem_id=cart_member)
				LEFT  JOIN prod ON (cart_prod = prod_id)	
where SUBSTRING(mem_add1,1,2)IN('서울','대전','부산')		
GROUP BY mem_name;

/*
상품분류 전체에 대한 상품분류건수가 몇개씩 있는지 집계
	- 조회 컬럼, 상품분류코드, 상품분류명, 상품건수
	- 정렬은 상품 건수를 기준으로 내림차순
*/

SELECT lprod_gu, lprod_nm, COUNT(prod_name) AS prod_count
FROM lprod LEFT OUTER JOIN prod ON(lprod_gu=prod_lgu)
GROUP BY lprod_gu, lprod_nm
ORDER BY prod_count desc;

SELECT lprod_gu, lprod_nm, COUNT(prod_name) AS prod_count
FROM lprod RIght OUTER JOIN prod ON(lprod_gu=prod_lgu)
GROUP BY lprod_gu, lprod_nm
ORDER BY prod_count DESC;

/*
2005년도에 주문된 상품에 대한 월별 판매현황 조회
	컬럼 : 주문월, 월별 총 주문수량, 월별 총구매금액
	구매금액 = 주문수량 * 판매가격
*/

SELECT SUBSTRING(cart_no,5,2)AS month, sum(nvl(cart_qty,0)) AS month_qty, SUM(nvl(prod_sale*cart_qty,0)) AS month_purchase
FROM cart LEFT OUTER JOIN prod ON (cart_prod = prod_id AND SUBSTRING(cart_no,1,4)=2005)
GROUP BY SUBSTRING(cart_no,5,2);

/*
회원아이디 b001 회원의 마일리지보다 큰 회원들을 조회
	- 조회컬럼 : 아이디, 이름, 마일리지
*/

-- subquery
SELECT mem_id, mem_name, mem_mileage
FROM member
WHERE mem_mileage > (SELECT mem_mileage FROM member WHERE mem_id ='b001');
-- -------------------------------------------------------------------------
SELECT mem_id, mem_name, member.mem_mileage
FROM member,(SELECT mem_mileage FROM member WHERE mem_id ='b001') MEM
WHERE member.mem_mileage > MEM.mem_mileage;

-- Self join
SELECT M1.mem_id, M1.mem_name, M1.mem_mileage, M2.mem_mileage
FROM member M1, member M2 
WHERE M2.mem_id = 'b001'
AND M1.mem_mileage >M2.mem_mileage;










